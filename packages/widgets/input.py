from flet_core import TextField


def Input(
        label=None,
        on_change=None,
        col=None,
        max_length=None
):
    return TextField(
        label=label,
        on_change=on_change,
        col=col,
        max_length=max_length,
        border_color="transparent",
        border_radius=8,
        filled=True,
    )
