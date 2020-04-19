""" The famous dice game in command line format using classes """
import random; import time; import sys

class Game:
    """ Game class"""

    def __init__(self, n_players):
        self.n_players = n_players
        self.n_round = 1
        self.top_score = 0
        self.scoreboard = list()
        self.players = list()

    def round(self):
        """ Runs a game round where each player has a go """
        for player in self.players:
            print(f"\nIt is now {player.name}'s turn")
            player.throw(6)
            player.play_round(self)
            print(f"{player.hand}\nEnd of {player.name}'s turn... you bitch\n")
            time.sleep(2)
            player.running_score = 0
        [player.dice_kept.clear() for player in self.players]
        print(f"end of round {self.n_round}")
        self.n_round += 1
        if self.n_round > 2:
            self.topscore()
        self.update_scoreboard(self.scoreboard)
        print(f"Scoreboard: {self.scoreboard}")
        time.sleep(3)
        if self.top_score <= 10000:
            print('Starting next round...'); time.sleep(2)

    def update_scoreboard(self, scoreboard):
        """ Creates an instance score and appends it to game scoreboard """
        current_score = dict()
        for player in self.players:
            current_score[player.name] = player.score
        scoreboard.append(current_score)
        return scoreboard

    def podium(self):
        """ Prints end of game stats """
        finish_line = self.scoreboard[-1]
        finish_line = sorted((score, name) for (name, score) in finish_line.items())
        winner = finish_line[-1]
        second = finish_line[-2]
        third = finish_line[-3]
        string = ''
        string += "\n\n\n-----------------------GAME--OVER--------------------\n"
        string += f"NUMBER OF ROUNDS PLAYED: {self.n_round}\n\n\n\n"
        string += f"WINNER: {winner[1]} with {winner[0]} points\n\n\n"
        string += f"SECOND: {second[1]} with {second[0]} points\n\n"
        string += f"THIRD: {third[1]} with {third[0]} points\n"
        return string

    # def get_score(self):
    #     return self.score
    #
    def topscore(self):
        """ Sets Game topscore to the highest score on the scoreboard """
        latest_round_score = self.scoreboard[-1]
        latest_round_score = sorted((score, name) for (name, score) in latest_round_score.items())
        top = latest_round_score[-1][0]
        self.top_score = top
        return self.top_score

class Player:
    """ Player class """

    def __init__(self, name):
        self.name = name
        self.score = 0
        self.running_score = 0
        self.hand = list()
        self.dice_kept = list()
        self.stop_round = 0
        self.is_on_scoreboard = 0

    def update_score(self, val):
        """ Add Player.running_score to Player.score """
        self.score += val

    def throw(self, n_dice):
        """ Creates a Player.hand given the number of dice """
        self.hand = [random.randint(1, 6) for dice in range(0, n_dice)]
        return self.hand

    def valid_throw(self):
        """ Verifies if Player.hand has playable numbers """
        # looking for triples
        trpl_dices = [dice for dice in self.hand if self.hand.count(dice) in [3, 4, 5, 6]]

        # looking for golden dice
        gold_dices = [dice for dice in self.hand if dice in [5, 1]]

        # looking for 123456
        one_to_six = (1, 2, 3, 4, 5, 6)
        diamond_dices = all(elem in self.hand for elem in one_to_six)

        return True if trpl_dices or gold_dices or diamond_dices else False

    def above_water(self):
        """
            Tests if the player has enough points to save them as well as
            checking if it is his first score on the scoreboard
        """
        return True if (self.is_on_scoreboard == 0 and self.running_score >= 450) or (self.is_on_scoreboard == 1 and self.running_score >= 350) else False

    def throw_to_score(self, hand):
        """ Takes dice values and returns its game score """
        if not hand:
            sys.exit()
        hand.sort(); triple = 3; prev = -1; count = result = 0

        # single score
        result += hand.count(5)*50
        result += hand.count(1)*100

        # triple score
        for dice in hand:
            if dice == prev:
                count += 1
            else:
                count = 1
            prev = dice
            if count == triple:
                if dice != 1:
                    if dice == 5:
                        result += (dice*100)-150
                    else:
                        result += dice*100
                else:
                    result += (dice*1000)-300
        return result

    def play_round(self, game):
        """ Game action function for individual player """
        # play while you have a valid throw or your hand is empty
        while self.valid_throw() or len(self.hand) == 0:
            if len(self.hand) == 0:
                print('cool! A new hand coming right up\n')
                time.sleep(2)
                self.throw(6)
                continue
            print(self.hand, ' hand')
            print(self.dice_kept, ' dicekept')
            while True:
                # user input
                selected_dice = input('What dices do you wish to keep? (seperate by comma)\n')
                try:
                    dice_arr = selected_dice.strip().split(',')
                    dice_arr = [int(dice) for dice in dice_arr]
                    #print(dice_arr,'\n')
                    hand_match = [dice for dice in dice_arr if dice in self.hand]
                    #print(len(dice_arr),':',len(hand_match),'\n')
                    if len(hand_match) != len(dice_arr):
                        raise ValueNotInError
                    if not valid_selection(hand_match):
                        raise ValueNotCorrect
                    for dice in hand_match:
                        self.dice_kept.append(int(dice))
                        self.hand.pop(self.hand.index(int(dice)))
                    break
                except ValueError:
                    print('The dice entered must be numbers\n')
                except ValueNotInError:
                    print("The dice don't match the hand... try again\n")
                except ValueNotCorrect:
                    print('Ones, fives and triples are only allowed in selection\n')
            self.running_score += self.throw_to_score(hand_match)
            if self.above_water() and len(self.hand) != 0:
                while True:
                    user_stop = input(f"""\nWould you like to stop with {self.running_score} points?\n1: Yes\n2: No\n""")
                    try:
                        user_stop = int(user_stop)
                        if user_stop not in [1, 2]:
                            continue
                    except ValueError:
                        print('1: Continue\n2: Stop here')
                        continue
                    if user_stop == 1:
                        self.update_score(self.running_score)
                        self.is_on_scoreboard = 1
                        break

                    elif user_stop == 2:
                        self.throw(len(self.hand))
                        self.stop_round = 1
                        break
            else:
                print('replaying...')
                self.throw(len(self.hand))
    # def get_score(self):
    #     return self.score
    #
    # def get_name(self):
    #     return self.name

class Error(Exception):
    """ Base class for other exceptions """
    pass

class ValueNotInError(Error):
    """ Raised when the user input's values don't match the Game hand values """
    pass

class ValueNotCorrect(Error):
    """ Raised when user's input is not a Game scoring dice """
    pass

def main():
    """ Main game funciton """
    print("\nHello and welcome to the Dice Game!\n\n~\n\n")
    while True:
        n_players = input("Please enter a number of players or press q to exit ")
        if n_players.lower().startswith('q'):
            print("Hope you had fun\nGoodbye!")
            break
        try:
            n_players = int(n_players)
            if n_players not in range(2, 7):
                continue
        except ValueError:
            continue

        # init game class with n players
        dice_game = Game(n_players)

        # init players with their names
        for i in range(0, dice_game.n_players):
            user_name = input(f"Enter the name of player {i + 1} ")
            player = Player(user_name)
            dice_game.players.append(player)

        # simple game loop
        while dice_game.top_score <= 10000:
            dice_game.round()
        final_result = dice_game.podium()
        print(final_result)
        time.sleep(3); print('\n\nEnd of game')
        time.sleep(1); print("\n\n\nAnother one?"); time.sleep(3)


def valid_selection(lst):
    """ Verifies if list has dice of interest to the Game """
    # looking for triples
    trpl_dices = [dice for dice in lst if lst.count(dice) in [3, 4, 5, 6]]

    # looking for golden dice
    gold_dices = [dice for dice in lst if dice in [5, 1]]

    # looking for 123456
    one_to_six = (1, 2, 3, 4, 5, 6)
    diamond_dices = all(elem in lst for elem in one_to_six)

    return True if trpl_dices or gold_dices or diamond_dices else False



if __name__ == '__main__':
    main()
