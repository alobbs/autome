import os

import plugin
import pluginconf

util = plugin.get("util")

FILE_COUNTER = "~/.vpn_counter"
FILE_VPN_SH = "~/.vpn_sh"

EXPECT_SCRIPT = """#!/usr/bin/expect

spawn {cmd}
expect -exact "Enter Auth Username:"
send -- "{user}\\n"
expect -exact "Enter Auth Password:"
send -- "{password}\\n"
interact
"""


class VPN:
    def __init__(self):
        # Read configuration
        self.conf = pluginconf.get('vpn')

    def is_connected(self):
        with os.popen("ps aux") as f:
            pcs = f.read()
        return self.conf['openvpn_conf'] in pcs

    def get_password(self):
        file_counter = os.path.expanduser(FILE_COUNTER)

        # Read usage counter
        with open(file_counter, 'r') as f:
            raw = f.read()
        counter = int(raw.strip()) + 1

        # OAuth
        cmd = "oathtool -b %s -c %s" % (self.conf['secret'], counter)
        with os.popen(cmd, 'r') as f:
            code = f.read().strip()

        # Update counter
        with open(file_counter, 'w') as f:
            f.write(str(counter))

        password = "%s%s" % (self.conf['pin'], code)
        return password

    def connect(self):
        # Compose connection script
        cmd = "sudo /usr/local/sbin/openvpn --config %s" % self.conf['openvpn_conf']
        user = self.conf['user']
        password = self.get_password()
        script = EXPECT_SCRIPT.format(cmd=cmd, user=user, password=password)

        # Write it to a file
        vpn_script = os.path.expanduser(FILE_VPN_SH)

        with open(vpn_script, 'w+') as f:
            f.write(script)
        os.chmod(vpn_script, 0o770)

        # Run
        os.system(vpn_script)
