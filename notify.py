import apprise
import os
import yaml

# from datetime import datetime

pbul = ""
msteams = ""

try:
    with open("notify.cfg", "r") as ymlfile:
        cfg = yaml.safe_load(ymlfile)
        pbul = cfg["pbul"]
        msteams = cfg["msteams"]
except FileNotFoundError:
    print("make sure you've got a notify.cfg file with secrets in it...")


def iphone(title="python notification", body=os.path.basename(__file__)):
    """
    usage:
    import notify
    sentence = "lets eat trail snacks"
    notify.iphone(sentence,sp.sentence(sentence)[2])
    """
    apobj = apprise.Apprise()
    # A pushbullet notification
    apobj.add(pbul)
    apobj.notify(body, title)


def teams(title="python notification", body=os.path.basename(__file__)):
    apobj = apprise.Apprise()
    # A teams notification
    apobj.add(msteams)
    apobj.notify(body, title)


# iphone("python script here", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
