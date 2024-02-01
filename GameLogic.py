import random


listofwords = five_letter_words = [
    "amber", "baked", "cider", "diary", "eagle", "frost", "gloom", "hotel", "ivory", "joust",
    "knack", "latch", "mango", "nudge", "olive", "prism", "quirk", "relay", "scout", "tramp",
    "unzip", "vowel", "wrist", "yacht", "zebra", "abide", "brave", "chime", "douse", "emote",
    "flute", "grind", "haste", "inlay", "jolly", "koala", "lemon", "magic", "nexus", "oasis",
    "piano", "quack", "rider", "sweep", "token", "unity", "virus", "watch", "xerox", "yield",
    "zealot", "acorn", "blade", "charm", "drown", "elope", "fable", "grape", "hymen", "igloo",
    "jumbo", "kebab", "lunar", "mirth", "nacho", "ocean", "pouch", "quake", "rifle", "savor",
    "tiger", "umbra", "vivid", "wager", "xylon", "yogic", "zappy", "apple", "braid", "cloak",
    "dusky", "elixir", "flint", "gaffe", "hazel", "inert", "jelly", "kiosk", "lucky", "mirth",
    "nylon", "overt", "plush", "quail", "risky", "sweep", "tulip", "ulcer", "vault", "whale",
    "xerox", "yogic", "zesty"]


class Singleplayer:
    def __init__(self):
        self.correct_word = random.choice(listofwords)
        self.guess_word = [''] * len(self.correct_word)

    def check_guess(self):
        return ''.join(self.guess_word) == self.correct_word

    def check_letter(self, letter):
        correct_positions = []
        correct_letters = []

        for i, char in enumerate(self.correct_word):
            if char == letter:
                correct_letters.append(char)
                if self.guess_word[i] == char:
                    correct_positions.append(i)

        return correct_positions, correct_letters