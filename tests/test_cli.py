import argparse
import unittest
from unittest import mock

from dm_job_utilities.cli import ProgressReporter, add_reporting_args


class TestAddReportingArgs(unittest.TestCase):

    def test_parses_interval(self):
        parser = argparse.ArgumentParser()
        add_reporting_args(parser)
        args = parser.parse_args(["--interval", "500"])
        self.assertEqual(args.interval, 500)

    def test_interval_defaults_to_none(self):
        # None means "no progress events unless asked for", which is what most
        # Jobs do today - no Job manifest passes --interval.
        parser = argparse.ArgumentParser()
        add_reporting_args(parser)
        args = parser.parse_args([])
        self.assertIsNone(args.interval)

    def test_interval_default_can_be_set(self):
        parser = argparse.ArgumentParser()
        add_reporting_args(parser, interval_default=1000)
        args = parser.parse_args([])
        self.assertEqual(args.interval, 1000)

    def test_explicit_interval_overrides_the_default(self):
        parser = argparse.ArgumentParser()
        add_reporting_args(parser, interval_default=1000)
        args = parser.parse_args(["--interval", "25"])
        self.assertEqual(args.interval, 25)

    def test_returns_the_group_for_further_options(self):
        parser = argparse.ArgumentParser()
        group = add_reporting_args(parser)
        group.add_argument("--extra")
        args = parser.parse_args(["--extra", "value"])
        self.assertEqual(args.extra, "value")

    def test_namespace_feeds_the_reporter(self):
        parser = argparse.ArgumentParser()
        add_reporting_args(parser)
        args = parser.parse_args(["--interval", "10"])
        self.assertEqual(ProgressReporter(args.interval).interval, 10)


class TestProgressReporter(unittest.TestCase):

    @mock.patch("dm_job_utilities.cli.DmLog")
    def test_report_emits_event_on_interval(self, mock_dm_log):
        reporter = ProgressReporter(interval=10)
        for count in range(1, 21):
            reporter.report(count)
        self.assertEqual(mock_dm_log.emit_event.call_count, 2)
        mock_dm_log.emit_event.assert_any_call("Processed 10 records")
        mock_dm_log.emit_event.assert_any_call("Processed 20 records")
        mock_dm_log.emit_cost.assert_not_called()

    @mock.patch("dm_job_utilities.cli.DmLog")
    def test_report_is_silent_between_intervals(self, mock_dm_log):
        reporter = ProgressReporter(interval=10)
        reporter.report(1)
        mock_dm_log.emit_event.assert_not_called()

    @mock.patch("dm_job_utilities.cli.DmLog")
    def test_report_without_interval_never_emits(self, mock_dm_log):
        reporter = ProgressReporter()
        reporter.report(100)
        mock_dm_log.emit_event.assert_not_called()

    @mock.patch("dm_job_utilities.cli.DmLog")
    def test_report_final_emits_event_and_cost(self, mock_dm_log):
        reporter = ProgressReporter(interval=10)
        reporter.report_final(42)
        mock_dm_log.emit_event.assert_called_once_with("Processed 42 records")
        mock_dm_log.emit_cost.assert_called_once_with(42)


if __name__ == "__main__":
    unittest.main()
