from datetime import datetime
import unittest
from contextlib import redirect_stdout

import pytest

from dm_job_utilities.dm_log import DmLog

class StdoutRedirectionContext():
    class ListIO():
        def __init__(self):
            # Container for messages sent to stdout.
            self.output = []
        def write(self, s):
            # Filter empty strings or naked newline characters.
            if s in ("\n", ""):
                return
            self.output.append(s)

    def __enter__(self):
        self._buf = self.ListIO()
        self._ctx = redirect_stdout(self._buf)
        self._ctx.__enter__()
        return self._buf

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self._ctx.__exit__(exc_type, exc_value, exc_traceback)


class StdoutTestCase(unittest.TestCase):
    def assertStdout(self):
        return StdoutRedirectionContext()


class TestDmLogMethods(StdoutTestCase):

    def test_dmlog_emit_event(self):
        with self.assertStdout() as cm:
            DmLog.emit_event("Test message")
        self.assertEqual(len(cm.output), 1)
        self.assertIn("# INFO -EVENT- Test message", cm.output[0])

    def test_dmlog_emit_fatal_event(self):
        with pytest.raises(SystemExit) as pytest_wrapped_e:
            with self.assertStdout() as cm:
                DmLog.emit_fatal_event("Bang!")
        assert pytest_wrapped_e.type == SystemExit
        assert pytest_wrapped_e.value.code == 1
        self.assertEqual(len(cm.output), 1)
        self.assertIn("# CRITICAL -EVENT-", cm.output[0])
        self.assertIn("Bang!", cm.output[0])
        # Lines must start with an ISO-8601 a date
        date_str = cm.output[0].split()[0]
        date_time = datetime.fromisoformat(date_str)
        self.assertIsNotNone(date_time)

    def test_dmlog_emit_cost_incremental(self):
        DmLog.reset_cost_sequence_number()
        with self.assertStdout() as cm:
            DmLog.emit_cost(4.0)
            DmLog.emit_cost(8.0)
        self.assertEqual(len(cm.output), 2)
        self.assertIn("# INFO -COST- 4.0 1", cm.output[0])
        self.assertIn("# INFO -COST- 8.0 2", cm.output[1])
        # Lines must start with an ISO-8601 a date
        date_str = cm.output[0].split()[0]
        date_time = datetime.fromisoformat(date_str)
        self.assertIsNotNone(date_time)

    def test_dmlog_emit_cost_non_incremental(self):
        DmLog.reset_cost_sequence_number()
        with self.assertStdout() as cm:
            DmLog.emit_cost(4.0, incremental=True)
            DmLog.emit_cost(4.0, incremental=True)
        self.assertEqual(len(cm.output), 2)
        self.assertIn("# INFO -COST- +4.0 1", cm.output[0])
        self.assertIn("# INFO -COST- +4.0 2", cm.output[1])
        # Lines must start with an ISO-8601 a date
        date_str = cm.output[0].split()[0]
        date_time = datetime.fromisoformat(date_str)
        self.assertIsNotNone(date_time)
