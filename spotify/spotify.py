import requests
from dotenv import load_dotenv
import os
import base64
import tkinter.messagebox
import tkinter.simpledialog


class Spotify:
    def __init__(self):
        load_dotenv()

        self.api_key = os.getenv('API_KEY')
        self.secret = os.getenv('SECRET')
        self.access_token = None
        self.user_id = None

        self.authorize()

    def authorize(self):
        END_POINT = "https://accounts.spotify.com/authorize"
        auth_params = {
            "client_id": self.api_key,
            "response_type": "code",
            "redirect_uri": "https://open.spotify.com/",
            "scope": "user-read-private user-read-email playlist-modify-private playlist-modify-public",
            "state": "random_state_string"
        }

        response1 = requests.get(url=END_POINT, params=auth_params)
        response1.raise_for_status()
        root = tkinter.Tk()
        root.withdraw()
        root.clipboard_clear()
        tkinter.messagebox.showinfo("Please visit this URL to authorize the app, Press ok to copy url:", response1.url)
        root.clipboard_append(response1.url)

        full_url = tkinter.simpledialog.askstring(root, "\nPlease go to the URL, if u are asked for permission accept and then paste the new url in the bar here:\n")
        auth_code= full_url.replace("code=","&").split("&")[1]

        root.destroy()


        # Step 2: Exchange the authorization code for an access token
        self.get_access_token(auth_code)

    def get_access_token(self, auth_code):
        POST = "https://accounts.spotify.com/api/token"
        token_params = {
            "grant_type": "authorization_code",
            "code": auth_code,
            "redirect_uri": "https://open.spotify.com/"
        }

        client_creds = f"{self.api_key}:{self.secret}"
        encoded_creds = base64.b64encode(client_creds.encode()).decode()

        headers_token = {
            "Authorization": f"Basic {encoded_creds}",
            "Content-Type": "application/x-www-form-urlencoded"
        }

        response2 = requests.post(url=POST, headers=headers_token, data=token_params)

        # Check if token request was successful
        if response2.status_code != 200:
            tkinter.messagebox.showerror(title="ERROR",message="Process failed, please try again later!")
            exit(1)

        token_info = response2.json()
        self.access_token = token_info['access_token']

        # Get the user ID
        self.get_user_id()

    def get_user_id(self):
        headers_id = {
            "Authorization": f"Bearer {self.access_token}"
        }

        response = requests.get(url="https://api.spotify.com/v1/me", headers=headers_id)

        # Check if user data request was successful
        if response.status_code != 200:
            tkinter.messagebox.showerror(title="ERROR",message="Process failed, please try again later!")
            exit(1)

        user_data = response.json()
        self.user_id = user_data['id']

    def create_playlist(self, name):
        '''make a  playlist and return the id of the playlist
        '''
        body = {
            "name": name,
            "description": "New playlist",
            "public": False
        }

        headers_playlist = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }

        response = requests.post(f"https://api.spotify.com/v1/users/{self.user_id}/playlists", json=body, headers=headers_playlist)

        if response.status_code == 201:
            tkinter.messagebox.showinfo(title="SUCCESS",message="Playlist created successfully!\nThe process of adding the songs will take some time!")
            return response.json()['id']  
        else:
            tkinter.messagebox.showerror(title="ERROR",message="Failed to create playlist! Please try again later")
            return None

    def search_track(self, track_name, artist_name):
        search_params = {
            "q": f"{track_name} artist:{artist_name}",
            "type": "track"
        }

        headers_id = {
            "Authorization": f"Bearer {self.access_token}"
        }

        search_response = requests.get("https://api.spotify.com/v1/search", headers=headers_id, params=search_params)
        return search_response.json()

    def add_songs_to_playlist(self, playlist_id, songs):
        track_ids = []
        for song in songs:
            search_data = self.search_track(song[0], song[1])
            if search_data['tracks']['items']:
                track_id = search_data['tracks']['items'][0]['id']  # Get the first track found
                track_ids.append(track_id)

        if track_ids:
            add_tracks_params = {
                "uris": [f"spotify:track:{track_id}" for track_id in track_ids]
            }
            headers_playlist = {
                "Authorization": f"Bearer {self.access_token}",
                "Content-Type": "application/json"
            }
            response = requests.post(f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks", json=add_tracks_params, headers=headers_playlist)
            tkinter.messagebox.showinfo(title="SUCCESS",message="Songs are added successfully")
            return response.json()
        else:
            tkinter.messagebox.showerror(title="ERROR",message="No tracks were found to add.")
            return None
