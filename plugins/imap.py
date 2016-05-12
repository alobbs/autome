import email
import imaplib
import time

import pluginconf


class IMAP:
    def __init__(self):
        self.conn = None
        self._known_msgs = {}

        # Read conf
        self.conf = pluginconf.get('imap')

    def _connect(self):
        conn = imaplib.IMAP4_SSL(self.conf['host'], self.conf['port'])
        conn.login(self.conf['user'], self.conf['password'])
        return conn

    def get_new_msgs(self, folder, filtering):
        """Returns a list of the new msgs matching a filter string

        :param folder: The folder naem. Eg: "INBOX"
        :param filtering: IMAP filtering string. Eg: "(TEXT autome)"
        """

        if not self.conn:
            self.conn = self._connect()

        # Select folder
        self.conn.select(mailbox=folder, readonly=True)

        # Search messages
        typ, data = self.conn.search(None, filtering)

        # Parse: newest first
        message_ids = [int(i) for i in data[0].split()]
        message_ids.reverse()

        # First run
        key = "{}_{}".format(folder, filtering)

        if key not in self._known_msgs:
            self._known_msgs[key] = set(message_ids)
            return []

        # New messages
        new_ids = set(message_ids) - self._known_msgs[key]
        self._known_msgs[key] = set(message_ids)

        new_msgs = []
        for num in new_ids:
            typ, data = self.conn.fetch(str(num), '(RFC822)')
            msg = email.message_from_bytes(data[0][1])
            new_msgs.append(msg)

        # Update cache
        return new_msgs

    def close(self):
        self.conn.close()
        self.conn.logout()


if __name__ == '__main__':
    i = IMAP()
    while True:
        msgs = i.update('INBOX', '(TEXT alvaro@alobbs.com)')
        print(msgs)
        time.sleep(10)
