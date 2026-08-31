import unittest

from parser import parse_ssh_failed_login


class TestSSHParser(unittest.TestCase):

    def test_failed_ssh_login(self):
        log = (
            "Aug 29 22:03:33 raspberrypi sshd[759]: "
            "Failed password for pi from 192.168.1.209 "
            "port 50007 ssh2"
        )

        event = parse_ssh_failed_login(log)

        self.assertIsNotNone(event)
        self.assertEqual(event["username"], "pi")
        self.assertEqual(event["ip_address"], "192.168.1.209")

    def test_non_ssh_log_returns_none(self):
        log = "Aug 29 22:03:33 raspberrypi systemd: Starting service"

        event = parse_ssh_failed_login(log)

        self.assertIsNone(event)


if __name__ == "__main__":
    unittest.main()