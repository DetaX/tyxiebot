# -*- coding: utf8 -*-

from os import system
import json
from configparser import NoOptionError
from bot import bot


def on_welcome(self, serv, ev):
    try:
        self.chans = json.loads(self.parser.get('channels', 'join'))
    except NoOptionError:
        self.chans = []
    bot.nickname = ev.target.split('/')[0]
    serv.send_raw('WHOIS ' + bot.nickname)
    for chan in self.chans:
        serv.join(chan)
        serv.privmsg(chan, 'Bot loaded.')


def on_whoischannels(self, serv, ev):
    if ev.target == ev.arguments[0]:
        chans = ev.arguments[1].split(' ')
        for chan in chans:
            if chan and chan not in self.chans:
                if chan[0] != '#':
                    serv.part(chan[1:])
                else:
                    serv.part(chan)


def on_pubmsg(self, serv, ev):
    chan = ev.target
    msg = ev.arguments[0]
    msg_split = msg.split()
    if msg_split[0] == '!reload':
        serv.privmsg(chan, 'Reloading...')
        system('python bot.py &')
        self.die()