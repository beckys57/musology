from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    help = 'Resets the DB with initial game state and objects. Does not load or create fixtures'

    def handle(self, *args, **options):
        from game_test import setup
        setup()