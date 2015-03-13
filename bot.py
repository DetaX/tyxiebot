# -*- coding: utf8 -*-

from lib import ircbot
from modules import quote


class Bot(ircbot.SingleServerIRCBot):
    def __init__(self):
        ircbot.SingleServerIRCBot.__init__(self, [("detax.eu", 8000, "lesuperpass")],
                                           "tyxiebot/tyxie", "tyxieBoT")

    def on_welcome(self, serv, ev):
        serv.join("#bot")

    def on_pubmsg(self, serv, ev):
        quote.on_pubmsg(self, serv, ev)


if __name__ == "__main__":
    Bot().start()