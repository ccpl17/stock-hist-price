from flet_core import Dropdown


def Select(
        label=None,
        options=None,
        on_change=None,
        col=None
):
    return Dropdown(
        label=label,
        options=options,
        on_change=on_change,
        col=col,
        border_color="transparent",
        border_radius=8,
        filled=True,
    )
