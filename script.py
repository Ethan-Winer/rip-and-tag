import musicbrainzngs as mb
from youtubesearchpython import VideosSearch as search_youtube
import yt_dlp
from urllib.parse import quote
from mutagen.easyid3 import EasyID3
import os

# Comments for jeff

def sanitize_file_name(file_name):
    char_map = {
        '/': '-',
        '\\': '-',
        '<': '-',
        '>': '-',
        ':': ' -',
        '"': '\'',
        '|': '-',
        '?': '(question mark)',
        '*': '.'
    }
    return file_name.translate(str.maketrans(char_map))

if __name__ == '__main__':
    artist = input('Artist: ')
    album = input('Album: ')
    do_increment = input('Increment filenames (y/n): ') == 'y'

    directory = f'{artist}/{album}'
    temp_file_path = f'{directory}/temp_name_before_sanitization.mp3'
    
    yt_dlp_options = {
        'format': 'mp3/bestaudio/best',
        'outtmpl': f'{directory}/temp_name_before_sanitization.%(ext)s',
        'restrict-filenames': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': 0,
        }]
    }

    # Get data from musicbrainz
    print('\nFinding album on MusicBrainz...')
    mb.set_useragent('Rip and Tag', '0.1')
    results = mb.search_releases(album, artistname=artist, strict=True)
    
    if results['release-count'] == 0:
        print('No record of artist and album :(')
        exit(0)

    os.makedirs(f'{directory}', exist_ok=True)
    album_id = results['release-list'][0]['id']
    mediums = mb.get_release_by_id(album_id, includes=['recordings'])['release']['medium-list']

    with yt_dlp.YoutubeDL(yt_dlp_options) as ytdl:
        # medium something like disk number
        for medium in mediums:
            for track in medium['track-list']:
                # Rip from youtube
                track_name = sanitize_file_name(track['recording']['title'])
                response = search_youtube(f'{track_name} by {artist}', limit=1)
                video = response.result()['result'][0]
                ytdl.download(video['link'])

                if do_increment:
                    prefix = f'[{medium['position']}, {str(track['position'].zfill(2))}]'
                    file_name = f'{directory}/{prefix} {track_name}.mp3'
                else:
                    file_name = f'{directory}/{track_name}.mp3'

                # Tag               
                file = EasyID3(temp_file_path)
                file['title'] = track_name
                file['album'] = album
                file['artist'] = artist
                file['tracknumber'] = track['position']
                file['discnumber'] = medium['position']
                file.save(v2_version=3)
                os.rename(temp_file_path, file_name)

    print('\n\ndone')