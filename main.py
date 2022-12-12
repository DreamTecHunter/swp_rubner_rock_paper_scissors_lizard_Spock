import copy
from random import random
import requests
import mysql.connector


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
        return any(opponent_hand.name == lower_hand.name for lower_hand in self.lower_hand)

    def is_losing(self, opponent_hand):
        return any(opponent_hand.name == upper_hand.name for upper_hand in self.upper_hand)

    def is_draw(self, opponent_hand):
        return self == opponent_hand


# on the one hand, it saves unnecessary thinking about number-distribution of the hands.
# on the other hand, it is more static code, but is better extendable with other hands.
def init_game_object_rpsls():
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


def spacer():
    return "-" * 100


class RPSLSHandler:

    def __init__(self, game_object: list = None):
        if game_object is not None:
            self.game_object = game_object
        else:
            self.game_object = init_game_object_rpsls()
        self.stats = Stats()
        self.user_name = "anonymous"

    def menu(self):
        print(spacer())
        print("Welcome to the RPSLSHandler")
        self.user_name = input("Please enter your name: ").lower()
        leave = False
        while not leave:
            print(spacer())
            options = [self.play, self.statistic, self.upload]
            messages = ["play", "statistic", "upload"]
            print("Please pick an option:")
            [print(f"{i}:\t{messages[i]}") for i in range(len(messages))]
            print("Or click something else to exit.")
            user_input = input("Your input: ")
            if user_input.isnumeric():
                user_input = int(user_input)
                if user_input < len(messages):
                    options[user_input]()
                else:
                    print("This option does not exist.")
            else:
                leave = True

    def play(self):
        dont_stop = True
        while dont_stop:
            print(spacer())
            [print(f"{i}:\t{self.game_object[i].name}") for i in range(len(self.game_object))]
            try:
                user_input = int(input("Please pick a hand:\t"))
                opponent_input = int(random() * len(self.game_object))
                print(spacer())

                print(f"user/{self.game_object[user_input].name} vs com/{self.game_object[opponent_input].name}")
            except (ValueError, IndexError):
                print(spacer())

                print(f"Numbers from {0} to {len(self.game_object) - 1} are ok!")
                continue
            if self.game_object[user_input].is_winning(self.game_object[opponent_input]):
                print(f"{self.game_object[user_input].name} wins against {self.game_object[opponent_input].name}")
            if self.game_object[user_input].is_losing(self.game_object[opponent_input]):
                print(f"{self.game_object[user_input].name} loses against {self.game_object[opponent_input].name}")
            if self.game_object[user_input].is_draw(self.game_object[opponent_input]):
                print(f"{self.game_object[user_input].name} is in a draw with {self.game_object[opponent_input].name}")
            self.stats.add_stat(
                self.user_name,
                self.game_object[user_input],
                self.game_object[opponent_input],
                self.game_object[user_input].is_winning(self.game_object[opponent_input]))
            print(spacer())

            if "x" == input("Click 'x' to leave the game:\t"):
                dont_stop = False
            print(spacer())

    def stat_supported_com_choice(self):
        # sort hand by pick-rate dec and search for the counter-picks
        # keep second hand in mind for the counter-picks of the first hand,
        # so the second hand might not be countering the counter-pick of the first hand
        pass

    def statistic(self):
        print(spacer())
        print(self.stats.get_stats(self.user_name))

    def upload(self):
        print(spacer())
        stats = self.stats.get_stats(self.user_name)
        d = {
            "name": self.user_name,
            "values": {value[0]: value[1] for value in stats}
        }
        print(d)
        for _d in d["values"]:
            response = requests.post(
                "http://127.0.0.1:8888/add",
                json={
                    "name": self.user_name,
                    "hand": _d,
                    "amount": d["values"][_d]
                }
            )
            print(response.text)


class Stats:
    round_info_template = {
        "user_name": "template",  # str
        "user_hand_id": None,  # RPSObjects
        "com_hand_id": None,  # RPSObject
        "has_user_won": None,  # boolean
    }

    def __init__(self):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute(open("prep.sql").read())
        cursor.close()
        connection.close()

    def get_connection(self):
        return mysql.connector.connect(
            host="localhost",
            user="swp-rubner",
            password="swp-rubner",
            database="swp_rubner_rpsls"
        )

    def prep_t_hand(self):
        connection = self.get_connection()
        cursor = connection.cursor(buffered=True)
        result = cursor.execute("show tables")
        sql = "insert ignore into t_hands (id, name) values (%s, %s);"
        hands = init_game_object_rpsls()
        for hand in hands:
            val = (hands.index(hand), hand.name)
            cursor.execute(sql, val)
            connection.commit()
        cursor.close()
        connection.close()

    def add_stat(self, user: str, user_hand: RPSObject, com_hand: RPSObject, has_user_won: bool):
        if user is None:
            print("username is not allowed to be None")
            return
        elif user == "":
            print("username is not allowed to be empty")
            return
        if user_hand is None or com_hand is None:
            print("hand/s is/are missing ")
            return
        if type(has_user_won) is not bool:
            print("has_user_won has to be a boolean")
            return
        connection = self.get_connection()
        cursor = connection.cursor(buffered=True)
        round_info = copy.deepcopy(self.round_info_template)
        hand_names = [hand.name for hand in init_game_object_rpsls()]
        for i in range(len(round_info.keys())):
            round_info[list(round_info.keys())[i]] = \
                [user, hand_names.index(user_hand.name), hand_names.index(com_hand.name), has_user_won][i]
        sql = "insert into t_stats (user_name, user_hand_id, com_hand_id, has_user_won) values (%s, %s, %s, %s);"
        print(sql)
        val = [round_info[key] for key in round_info]
        print(val)
        cursor.execute(sql, val)
        connection.commit()
        cursor.close()
        connection.close()

    # user_name, hand, anzahl
    def get_stats(self, user_name: str):
        connection = self.get_connection()
        cursor = connection.cursor(buffered=True)
        sql = "select h.name, count(user_hand_id) " \
              "from t_stats as s " \
              "inner join t_hands as h " \
              "on  s.user_hand_id = h.id " \
              "where user_name = %s " \
              "group by user_name, user_hand_id " \
              "ORDER BY USER_NAME asc, count(user_hand_id) desc;"
        val = [user_name]
        cursor.execute(sql, val)
        result = cursor.fetchall()
        cursor.close()
        connection.close()
        return result


class MyAPI:
    pass


if __name__ == '__main__':
    s = Stats()
    s.prep_t_hand()
    s.get_stats("tobi")
    handler = RPSLSHandler()
    handler.menu()
