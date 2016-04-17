import requests
from django.core.management import BaseCommand
from songs.models import Song


class Command(BaseCommand):
    help = "Andreas tester"

    def get_spotify_data(self, spotify_uri):
        r = requests.get('https://api.spotify.com/v1/tracks/' + spotify_uri)
        return r.json()

    def handle(self, *args, **options):
        songs = Song.objects.all()
        for song in songs:
            if not song.url or not song.artist or not song.name:
                data = self.get_spotify_data(song.spotify_uri)
                song.artist = data['artists'][0]['name']
                song.name = data['name']
                song.url = data['preview_url']
                song.save()
        self.stdout.write("Done")
