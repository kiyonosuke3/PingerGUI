from flet import AlertDialog, Text, Column, OutlinedButton
from ip_address_text_field import IpAddressTextField
from ip_addr_parser import parse_ips


class AddDestinationDialog(AlertDialog):
    def __init__(self, func):
        self.func = func
        super().__init__(
            modal=False,
            title=Text("Destination IP Address"),
            content=Column(
                [
                    IpAddressTextField(label="IP Address", on_submit=self.add_button),
                    Text(
                        "カンマ(,)：複数IPの指定　ex.192.168.1.1,4,114\nハイフン(-)：連番IPの指定　ex.192.168.1.100-130\nアスタリスク(*)：0-255まですべて　ex.192.168.1.*"
                    ),
                ],
                tight=True,
            ),
            actions=[
                OutlinedButton("Cancel", on_click=self.close_dialog),
                OutlinedButton("Add", on_click=self.add_button),
            ],
            on_dismiss=self.close_dialog,
        )

    def add_button(self, e):
        try:
            self.func(e, parse_ips(self.content.controls[0].value))
            self.close_dialog(e)
        except ValueError as ve:
            self.content.controls[0].error_text = ve
            e.page.update()

    def close_dialog(self, e):
        e.page.close(self)
        e.page.update()
