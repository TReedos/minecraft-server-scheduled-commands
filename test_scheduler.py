"""
Unit tests for the Minecraft server scheduler.
"""

import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime

import config
from server_manager import MinecraftServerManager
from scheduler import should_server_be_running


class TestServerManager(unittest.TestCase):
    """Tests for the MinecraftServerManager class."""

    def test_initial_state(self):
        """Test that server manager starts in stopped state."""
        manager = MinecraftServerManager()
        self.assertFalse(manager.is_running())
        self.assertEqual(manager.get_status(), "Stopped")

    def test_stop_when_not_running(self):
        """Test stopping a server that isn't running."""
        manager = MinecraftServerManager()
        result = manager.stop_server()
        self.assertFalse(result)


class TestScheduleLogic(unittest.TestCase):
    """Tests for the scheduling logic."""

    def setUp(self):
        """Save original config values."""
        self.original_start = config.START_TIME
        self.original_stop = config.STOP_TIME

    def tearDown(self):
        """Restore original config values."""
        config.START_TIME = self.original_start
        config.STOP_TIME = self.original_stop

    def test_overnight_schedule_during_day(self):
        """Test overnight schedule during daytime hours."""
        config.START_TIME = "07:00"
        config.STOP_TIME = "02:00"

        with patch('scheduler.datetime') as mock_datetime:
            mock_datetime.now.return_value = datetime(2025, 1, 1, 10, 0)  # 10:00 AM
            self.assertTrue(should_server_be_running())

    def test_overnight_schedule_before_stop(self):
        """Test overnight schedule before stop time."""
        config.START_TIME = "07:00"
        config.STOP_TIME = "02:00"

        with patch('scheduler.datetime') as mock_datetime:
            mock_datetime.now.return_value = datetime(2025, 1, 1, 1, 0)  # 1:00 AM
            self.assertTrue(should_server_be_running())

    def test_overnight_schedule_after_stop(self):
        """Test overnight schedule after stop time."""
        config.START_TIME = "07:00"
        config.STOP_TIME = "02:00"

        with patch('scheduler.datetime') as mock_datetime:
            mock_datetime.now.return_value = datetime(2025, 1, 1, 3, 0)  # 3:00 AM
            self.assertFalse(should_server_be_running())

    def test_overnight_schedule_before_start(self):
        """Test overnight schedule before start time."""
        config.START_TIME = "07:00"
        config.STOP_TIME = "02:00"

        with patch('scheduler.datetime') as mock_datetime:
            mock_datetime.now.return_value = datetime(2025, 1, 1, 5, 0)  # 5:00 AM
            self.assertFalse(should_server_be_running())

    def test_same_day_schedule(self):
        """Test schedule where start and stop are on the same day."""
        config.START_TIME = "09:00"
        config.STOP_TIME = "21:00"

        with patch('scheduler.datetime') as mock_datetime:
            # During running hours
            mock_datetime.now.return_value = datetime(2025, 1, 1, 12, 0)  # 12:00 PM
            self.assertTrue(should_server_be_running())

            # Before start
            mock_datetime.now.return_value = datetime(2025, 1, 1, 8, 0)  # 8:00 AM
            self.assertFalse(should_server_be_running())

            # After stop
            mock_datetime.now.return_value = datetime(2025, 1, 1, 22, 0)  # 10:00 PM
            self.assertFalse(should_server_be_running())


if __name__ == "__main__":
    unittest.main()
