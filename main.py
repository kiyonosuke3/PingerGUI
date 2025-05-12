import flet as ft
from add_destination_dialog import AddDestinationDialog
from config_dialog import ConfigDialog
from ping_sender import ping_sender
import asyncio
from time import sleep


def main(page: ft.Page):
    page.title = "PingerGUI"
    page.window.width, page.window.height = (600, 500)
    page.window.maximizable = False
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    conf_dlg = ConfigDialog()
    isCanceled = False

    def click_add_btn(e):
        e.page.open(AddDestinationDialog(add_list))

    def add_list(e, adr_lst):
        before_len = len(target_list.controls)
        for i, adr in enumerate(adr_lst):
            target_list.controls.append(
                ft.Container(
                    ft.Row(
                        [
                            ft.Text(adr, width=200, size=18),
                            ft.Text("0", width=100, size=18),
                            ft.Text("0", width=100, size=18),
                            ft.Text("", width=200, size=18),
                        ],
                        spacing=0,
                    ),
                    bgcolor=None if (i + before_len) % 2 else ft.Colors.PRIMARY_CONTAINER,
                    expand=True,
                )
            )
        e.page.update()

    def click_remove_list_btn(e):
        target_list.controls.clear()
        e.page.update()

    async def click_run_ping_btn(e):  # async としてマーク
        nonlocal isCanceled
        run_btn.visible = False
        stop_btn.visible = add_btn.disabled = remove_btn.disabled = setting_btn.disabled = True
        e.page.update()

        isCanceled = False
        loop_cnf = conf_dlg.value_other
        loop_cnt = 0

        while loop_cnt < loop_cnf["count"] if loop_cnf["count"] != 0 else True:  # 0で無限ループ
            for cont in target_list.controls:
                if isCanceled:
                    break
                # UIをブロックしないように、ping_senderを別スレッドで実行
                rslt = await asyncio.to_thread(ping_sender, cont.content.controls[0].value, **conf_dlg.value_ping)

                # Textコントロールの値を設定する前に文字列に変換
                cont.content.controls[1].value = str(int(cont.content.controls[1].value) + 1)
                if rslt[0]:
                    cont.content.controls[2].value = str(int(cont.content.controls[2].value) + 1)
                cont.content.controls[3].value = rslt[1]
                e.page.update()
                await asyncio.sleep(loop_cnf["interval"])  # asyncio.sleep を使用

            loop_cnt += 1
            if isCanceled:
                break
        run_btn.visible = True
        stop_btn.visible = add_btn.disabled = remove_btn.disabled = setting_btn.disabled = False
        e.page.update()

    def click_stop_ping_btn(e):
        nonlocal isCanceled
        isCanceled = True
        run_btn.visible = True
        stop_btn.visible = add_btn.disabled = remove_btn.disabled = setting_btn.disabled = False
        e.page.update()

    def click_clean_btn(e):
        for cont in target_list.controls:
            cont.content.controls[1].value = "0"
            cont.content.controls[2].value = "0"
            cont.content.controls[3].value = ""
        e.page.update()

    def click_setting_btn(e):
        e.page.open(conf_dlg)

    main_page = ft.Column(
        [
            ft.Row(
                [
                    ft.Row(
                        [
                            add_btn := ft.IconButton(icon=ft.Icons.ADD, on_click=click_add_btn, tooltip="Add target"),
                            remove_btn := ft.IconButton(
                                icon=ft.Icons.PLAYLIST_REMOVE,
                                on_click=click_remove_list_btn,
                                tooltip="Delete target",
                            ),
                            ft.VerticalDivider(),
                            run_btn := ft.IconButton(
                                icon=ft.Icons.PLAY_CIRCLE, on_click=click_run_ping_btn, tooltip="Ping send"
                            ),
                            stop_btn := ft.IconButton(
                                icon=ft.Icons.STOP_CIRCLE,
                                visible=False,
                                on_click=click_stop_ping_btn,
                                tooltip="Ping cancel",
                            ),
                            clean_btn := ft.IconButton(
                                icon=ft.Icons.CLEANING_SERVICES, on_click=click_clean_btn, tooltip="Clean the result"
                            ),
                        ],
                    ),
                    setting_btn := ft.IconButton(
                        icon=ft.Icons.SETTINGS, on_click=click_setting_btn, tooltip="Ping setting"
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            ft.Container(height=5),
            ft.Row(
                [
                    ft.Text("Target", width=200, size=18),
                    ft.Text("Count", width=100, size=18),
                    ft.Text("Failed", width=100, size=18),
                    ft.Text("detail", width=200, size=18),
                ],
                spacing=0,
            ),
            ft.Divider(height=10),
            target_list := ft.ListView(spacing=5, expand=True),
        ],
        expand=True,
        spacing=0,
    )

    conf_page = ft.Column(
        [
            ft.IconButton(icon=ft.Icons.ARROW_BACK),
        ]
    )

    page.add(main_page)


ft.app(main)
