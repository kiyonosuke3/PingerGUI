import itertools


def parse_octet(octet_str):
    """
    各オクテットを解析し、0-255の範囲で値のリストを返す。
    サポートする形式:
    - 単一の数字: '192'
    - カンマ区切り: '1,54,80'
    - ハイフンで範囲指定: '1-3'
    - ワイルドカード: '*'
    """
    if octet_str == "*":
        return list(range(0, 256))

    parts = octet_str.split(",")
    values = []
    for part in parts:
        if "-" in part:
            start, end = part.split("-")
            start = int(start)
            end = int(end)
            if start > end or not (0 <= start <= 255) or not (0 <= end <= 255):
                raise ValueError(f"無効な範囲: {part}")
            values.extend(range(start, end + 1))
        else:
            val = int(part)
            if not (0 <= val <= 255):
                raise ValueError(f"無効な値: {val}")
            values.append(val)
    return values


def parse_ips(input_str):
    """
    入力文字列を解析し、対応するIPアドレスのリストを返す。
    サポートする入力形式:
    - カンマ区切り
    - ハイフンによる範囲指定
    - ワイルドカード '*'
    """
    # 入力をドットで分割
    octets = input_str.strip().split(".")
    if len(octets) != 4:
        raise ValueError("IPアドレスの形式を満たしていません")

    # 各オクテットを解析
    try:
        parsed_octets = [parse_octet(octet) for octet in octets]
    except ValueError as ve:
        raise ValueError(ve)

    # すべての組み合わせを生成
    ip_list = []
    for o in itertools.product(*parsed_octets):
        ip = ".".join(map(str, o))
        ip_list.append(ip)

    return ip_list
