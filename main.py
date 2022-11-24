import copy
from random import random


class RPSObject:
    def __init__(self, name: str, upper_hand: list = None, lower_hand: list = None):
        self.name = name

        self.upper_hand = copy.deepcopy(upper_hand) if upper_hand is not None else list()
        self.lower_hand = copy.deepcopy(lower_hand) if lower_hand is not None else list()

    def __str__(self):
        return f"RPSLSObject:\nupper_hand\t{self.upper_hand.name}\n\tlower_hand{self.lower_hand.name}"

    def add_upper_hand(self, upper_hands: list):
        [self.upper_hand.append(upper_hand) for upper_hand in upper_hands]

    def remove_upper_hand(self, upper_hands: list):
        [self.upper_hand.remove(upper_hand) for upper_hand in upper_hands]

    def add_lower_hand(self, lower_hands: list):
        [self.lower_hand.append(lower_hand) for lower_hand in lower_hands]

    def remove_lower_hand(self, lower_hands: list):
        [self.lower_hand.remove(lower_hands) for lower_hand in lower_hands]

    def is_winning(self, opponent_hand):
        return any(opponent_hand == lower_hand for lower_hand in self.lower_hand)

    def is_losing(self, opponent_hand):
        return any(opponent_hand == upper_hand for upper_hand in self.upper_hand)

    def is_draw(self, opponent_hand):
        return self == opponent_hand


class RPSLSHandler:
    def init_game_object_rpsls(self):
        rock = RPSObject("rock")
        paper = RPSObject("paper")
        scissors = RPSObject("scissors")
        lizard = RPSObject("lizard")
        spock = RPSObject("spock")
        rock.add_upper_hand([paper, spock])
        rock.add_lower_hand([scissors, lizard])
        paper.add_upper_hand([scissors, lizard])
        paper.add_lower_hand([rock, spock])
        scissors.add_upper_hand([rock, spock])
        scissors.add_lower_hand([paper, lizard])
        lizard.add_upper_hand([scissors, rock])
        lizard.add_lower_hand([spock, paper])
        spock.add_upper_hand([lizard, paper])
        spock.add_lower_hand([rock, scissors])
        return [rock, paper, scissors, lizard, spock]

    def __init__(self, game_object: list = None):
        if game_object is not None:
            self.game_object = game_object
        else:
            self.game_object = self.init_game_object_rpsls()

    def play(self):
        dont_stop = True
        spacer = 40
        while dont_stop:
            print("-" * spacer)
            [print(f"{i}:\t{self.game_object[i].name}") for i in range(len(self.game_object))]
            try:
                user_input = int(input("Please pick a hand:\t"))
                opponent_input = int(random() * len(self.game_object))
                print("-" * spacer)
                print(f"user/{self.game_object[user_input].name} vs com/{self.game_object[opponent_input].name}")
            except (ValueError, IndexError):
                print("-" * spacer)
                print(f"Numbers from {0} to {len(self.game_object) - 1} are ok!")
                continue
            if self.game_object[user_input].is_winning(self.game_object[opponent_input]):
                print(f"{self.game_object[user_input].name} wins against {self.game_object[opponent_input].name}")
            if self.game_object[user_input].is_losing(self.game_object[opponent_input]):
                print(f"{self.game_object[user_input].name} loses against {self.game_object[opponent_input].name}")
            if self.game_object[user_input].is_draw(self.game_object[opponent_input]):
                print(f"{self.game_object[user_input].name} is in a draw with {self.game_object[opponent_input].name}")
            print("-" * spacer)
            if "x" == input("Click 'x' to leave the game:\t"):
                dont_stop = False
            print("-" * spacer)


if __name__ == '__main__':
    handler = RPSLSHandler()
    handler.play()
