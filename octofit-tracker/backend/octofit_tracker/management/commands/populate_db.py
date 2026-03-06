from django.core.management.base import BaseCommand
from octofit_tracker.models import User, Team, Activity, Workout, Leaderboard

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **kwargs):
        # Delete existing data using raw MongoDB collection drops
        from django.db import connection
        db = connection.cursor().db_conn
        db.drop_collection('octofit_tracker_activity')
        db.drop_collection('octofit_tracker_workout')
        db.drop_collection('octofit_tracker_leaderboard')
        db.drop_collection('octofit_tracker_user')
        db.drop_collection('octofit_tracker_team')

        # Create teams
        marvel = Team.objects.create(name='Marvel')
        dc = Team.objects.create(name='DC')

        # Create users
        users = [
            User(name='Spider-Man', email='spiderman@marvel.com', team=marvel),
            User(name='Iron Man', email='ironman@marvel.com', team=marvel),
            User(name='Wonder Woman', email='wonderwoman@dc.com', team=dc),
            User(name='Batman', email='batman@dc.com', team=dc),
        ]
        for user in users:
            user.save()

        # Create activities
        Activity.objects.create(user=users[0], type='Running', duration=30, date='2026-03-01')
        Activity.objects.create(user=users[1], type='Cycling', duration=45, date='2026-03-02')
        Activity.objects.create(user=users[2], type='Swimming', duration=60, date='2026-03-03')
        Activity.objects.create(user=users[3], type='Yoga', duration=20, date='2026-03-04')

        # Create workouts
        w1 = Workout.objects.create(name='Hero Strength', description='Full body workout for superheroes')
        w2 = Workout.objects.create(name='Speed Training', description='Improve your speed and agility')
        w1.suggested_for.set(users)
        w2.suggested_for.set([users[0], users[2]])

        # Create leaderboard
        Leaderboard.objects.create(team=marvel, points=100)
        Leaderboard.objects.create(team=dc, points=90)

        self.stdout.write(self.style.SUCCESS('octofit_db populated with test data'))
