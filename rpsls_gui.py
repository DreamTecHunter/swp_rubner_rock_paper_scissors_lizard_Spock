from random import random
from tkinter import *

import requests

from main import init_game_object_rpsls, Stats, RPSLSHandler

title = "Rock-Paper-Scissors-Lizard-Spock"


# TODO: use design pattern, which recognized last page or the page next coming
class RPSLS_GUI:
    def __init__(self, username: str = None):
        self.root = Tk()
        self.root.title(title)
        self.root.config(width=1600, height=900)
        self.menu = Menu(self.root)
        self.root.config(menu=self.menu)

        self.file_menu = Menu(self.menu)
        self.edit_menu = Menu(self.menu)

        self.menu.add_cascade(label="File", menu=self.file_menu)
        self.menu.add_cascade(label="Edit", menu=self.edit_menu)

        self.file_menu.add_command(label="start", command=self.start)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="play", command=self.play)
        self.file_menu.add_command(label="statistic", command=self.statistic)
        self.file_menu.add_command(label="upload", command=self.upload)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="exit", command=self.root.quit)

        self.edit_menu.add_command(label="change username", command=self.change_username)

        self.statusbar = Label(self.root, text=f"Welcome to {title}!", bd=1, relief=SUNKEN, anchor=W)
        self.statusbar.pack(side=BOTTOM, fill=X)
        self.main_frame = Frame(self.root)
        self.main_frame.pack(side=TOP, expand=True, fill=BOTH)
        self.round = 0
        self.game_object = init_game_object_rpsls()
        self.opponent_picked_label = None
        self.round_label = None
        self.stats = Stats()
        self.stats.prep_t_hand()
        self.rpsls_handler = RPSLSHandler()

        if username is None:
            self.change_username()
        else:
            self.username = username

    def show(self):
        self.root.mainloop()

    def close(self):
        self.root.quit()

    def change_username(self):
        self.clear_frame(self.main_frame)
        username_label = Label(self.main_frame, text="username")
        self.statusbar.config(text=f"Please enter your username.")
        self.username_entry = Entry(self.main_frame)
        """password_label = Label(self.main_frame, text="password")
        self.password_entry = Entry(self.main_frame, show="*")
        self.keep_logged_in_checkbox = Checkbutton(self.main_frame, text="Keep me logged in.")"""
        self.log_in_button = Button(self.main_frame, text="log in", command=self.pre_start)

        username_label.grid(row=0, column=0, sticky=E)
        self.username_entry.grid(row=0, column=1)
        """password_label.grid(row=1, column=0, sticky=E)
        self.password_entry.grid(row=1, column=1)
        self.keep_logged_in_checkbox.grid(row=2, columnspan=2)"""
        self.log_in_button.grid(row=3, column=0)

    def pre_start(self):
        self.username = self.username_entry.get()
        self.rpsls_handler.user_name = self.username
        self.statusbar.config(text=f"{self.username} logged successfully in.")
        self.start()

    def start(self):
        self.clear_frame(self.main_frame)
        self.statusbar.config(text=f"Welcome to {title}!")
        play_button = Button(self.main_frame, text="play", command=self.play)
        statistic_button = Button(self.main_frame, text="statistic", command=self.statistic)
        upload_button = Button(self.main_frame, text="upload", command=self.upload)
        buttons = [play_button, statistic_button, upload_button]
        for button in buttons:
            button.config(padx=2, pady=2)
            button.pack()

    def play(self):
        self.clear_frame(self.main_frame)
        self.statusbar.config(text="Please pick a hand")
        self.round_label = Label(self.main_frame, text=f"round: {self.round}")
        rock_button = Button(self.main_frame, text="rock", command=lambda: self._play(0))
        paper_button = Button(self.main_frame, text="paper", command=lambda: self._play(1))
        scissors_button = Button(self.main_frame, text="scissors", command=lambda: self._play(2))
        lizard_button = Button(self.main_frame, text="lizard", command=lambda: self._play(3))
        spock_button = Button(self.main_frame, text="spock", command=lambda: self._play(4))
        opponent_label = Label(self.main_frame, text=f"Your opponent:")
        self.opponent_picked_label = Label(self.main_frame, text="")

        self.round_label.grid(row=0, columnspan=5)
        rock_button.grid(row=1, column=0)
        paper_button.grid(row=1, column=1)
        scissors_button.grid(row=1, column=2)
        lizard_button.grid(row=1, column=3)
        spock_button.grid(row=1, column=4)
        opponent_label.grid(row=2, column=0, columnspan=3)
        self.opponent_picked_label.grid(row=2, column=3, columnspan=2)

    def _play(self, user_hand: int):
        self.round += 1
        self.round_label.config(text=f"round: {self.round}")
        opponent_hand = int(random() * len(self.game_object))
        opponent_hand = self.rpsls_handler.stat_supported_com_choice_number()
        self.opponent_picked_label.config(text=f"{self.game_object[opponent_hand].name.lower()}")
        if self.game_object[user_hand].is_winning(self.game_object[opponent_hand]):
            self.statusbar.config(text="You won")
        if self.game_object[user_hand].is_losing(self.game_object[opponent_hand]):
            self.statusbar.config(text="You lost")
        if self.game_object[user_hand].is_draw(self.game_object[opponent_hand]):
            self.statusbar.config(text="It's a draw")
        self.stats.add_stat(
            self.username,
            self.game_object[user_hand],
            self.game_object[opponent_hand],
            self.game_object[user_hand].is_winning(self.game_object[opponent_hand]))

    # TODO: packing this code in a loop for better readability
    def statistic(self):
        self.clear_frame(self.main_frame)
        values = self.stats.get_stats(self.username)
        rock_name_label = Label(self.main_frame, text="rock")
        rock_value_label = Label(self.main_frame, text=f"{values[0][1]}")
        paper_name_label = Label(self.main_frame, text="paper")
        paper_value_label = Label(self.main_frame, text=f"{values[1][1]}")
        scissors_name_label = Label(self.main_frame, text="scissors")
        scissors_value_label = Label(self.main_frame, text=f"{values[2][1]}")
        lizard_name_label = Label(self.main_frame, text="lizard")
        lizard_value_label = Label(self.main_frame, text=f"{values[3][1]}")
        spock_name_label = Label(self.main_frame, text="spock")
        spock_value_label = Label(self.main_frame, text=f"{values[4][1]}")

        rock_name_label.grid(row=0, column=0)
        rock_value_label.grid(row=0, column=1)
        paper_name_label.grid(row=1, column=0)
        paper_value_label.grid(row=1, column=1)
        scissors_name_label.grid(row=2, column=0)
        scissors_value_label.grid(row=2, column=1)
        lizard_name_label.grid(row=3, column=0)
        lizard_value_label.grid(row=3, column=1)
        spock_name_label.grid(row=4, column=0)
        spock_value_label.grid(row=4, column=1)

    def upload(self):
        self.clear_frame(self.main_frame)
        try:
            stats = self.stats.get_stats(self.username)
            d = {
                "name": self.username,
                "values": {value[0]: value[1] for value in stats}
            }
            for _d in d["values"]:
                response = requests.post(
                    "http://127.0.0.1:8888/add",
                    json={
                        "name": self.username,
                        "hand": _d,
                        "amount": d["values"][_d]
                    }
                )
            self.statusbar.config(text="stats are uploaded to flaskAPI")
        except:
            self.statusbar.config(text="Unable to upload to flaskAPI. Please try later again")

    def clear_frame(self, frame: Frame):
        if frame is not None:
            for element in frame.winfo_children():
                element.destroy()


if __name__ == "__main__":
    gui = RPSLS_GUI()
    gui.show()
