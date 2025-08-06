from dotenv import load_dotenv
import os
import requests # HTTP library, used for sending a POST request to Spotfy's /api/token endpoint
import base64 # Spotify requires client_id and client_secret to be base64-encoded for authentication

# Load .env variables into the environment
load_dotenv()
client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')
refresh_token = os.getenv('REFRESH_TOKEN')
redirect_uri = os.getenv('REDIRECT_URI')

# Uses refresh token to request a new access token
def get_access_token(client_id, client_secret, refresh_token):
    # Combine client id and secret for standard username:password format, then encode to base64
    auth_str = f"{client_id}:{client_secret}" 
    b64_auth_str = base64.b64encode(auth_str.encode()).decode() 

    # Spotify's token endpoint
    token_url = 'https://accounts.spotify.com/api/token'

    # Headers and body for the POST request 
    headers = {'Authorization': f'Basic {b64_auth_str}', 
            'Content-Type': 'application/x-www-form-urlencoded'}
    
    data = {'grant_type': 'refresh_token',
            'refresh_token': refresh_token}

    # Send POST request to Spotify to exchange authorization code for access token
    response = requests.post(token_url, headers=headers, data=data)

    # Parse the response, 200 if succeeded, gets access token, if failed, reports status code
    if response.status_code == 200:
        token_info = response.json() # converts json string to dict
        access_token = token_info['access_token']
        print("Access token refreshed")
        # refresh_token = token_info.get('refresh_token')
        # print("Refresh token: " + refresh_token)
        return access_token

    else:
        print("Failed to get token. Status code:", response.status_code)
        print("Response:", response.text)
        return None

# Sends request to Spotify's /v1/me endpoint and gets profile info
def get_user_profile(access_token):
    me_url = 'https://api.spotify.com/v1/me'

    # Set up the authorization header with the access token
    auth_headers = {
        'Authorization': f'Bearer {access_token}'
    }

    # Make the GET request to /v1/me
    me_response = requests.get(me_url, headers=auth_headers)

    # Check if the request succeeded, if succeeded, print profile info, if failed, reports status code
    if me_response.status_code == 200:
        return me_response.json()
    else:
        print("Failed to get user profile. Status code:", me_response.status_code)
        print("Response:", me_response.text)
        return None

def get_top_artists(access_token):
    me_url = 'https://api.spotify.com/v1/me/top/artists'

    # Limiting to just the user's top 5 artists
    params = {
        "limit": 5
    }

    # Set up the authorization header with the access token
    auth_headers = {
        'Authorization': f'Bearer {access_token}'
    }

    # Make the GET request to /v1/me/top/artists
    me_response = requests.get(me_url, headers=auth_headers, params=params)

    # Check if the request succeeded, if succeeded, print top artists, if failed, reports status code
    if me_response.status_code == 200:
        return me_response.json()
    else:
        print("Failed to get top artists. Status code:", me_response.status_code)
        print("Response:", me_response.text)
        return None
    
def get_top_tracks(access_token):
    me_url = 'https://api.spotify.com/v1/me/top/tracks'

    # Limiting to just the user's top 25 tracks
    params = {
        "limit": 5
    }

    # Set up the authorization header with the access token
    auth_headers = {
        'Authorization': f'Bearer {access_token}'
    }

    # Make the GET request to /v1/me/top/tracks
    me_response = requests.get(me_url, headers=auth_headers, params=params)

    # Check if the request succeeded, if succeeded, print top tracks, if failed, reports status code
    if me_response.status_code == 200:
        raw_data =  me_response.json()
        cleaned_tracks = []

        for track in raw_data['items']:
            cleaned_tracks.append({
                'name': track['name'],
                'id': track['id'],
                'popularity': track['popularity']
            })
        return cleaned_tracks
    else:
        print("Failed to get top tracks. Status code:", me_response.status_code)
        print("Response:", me_response.text)
        return None    
    
def get_audio_features_for_tracks(top_tracks):
    from mock_data import mock_audio_features
    print("\n")
    features_list = []
    for track in top_tracks:
        track_id = track["id"]
        track_name = track["name"]
        if track_id in mock_audio_features:    
            audio_features = mock_audio_features[track_id]
            features_list.append({
                "name": track_name,
                **audio_features
            })
        else:
            print(f"No mock data for track ID: {track_name}")
    
    return features_list

def display_top_tracks(top_tracks, profile_info):
    print("\n")
    print(f"{profile_info['display_name']}'s Top 5 Tracks:")
    print("=" * 25)
    
    # Prints the names of the user's top 25 tracks
    for i, track in enumerate(top_tracks, start=1):
        print(f"{i}. {track['name']}, Track ID: {track['id']}, Popularity: {track['popularity']}")
    
def display_top_artists(top_artists, profile_info):
    print("\n")
    print(f"{profile_info['display_name']}'s Top 5 Artists:")
    print("=" * 25)
    
    # Prints the names of the user's top 5 artists
    for i, artist in enumerate(top_artists['items'], start=1):
        print(f"{i}. {artist['name']}")

# Prints user profile data to the terminal
def display_user_profile(profile_info):
    print("\nSpotify Profile")
    print("=" * 15)
    print(f"Display Name: {profile_info['display_name']}")
    print(f"Email: {profile_info['email']}")
    print(f"Country: {profile_info['country']}")
    print(f"Plan: {profile_info['product'].capitalize()}")
    print(f"Followers: {profile_info['followers']['total']}")
    print(f"Profile URL: {profile_info['external_urls']['spotify']}")

import matplotlib.pyplot as plt

def plot_audio_features_bar(features_list):
    # Choose the features to visualize
    feature_names = ['danceability', 'energy', 'tempo', 'valence']

    # Get track names and feature values
    track_names = [track['name'] for track in features_list]

    # Set up subplots: 1 row per feature
    fig, axs = plt.subplots(len(feature_names), 1, figsize=(10, 8), tight_layout=True)

    for i, feature in enumerate(feature_names):
        values = [track[feature] for track in features_list]
        
        axs[i].bar(track_names, values, color='mediumseagreen')
        axs[i].set_title(feature.capitalize())
        
        # Adjust Y axis depending on the feature
        if feature == 'tempo':
            axs[i].set_ylim(0, max(values) + 20)
        else:
            axs[i].set_ylim(0, 1)
        
        axs[i].tick_params(axis='x', rotation=45)

    plt.suptitle("Audio Features of Top Tracks", fontsize=16)
    plt.tight_layout()
    plt.savefig("audio_features.png", dpi=300, bbox_inches='tight')
    plt.show()

# Gets an access token, if access token exists, gets profile info, if profile info exists, displays it
def main():
    # get_access_token(client_id, client_secret, redirect_uri)

    access_token = get_access_token(client_id, client_secret, refresh_token)
    # test_known_track(access_token)
    if access_token:
        profile_info = get_user_profile(access_token)
        top_artists = get_top_artists(access_token)
        top_tracks = get_top_tracks(access_token)
        # if profile_info:
        #     display_user_profile(profile_info)
        # if top_artists:
        #     display_top_artists(top_artists, profile_info)
        if top_tracks:
            top_features = get_audio_features_for_tracks(top_tracks)
            plot_audio_features_bar(top_features)
            # display_top_tracks(top_tracks, profile_info)
            # get_audio_features_for_tracks(top_tracks)

if __name__ == '__main__':
    main()