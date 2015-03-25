# -*- coding: utf8 -*-
from bot import bot
from datetime import datetime
import sqlite3
import sys
from lib import irc_wrapper

quote_db = 'quote.db'
quote_table_name = 'quote'


class Quote:
    def __init__(self, id, message, date_time):
        self.id = id
        self.message = message
        self.datetime = date_time

    def __repr__(self):
        return self.message


class QuoteManager:
    def __init__(self):
        self.conn = sqlite3.connect(quote_db)
        #self.conn.text_factory = str
        self.text_factory = lambda x: str(x, 'utf-8', 'ignore')
        self.cur = self.conn.cursor()
        self.cur.execute(
            'create table if not exists ' + quote_table_name + ' (id integer primary key, message text, datetime text)')
        self.conn.commit()

    def __del__(self):
        self.cur.close()
        self.conn.close()

    def get_next_id(self):
        self.cur.execute('select id from ' + quote_table_name + ' order by id desc limit 1')
        id = self.cur.fetchone()
        if id:
            return id[0] + 1
        else:
            return 1

    def add_quote(self, quote):
        self.cur.execute('insert into ' + quote_table_name + ' (id, message, datetime) values (?,?,?)',
                         (quote.id, quote.message, quote.datetime))
        self.conn.commit()

    def del_quote(self, quote_id):
        self.cur.execute('delete from ' + quote_table_name + ' where id=?', (quote_id,))
        self.conn.commit()

    def get_quote(self, quote_id):
        self.cur.execute('select * from ' + quote_table_name + ' where id=?', (quote_id,))
        fetch = self.cur.fetchone()
        if fetch:
            return Quote(id=fetch[0], message=fetch[1], date_time=fetch[2])

    def get_quotes(self):
        quotes = self.search_quote('')
        return quotes

    def search_quote(self, message):
        quotes = []
        for row in self.cur.execute('select * from ' + quote_table_name + ' where message like \'%' + message + '%\''):
            quote = Quote(id=row[0], message=row[1], date_time=row[2])
            quotes.append(quote)
        return quotes


def on_welcome(self, serv, ev):
    bot.qm = QuoteManager()


def on_pubmsg(self, serv, ev):
    chan = ev.target
    msg = ev.arguments[0]
    msg_split = msg.split()

    if msg_split[0] == '!quote':
        if len(msg_split) > 1:
            if msg_split[1] == 'add':
                print(msg_split)
                if len(msg_split) > 3:
                    quote = Quote(id=bot.qm.get_next_id(), message=' '.join(msg_split[2:]), date_time=datetime.now())
                    bot.qm.add_quote(quote)
                    #irc_wrapper.privmsg(serv, chan, 'La citation a été ajoutée ! (' + str(quote.id) + ')')
                    #serv.send_raw('PRIVMSG %s :%s' % (chan, 'La citation a été ajoutée ! (' + str(quote.id) + ')'))
                    irc_wrapper.privmsg(serv, chan, 'La citation a été ajoutée ! (' + str(quote.id) + ')')
            if msg_split[1] == 'show':
                if len(msg_split) > 2:
                    quote = bot.qm.get_quote(msg_split[2])
                    if quote:
                        irc_wrapper.privmsg(serv, chan, '(' + quote.datetime + ') ' + quote.message)
                    else:
                        irc_wrapper.privmsg(serv, chan, 'La citation ' + msg_split[2] + ' n\'existe pas')
            if msg_split[1] == 'list':
                quotes = bot.qm.get_quotes()
                for quote in quotes:
                    irc_wrapper.privmsg(serv, chan, '#' + str(quote.id) + ' : (' + quote.datetime + ') ' + quote.message)
            if msg_split[1] == 'search':
                if len(msg_split) > 2:
                    quotes = bot.qm.search_quote(' '.join(msg_split[2:]))
                    for quote in quotes:
                        irc_wrapper.privmsg(serv, chan, '#' + str(quote.id) + ' : (' + quote.datetime + ') ' + quote.message)
            if msg_split[1] == 'del':
                if len(msg_split) > 2:
                    bot.qm.del_quote(msg_split[2])
                    irc_wrapper.privmsg(serv, chan, 'La citation ' + msg_split[2] + ' a été supprimée !')
