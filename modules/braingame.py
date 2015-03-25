# -*- coding: utf8 -*-

import random
import operator
import re


class Question(object):
    state = 0  # Number of time question was print
    clues_left = 3

    def __init__(self, question, response):
        self.question = question
        self.response = response
        self.coded_response = ''
        for char in str(response):
            self.coded_response += '*' if char.isdigit() else char
        nb_stars = self.coded_response.count('*')
        self.clues_left = self.clues_left if nb_stars > self.clues_left else nb_stars-1

    def get_question(self):
        return self.question

    def get_response(self):
        return self.response

    def get_coded_response(self):
        if self.state > 0:
            if self.clues_left > 0:
                self.clues_left -= 1
                nb_stars = self.coded_response.count('*')
                if nb_stars > 1:
                    stars_pos = [m.start() for m in re.finditer('\*', self.coded_response)]
                    _c = list(self.coded_response)
                    clue_index = random.randint(0, nb_stars-1)
                    _c[stars_pos[clue_index]] = str(self.response)[stars_pos[clue_index]]
                    self.coded_response = ''.join(c for c in _c)
        self.state += 1
        return self.coded_response


class Calculus(Question):
    def __init__(self):
        ops = {'+': operator.add,
           '-': operator.sub,
           '*': operator.mul,
           '/': operator.truediv}
        num1 = random.randint(1,10)
        num2 = random.randint(1,10)
        num3 = random.randint(1,10)
        num4 = random.randint(1,10)
        op1 = random.choice(list(ops.keys()))
        op2 = random.choice(list(ops.keys()))
        op3 = random.choice(list(ops.keys()))
        response = round(ops.get(op3)(ops.get(op2)(ops.get(op1)(num1, num2), num3), num4), 2)
        if str(response)[-2:] == '.0':
            response = int(response)
        question = 'Calcul mental : ((({} {} {}) {} {}) {} {}) ?\n'.format(num1, op1, num2, op2, num3, op3, num4)
        super(Calculus, self).__init__(question, response)


class BrainGame():
    question = None

    def __init__(self):
        self.is_running = False

    def start(self):
        self.is_running = True

    def main_loop(self, verif_code):
        if verif_code == self.question:
            if self.is_running:
                if not self.question:
                    self.question = Calculus()
                if self.question:
                    if self.question.clues_left :
                        self.serv.privmsg(self.chan, self.question.get_question())
                        self.serv.privmsg(self.chan, self.question.get_coded_response())
                        if self.question.clues_left > 0:
                            self.serv.execute_delayed(10, self.main_loop, (self.question,))
                        else:
                            self.serv.execute_delayed(30, self.main_loop, (self.question,))
                    else:
                        self.serv.privmsg(self.chan, 'Bande de sous-merdes')
                        self.question = Calculus()
                        self.serv.execute_delayed(5, self.main_loop, (self.question,))

    def stop(self):
        self.is_running = False

    def found(self):
        self.question = None
        self.serv.execute_delayed(10, self.main_loop, (self.question,))

game = BrainGame()


def on_pubmsg(self, serv, ev):
    chan = ev.target
    msg = ev.arguments[0]
    msg_split = msg.split()
    game.serv = serv
    game.chan = chan
    if game.is_running:
        try:
            if float(msg) == game.question.get_response():
                serv.privmsg(chan, 'Bravo !')
                game.found()
        except:
            pass
    if msg_split[0] == '!braingame':
        if len(msg_split) > 1:
            if msg_split[1] == 'start':
                game.start()
                serv.privmsg(chan, 'BrainGame started !')
                serv.execute_delayed(delay=1, function=game.main_loop, arguments=(game.question,))
            if msg_split[1] == 'stop':
                game.stop()
                serv.privmsg(chan, 'BrainGame stopped !')

