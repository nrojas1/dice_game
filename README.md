# DixMille py
A command line game to play Dice 10,000 (Dix Mille, 6-Dice, 10,000 Dice, Ten Grand)


Since COVID-19, hanging out and playing dice isn't recommended. Still, people want to play dice! So here is a script that runs with `python`
that keeps score, throws the dice, and let's you play Dix Mille with multiple players. Here is a wiki about the game: https://en.wikipedia.org/wiki/Dice_10000


The idea is to have one person run the script on his personal computer and share his/her screen with other people on any given web chat
platform.

## Scoring
Everyone has their own way of playing (given the number of names this games has...) so here are the rules used in **this** dice game.
* Single fives are worth 50 points
* Single ones are worth 100 points
* Three of a kind are worth 100 points times the number rolled, except for three ones which are worth 1000 points
* A straight from 1 to 6 is worth 1000 points
* Points are added to make a score

## Rules
* The game is played in rounds. Each player has a go per round.
* A players' go involves:
    1. him/her throwing 6 dice
    2. putting aside at least one scoring dice (three of a kind, 1 or 5)
    3. throwing the others and repeating step ii until her/him can write down the score on the scoreboard


* A player can write her/his score down if the score in the dice put aside in step ii is greater than **350 points** unless it is the 
players first score.
* If it is the first score on the scoreboard for the player (i.e. had 0 points before this moment) the score of the dice put aside must be 
greater than **450 points**.

## Running the script
To run this you need `python3`. If you don't have it, download here: https://www.python.org/downloads/

Simply download the file, open the terminal, write `cd <downloaded file>` where `<downloaded file>` is the path to the script. Then type
`python3 main.py` and play away.
