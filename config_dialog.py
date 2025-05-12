from flet import AlertDialog, Column, Text, TextField, OutlinedButton, NumbersOnlyInputFilter


class ConfigDialog(AlertDialog):
    def __init__(self):
        self.form_count = TextField(
            value=4,
            label="Repeat counts",
            dense=True,
            suffix_text="times",
            tooltip="If set to 0, ping will repeat endlessly",
        )
        self.form_interval = TextField(
            value=100, label="Wait intervals", dense=True, suffix_text="ms", input_filter=NumbersOnlyInputFilter()
        )
        self.form_timeout = TextField(
            value=4, label="Timeout", dense=True, suffix_text="s", input_filter=NumbersOnlyInputFilter()
        )
        self.form_TimeToLive = TextField(value=128, label="TTL", dense=True, input_filter=NumbersOnlyInputFilter())
        self.form_size = TextField(
            value=56, label="Block size", dense=True, suffix_text="Byte", input_filter=NumbersOnlyInputFilter()
        )
        super().__init__(
            title=Text("Configuration"),
            content=Column(
                [
                    self.form_count,
                    self.form_interval,
                    self.form_TimeToLive,
                    self.form_size,
                    self.form_timeout,
                ],
                tight=True,
            ),
            actions=[
                OutlinedButton("Cancel", on_click=self.close_dialog),
                OutlinedButton("OK", on_click=self.OK_button),
            ],
            on_dismiss=self.close_dialog,
        )

    def OK_button(self, e):
        self.close_dialog(e)

    def close_dialog(self, e):
        e.page.close(self)
        e.page.update()

    @property
    def value_ping(self):
        return {
            "timeout": int(self.form_timeout.value),
            "unit": "ms",
            "size": int(self.form_size.value),
            "ttl": int(self.form_TimeToLive.value),
        }

    @property
    def value_other(self):
        return {"count": int(self.form_count.value), "interval": float(self.form_interval.value) / 1000}
