# Credit to @Quattro for the original implementation - https://discord.com/channels/736279277242417272/761721971129843712/1005966507114758224
from __future__ import annotations
from typing import Any, Callable
from enum import Enum

import dearpygui.dearpygui as dpg


class AlignmentType(Enum):
    HORIZONTAL = 0
    VERTICAL = 1
    BOTH = 2


def auto_align(
        item: int | str,
        alignment_type: AlignmentType = AlignmentType.HORIZONTAL, 
        x_align: float = 0.5, 
        y_align: float = 0.5
    ):
    def _center_h(_s, _d, data):
        parent = dpg.get_item_parent(data[0])
        while dpg.get_item_info(parent)['type'] != "mvAppItemType::mvWindowAppItem":  # type: ignore
            parent = dpg.get_item_parent(parent)  # type: ignore
        parent_width = dpg.get_item_rect_size(parent)[0]  # type: ignore
        width = dpg.get_item_rect_size(data[0])[0]
        new_x = (parent_width // 2 - width // 2) * data[1] * 2
        dpg.set_item_pos(data[0], [new_x, dpg.get_item_pos(data[0])[1]])

    def _center_v(_s, _d, data):
        parent = dpg.get_item_parent(data[0])
        while dpg.get_item_info(parent)['type'] != "mvAppItemType::mvWindowAppItem":  # type: ignore
            parent = dpg.get_item_parent(parent)  # type: ignore
        parent_height = dpg.get_item_rect_size(parent)[1]  # type: ignore
        height = dpg.get_item_rect_size(data[0])[1]
        new_y = (parent_height // 2 - height // 2) * data[1] * 2
        dpg.set_item_pos(data[0], [dpg.get_item_pos(data[0])[0], new_y])

    if alignment_type in AlignmentType:
        with dpg.item_handler_registry() as handler:
            if alignment_type == AlignmentType.HORIZONTAL:
                dpg.add_item_visible_handler(callback=_center_h, user_data=[item, x_align])
            elif alignment_type == AlignmentType.VERTICAL:
                dpg.add_item_visible_handler(callback=_center_v, user_data=[item, y_align])
            elif alignment_type == AlignmentType.BOTH:
                dpg.add_item_visible_handler(callback=_center_h, user_data=[item, x_align])
                dpg.add_item_visible_handler(callback=_center_v, user_data=[item, y_align])

        dpg.bind_item_handler_registry(item, handler)


def add_centered_text(
        default_value : str ='',
        alignment_type: AlignmentType = AlignmentType.HORIZONTAL,
        *, 
        label: str | None = None,
        user_data: Any =None, 
        use_internal_label: bool =True, 
        tag: int | str = 0, 
        indent: int =-1, 
        parent: int | str = 0, 
        before: int | str = 0, 
        source: int | str = 0, 
        payload_type: str ='$$DPG_PAYLOAD', 
        drag_callback: Callable | None = None, 
        drop_callback: Callable | None = None, 
        show: bool =True, 
        pos: list[int] | tuple[int, ...] = [], 
        filter_key: str ='', 
        tracked: bool =False, 
        track_offset: float =0.5, 
        wrap: int =-1, 
        bullet: bool =False, 
        color: list[int] | tuple[int, ...] = (-255, 0, 0, 255), 
        show_label: bool =False, 
        **kwargs
    ):
    with dpg.group(parent=parent):
        dpg.add_text(
            default_value, 
            label=label,   # type: ignore
            user_data=user_data, 
            use_internal_label=use_internal_label, 
            tag=tag, 
            indent=indent, 
            before=before, 
            source=source, 
            payload_type=payload_type, 
            drag_callback=drag_callback,   # type: ignore
            drop_callback=drop_callback,  # type: ignore
            show=show, pos=pos, 
            filter_key=filter_key, 
            tracked=tracked, 
            track_offset=track_offset, 
            wrap=wrap, 
            bullet=bullet, 
            color=color, 
            show_label=show_label, 
            **kwargs
        )
        auto_align(dpg.last_item(), alignment_type)


def add_multi_line_centered_text(text, parent, wrap=None):
    char_width = 7.25
    available_width = 498

    text_width = len(text) * char_width
    center_x = int((available_width - text_width) / 2) - 2
    wrap_width = wrap if wrap is not None else available_width

    with dpg.group(horizontal=True, parent=parent):
        dpg.add_spacer(width=max(center_x, 0))
        dpg.add_text(text, wrap=wrap_width)
