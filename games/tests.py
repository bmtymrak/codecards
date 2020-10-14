from django.test import TestCase, SimpleTestCase
from django.urls import reverse
from django.http import HttpRequest
from .models import Game, Count
from collections import Counter


class HomePageTests(TestCase):
    def setUp(self):
        Count.objects.create()

    def test_home_page_status_code(self):
        response = self.client.get("/")
        self.assertEquals(response.status_code, 200)

    def test_view_url_name(self):
        response = self.client.get(reverse("home"))
        self.assertEquals(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse("home"))
        self.assertTemplateUsed(response, "index.html")

    def test_redirect_on_start_game(self):
        response = self.client.post("/")
        self.assertEqual(response.status_code, 302)


class GameTests(TestCase):
    def setUp(self):
        Count.objects.create()
        Game.objects.create()

    def test_game_page_status_code(self):
        game = Game.objects.first()
        response = self.client.get(f"/{game.pk}")
        self.assertEquals(response.status_code, 200)

    def test_counter_increments_with_new_game(self):
        counter = Count.objects.first()
        games_played_before = counter.games_played
        Game.objects.create()
        counter = Count.objects.first()
        self.assertEquals(counter.games_played, games_played_before + 1)

    def test_correct_number_of_cards(self):
        new_game = Game.objects.create()
        number_of_cards = len(new_game.card_set.all())
        self.assertEquals(number_of_cards, 25)

    def test_no_duplicate_cards(self):
        game = Game.objects.first()
        words = {card.word for card in game.card_set.all()}
        self.assertEqual(len(words), 25)

    def test_correct_first_team(self):
        game = Game.objects.first()
        teams = [card.team for card in game.card_set.all()]
        cards_per_team = Counter(teams)
        calculated_first_team = cards_per_team.most_common(1)[0][0]
        self.assertEqual(game.active_team, calculated_first_team)
