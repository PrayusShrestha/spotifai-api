import requests
from rest_framework.response import Response

class Song:
    def __init__(self, data: dict):
        """init for Song class

        Args:
            data (dict): dictionary of song info. Formatted according to Spotify's web API for tracks
        """
        self.artist_name = data["artists"][0]["name"]
        self.artist_id = data["artists"][0]["id"]
        self.name = data["name"]
        self.id = data["id"]
        self.external_url = data["external_urls"]["spotify"]
        self.album_image_url = data["album"]["images"][0]["url"]
        self.uri = data["uri"]

    def json(self):
        """returns dict of object data in json format
        """

        return {
            "artist_name": self.artist_name,
            "artist_id": self.artist_id,
            "name": self.name,
            "id": self.id,
            "album_image_url": self.album_image_url,
            "external_url": self.external_url,
            "uri": self.uri
        }


def get_user_playlists(token: str):
    """[summary]

    Args:
        token ([type]): [description]

    Returns:
        [type]: [description]
    """

    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
    }

    response = requests.get("https://api.spotify.com/v1/me/playlists", headers=headers)
    response = response.json()
    
    if not response:
        return "Could not get playlists", 502

    information = response

    # print(information)

    playlists = []

    for playlist in information["items"]:
        id = playlist["id"]
        name = playlist["name"]

        song_response = requests.get(f"https://api.spotify.com/v1/playlists/{id}/tracks?market=US", headers=headers)

        if not song_response:
            return Response(data="Could not get song response", status=502)

        song_info = song_response.json()
        
        songs = []
        for item in song_info["items"]:
            #print(item["track"]['id'])
            if (item["track"]["id"] == None):
                continue
            song = Song(item["track"])
            # print(song.name)
            songs.append(song.json())

        playlists.append({
            "name": name,
            "songs": songs
        })
    
    return playlists, 200

def get_user_songs(token: str):
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
    }

    tracks_response = requests.get("https://api.spotify.com/v1/me/tracks", headers=headers)

    if not tracks_response:
        return "Could not get songs", 502

    tracks_response_json = tracks_response.json()
    # print(tracks_response_json)

    songs = []

    for item in tracks_response_json["items"]:
        song = Song(item["track"])
        songs.append(song.json())

    return songs, 200

def get_song_suggestions(token: str, seed_tracks, seed_artists):
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
    }

    params = {
        "seed_tracks": seed_tracks,
        "seed_artists": seed_artists
    }

    suggestions_response = requests.get("https://api.spotify.com/v1/recommendations", headers=headers, params=params)
    suggestions_response_json = suggestions_response.json()
    # print(suggestions_response_json)

    songs = []

    for track in suggestions_response_json["tracks"]:
        song = get_song_data(track["id"], token)
        songs.append(song.json())

    return songs, 200

def get_song_data(song_id: str, token: str):
    # print(song_id)
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
    }

    res = requests.get(f"https://api.spotify.com/v1/tracks/{song_id}", headers=headers)
    # print(res)
    res = res.json()
    # print(res)
    
    return Song(res)

def get_user_id(token: str):
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
    }

    res = requests.get(f"https://api.spotify.com/v1/me", headers=headers)
    res = res.json()

    return res["id"]

