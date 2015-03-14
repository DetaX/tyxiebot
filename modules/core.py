from os import system


def on_welcome(self, serv, ev):
        serv.send_raw("WHOIS " + ev.target().split('/')[0])
        for chan in self.chans:
            serv.join(chan)


def on_whoischannels(self, serv, ev):
    if ev.target() == ev.arguments()[0]:
        chans = ev.arguments()[1].split(' ')
        for chan in chans:
            if chan and chan not in self.chans:
                if chan[0] != '#':
                    serv.part(chan[1:])
                else:
                    serv.part(chan)


def on_pubmsg(self, serv, ev):
    chan = ev.target()
    msg = ev.arguments()[0]
    msg_split = msg.split()
    if msg_split[0] == '!reload':
        serv.privmsg(chan, 'Reloading...')
        system('python bot.py &')
        self.die()