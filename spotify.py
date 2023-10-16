import spotipy
import time
from spotipy.oauth2 import SpotifyOAuth
from flask import Flask, request, url_for, session, redirect, render_template
from datetime import date

import serial
import webbrowser

app = Flask(__name__)

app.config['SESSION_COOKIE_NAME'] = 'Cookie'
app.secret_key = 'ea3b71852d3c4355ba8e721e4858cf83'
TOKEN_INFO = 'token_info'

# route to handle logging in
@app.route('/')
def login(): 
    auth_url = create_spotify_oauth().get_authorize_url()
    return redirect(auth_url)

# route to handle the redirect URI after authorization
@app.route('/redirect')
def redirect_page():
    session.clear()
    code = request.args.get('code')
    token_info = create_spotify_oauth().get_access_token(code)
    session[TOKEN_INFO] = token_info
    return redirect(url_for('save_playlist',_external=True))

# route to save playlist and push tracks to the playback
@app.route('/savePlaylist')
def save_playlist():
    try:      
        token_info = get_token()
        print('Token info', token_info)
    except:
        print('User not logged in')
        return redirect("/")

    # create a Spotipy instance 
    sp = spotipy.Spotify(auth=token_info['access_token'])

    # get the user's top tracks
    top_tracks = sp.current_user_top_tracks(150, 0, 'medium_term')['items']
    top_tracks_ids = []

    # loop trough user's top tracks, select the tracks where the feature of "danceability" is geq 0.75
    # push the selected tracks to the playback
    # build a new playlist and add the selected tracks to the playlist
    for playlist in top_tracks:
        feature = sp.audio_features(playlist['id'])
        danceability = feature[0]['danceability']

        # if('k-pop' in artist["genres"]):
        #     top_tracks_ids.append(playlist['uri'])
            # print (playlist['id']) debug

        if(danceability >= 0.75 ):
            # print(playlist['id']) #for debug
            top_tracks_ids.append(playlist['uri'])

    if len(top_tracks_ids) == 0:
        return 'Hmmm. None of your tracks are for party.'

    # create a new playlist
    user_id = sp.me()['id']
    today = date.today()
    playlist_name = f'Personalized Party Playlist for {today}'

    playlist = sp.user_playlist_create(user=user_id, name=playlist_name, public=True)
    # add the party tracks to the playlist
    sp.user_playlist_add_tracks(user_id, playlist['id'], top_tracks_ids)

    # get playlist context url
    playlist_url = playlist['external_urls']['spotify']

    # start playback of the playlist on an active Spotify device
    devices = sp.devices()
    if devices['devices']:
        device_id = devices['devices'][0]['id']  # Get the first available device
        sp.start_playback(device_id=device_id, context_uri=playlist_url)
        return f'Playback started on device: {device_id}'
    else:
        print('No active Spotify devices found.')
        return f'{playlist} created successfully.'

# function to get the token info from the session
def get_token():
    token_info = session.get(TOKEN_INFO, None)
    if not token_info:
        return redirect(url_for('login', _external=False))
    
    # check if the token is expired and refresh it
    now = int(time.time())

    is_expired = token_info['expires_at'] - now < 60
    if(is_expired):
        spotify_oauth = create_spotify_oauth()
        token_info = spotify_oauth.refresh_access_token(token_info['refresh_token'])

    return token_info

def create_spotify_oauth():
    return SpotifyOAuth(
        client_id = '89d97481e689412dac9ffa13ba3df86d',
        client_secret = 'ea3b71852d3c4355ba8e721e4858cf83',
        redirect_uri = url_for('redirect_page', _external=True),
        scope='user-library-read playlist-modify-public playlist-modify-private user-top-read user-modify-playback-state user-read-playback-state'
    )

if __name__ == '__main__':
    app.run(debug=True)


