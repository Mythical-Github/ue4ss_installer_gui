from typing import Protocol, Any
import dearpygui.dearpygui as dpg


class StepFunction(Protocol):
    def __call__(self, user_data: Any) -> None: ...


def push_setup_screen(
    tag: str,
    task_text: str,
    step_text_to_step_functions: dict[str, StepFunction],
    finished_all_steps_function: StepFunction,
    user_data: Any
):
    tags = [
        'task_text',
        'step_text',
        'progress_bar',
        tag
    ]

    for single_tag in tags:
        if dpg.does_item_exist(single_tag):
            dpg.delete_item(single_tag)

    with dpg.window(
        tag=tag,
        modal=True,
        no_title_bar=True,
        min_size=[524, 1],
        no_open_over_existing_popup=False,
        no_resize=True
    ):
        # later replace these buttons with actually centered text
        dpg.add_button(label=f'{task_text}:', tag='task_text', enabled=False, width=-1, height=28)
        dpg.add_spacer()
        dpg.add_button(label="Starting...", tag='step_text', enabled=False, width=-1, height=28)
        dpg.add_spacer()
        dpg.add_progress_bar(default_value=0.0, tag='progress_bar', width=-1, height=28)

        step_keys = list(step_text_to_step_functions.keys())
        total_steps = len(step_keys)
        progress = 0.0
        step_increment = 1.0 / total_steps if total_steps > 0 else 1.0

        for i, step_name in enumerate(step_keys):
            dpg.set_item_label('step_text', step_name)
            function_to_call = step_text_to_step_functions[step_name]
            function_to_call(user_data)
            progress += step_increment
            dpg.set_value('progress_bar', progress)

        dpg.set_item_label('step_text', "Setup complete.")
        finished_all_steps_function(user_data)
