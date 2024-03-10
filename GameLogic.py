import random


listofwords = [
    "amber", "baked", "cider", "diary", "eagle", "frost", "gloom", "hotel", "ivory", "joust",
    "knack", "latch", "mango", "nudge", "olive", "prism", "quirk", "relay", "scout", "tramp",
    "unzip", "vowel", "wrist", "yacht", "zebra", "abide", "brave", "chime", "douse", "emote",
    "flute", "grind", "haste", "inlay", "jolly", "koala", "lemon", "magic", "nexus", "oasis",
    "piano", "quack", "rider", "sweep", "token", "unity", "virus", "watch", "xerox", "yield",
    "rusty", "acorn", "blade", "charm", "drown", "elope", "fable", "grape", "hymen", "igloo",
    "jumbo", "kebab", "lunar", "mirth", "nacho", "ocean", "pouch", "quake", "rifle", "savor",
    "tiger", "umbra", "vivid", "wager", "xylon", "yogic", "zappy", "apple", "braid", "cloak",
    "dusky", "perse", "flint", "gaffe", "hazel", "inert", "jelly", "kiosk", "lucky", "mirth",
    "nylon", "overt", "plush", "quail", "risky", "sweep", "tulip", "ulcer", "vault", "whale",
    "xerox", "yogic", "zesty"]


class SinglePlayer:
    def __init__(self):
        self.correct_word = random.choice(listofwords)
        self.guess_word = [''] * len(self.correct_word)

    def get_correct_word(self):
        return self.correct_word
    
    def check_guess(self,guess):
        
        #self.correct_word = "mikko" #debug
        if len(guess) != 5:
            return False
        return guess == self.correct_word

    def check_letter(self, guess): # This checks if there are letters at correct spots
        if len(guess) != 5:
            return False, "Word not 5 letters"
        correct_positions = []
        correct_letters = []
        
        #self.correct_word = "mikko" #debug
        for i, char in enumerate(guess):
            if char == self.correct_word[i]:  # Correct letter at correct spot
                correct_letters.append(char)
                correct_positions.append(i)

        for i, char in enumerate(guess):
            if char in self.correct_word and i not in correct_positions:  # Correct letter in wrong spot
                correct_letters.append(char)

        return correct_positions, correct_letters

class Multiplayer:
    def __init__(self):
        self.correct_word = None
        self.guess_word = None

    def start_game(self,players):
        if not players:
            return False,"Waiting for another player to join..."
        
        self.correct_word = random.choice(listofwords)
        self.guess_word = [''] * len(self.correct_word)
        return True,"Game started"

    def get_correct_word(self):
        return self.correct_word

    def check_guess(self, guess):
        if len(guess) != len(self.correct_word):
            return False
        return guess == self.correct_word

    def check_letter(self, guess):
        if len(guess) != len(self.correct_word):
            return False, "Word not {} letters".format(len(self.correct_word))
        correct_positions = []
        correct_letters = []

        for i, char in enumerate(guess):
            if char == self.correct_word[i]:
                correct_letters.append(char)
                correct_positions.append(i)

        for i, char in enumerate(guess):
            if char in self.correct_word and i not in correct_positions:
                correct_letters.append(char)

        return correct_positions, correct_letters