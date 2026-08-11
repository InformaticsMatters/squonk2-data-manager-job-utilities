"""Command-line helpers shared by Job scripts: an argparse builder for the
progress/cost reporting option, and a ProgressReporter that wraps the
interval-based event/cost reporting idiom used throughout those scripts.

The molecule "Input/output options" group lives in ``rdkit_utils`` as
``add_common_molecule_io_args()``, beside the readers and writers its options
feed. Only the Data Manager logging concerns are here.
"""

import argparse
from typing import Optional

from dm_job_utilities.dm_log import DmLog


def add_reporting_args(
    parser: argparse.ArgumentParser,
    *,
    interval_default: Optional[int] = None,
) -> argparse._ArgumentGroup:  # pylint: disable=protected-access
    """Add the "Reporting options" argument group, and return the group so a
    caller can add more options to it.

    Adds ``--interval``, the record count between "Processed N records" events,
    which pairs with :class:`ProgressReporter`.

    :param interval_default: default reporting interval. ``None`` — the
        default — means no progress events are emitted unless the Job is run
        with ``--interval``, which matches the behaviour of most Jobs today.
        Pass a value for Jobs that should report by default.
    """
    group = parser.add_argument_group("Reporting options")
    group.add_argument(
        "--interval",
        type=int,
        default=interval_default,
        help="Reporting interval (number of records between progress events)",
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
