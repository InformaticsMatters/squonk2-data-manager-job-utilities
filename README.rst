Informatics Matters Data Manager Job Utilities
==============================================

.. image:: https://badge.fury.io/py/im-data-manager-job-utilities.svg
   :target: https://badge.fury.io/py/im-data-manager-job-utilities
   :alt: PyPI package (latest)

A package that simplifies the generation of *events* and *cost lines*
written to the Job stdout stream.

The following utilities are supported: -

- DmLog.emit_event()
- DmLog.emit_cost()

Installation (Python)
=====================

The Job decoder is published on `PyPI`_ and can be installed from
there::

    pip install im-data-manager-job-utilities

Once installed you can use the utilities using the supplied classes::

    >>> from dm_job_utilities.dm_log import DmLog
    >>> from decimal import Decimal
    >>> DmLog.emit_event('Hello World!')
    2022-02-03T16:39:27+00:00 # INFO -EVENT- Hello World!
    >>> DmLog.emit_cost(Decimal('5.7'))
    2022-02-03T16:40:16+00:00 # INFO -COST- 5.7 1


Costs are *total* by default but can be issued as an incremental value::

    >>> DmLog.emit_cost(Decimal('0.5'), incremental=True)
    2022-02-03T16:40:16+00:00 # INFO -COST- +0.5 2


The final value on the COST line is a unique sequence number. This value
is required and is used by the Data Manager to avoid duplicating costs.

.. _PyPI: https://pypi.org/project/im-data-manager-job-utilities

Get in touch
============

- Report bugs, suggest features or view the source code `on GitHub`_.

.. _on GitHub: https://github.com/informaticsmatters/data-manager-job-utilities
