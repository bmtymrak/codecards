from django.shortcuts import render
from django.views.generic import View, TemplateView
from django.http import HttpResponseRedirect
from .models import Game


class HomePageView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "index.html")

    def post(self, request, *args, **kwargs):
        game = Game()
        game.save()
        return HttpResponseRedirect(f"/{game.pk}")


class GameView(TemplateView):
    template_name = "game.html"

    def get_context_data(self, **kwargs):
        kwargs.update({"game": self.kwargs["id"]})
        kwargs.update(
            {
                "cards": [
                    {
                        "word": card.word,
                        "team": card.team,
                        "clicked": card.clicked,
                        "game": card.game.id,
                    }
                    for card in Game.objects.get(id=self.kwargs["id"]).card_set.all()
                ],
                "active_team": Game.objects.get(id=self.kwargs["id"]).active_team,
            }
        )
        return kwargs
