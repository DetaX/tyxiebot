# -*- coding: utf8 -*-

from datetime import datetime
import sqlite3
import irc
import json
from configparser import NoOptionError
from bot import bot

log_db = 'log.db'
log_table= 'log'


class LogManager:
    def __init__(self, chans):
        self.conn = sqlite3.connect(log_db)
        self.text_factory = lambda x: str(x, 'utf-8', 'ignore')
        self.cur = self.conn.cursor()
        self.chans = chans
        for chan in self.chans:
            self.cur.execute(
                'create table if not exists ' + log_table + ' (chan text, datetime text, author text, message text)')
            self.conn.commit()

    def __del__(self):
        self.cur.close()
        self.conn.close()

    def add_log(self, chan, date_time, author, message):
        self.cur.execute('insert into ' + log_table + ' (chan, datetime, author, message) values (?, ?,?,?)',
                         (chan, str(date_time), author, message))
        self.conn.commit()


def on_welcome(self, serv, ev):
    serv.__class__.privmsg = privmsg
    try:
        bot.lm = LogManager(json.loads(self.parser.get('log', 'chans')))
    except NoOptionError:
        pass


def privmsg(self, target, text):
    self.send_raw('PRIVMSG %s :%s' % (target, text))
    if target in bot.lm.chans:
        bot.lm.add_log(target, datetime.now(), bot.nickname, text)


def on_pubmsg(self, serv, ev):
    user = ev.source.nick
    chan = ev.target
    msg = ev.arguments[0]
    bot.lm.add_log(chan, datetime.now(), user, msg)