import flet as ft
from add_destination_dialog import AddDestinationDialog
from config_dialog import ConfigDialog
from ping_sender import ping_sender
from time import sleep


def main(page: ft.Page):
    page.title = "PingerGUI"
    page.window.width, page.window.height = (600, 500)
    page.window.maximizable = False
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    dist_lst = []
    conf_dlg = ConfigDialog()
    isCanceled = False

    def add_btn(e):
        e.page.open(AddDestinationDialog(add_list))

    def add_list(e, adr_lst):
        nonlocal dist_lst
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
                    bgcolor=None if i % 2 else ft.Colors.PRIMARY_CONTAINER,
                    expand=True,
                )
            )
        dist_lst = adr_lst.copy()
        e.page.update()

    def remove_list(e):
        target_list.controls.clear()
        e.page.update()

    def run_ping_btn(e):
        nonlocal isCanceled
        run_btn.visible = False
        stop_btn.visible = True
        e.page.update()

        isCanceled = False
        loop_cnf = conf_dlg.value_other
        loop_cnt = 0
        while loop_cnt < loop_cnf["count"]:
            for cont in target_list.controls:
                if isCanceled:
                    break
                rslt = ping_sender(cont.content.controls[0].value, **conf_dlg.value_ping)
                cont.content.controls[1].value = int(cont.content.controls[1].value) + 1
                if rslt[0]:
                    cont.content.controls[2].value = int(cont.content.controls[2].value) + 1
                cont.content.controls[3].value = rslt[1]
                e.page.update()
                sleep(loop_cnf["interval"])
            if isCanceled:
                break
            if loop_cnf["count"] != 0:
                loop_cnt += 1
        run_btn.visible = True
        stop_btn.visible = False
        e.page.update()

    def stop_ping_btn(e):
        nonlocal isCanceled
        isCanceled = True
        run_btn.visible = True
        stop_btn.visible = False
        e.page.update()

    def clean_btn(e):
        for cont in target_list.controls:
            cont.content.controls[1].value = "0"
            cont.content.controls[2].value = "0"
            cont.content.controls[3].value = ""
        e.page.update()

    def setting_btn(e):
        e.page.open(conf_dlg)

    main_page = ft.Column(
        [
            ft.Row(
                [
                    ft.Row(
                        [
                            ft.IconButton(icon=ft.Icons.ADD, on_click=add_btn, tooltip="宛先リストに追加"),
                            ft.IconButton(
                                icon=ft.Icons.PLAYLIST_REMOVE, on_click=remove_list, tooltip="宛先リストを削除"
                            ),
                            ft.VerticalDivider(),
                            run_btn := ft.IconButton(
                                icon=ft.Icons.PLAY_CIRCLE, on_click=run_ping_btn, tooltip="Ping送出開始"
                            ),
                            stop_btn := ft.IconButton(
                                icon=ft.Icons.STOP_CIRCLE, visible=False, on_click=stop_ping_btn, tooltip="Ping送出中止"
                            ),
                            ft.IconButton(icon=ft.Icons.CLEANING_SERVICES, on_click=clean_btn, tooltip="結果を削除"),
                        ],
                    ),
                    ft.IconButton(icon=ft.Icons.SETTINGS, on_click=setting_btn),
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
