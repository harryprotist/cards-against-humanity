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

from __future__ import with_statement, unicode_literals, print_function
from rabbit.all import (
    str,
    print,
    serverbase,
    strlist,
    random,
    readfile,
    openfile,
    basicformat,
    superformat,
    isreal,
    islist,
    Tkinter,
    console,
    entry,
    rootbind,
    formatisyes,
    formatisno,
    madeof,
    containsany,
    re
    )
import socket

try:
    import hackergen.phrasegen as hackergen
except ImportError:
    try:
        import hackergen
    except ImportError:
        hackergen = None
else:
    hackergen.tense("fut")

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# CODE AREA: (IMPORTANT: DO NOT MODIFY THIS SECTION!)
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# fake substitute for popup
def popup():
	pass

def getPhrase(*args, **kwargs):
    out = hackergen.getPhrase(*args, **kwargs)
    if out.endswith("."):
        out = out[:-1]
    return out

class card(object):
    def __init__(self, text, scan=False):
        if hackergen:
            out = self.phrasesub(text)
        else:
            out = str(text)
        self.blanks = 0
        if re.compile(r".* \(\d+\)").match(out):
            self.text, self.blanks = out.rsplit(" (", 1)
            self.blanks = int(self.blanks[:-1])
        elif scan:
            self.text = ""
            inside = False
            for c in out:
                if c != "_":
                    inside = False
                elif not inside:
                    do = False
                    if len(self.text) != 0 and self.text[-1] == "\\":
                        self.text = self.text[:-1]
                        if len(self.text) != 1 and self.text[-2] == "\\":
                            do = True
                    else:
                        do = True
                    if do:
                        self.blanks += 1
                        inside = True
                self.text += c
        else:
            self.text = out
        self.check()

    def check(self):
        if self.text:
            self.text = self.text[0].upper()+self.text[1:]
        else:
            raise ValueError("Cannot have an empty card.")

    def phrasesub(self, text):
        out = ""
        inside = False
        for c in str(text):
            if inside:
                if c == "}":
                    if inside is True:
                        inside = ""
                    parts = inside.split(":")
                    if len(parts) == 2:
                        done = False
                        if parts[0] and parts[0] != "fut":
                            try:
                                hackergen.tense(parts[0])
                            except:
                                done = None
                            else:
                                done = True
                        if done is not None:
                            if not parts[1]:
                                out += getPhrase()
                                inside = False
                            else:
                                try:
                                    num = int(parts[1])
                                except ValueError:
                                    inside = parts[1]
                                else:
                                    out += getPhrase(num)
                                    inside = False
                            if done:
                                hackergen.tense("fut")
                    if inside is not False:
                        out += "{"+inside+"}"
                        inside = False
                elif inside is True:
                    inside = c
                else:
                    inside += c
            elif c == "{":
                if len(out) != 0 and out[-1] == "\\":
                    if len(out) != 1 and out[-2] == "\\":
                        out = out[:-1]
                        inside = True
                    else:
                        out = out[:-1]+c
                else:
                    inside = True
            else:
                out += c
        if inside is True:
            out += "{"
        elif inside:
            out += "{"+inside
        return out

    def black(self):
        if self.blanks == 0:
            self.blanks = 1

    def white(self):
        self.blanks = 0

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

def getcards(filenames, black=False):
    cards = []
    for name in filenames:
	f = fakeFile()
        try:
            f = openfile(name, "rb")
            for line in readfile(f).splitlines():
                line = basicformat(line)
                if line and not line.startswith("#"):
                    if line.endswith(":"):
                        if len(line) > 1 and line[-2] == "\\":
                            line = line[:-2]+line[-1]
                        else:
                            continue
                    elif not black and line.endswith(".") and len(line) > 1:
                        if line[-2] == "\\":
                            if len(line) > 2 and line[-3] == "\\":
                                line = line[:-2]
                            else:
                                line = line[:-2]+line[-1]
                        elif not containsany(line[:-1], ["!", "?", "."]):
                            line = line[:-1]
                    line = line.replace("\\n", "\n").replace("\\\n", "\\n")
                    cards.append(card(line, black))
                    if black:
                        cards[-1].black()
                    else:
                        cards[-1].white()
        except IOError:
            print("WARNING: Unable to find file "+str(name))
        finally:
            f.close()
    return list(set(cards))

class ircbot():
    def __init__(self, ip, port, channel, nick="cabbot"):
        self.ip = ip
        self.port = port
        self.channel = channel

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect(ip, port)
        self.socket.send("USER " + (nick + " ") * 3 + ": This bot is for playing cards against the brotherhood\n")
        self.socket.send("NICK " + nick + "\n")
        self.socket.send("JOIN " + channel + "\n")

    def send(self, message):

    def psend(self, message)

class main():

    # fake functions
    def start(self):
        self.begin()
    def printdebug(self, string):
        pass

    def __init__(self, server,
        name="Cards Against the Brotherhood",
        message="Initializing...",
        speed=400,
        port=6775,
        whites=["whites.txt"],
        blacks=["blacks.txt"],
        cards=10,
        debug=False):

    def getinput(self):
        
        for 

main(True).start()
