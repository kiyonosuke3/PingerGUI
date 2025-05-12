import re
from flet import TextField


class IpAddressTextField(TextField):
    def __init__(self, *args, on_submit=None, **kwargs):
        # on_change イベントをフック
        super().__init__(*args, on_change=self._on_change, on_submit=on_submit, **kwargs)

    def _on_change(self, e):
        """
        入力値を検証・整形します。
        ・許可文字は 0-9、ドット(.)（最大3つまで）、カンマ(,)、ハイフン(-)、アスタリスク(*) のみ
        ・セグメント（区切り記号で分割された部分）は 0～255 の値のみ許可
        """
        text = self.value or ""
        # 区切り文字を含めて分割
        parts = re.split(r"([.,\-*])", text)
        new_text = ""

        for part in parts:
            if part in ".,-*":
                # ドットは3回まで
                if part == "." and new_text.count(".") >= 3:
                    continue
                # その他の区切り文字はそのまま
                new_text += part
            else:
                # 数字以外を除去
                digits = "".join(filter(str.isdigit, part))
                # 最大3桁に制限
                if len(digits) > 3:
                    digits = digits[:3]
                # 0～255 の範囲に収める
                if digits:
                    num = int(digits)
                    if num > 255:
                        digits = "255"
                new_text += digits

        # テキストが変わっていれば更新
        if new_text != text:
            self.value = new_text
            self.page.update(self)
