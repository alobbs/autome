import datetime
import glob
import importlib.machinery
import io
import os
import sys
import threading
import time
import traceback

import dateutil.parser

import conf


def load(filepath):
    filename = os.path.basename(filepath)
    modname = filename.replace('.py', '')
    loader = importlib.machinery.SourceFileLoader(modname, filepath)
    m = loader.load_module()

    # Convert lapse(str) to lapse(int)
    if hasattr(m, "lapse"):
        if type(m.lapse) == str:
            total = 0
            LETTERS = {'w': 7*24*60*60, 'd': 24*60*60, 'h': 60*60, 'm': 60}
            for ls in m.lapse.split(' '):
                for c, v in LETTERS.items():
                    if c in ls:
                        total += int(ls.replace(c, '').strip()) * v
            m.lapse = total
    else:
        m.lapse = None

    # When
    if hasattr(m, "when"):
        if type(m.when) == str:
            dt = dateutil.parser.parse(m.when)
            m.when = dt.time()
    else:
        m.when = None

    return m


def time_str():
    return time.strftime("%d-%m-%y %H:%M")


def log_exceptions(func):
    def wrapper(self, *args):
        time_start = time_str()

        f = io.StringIO()
        try:
            func(self, *args)
        except Exception:
            e = sys.exc_info()
            msg = str(e[:2]) + '\n'
            msg += "".join(traceback.format_exception(*e))
            f.write(msg)

        logged = f.getvalue()
        if logged:
            # Log
            log_fname = os.path.basename(self.script_fp).replace('.py', '.log')
            dirfp = os.path.expanduser("~/.autome/logs")
            log_fp = os.path.join(dirfp, log_fname)

            with open(log_fp, 'a+') as lf:
                lf.write("[%s]: Starts {\n" % time_start)
                lf.write(logged)
                lf.write("[%s]: } Ends\n" % time_str())

    return wrapper


def format_lapse(secs):
    def format_hms(s):
        p = [int(n) for n in s.split(':', 3)]
        if len(p) != 3:
            return s
        if p[0] == p[1] == p[2] == 0:
            return '0s'
        elif p[0] == p[1] == 0:
            return '%ss' % (p[2])
        elif p[0] == 0:
            return '%sm %ss' % (p[1], p[2])
        else:
            return '%sh %sm' % (p[0], p[1])

    tmp = str(datetime.timedelta(seconds=int(secs)))
    if ', ' in tmp:
        days, hms = tmp.split(', ')
        hmsf = format_hms(hms)
        if hmsf == '0s':
            return '%s' % (days)
        else:
            return '%s, %s' % (days, hmsf)

    return format_hms(tmp)


class ThreadJob(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.run_times = 0
        self.errors = 0
        self.script_fp = None
        self.time_start = time.time()

    @log_exceptions
    def load_script(self, fullpath):
        self.script_fp = fullpath
        self.script = load(fullpath)
        self.func = self.script.run

    @log_exceptions
    def run_func(self):
        # Keep this call as a method so @log_exceptions() is executed before
        # exceptions are caught by the mainloop's try:catch block and ignored
        return self.func()

    def run(self):
        while True:
            self.run_times += 1
            try:
                self.run_func()
            except Exception:
                self.errors += 1

    def get_info(self):
        return {'name': os.path.basename(self.script_fp),
                'duration': format_lapse(time.time() - self.time_start),
                'runs': self.run_times,
                'running': 'yes',
                'elapse': "*"}


class CronJob:
    def __init__(self):
        self.func = None
        self.func_params = None
        self.script = None
        self.script_fp = None
        self.running = False
        self.run_times = 0

    @log_exceptions
    def load_script(self, fullpath):
        self.time_next = sys.maxsize
        self.script_fp = fullpath
        self.script = load(fullpath)
        self.func = self.script.run
        self.duration_last_run = 0

        if self.script.when:
            t = self.script.when
            dt_now = datetime.datetime.now()
            dt = datetime.datetime.combine(datetime.datetime.now().date(), t)
            if dt < dt_now:
                dt += datetime.timedelta(days=1)
            delta = dt - dt_now
            self.time_next = time.time() + delta.total_seconds()
        else:
            self.time_next = time.time() + self.script.lapse

    def exec_time(self):
        return time.time() > self.time_next

    def execute_guts(self):
        self.running = True
        time_before = time.time()
        self.time_next = time.time() + self.script.lapse

        if self.func_params:
            re = self.func(*self.func_params)
        else:
            re = self.func()

        time_after = time.time()
        self.time_next = time_after + self.script.lapse
        self.duration_last_run = time_after - time_before

        self.run_times += 1
        self.running = False
        return re

    @log_exceptions
    def execute(self, *args):
        return self.execute_guts(*args)

    def get_info(self):
        nextt = "%s, in %s" % (
            time.strftime('%H:%M', time.gmtime(self.time_next)),
            format_lapse(self.time_next - time.time())
        )

        return {'name': os.path.basename(self.script_fp),
                'elapse': format_lapse(self.script.lapse),
                'next': nextt,
                'duration': format_lapse(self.duration_last_run),
                'running': ('no', 'yes')[self.running],
                'runs': self.run_times}


class Cron(threading.Thread):
    def __init__(self):
        self.jobs = []
        self.threads = []
        self.lapse = 10
        threading.Thread.__init__(self)
        # Don't do anything here: Exec'ed twice

    def run(self):
        # Load jobs
        self.load_jobs()

        # Iterate
        loop = 0
        while True:
            loop += 1
            time.sleep(self.lapse)

            for job in self.jobs:
                if job.exec_time():
                    job.execute()

    def load_jobs(self):
        # Scripts
        path = os.path.normpath(conf.CHIEF_API_SCRIPTS_PATH)
        srcroot = os.path.normpath(__file__ + '/../../')
        sys.path.insert(0, srcroot)

        for job_file in glob.glob(path + "/*.py"):
            job = CronJob()
            job.load_script(job_file)
            self.jobs.append(job)

        # Threads
        path = os.path.normpath(conf.CHIEF_API_THREADS_PATH)
        srcroot = os.path.normpath(__file__ + '/../../')
        sys.path.insert(0, srcroot)

        for job_file in glob.glob(path + "/*.py"):
            thr = ThreadJob()
            thr.load_script(job_file)
            self.threads.append(thr)
            thr.start()

    def jobs_get_info(self):
        info = []

        # Jobs
        sjobs = sorted(self.jobs, key=lambda c: c.time_next)
        for j in sjobs:
            info.append(j.get_info())

        # Threads
        for t in self.threads:
            info.append(t.get_info())

        return info

    def force_run_job(self, script_name):
        for job in self.jobs:
            j_name = os.path.basename(job.script_fp)
            if j_name == script_name:
                job.time_next = time.time() - 1
                return True
        return False
