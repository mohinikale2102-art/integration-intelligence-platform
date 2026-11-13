
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from app import database, repository
from app.services import simulator


class SimulatorTests(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_path = Path(self.temp_dir.name) / "test.db"

        self.db_patch = patch("app.database.DB_PATH", self.db_path)
        self.db_patch.start()

        database.initialize()
        simulator.seed()

    def tearDown(self):
        self.db_patch.stop()
        self.temp_dir.cleanup()

    def test_successful_delivery(self):
        result = simulator.create_order(
            "Test Customer", 125, "success"
        )

        self.assertEqual(result["event"]["status"], "success")
        self.assertEqual(result["event"]["http_status"], 200)

    def test_missing_field_is_rejected(self):
        result = simulator.create_order(
            "Test Customer", 125, "missing_order_id"
        )

        self.assertEqual(result["event"]["status"], "failed")
        self.assertEqual(result["event"]["http_status"], 400)

    def test_authentication_failure(self):
        result = simulator.create_order(
            "Test Customer", 125, "invalid_auth"
        )

        self.assertEqual(result["event"]["http_status"], 401)

    def test_timeout_is_recorded(self):
        result = simulator.create_order(
            "Test Customer", 125, "timeout"
        )

        self.assertEqual(result["event"]["http_status"], 504)

    def test_retry_creates_new_attempt(self):
        result = simulator.create_order(
            "Test Customer", 125, "missing_order_id"
        )

        event_id = result["event"]["id"]
        retried = simulator.retry_event(event_id)

        self.assertEqual(retried["status"], "success")
        self.assertEqual(len(repository.attempts(event_id)), 2)

        self.assertIsNotNone(
            repository.processed_event(event_id)
        )

    def test_duplicate_delivery_is_ignored(self):
        result = simulator.create_order(
            "Test Customer", 125, "duplicate"
        )

        event = result["event"]
        event_id = event["id"]
        order_id = result["order_id"]

        attempts = repository.attempts(event_id)

        self.assertEqual(len(attempts), 2)

        first_response = json.loads(
            attempts[0]["response_payload"]
        )

        second_response = json.loads(
            attempts[1]["response_payload"]
        )

        self.assertEqual(first_response["status"], "accepted")
        self.assertEqual(second_response["status"], "duplicate_ignored")

        self.assertEqual(attempts[0]["http_status"], 200)
        self.assertEqual(attempts[1]["http_status"], 200)

        self.assertEqual(
            repository.processed_event_count(order_id), 1
        )

        self.assertEqual(
            repository.order(order_id)["status"], "confirmed"
        )

    def test_repeated_event_processing_does_not_repeat_business_action(self):
        result = simulator.create_order(
            "Test Customer", 125, "success"
        )

        event_id = result["event"]["id"]
        order_id = result["order_id"]

        self.assertIsNotNone(
            repository.processed_event(event_id)
        )

        first_duplicate = repository.process_event_once(
            event_id, order_id, simulator.timestamp()
        )

        second_duplicate = repository.process_event_once(
            event_id, order_id, simulator.timestamp()
        )

        self.assertFalse(first_duplicate)
        self.assertFalse(second_duplicate)

        self.assertEqual(
            repository.processed_event_count(order_id), 1
        )

        self.assertEqual(
            repository.order(order_id)["status"], "confirmed"
        )



if __name__ == "__main__":
    unittest.main()
