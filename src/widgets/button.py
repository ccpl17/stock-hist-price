from flet_core import (
    ButtonStyle,
    FilledButton,
    FilledTonalButton,
    RoundedRectangleBorder
)


def Button(
        text=None,
        colorful=None,
        on_click=None,
        col=None,
        disabled=None
):
    if colorful:
        return FilledButton(
            text=text,
            style=ButtonStyle(
                padding=17,
                shape=RoundedRectangleBorder(radius=8)
            ),
            on_click=on_click,
            col=col,
            disabled=disabled
        )
    else:
        return FilledTonalButton(
            text=text,
            style=ButtonStyle(
                padding=17,
                shape=RoundedRectangleBorder(radius=8)
            ),
            on_click=on_click,
            col=col,
            disabled=disabled
        )
