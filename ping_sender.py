import ping3


def ping_sender(target_ip, timeout, unit, size, ttl):
    if target_ip == "0.0.0.0":
        return 1, f"Invalid address"
    ping3.EXCEPTIONS = True
    try:
        result = ping3.ping(target_ip, timeout=timeout, unit=unit, size=size, ttl=ttl)
    except ping3.errors.Timeout:
        return 1, f"Timeout"
    except ping3.errors.TimeToLiveExpired:
        return 1, f"TTL"
    except ping3.errors.PingError:
        return 1, f"Error"
    else:
        return 0, f"reached:{result:.2f}(ms)"
