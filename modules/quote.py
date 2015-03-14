# -*- coding: utf8 -*-

from datetime import datetime
import sqlite3

quote_db = 'quote.db'
quote_table_name = 'quote'


class Quote:
    def __init__(self, citation, date_time):
        self.citation = citation
        self.datetime = date_time

    def __repr__(self):
        return self.citation


class QuoteManager:
    def __init__(self):
        self.conn = sqlite3.connect(quote_db)
        self.cur = self.conn.cursor()
        self.cur.execute(
            'create table if not exists ' + quote_table_name + ' (id integer primary key autoincrement, citation text, datetime text)')
        self.conn.commit()

    def __del__(self):
        self.cur.close()
        self.conn.close()

    def add_quote(self, quote):
        self.cur.execute('insert into ' + quote_table_name + ' (citation, datetime) values (?,?)',
                         (quote.citation, str(quote.datetime)))
        self.conn.commit()
        self.cur.execute('select id from ' + quote_table_name + ' order by id desc limit 1')
        return self.cur.fetchone()[0]

    def del_quote(self, quote_id):
        self.cur.execute('delete from ' + quote_table_name + ' where id=?', (quote_id,))
        self.conn.commit()

    def get_quote(self, quote_id):
        self.cur.execute('select * from ' + quote_table_name + ' where id=?', (quote_id,))
        fetch = self.cur.fetchone()
        if fetch:
            return Quote(citation=fetch[1], date_time=fetch[2])

    def get_quotes(self):
        quotes = []
        for row in self.cur.execute('select * from ' + quote_table_name):
            quote = Quote(citation=row[1], date_time=row[2])
            quotes.append(quote)
        return quotes

qm = QuoteManager()


def on_pubmsg(self, serv, ev):
    chan = ev.target()
    msg = ev.arguments()[0]
    msg_split = msg.split()

    if msg_split[0] == '!quote':
        if msg_split[1] == 'add':
            if len(msg_split) > 3:
                quote = Quote(citation=' '.join(msg_split[2:]), date_time=datetime.now())
                quote_id = qm.add_quote(quote)
                serv.privmsg(chan, 'La citation a été ajouté ! (' + str(quote_id) + ')')
        if msg_split[1] == 'show':
            if len(msg_split) > 2:
                quote = qm.get_quote(msg_split[2])
                if quote:
                    serv.privmsg(chan, '(' + quote.datetime + ') ' + quote.citation)
                else:
                    serv.privmsg(chan, 'La citation ' + msg_split[2] + ' n\'existe pas')
        if msg_split[1] == 'list':
            quotes = qm.get_quotes()
            for quote in quotes:
                serv.privmsg(chan, '(' + quote.datetime + ') ' + quote.citation)

