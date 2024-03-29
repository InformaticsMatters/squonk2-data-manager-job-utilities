Informatics Matters Data Manager Job Utilities
==============================================

.. image:: https://badge.fury.io/py/im-data-manager-job-utilities.svg
   :target: https://badge.fury.io/py/im-data-manager-job-utilities
   :alt: PyPI package (latest)

.. image:: https://github.com/InformaticsMatters/squonk2-data-manager-job-utilities/actions/workflows/build.yaml/badge.svg
   :target: https://github.com/InformaticsMatters/squonk2-data-manager-job-utilities/actions/workflows/build.yaml
   :alt: Build

.. image:: https://github.com/InformaticsMatters/squonk2-data-manager-job-utilities/actions/workflows/publish.yaml/badge.svg
   :target: https://github.com/InformaticsMatters/squonk2-data-manager-job-utilities/actions/workflows/publish.yaml
   :alt: Publish

A Python 2/3 package that simplifies the generation of *events* and *cost*
lines written to a **Squonk2 Job** stdout stream.

The following utilities are available: -

- ``DmLog.emit_event()``
- ``DmLog.emit_cost()``

A number of miscellaneous utilities are also included. These have been
extracted form the squonk2 virtual-screening ``utils.py`` module and moved
here into ``utils.py``.

Installation (Python)
=====================

The Job utilities are published on `PyPI`_ and can be installed from
there::

    pip install im-data-manager-job-utilities

Once installed you can use the available classes::

    >>> from dm_job_utilities.dm_log import DmLog
    >>> DmLog.emit_event('Hello World!')
    2022-02-03T16:39:27+00:00 # INFO -EVENT- Hello World!
    >>> from decimal import Decimal
    >>> DmLog.emit_cost(Decimal('5.7'))
    2022-02-03T16:40:16+00:00 # INFO -COST- 5.7 1


Costs are *total* by default but can be issued as an incremental value::

    >>> DmLog.emit_cost(Decimal('0.5'), incremental=True)
    2022-02-03T16:40:16+00:00 # INFO -COST- +0.5 2


The final value on each cost line is a unique sequence number. This value
is typically an integer that increments with each line. It is required and
is used by the Data Manager to avoid duplicating costs.

The Data Manager uses the `python-dateutil`_ package to parse
dates and times from the generated log lines. The package is extremely
tolerant of many formats but if you are in control of the
string, the preferred format would be to use a classic UTC ISO string like
``%Y-%m-%dT%H:%M:%S%z`` so that the date and time is written as::

    2022-03-20T10:49:41+00:00

.. _PyPI: https://pypi.org/project/im-data-manager-job-utilities
.. _python-dateutil: https://pypi.org/project/python-dateutil

Get in touch
============

- Report bugs, suggest features or view the source code `on GitHub`_.

.. _on GitHub: https://github.com/informaticsmatters/squonk2-data-manager-job-utilities
