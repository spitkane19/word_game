import random

listofwords = [
    "AMBER", "BAKED", "CIDER", "DIARY", "EAGLE", "FROST", "GLOOM", "HOTEL", "IVORY", "JOUST",
    "KNACK", "LATCH", "MANGO", "NUDGE", "OLIVE", "PRISM", "QUIRK", "RELAY", "SCOUT", "TRAMP",
    "UNZIP", "VOWEL", "WRIST", "YACHT", "ZEBRA", "ABIDE", "BRAVE", "CHIME", "DOUSE", "EMOTE",
    "FLUTE", "GRIND", "HASTE", "INLAY", "JOLLY", "KOALA", "LEMON", "MAGIC", "NEXUS", "OASIS",
    "PIANO", "QUACK", "RIDER", "SWEEP", "TOKEN", "UNITY", "VIRUS", "WATCH", "XEROX", "YIELD",
    "RUSTY", "ACORN", "BLADE", "CHARM", "DROWN", "ELOPE", "FABLE", "GRAPE", "HYMEN", "IGLOO",
    "JUMBO", "KEBAB", "LUNAR", "MIRTH", "NACHO", "OCEAN", "POUCH", "QUAKE", "RIFLE", "SAVOR",
    "TIGER", "UMBRA", "VIVID", "WAGER", "XYLON", "YOGIC", "ZAPPY", "APPLE", "BRAID", "CLOAK",
    "DUSKY", "PERSE", "FLINT", "GAFFE", "HAZEL", "INERT", "JELLY", "KIOSK", "LUCKY", "MIRTH",
    "NYLON", "OVERT", "PLUSH", "QUAIL", "RISKY", "SWEEP", "TULIP", "ULCER", "VAULT", "WHALE",
    "XEROX", "YOGIC", "ZESTY"
]

class Game:
    def __init__(self):
        self.correct_word = random.choice(listofwords)
        self.guess_word = [''] * len(self.correct_word)
        print(self.correct_word)

    def get_correct_word(self):
        return self.correct_word
    
    def check_letter(self, guess):
    # This checks if there are letters at correct spots

        correct_positions = []
        correct_letters = []
        
        #self.correct_word = "mikko" #debug
        for i, char in enumerate(guess):
            if char == self.correct_word[i]:  
                correct_letters.append(char)
                correct_positions.append(i)

        for i, char in enumerate(guess):
            if char in self.correct_word and i not in correct_positions:  
                correct_letters.append(char)
        return str(correct_positions), correct_letters
    
    def did_you_win(self, guess):
        if guess == self.correct_word:
            return 1
        else:
            return 0

