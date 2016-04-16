#!/usr/bin/env python3

import logging

import flask
import ujson as json

import conf
import cron

app_name = __name__.split('.')[0]
app = flask.Flask(app_name)
app.cron = cron.Cron()


@app.route("/jobs/run/<string:job_id>", methods=['GET'])
def get_run(job_id):
    found = app.cron.force_run_job(job_id)
    if found:
        r = {"status": "ok"}
    else:
        r = {"status": "failed",
             "description": "Could not find {}".format(job_id)}
    return flask.Response(json.dumps(r), status=200, mimetype='application/javascript')


@app.route("/jobs/list", methods=['GET'])
def get_tasks_list():
    r = app.cron.jobs_get_info()
    r_json = json.dumps(r)
    return flask.Response(r_json, status=200, mimetype='application/javascript')


def main():
    app.cron.start()
    print("http://localhost:{}/".format(conf.CHIEF_API_PORT))
    app.run(debug=conf.CHIEF_API_DEBUG, port=conf.CHIEF_API_PORT, **conf.CHIEF_API_OPTS)


if __name__ == "__main__":
    if not conf.CHIEF_API_DEBUG:
        log = logging.getLogger('werkzeug')
        log.setLevel(logging.ERROR)

    try:
        main()
    except KeyboardInterrupt:
        pass
