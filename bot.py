# -*- coding: utf8 -*-

from lib import ircbot
import importlib
from ConfigParser import SafeConfigParser, NoOptionError
import json


class Bot(ircbot.SingleServerIRCBot):
    def __init__(self):
        self.parser = SafeConfigParser()
        self.parser.read('config.ini')
        server = self.parser.get('connection', 'server')
        port = self.parser.getint('connection', 'port')
        nickname = self.parser.get('connection', 'nickname')
        realname = self.parser.get('connection', 'realname')
        try:
            password = self.parser.get('connection', 'password')
        except NoOptionError:
            password = ''
        try:
            self.modules = json.loads(self.parser.get('modules', 'load'))
        except NoOptionError:
            self.modules = []

        ircbot.SingleServerIRCBot.__init__(self, [(server, port, password)],
                                           nickname, realname)

    def on_welcome(self, serv, ev):
        for module in self.modules:
            module = importlib.import_module('modules.' + module)
            try:
                function = getattr(module, 'on_welcome')
                function(self, serv, ev)
            except AttributeError:
                pass

    def on_pubmsg(self, serv, ev):
        for module in self.modules:
            module = importlib.import_module('modules.' + module)
            try:
                function = getattr(module, 'on_pubmsg')
                function(self, serv, ev)
            except AttributeError:
                pass

    def on_whoischannels(self, serv, ev):
        for module in self.modules:
            module = importlib.import_module('modules.' + module)
            try:
                function = getattr(module, 'on_whoischannels')
                function(self, serv, ev)
            except AttributeError:
                pass

bot = Bot()
if __name__ == "__main__":
    bot.start()

