import json
import sys
import urllib.request
import webbrowser
from os import path

from flet_core import (
    AlertDialog,
    Column,
    Divider,
    FilePicker,
    FilePickerResultEvent,
    Image,
    MainAxisAlignment,
    Page,
    ResponsiveRow,
    Row,
    ScrollMode,
    SnackBar,
    Text,
    TextAlign,
    TextButton,
    TextThemeStyle,
    Theme,
    ThemeMode,
)
from flet_core.dropdown import Option
from flet_runtime import app

from packages.date import generate_days, generate_months, is_big_month, is_leap_year
from packages.fetch import fetch_price
from packages.widgets import Button, Input, Select

root = path.dirname(path.realpath(__file__))
with open(f"{root}/assets/app-icon.txt", "r") as base64:
    app_icon = base64.readline()

with open(f"{root}/assets/third-party-licenses/{sys.platform}/THIRDPARTYLICENSES", "r") as file:
    third_party_licenses = file.read()


def main(page: Page):
    page.window_center()
    page.window_width = 1280
    page.window_height = 720
    page.title = "股票歷史價格"
    page.theme = Theme(color_scheme_seed="#7f0020")
    page.theme_mode = ThemeMode.SYSTEM
    page.scroll = ScrollMode.AUTO

    current_version = "23.9.1"

    endpoint = "https://gist.githubusercontent.com/ccpl17/be3362652dd53ad5f63962993b145a0e/raw/"

    with urllib.request.urlopen(endpoint) as endpoint:
        data = json.loads(endpoint.read().decode())
        remote_version = data["version"]

    def close_update_dialog(e):
        update_dialog.open = False
        page.update()

    def release_page(e):
        webbrowser.open("https://github.com/ccpl17/stock-historical-price/releases")
        close_update_dialog(e)

    update_dialog = AlertDialog(
        modal=True,
        title=Text("有可用的更新"),
        content=Text("你想要現在下載嗎"),
        actions=[
            TextButton("是", on_click=release_page),
            TextButton("否", on_click=close_update_dialog)
        ],
        actions_alignment=MainAxisAlignment.END
    )

    if current_version < remote_version:
        page.dialog = update_dialog
        update_dialog.open = True
        page.update()

    def start_date_change(e):
        try:
            start_year = int(start_year_input.value)
            if is_big_month(start_month_select.value):
                start_day_select.options = start_big_month_days
            elif not is_big_month(start_month_select.value):
                start_day_select.options = start_small_month_days
            if start_month_select.value == "02" and not is_leap_year(start_year):
                start_day_select.options = start_norm_feb_days
            elif start_month_select.value == "02" and is_leap_year(start_year):
                start_day_select.options = start_leap_feb_days
            start_day_select.update()
        except:
            pass

    def end_date_change(e):
        try:
            end_year = int(end_year_input.value)
            if is_big_month(end_month_select.value):
                end_day_select.options = end_big_month_days
            elif not is_big_month(end_month_select.value):
                end_day_select.options = end_small_month_days
            if end_month_select.value == "02" and not is_leap_year(end_year):
                end_day_select.options = end_norm_feb_days
            elif end_month_select.value == "02" and is_leap_year(end_year):
                end_day_select.options = end_leap_feb_days
            end_day_select.update()
        except:
            pass

    start_months = generate_months()
    end_months = generate_months()

    start_big_month_days = generate_days(31)
    start_small_month_days = generate_days(30)
    start_norm_feb_days = generate_days(28)
    start_leap_feb_days = generate_days(29)

    end_big_month_days = generate_days(31)
    end_small_month_days = generate_days(30)
    end_norm_feb_days = generate_days(28)
    end_leap_feb_days = generate_days(29)

    banner = Row([Image(src_base64=app_icon)], alignment=MainAxisAlignment.CENTER)
    title = Row([Text("股票歷史價格", style=TextThemeStyle.HEADLINE_LARGE)], alignment=MainAxisAlignment.CENTER)

    ticker = Input("股票代號")

    start_date = Text("開始日期")
    start_year_input = Input(
        "年",
        on_change=start_date_change,
        col={"xs": 12, "sm": 4},
        max_length=4
    )
    start_month_select = Select(
        "月",
        options=start_months,
        on_change=start_date_change,
        col={"xs": 12, "sm": 4}
    )
    start_day_select = Select(
        "日",
        options=[Option("日")],
        on_change=start_date_change,
        col={"xs": 12, "sm": 4}
    )

    end_date = Text("結束日期")
    end_year_input = Input(
        "年",
        on_change=end_date_change,
        col={"xs": 12, "sm": 4},
        max_length=4
    )
    end_month_select = Select(
        "月",
        options=end_months,
        on_change=end_date_change,
        col={"xs": 12, "sm": 4}
    )
    end_day_select = Select(
        "日",
        options=[Option("日")],
        on_change=end_date_change,
        col={"xs": 12, "sm": 4}
    )

    frequency = Select(
        "資料頻率",
        options=[
            Option(key="1d", text="每日"),
            Option(key="1wk", text="每週"),
            Option(key="1mo", text="每月")
        ])

    output_to_excel_button = Button(
        "輸出為 Excel 試算表",
        colorful=True,
        on_click=lambda _: get_directory_dialog.get_directory_path(),
        disabled=page.web
    )

    def get_directory_result(e: FilePickerResultEvent):
        try:
            if e.path:
                output_to_excel_button.disabled = True
                page.snack_bar = SnackBar(Text("請稍候"))
                page.snack_bar.open = True
                page.update()
                code = fetch_price(ticker.value,
                                   f"{start_year_input.value}-{start_month_select.value}-{start_day_select.value}",
                                   f"{end_year_input.value}-{end_month_select.value}-{end_day_select.value}",
                                   frequency.value,
                                   e.path)
                if code == 0:
                    output_to_excel_button.disabled = False
                    page.snack_bar = SnackBar(Text("操作成功"))
                    page.snack_bar.open = True
                    page.update()
                if code == 1:
                    output_to_excel_button.disabled = False
                    page.snack_bar = SnackBar(Text("操作失敗"))
                    page.snack_bar.open = True
                    page.update()
        except Exception:
            output_to_excel_button.disabled = False
            page.snack_bar = SnackBar(Text("操作失敗"))
            page.snack_bar.open = True
            page.update()

    get_directory_dialog = FilePicker(on_result=get_directory_result)
    page.overlay.extend([get_directory_dialog])

    def open_website(e):
        webbrowser.open("https://ccpl17.github.io/stock-historical-price/")

    open_website_button = Button("網站", on_click=open_website, col={"xs": 12, "sm": 4})

    about_dialog = AlertDialog(title=Text("股票歷史價格", text_align=TextAlign.CENTER),
                               content=Text(f"版本 {current_version}\n\n© 2023 鐘柏倫 (Cenlun Chung Po Lun)",
                                            text_align=TextAlign.CENTER))

    def toggle_about_dialog(e):
        page.dialog = about_dialog
        about_dialog.open = True
        page.update()

    third_party_licenses_dialog = AlertDialog(title=Text("第三方授權條款", text_align=TextAlign.CENTER),
                                              content=Column([Text(third_party_licenses)], scroll=ScrollMode.AUTO))

    about_button = Button("關於", on_click=toggle_about_dialog, col={"xs": 12, "sm": 4})

    def toggle_third_party_licenses_dialog(e):
        page.dialog = third_party_licenses_dialog
        third_party_licenses_dialog.open = True
        page.update()

    third_party_licenses_button = Button(
        "第三方授權條款",
        on_click=toggle_third_party_licenses_dialog,
        col={"xs": 12, "sm": 4}
    )

    page.add(
        Column(
            [
                banner,
                title,
                ticker,
                start_date,
                ResponsiveRow([start_year_input, start_month_select, start_day_select]),
                end_date,
                ResponsiveRow([end_year_input, end_month_select, end_day_select]),
                frequency,
                ResponsiveRow([output_to_excel_button]),
                Divider(),
                ResponsiveRow([open_website_button, about_button, third_party_licenses_button])
            ]
        )
    )


app(target=main)
