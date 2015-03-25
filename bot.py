# -*- coding: utf8 -*-

import importlib
from configparser import NoOptionError, ConfigParser
import json

from irc import bot
from irc import client

from lib.ssl_wrapper import wrap_socket_patched


class Bot(bot.SingleServerIRCBot):
    def __init__(self):
        self.parser = ConfigParser()
        self.parser.read('config.ini')
        server = self.parser.get('connection', 'server')
        port = self.parser.getint('connection', 'port')
        nickname = self.parser.get('connection', 'nickname')
        realname = self.parser.get('connection', 'realname')
        ssl = self.parser.get('connection', 'ssl')
        factory = None

        if ssl:
            factory = client.connection.Factory(wrapper=wrap_socket_patched)

        try:
            password = self.parser.get('connection', 'password')
        except NoOptionError:
            password = ''
        try:
            self.modules = json.loads(self.parser.get('modules', 'load'))
        except NoOptionError:
            self.modules = []

        print('Trying to connect to %s:%s' % (server, port))
        if factory is not None:
            bot.SingleServerIRCBot.__init__(self, [(server, port, password)], nickname, realname,
                                            connect_factory=factory)
        else:
            bot.SingleServerIRCBot.__init__(self, [(server, port, password)], nickname, realname)

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

