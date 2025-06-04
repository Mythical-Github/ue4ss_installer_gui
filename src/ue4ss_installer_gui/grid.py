from __future__ import annotations
import math
from enum import Enum
from collections.abc import Sized
from typing import Any, Callable, Optional

import dearpygui.dearpygui as dpg


class ColumnRowPreference(Enum):
    Column = 0
    Row = 1


def calculate_grid_dimensions(
    items: Sized,
    column_row_preference: ColumnRowPreference = ColumnRowPreference.Column,
    max_columns: Optional[int] = None,
    max_rows: Optional[int] = None,
) -> tuple[int, int]:
    count = len(items)
    if count == 0:
        return 0, 0

    max_side = math.ceil(math.sqrt(count)) + 1

    for rows in range(1, max_side + 1):
        if max_rows is not None and rows > max_rows:
            continue
        for cols in range(1, rows + 1):
            if max_columns is not None and cols > max_columns:
                continue
            if rows * cols >= count:
                if column_row_preference == ColumnRowPreference.Column:
                    return rows, cols
                else:
                    return cols, rows

    return count, 1


def add_spaced_item_grid(
    callbacks_with_kwargs: dict[str, dict[Callable[..., Any], dict[str, Any]]],
    column_row_preference: ColumnRowPreference = ColumnRowPreference.Column,
    max_columns: Optional[int] = None,
    max_rows: Optional[int] = None,
    parent_tag: str | int | None = None,
):
    counter = 0
    total = len(callbacks_with_kwargs)
    column_amount, row_amount = calculate_grid_dimensions(
        callbacks_with_kwargs, column_row_preference, max_columns, max_rows
    )

    table_kwargs = dict(
        header_row=False,
        resizable=False,
        policy=dpg.mvTable_SizingStretchProp,
        width=-1,
    )
    if parent_tag is not None:
        table_kwargs["parent"] = parent_tag  # type: ignore

    with dpg.table(**table_kwargs):  # type: ignore
        for _ in range(column_amount):
            dpg.add_table_column()

        for _ in range(row_amount):
            with dpg.table_row():
                for _ in range(column_amount):
                    if counter >= total:
                        break
                    inner_dict = list(callbacks_with_kwargs.values())[counter]
                    func, kwargs = next(iter(inner_dict.items()))
                    func(**kwargs)
                    counter += 1


# example var to pass
# example_variable: dict[str, dict[Callable[..., Any], dict[str, Any]]] = {
#     "button_1": {
#         dpg.add_button: {
#             "label": "Button One",
#             "width": -1,
#             "height": 28
#         }
#     },
#     "button_2": {
#         dpg.add_button: {
#             "label": "Button Two",
#             "width": -1,
#             "height": 28
#         }
#     }
# }
