import uuid
from django.db import models
import random


class Game(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    def save(self, *args, **kwargs):
        if not self.card_set.all():
            super().save(*args, **kwargs)
            cards = self.build_board()
            for card in cards:
                new_card = Card(game=self, word=card["word"], team=card["team"])
                new_card.save()
            game_tracker = Count.objects.first()
            game_tracker.games_played += 1
            game_tracker.save()
        else:
            super().save(*args, **kwargs)

    def build_board(self):
        word_list = [
            "africa",
            "agent",
            "air",
            "alien",
            "amazon",
            "angel",
            "antarctica",
            "apple",
            "arm",
            "back",
            "band",
            "bank",
            "bark",
            "beach",
            "belt",
            "berlin",
            "berry",
            "board",
            "bond",
            "boom",
            "bow",
            "box",
            "bug",
            "canada",
            "capital",
            "cell",
            "center",
            "china",
            "chocolate",
            "circle",
            "club",
            "compound",
            "copper",
            "crash",
            "cricket",
            "cross",
            "death",
            "dice",
            "dinosaur",
            "doctor",
            "dog",
            "dress",
            "dwarf",
            "eagle",
            "egypt",
            "engine",
            "england",
            "europe",
            "eye",
            "fair",
            "fall",
            "fan",
            "field",
            "file",
            "film",
            "fish",
            "flute",
            "fly",
            "forest",
            "fork",
            "france",
            "gas",
            "ghost",
            "giant",
            "glass",
            "glove",
            "gold",
            "grass",
            "greece",
            "green",
            "ham",
            "head",
            "himalaya",
            "hole",
            "hood",
            "hook",
            "human",
            "horseshoe",
            "hospital",
            "hotel",
            "ice",
            "ice cream",
            "india",
            "iron",
            "ivory",
            "jam",
            "jet",
            "jupiter",
            "kangaroo",
            "ketchup",
            "kid",
            "king",
            "kiwi",
            "knife",
            "knight",
            "lab",
            "lap",
            "laser",
            "lawyer",
            "lead",
            "lemon",
            "limousine",
            "lochness",
            "log",
            "mammoth",
            "maple",
            "march",
            "mass",
            "mercury",
            "millionaire",
            "model",
            "mole",
            "moscow",
            "mouth",
            "mug",
            "needle",
            "net",
            "new york",
            "night",
            "note",
            "novel",
            "nurse",
            "nut",
            "oil",
            "olive",
            "olympus",
            "opera",
            "orange",
            "paper",
            "park",
            "part",
            "paste",
            "phoenix",
            "piano",
            "telescope",
            "teacher",
            "switch",
            "swing",
            "sub",
            "stick",
            "staff",
            "stadium",
            "sprint",
            "spike",
            "snowman",
            "slip",
            "shot",
            "shadow",
            "server",
            "ruler",
            "row",
            "rose",
            "root",
            "rome",
            "rock",
            "robot",
            "robin",
            "revolution",
            "rat",
            "racket",
            "queen",
            "press",
            "port",
            "pilot",
            "time",
            "tooth",
            "tower",
            "truck",
            "triangle",
            "trip",
            "turkey",
            "undertaker",
            "unicorn",
            "vacuum",
            "van",
            "wake",
            "wall",
            "war",
            "washer",
            "washington",
            "water",
            "wave",
            "well",
            "whale",
            "whip",
            "worm",
            "yard",
        ]

        # Create list of teams
        team1 = random.choice(["red", "blue"])
        team2 = "red" if team1 == "blue" else "blue"

        teams = [team1] * 9
        teams.extend([team2] * 8)
        teams.extend(["none"] * 7)
        teams.extend(["assassin"])

        # Shuffle list of teams
        teams_remaining = len(teams)
        while teams_remaining:
            teams_remaining -= 1
            index = random.randint(0, teams_remaining)
            teams[index], teams[teams_remaining] = teams[teams_remaining], teams[index]

        # Randomly select words from list
        words = []
        while len(words) < 25:
            word = word_list[random.randint(0, len(word_list) - 1)]
            if word not in words:
                words.append(word)

        # Assign team to card
        cards = [{"word": word, "team": team} for word, team in zip(words, teams)]

        return cards


class Card(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    word = models.CharField(max_length=75, blank=False)
    team = models.CharField(max_length=20, blank=False)
    clicked = models.BooleanField(default=False)

    def __str__(self):
        return self.word


class Count(models.Model):
    games_played = models.IntegerField(default=0)

    def __str__(self):
        return str(self.games_played)

