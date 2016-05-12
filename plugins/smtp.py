import email.encoders
import email.message
import email.mime.audio
import email.mime.base
import email.mime.image
import email.mime.multipart
import email.mime.text
import mimetypes
import os
import smtplib

import pluginconf


class SMTP:
    def __init__(self):
        # Read conf
        self.conf = pluginconf.get('smtp')

    def _connect(self):
        conn = smtplib.SMTP(self.conf['host'], self.conf['port'])
        return conn

    def send_msg(self, msg, to=None):
        conn = self._connect()
        conn.send_message(msg, to_addrs=to)
        conn.quit()

    def forward_msg(self, msg, from_, to, subject=None):
        message = email.mime.base.MIMEBase("multipart", "mixed")
        message["From"] = from_
        message["To"] = to
        message["Subject"] = subject or "Fwd: {}".format(msg['subject'])
        message.attach(msg)

        conn = self._connect()
        conn.send_message(message)
        conn.quit()

    def send_files(self, to, files_fp, subject=None):
        if type(to) != list:
            to = [to]
        if type(files_fp) != list:
            files_fp = [files_fp]

        outer = email.mime.multipart.MIMEMultipart()
        outer['From'] = self.conf['from']
        outer['To'] = ", ".join(to)
        outer['Subject'] = subject or ', '.join([os.path.basename(f) for f in files_fp])
        outer.preamble = 'You will not see this in a MIME-aware mail reader.\n'

        for fp in files_fp:
            # Type of attachment
            ctype, encoding = mimetypes.guess_type(fp)
            if ctype is None or encoding is not None:
                ctype = 'application/octet-stream'

            maintype, subtype = ctype.split('/', 1)
            if maintype == 'text':
                with open(fp, 'r') as f:
                    msg = email.mime.text.MIMEText(f.read(), _subtype=subtype)
            elif maintype == 'image':
                with open(fp, 'rb') as f:
                    msg = email.mime.image.MIMEImage(f.read(), _subtype=subtype)
            elif maintype == 'audio':
                with open(fp, 'rb') as f:
                    msg = email.mime.audio.MIMEAudio(f.read(), _subtype=subtype)
            else:
                with open(fp, 'rb') as f:
                    msg = email.mime.base.MIMEBase(maintype, subtype)
                    msg.set_payload(f.read())
                email.encoders.encode_base64(msg)

            # Set the filename parameter
            filename = os.path.basename(fp)
            msg.add_header('Content-Disposition', 'attachment', filename=filename)
            outer.attach(msg)

        # Send
        conn = self._connect()
        conn.send_message(outer)
        conn.quit()


if __name__ == '__main__':
    from email.mime.text import MIMEText

    msg = MIMEText('This is a test 6 :)')
    msg['Subject'] = 'Pruebecillaaa'
    msg['From'] = 'from@redhat.com'
    msg['To'] = 'kaka@culo.com'

    s = SMTP()
    s.forward_msg(msg, "aortega@redhat.com", "alvaro@alobbs.com")
