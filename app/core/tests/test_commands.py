"""
Test custom Django management commands.
"""

# to mock the behavior of the database
from unittest.mock import patch

# Error when trying to connect before the DB is ready
from psycopg2 import OperationalError as Psycopg2Error
from django.core.management import call_command

# Error when the DB is ready but not properly set up
from django.db.utils import OperationalError
from django.test import SimpleTestCase


# Command for mocking
@patch('core.management.commands.wait_for_db.Command.check')
class CommandTests(SimpleTestCase):
    """Test waiting for database if database ready."""
    def test_wait_for_db_ready(self, patched_check):

        # When check is called, we return true value
        patched_check.return_value = True

        # Execute wait_for_db.py
        call_command('wait_for_db')

        patched_check.assert_called_once_with(databases=['default'])

    # When database isn't ready.
    @patch('time.sleep')
    def test_wait_for_db_delay(self, patched_sleep, patched_check):
        """Test waiting for database when getting OPerationalError"""

        """Raise Psycopg2Error 2 times, next 3 time raise OperationalError,
        side_effect allows to raise exception call_command('wait_for_db')"""
        patched_check.side_effect = [Psycopg2Error] * 2 + \
            [OperationalError] * 3 + [True]

        call_command('wait_for_db')
        self.assertEqual(patched_check.call_count, 6)
        patched_check.assert_called_with(databases=['default'])
