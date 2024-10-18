from scrapping import*
from spotify import*

class Controller:
    def __init__(self, playlist_name, selected_year):
        spotify=Spotify()
        scrap(selected_year)

        songs=get_songs()
        id=spotify.create_playlist(name=playlist_name)

        spotify.add_songs_to_playlist(playlist_id=id,songs=songs)


