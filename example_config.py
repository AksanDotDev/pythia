from munch import Munch

params = {
    "discord": {
        "token": FromDiscord
    }
}

config = Munch.fromDict(params)