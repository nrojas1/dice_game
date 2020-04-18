import random; import time

class Game:
    """docstring for Game."""

    def __init__(self, n_players):
        self.n_players = n_players
        self.n_round = 1
        self.top_score = 0
        self.scoreboard = list()
        self.players = list()
        self.first_turn = True

    def round(self):
        for player in self.players:
            print(f"It is now {player.name}'s turn")
            player.throw(6)
            while player.valid_throw(player.hand) or len(player.hand) == 0:
                if len(player.hand) == 0: # NOT WORKING
                    player.throw(6)
                # TODO: FIND A SOLUTION FOR WHEN HAND IN EMPTY
                print(player.hand,' hand')
                print(player.dice_kept,' dicekept')
                # user input
                selected_dice = input('what dices do you wish to keep? (seperate by comma) ')

                # treat into int
                str_array = selected_dice.strip().split(',')
                crt = 0
                input_temp = list()
                for d in str_array:
                    input_temp.append(int(d))
                    player.dice_kept.append(int(d))
                    player.hand.pop(player.hand.index(int(d)))
                    crt += 1
                player.running_score += player.throw_to_score(input_temp)
                if player.above_water(self.first_turn):
                    while True:
                        user_stop = input(f"Would you like to stop with {player.running_score} points?\n1: Yes\n2: No\n")
                        try:
                            user_stop = int(user_stop)
                            if user_stop not in [1,2]:
                                continue
                            elif user_stop == 1:
                                player.update_score(player.running_score)
                                break
                            elif user_stop == 2:
                                break
                        except ValueError:
                            continue
                    break

                player.throw(len(player.hand))
            else: #player.valid_throw(player.hand):
                print(f"{player.hand}\nOut of luck, {player.name} (you bitch)")
            player.running_score = 0
            print(player.running_score)

        [player.dice_kept.clear() for player in self.players]


        print(f"end of round {self.n_round}")
        self.n_round += 1
        self.first_turn = False # nah this is a Player attr
        # TODO: ADD FIRST TURN AS A PLAYER ATTR AND MAKE A FUNCTION THAT CHANGES THE VALUE OF THE THING. MAYBE USE 0 AND 1 INSTEAD OF TRUE AND FALSE
        self.update_scoreboard(self.scoreboard)
        print(f"Scoreboard: {self.scoreboard}")

    def update_scoreboard(self, scoreboard):
        current_score = dict()
        for player in self.players:
            current_score[player.name] = player.score
        scoreboard.append(current_score)
        return scoreboard

    def podium(self):
        finish_line = self.scoreboard[-1]
        finish_line = sorted((score, name) for (name,score) in finish_line.items())
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
    # def get_topscore(self, scores):
    #     self.top_score = max(scores)
    #     return self.top_score

class Player:
    """Player"""

    def __init__(self, name):
        self.name = name
        self.id = 0
        self.score = 0
        self.running_score = 0
        self.hand = list()
        self.dice_kept = list()

    def update_score(self, x):
        self.score += x

    def throw(self, n_dice):
        self.hand = [random.randint(1,6) for dice in range(0,n_dice)]
        return self.hand

    def valid_throw(self, hand):
        # looking for triples
        trpl_dices = [dice for dice in self.hand if self.hand.count(dice) in [3,4,5,6]]

        # looking for golden dice
        gold_dices = [dice for dice in self.hand if dice in [5,1]]

        # looking for 123456
        one_to_six = (1, 2, 3, 4, 5, 6)
        diamond_dices = all(elem in self.hand for elem in one_to_six)

        return True if trpl_dices or gold_dices or diamond_dices else False

    def above_water(self, first_turn):
        return True if (first_turn and self.running_score >= 450) or (not first_turn and self.running_score >= 350) else False

    def throw_to_score(self, hand):
        if not hand:
            exit(0)
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

    # def get_score(self):
    #     return self.score
    #
    # def get_name(self):
    #     return self.name

def main():
    print("\nHello and welcome to the Dice Game!\n\n~\n\n")
    while True:
        n_players = input("Please enter a number of players or press q to exit ")
        if n_players.lower().startswith('q'):
            print("Hope you had fun\nGoodbye!")
            break
        try:
            n_players = int(n_players)
            if n_players not in range(2,7):
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
        while dice_game.n_round < 3: # TODO: SET A CONDITION WHICH STOPS AT LIMIT SCORE
            dice_game.round()
        final_result = dice_game.podium()
        print(final_result)
        time.sleep(3); print('\n\nEnd of game');
        time.sleep(1); print("\n\n\nAnother one?"); time.sleep(3)

if __name__ == '__main__':
    main()
