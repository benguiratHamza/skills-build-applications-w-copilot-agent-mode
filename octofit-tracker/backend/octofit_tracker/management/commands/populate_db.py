from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db import connection

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        User = get_user_model()
        # Clean up existing data
        User.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Users cleared.'))

        # Teams
        from django.apps import apps
        Team = apps.get_model('octofit_tracker', 'Team')
        Activity = apps.get_model('octofit_tracker', 'Activity')
        Leaderboard = apps.get_model('octofit_tracker', 'Leaderboard')
        Workout = apps.get_model('octofit_tracker', 'Workout')

        Team.objects.all().delete()
        Activity.objects.all().delete()
        Leaderboard.objects.all().delete()
        Workout.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Teams, Activities, Leaderboard, Workouts cleared.'))

        # Create Teams
        marvel = Team.objects.create(name='Marvel')
        dc = Team.objects.create(name='DC')

        # Create Users
        users = [
            {'email': 'ironman@marvel.com', 'username': 'ironman', 'team': marvel},
            {'email': 'spiderman@marvel.com', 'username': 'spiderman', 'team': marvel},
            {'email': 'batman@dc.com', 'username': 'batman', 'team': dc},
            {'email': 'superman@dc.com', 'username': 'superman', 'team': dc},
        ]
        for u in users:
            User.objects.create_user(email=u['email'], username=u['username'], password='password', team=u['team'])
        self.stdout.write(self.style.SUCCESS('Users created.'))

        # Create Activities
        Activity.objects.create(user=User.objects.get(username='ironman'), type='run', duration=30)
        Activity.objects.create(user=User.objects.get(username='spiderman'), type='cycle', duration=45)
        Activity.objects.create(user=User.objects.get(username='batman'), type='swim', duration=60)
        Activity.objects.create(user=User.objects.get(username='superman'), type='run', duration=50)
        self.stdout.write(self.style.SUCCESS('Activities created.'))

        # Create Leaderboard
        Leaderboard.objects.create(team=marvel, points=100)
        Leaderboard.objects.create(team=dc, points=90)
        self.stdout.write(self.style.SUCCESS('Leaderboard created.'))

        # Create Workouts
        Workout.objects.create(name='Morning Cardio', description='Cardio for all heroes')
        Workout.objects.create(name='Strength Training', description='Strength for all heroes')
        self.stdout.write(self.style.SUCCESS('Workouts created.'))

        self.stdout.write(self.style.SUCCESS('Database populated successfully.'))
