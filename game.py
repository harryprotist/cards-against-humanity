#!/usr/bin/python

# NOTE:
# This is the code. If you are seeing this when you open the program normally, please follow the steps here:
# https://sites.google.com/site/evanspythonhub/having-problems

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# INFO AREA:
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Program by: Evan
# PROGRAM made in 2012
# This program will facilitate games of Cards Against Humanity.

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# DATA AREA: (IMPORTANT: DO NOT MODIFY THIS SECTION!)
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

from __future__ import print_function
from rabbit.all import serverbase, strlist, random, readfile, openfile, basicformat, superformat, popup
import re

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# CODE AREA: (IMPORTANT: DO NOT MODIFY THIS SECTION!)
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class card(object):
    def __init__(self, text):
        self.text = str(text)
        if re.compile(r".* \(\d+\)").match(self.text):
            self.text, self.blanks = self.text.rsplit(" (", 1)
            self.blanks = int(self.blanks[:-1])
        else:
            self.blanks = 0
            inside = False
            for c in self.text:
                if c == "_" and not inside:
                    self.blanks += 1
                    inside = True
                else:
                    inside = False
    def __str__(self):
        out = self.text
        if self.blanks > 0:
            out += " ("+str(self.blanks)+")"
        return out
    def __eq__(self, other):
        if isinstance(other, card):
            return self.text == other.text and self.blanks == other.blanks
        else:
            return str(self) == other

def getcards(filenames):
    cards = []
    for name in filenames:
        try:
            f = openfile(name, "rb")
            for line in readfile(f).splitlines():
                line = basicformat(line)
                if not (line.startswith("#") or line.endswith(":")):
                    cards.append(card(basicformat(line)))
        except IOError:
            pass
        else:
            f.close()
    return cards

class main(serverbase):
    def __init__(self, name="Cards Against the Brotherhood", message="Loading...", height=35, speed=400, whites=["whites.txt"], blacks=["blacks.txt"], cards=10, debug=False):
        self.cards = int(cards)
        self.whites = whites
        self.blacks = blacks
        serverbase.__init__(self, name, message, height, speed, debug)
    def getwhites(self, count=1):
        self.whites, out = self.gen.take(self.whites, count)
        return out
    def getblacks(self, count=1):
        self.blacks, out = self.gen.take(self.blacks, count)
        return out
    def begin(self):
        self.printdebug(": BEGIN")
        self.gen = random()
        if self.server:
            self.whites = getcards(self.whites)
            self.printdebug("A#: "+str(len(self.whites)))
            self.blacks = getcards(self.blacks)
            self.printdebug("Q#: "+str(len(self.blacks)))
            self.scores = {None:0}
            for a in self.c.c:
                self.queue[a].append(strlist(self.getwhites(self.cards), ";;"))
                self.scores[a] = 0
            self.hand = self.getwhites(self.cards)
            self.order = [None]+self.c.c.keys()
            self.x = -1
        else:
            self.czar = False
            self.hand = map(card, self.receive().split(";;"))
        self.printdebug("A$: "+repr(self.hand))
        self.app.display("You just drew: '"+strlist(self.hand, "', '")+"'.")
        self.black = None
        self.played = []
        self.phased = False
        self.endturn(False)
        self.ready = True
    def phaseturn(self):
        self.phased = True
        if self.server == None:
            return False
        else:
            if self.server:
                played = [(self.played, None)]
                self.played = {}
                for m,a in played+self.receive():
                    if m != "$":
                        ms = map(card, m.split(";;"))
                        self.whites.extend(ms)
                        self.played[ms] = a
                self.broadcast("The cards played were: '"+strlist(self.played.keys(), "', '", lambda ms: "('"+strlist(ms, "', '")+"')")+"'.")
                played = {}
                for ms,a in self.played.items():
                    played[strlist(ms, "; ")] = a
                self.played = played
                if self.x:
                    self.send(strlist(self.played.keys(), ";;"), self.order[self.x])
                    for a in self.c.c:
                        if a != self.order[self.x]:
                            self.queue[a].append(strlist(self.getwhites(self.black.blanks), ";;"))
                else:
                    for a in self.c.c:
                        self.queue[a].append(strlist(self.getwhites(self.black.blanks), ";;"))
            else:
                if self.played:
                    self.send(strlist(self.played, ";;"))
                else:
                    self.send("$")
                if self.czar:
                    self.played = self.receive().split(";;")
                    self.app.display("Make your choice, Card Czar.")
                else:
                    drew = map(card, self.receive().split(";;"))
                    self.hand.extend(drew)
                    self.app.display("You just drew: '"+strlist(drew, "', '")+"'.")
            if not self.isczar():
                self.phased = False
                if self.server:
                    choice = self.receive()
                    self.scores[self.played[choice]] += 1
                    self.broadcast("An awesome point was awarded to '"+self.names[self.played[choice]]+"'.")
                self.played = None
                self.endturn()
        return True
    def endturn(self, send=True):
        if self.server:
            self.x += 1
            self.x %= len(self.order)
            self.broadcast("The Card Czar is: '"+self.names[self.order[self.x]]+"'.")
            if self.black:
                self.blacks.append(self.black)
            self.black = self.getblacks()[0]
            self.send(str(self.black))
            self.broadcast("The Black Card is: '"+str(self.black)+"'.")
            if send:
                if self.x == 0:
                    self.send("$")
                else:
                    self.send("!", self.order[self.x])
                    self.send("$", exempt=self.order[self.x])
        elif self.server != None:
            self.black = card(self.receive())
            if send:
                self.czar = self.receive() == "!"
        else:
            return False
        if self.isczar():
            self.phaseturn()
        return True
    def handler(self, event=None):
        if self.ready and self.server != None:
            self.process(self.box.output())
    def process(self, inputstring):
        original = basicformat(inputstring)
        foriginal = superformat(original)
        if foriginal.startswith("pick "):
            original = original[5:]
            testnum = isreal(original)
            if testnum and (testnum <= 0 or testnum > len(self.played) or testnum != int(testnum)):
                self.app.display("That's not a valid card index.")
            else:
                if testnum:
                    original = self.played.keys()[int(1+testnum)]
                else:
                    original = card(original)
                if not self.phased:
                    self.app.display("You can't pick yet, you're still in the playing stage.")
                elif not self.isczar():
                    self.app.display("You're not the Card Czar, so you're playing, not picking.")
                else:
                    test = False
                    for play in self.played:
                        if play.startswith(original):
                            original = play
                            test = True
                            break
                    if not test:
                        self.app.display("You can't pick a card that nobody played.")
                    else:
                        self.phased = False
                        if self.server:
                            self.scores[self.played[original]] += 1
                            self.broadcast("An awesome point was awarded to "+self.names[self.played[original]]+".")
                        else:
                            self.send(original)
                        self.played = None
                        self.endturn()
        elif foriginal.startswith("play "):
            original = original[5:]
            testnum = isreal(original)
            if testnum and (testnum <= 0 or testnum > len(self.hand) or testnum != int(testnum)):
                self.app.display("That's not a valid card index.")
            else:
                if testnum:
                    original = self.hand[int(1+testnum)]
                else:
                    original = card(original)
                if self.phased:
                    self.app.display("You can't play yet, you're still in the picking stage.")
                elif self.isczar():
                    self.app.display("You're the Card Czar, so you're picking, not playing.")
                else:
                    test = False
                    for choice in self.hand:
                        choice = str(choice)
                        if choice.startswith(original):
                            original = choice
                            test = True
                            break
                    if not test:
                        if ";" in original:
                            for item in original.split(";"):
                                self.process("play "+item)
                        else:
                            self.app.display("You can't play a card that you don't have in your hand.")
                    else:
                        self.played.append(original)
                        self.app.display("You just played: '"+str(self.played)+"'.")
                        self.hand.remove(self.played)
                        if len(self.played) < self.black.blanks:
                            self.app.display("You still have "+str(self.black.blanks-len(self.played))+" more cards to play.")
                        else:
                            self.phaseturn()
        elif foriginal == "score":
            if self.server:
                points = self.scores[None]
            else:
                self.send("%%")
                points = self.receive()
            self.app.display("You currently have "+str(points)+" awesome points.")
        elif foriginal == "hand":
            self.app.display("Your hand contains: '"+strlist(self.hand, "', '")+"'.")
        elif foriginal.startswith("say "):
            self.textmsg(original[4:])
        elif original:
            self.textmsg(original)
    def addsent(self, item):
        if self.server:
            item, a = item
            if item.startswith("+:"):
                item = item[2:]
                self.app.display(item)
                self.broadcast(item, exempt=a)
            elif item == "%%":
                self.send(str(self.scores[a]), a)
            else:
                self.sent[a].append(item)
        elif self.server != None:
            if item.startswith("+:"):
                self.app.display(item[2:])
            else:
                self.sent.append(item)
        else:
            return False
        return True
    def isczar(self):
        if self.server:
            return self.x == 0
        elif self.server != None:
            return self.czar
        else:
            return None
