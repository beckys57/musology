from game.models import Game

def main():
  game = Game.objects.create()
  game.initialize()