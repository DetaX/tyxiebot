# -*- coding: utf8 -*-

from datetime import datetime
import sqlite3
from lib import irclib
import json
from ConfigParser import NoOptionError
from bot import bot

log_db = 'log.db'
log_table_name_prefix = 'log_'


class LogManager:
    def __init__(self, chans):
        self.conn = sqlite3.connect(log_db)
        self.conn.text_factory = str
        self.cur = self.conn.cursor()
        self.chans = chans
        for chan in self.chans:
            self.cur.execute(
                'create table if not exists ' + log_table_name_prefix + chan.strip('#') + ' (datetime text, author text, message text)')
            self.conn.commit()

    def __del__(self):
        self.cur.close()
        self.conn.close()

    def add_log(self, chan, date_time, author, message):
        self.cur.execute('insert into ' + log_table_name_prefix + chan.strip('#') + ' (datetime, author, message) values (?,?,?)',
                         (str(date_time), author, message))
        self.conn.commit()


def on_welcome(self, serv, ev):
    serv.__class__.privmsg = privmsg
    try:
        bot.lm = LogManager(json.loads(self.parser.get('log', 'chans')))
    except NoOptionError:
        pass


def privmsg(self, target, text):
    self.send_raw("PRIVMSG %s :%s" % (target, text))
    if target in bot.lm.chans:
        bot.lm.add_log(target, datetime.now(), bot.nickname, text)


def on_pubmsg(self, serv, ev):
    user = irclib.nm_to_n(ev.source())
    chan = ev.target()
    msg = ev.arguments()[0]
    bot.lm.add_log(chan, datetime.now(), user, msg)