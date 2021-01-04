from munch import Munch

params = {
    "discord": {
        "token": "FromDiscord",
    },
    "hosts": {
        "hostname": {
            "MAC": "MacAddress",
            "IPv4": "IPv4Address",
            "URL": "URL",
            "IPv6": "IPv6Address",
        }
    },
    "network": {
        "broadcast": "BroadcastIP",
    },
}

config = Munch.fromDict(params)
