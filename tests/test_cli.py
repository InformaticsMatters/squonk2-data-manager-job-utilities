import argparse
import unittest
from unittest import mock

from dm_job_utilities.cli import ProgressReporter, add_common_io_args, str_or_int


class TestStrOrInt(unittest.TestCase):

    def test_int_like_value_returns_int(self):
        result = str_or_int("3")
        self.assertEqual(result, 3)
        self.assertIsInstance(result, int)

    def test_non_int_value_returns_original_string(self):
        self.assertEqual(str_or_int("SMILES"), "SMILES")


class TestAddCommonIoArgs(unittest.TestCase):

    def test_parses_expected_namespace(self):
        parser = argparse.ArgumentParser()
        add_common_io_args(parser)
        args = parser.parse_args(
            [
                "-i", "input.smi",
                "-o", "output.smi",
                "-d", "tab",
                "--id-column", "0",
                "--mol-column", "SMILES",
                "--y-column", "2",
                "--read-header",
                "--write-header",
                "--read-records", "50",
                "--interval", "500",
                "--omit-fields",
            ]
        )
        self.assertEqual(args.input, "input.smi")
        self.assertEqual(args.output, "output.smi")
        self.assertEqual(args.delimiter, "tab")
        self.assertEqual(args.id_column, 0)
        self.assertEqual(args.mol_column, "SMILES")
        self.assertEqual(args.y_column, 2)
        self.assertTrue(args.read_header)
        self.assertTrue(args.write_header)
        self.assertEqual(args.read_records, 50)
        self.assertEqual(args.interval, 500)
        self.assertTrue(args.omit_fields)

    def test_infile_is_an_alias_for_input(self):
        parser = argparse.ArgumentParser()
        add_common_io_args(parser)
        args = parser.parse_args(["--infile", "input.smi"])
        self.assertEqual(args.input, "input.smi")

    def test_defaults(self):
        parser = argparse.ArgumentParser()
        add_common_io_args(parser, output_default="out.smi")
        args = parser.parse_args(["-i", "in.smi"])
        self.assertEqual(args.output, "out.smi")
        self.assertIsNone(args.delimiter)
        self.assertIsNone(args.id_column)
        self.assertFalse(args.read_header)
        self.assertFalse(args.write_header)
        self.assertEqual(args.read_records, 100)
        self.assertEqual(args.interval, 1000)
        self.assertFalse(args.omit_fields)

    def test_input_is_required(self):
        parser = argparse.ArgumentParser()
        add_common_io_args(parser)
        with self.assertRaises(SystemExit):
            parser.parse_args([])


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
