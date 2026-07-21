"""Command-line helpers shared by Job scripts: an argparse builder for the
"Input/output options" group re-typed across the descriptor generators,
train_test_split and other Jobs, and a ProgressReporter that wraps the
interval-based event/cost reporting idiom used throughout those scripts.
"""

import argparse
from typing import Optional, Union

from dm_job_utilities.dm_log import DmLog


def str_or_int(value: str) -> Union[str, int]:
    """Argparse type for column specifiers that may be given as a zero-based
    integer index or as a field name. Returns an int when the value looks
    like one, otherwise returns the original string.
    """
    try:
        return int(value)
    except ValueError:
        return value


def add_common_io_args(
    parser: argparse.ArgumentParser,
    output_default: Optional[str] = None,
) -> argparse._ArgumentGroup:
    """Add the "Input/output options" argument group that's re-typed in
    numerous Job scripts (the descriptor generators, train_test_split, skl).

    Adds -i/--input (accepting the --infile alias used by some Jobs),
    -o/--output, -d/--delimiter, --id-column, --mol-column, --y-column,
    --read-header, --write-header, --read-records, --interval and
    --omit-fields. The column options use str_or_int so a Job can accept
    either a zero-based column index or a field name.
    """
    group = parser.add_argument_group("Input/output options")
    group.add_argument(
        "-i",
        "--input",
        "--infile",
        dest="input",
        required=True,
        help="Input file (.smi, .sdf or .tab/.txt)",
    )
    group.add_argument(
        "-o", "--output", default=output_default, help="Output file"
    )
    group.add_argument("-d", "--delimiter", help="Delimiter when using SMILES")
    group.add_argument(
        "--id-column",
        type=str_or_int,
        help="Column for the molecule ID (zero-based index or field name)",
    )
    group.add_argument(
        "--mol-column",
        type=str_or_int,
        help="Column for the molecule (zero-based index or field name)",
    )
    group.add_argument(
        "--y-column",
        type=str_or_int,
        help="Column for the Y variable (zero-based index or field name)",
    )
    group.add_argument(
        "--read-header",
        action="store_true",
        help="Read a header line with the field names when reading .smi or .txt",
    )
    group.add_argument(
        "--write-header",
        action="store_true",
        help="Write a header line when writing .smi or .txt",
    )
    group.add_argument(
        "--read-records",
        type=int,
        default=100,
        help="Read this many records to determine the fields that are present",
    )
    group.add_argument(
        "--interval", type=int, default=1000, help="Reporting interval"
    )
    group.add_argument(
        "--omit-fields",
        action="store_true",
        help="Don't include fields from the input in the output",
    )
    return group


class ProgressReporter:
    """Wraps the interval-based DmLog.emit_event("Processed N records") /
    trailing DmLog.emit_cost(N) idiom that recurs across the Job scripts.

    Call report() from within a processing loop, after incrementing the
    record count, and report_final() once after the loop completes.
    """

    def __init__(self, interval: Optional[int] = None):
        self.interval = interval

    def report(self, count: int) -> None:
        """Emit a "Processed N records" event if count has reached interval."""
        if self.interval and count % self.interval == 0:
            DmLog.emit_event(f"Processed {count} records")

    def report_final(self, count: int) -> None:
        """Emit the closing "Processed N records" event and the final cost."""
        DmLog.emit_event(f"Processed {count} records")
        DmLog.emit_cost(count)
