Cards Against Humanity, IRC Version
======================

An extensible Cards Against Humanity game engine.

This fork is an IRC bot that allows a game to be run in an IRC channel.
Only one person needs to run the bot, and the rest of the players can
connect through the IRC server, controlling the game by private messaging
commands to the bot.

In order to run the bot, CardGame.py must be run with commandline arguments
for the server ip, port, and channel name (including the #), in that order.

## Commands:
* `cab prepare` - sets the bot to 'join' mode, where players can join
* `cab join` - joins the game, if the bot is in 'join' mode
* `cab play <number>` eg. `cab play 5` - plays the card with the number &lt;number&gt;. Note: after playing a card, your other cards' numbers may change.
* `cab cards` - tells the bot to PM you your cards. Note: it will PM you your cards automatically at the start of each round.
* `cab pick <beginning of card name>` eg. `cab pick na` - for the card czar, when it's time to pick a card. Case insensitive.
* `cab abort` - ends the game.

## Installation Instructions:

1. Download and install Python 2.7.8:
	* https://www.python.org/download/releases/2.7.8/
2. Download and unzip the latest version of Rabbit:
	* https://github.com/evhub/rabbit/releases/latest
3. Drag the "rabbit" folder into the "resources" folder
4. Run the CardGame executable file:
	* "CardGame.bat" on Windows
	* "CardGame.sh" on Unix (Mac, Linux, etc.)

## Hackergen Support:

1. Clone Hacker Phrase Gen:
	* https://github.com/evhub/hacker-phrase-generator
2. Copy the "hackergen" folder into the "resources" folder
	* _If there is no hackergen folder, copy all the contents of hacker-phrase-generator into "resources" directly_
