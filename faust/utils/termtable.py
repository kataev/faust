"""Using :pypi:`terminaltables` to draw ANSI tables."""
import sys
from typing import Any, IO, Sequence, Type

from mode.utils import logging
from mode.utils.compat import isatty
from terminaltables import AsciiTable, SingleTable
from terminaltables.base_table import BaseTable as Table

__all__ = ['Table', 'TableDataT', 'table', 'logtable']

TableDataT = Sequence[Sequence[str]]


def table(data: TableDataT,
          *,
          title: str,
          target: IO = None,
          tty: bool = None,
          **kwargs: Any) -> Table:
    """Create suitable :pypi:`terminaltables` table for target.

    Arguments:
        data (Sequence[Sequence[str]]): Table data.

        target (IO): Target should be the destination output file
                     for your table, and defaults to :data:`sys.stdout`.
                     ANSI codes will be used if the target has a controlling
                     terminal, but not otherwise, which is why it's important
                     to pass the correct output file.
    """
    if target is None:
        target = sys.stdout
    if tty is None:
        tty = isatty(target)
    return _get_best_table_type(tty)(data, title=title, **kwargs)


def logtable(data: TableDataT,
             *,
             title: str,
             target: IO = None,
             tty: bool = None,
             headers: Sequence[str] = None,
             **kwargs: Any) -> str:
    """Prepare table for logging.

    Will use ANSI escape codes if the log file is a tty.
    """
    if tty is None:
        tty = logging.LOG_ISATTY
    if headers:
        data = [headers] + list(data)
    return table(data, title=title, target=target, tty=tty, **kwargs).table


def _get_best_table_type(tty: bool) -> Type[Table]:
    return SingleTable if tty else AsciiTable
