from munch import Munch

usefuls = {
    "curls": {
        "```curl -h```"
    },
    "bins": {
        "Wednesdays"
    }
}

useful_dict = Munch.fromDict(usefuls)
