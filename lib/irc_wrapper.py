__author__ = 'tyxie'

'''
This file has a meaning only because the serv object given in the on_XX methods seems to have non-working one (looping).
If that's not the problem and you have an idea to solve it, please do so. For now this works and I'm fine with it.
'''

def privmsg(serv, target, text):
    serv.send_raw('PRIVMSG %s :%s' % (target, text))