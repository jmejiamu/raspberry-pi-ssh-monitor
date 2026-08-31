import unittest
from datetime import datetime, timedelta

from detector import detect_threat, failed_attempts, alerted_ips


class TestThreatDetector(unittest.TestCase):

    def setUp(self):
        failed_attempts.clear()
        alerted_ips.clear()

    def test_single_attempt_is_medium(self):
        event = {
            "username": "pi",
            "ip_address": "192.168.1.100",
            "timestamp": datetime.now()
        }

        detection = detect_threat(event)

        self.assertEqual(detection["type"], "ssh_failed_login")
        self.assertEqual(detection["severity"], "medium")
        self.assertEqual(detection["attempt_count"], 1)

    def test_five_attempts_trigger_brute_force(self):
        start_time = datetime.now()

        detection = None

        for i in range(5):
            event = {
                "username": "pi",
                "ip_address": "192.168.1.100",
                "timestamp": start_time + timedelta(seconds=i * 5)
            }

            detection = detect_threat(event)

        self.assertEqual(
            detection["type"],
            "possible_brute_force"
        )

        self.assertEqual(
            detection["severity"],
            "high"
        )

        self.assertEqual(
            detection["attempt_count"],
            5
        )

    def test_old_attempts_are_removed(self):
        start_time = datetime.now()

        first_event = {
            "username": "pi",
            "ip_address": "192.168.1.100",
            "timestamp": start_time
        }

        detect_threat(first_event)

        later_event = {
            "username": "pi",
            "ip_address": "192.168.1.100",
            "timestamp": start_time + timedelta(seconds=61)
        }

        detection = detect_threat(later_event)

        self.assertEqual(
            detection["attempt_count"],
            1
        )


if __name__ == "__main__":
    unittest.main()