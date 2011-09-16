import os
import argparse
from appscript import *
from mactypes import *

parser = argparse.ArgumentParser()
parser.add_argument('-d', '--directory', dest='dir', help='directory to scan')
parser.add_argument('-v', '--verbose', dest='verbose', help='display debugging information', action='store_const', const=True)
args = parser.parse_args()

def delete_song(iTunes, song):
    if args.verbose:
        print('Deleting missing song from library')
    iTunes.sources.library_playlists[1].delete(song)

if args.dir:
    cur_songs = []
    iTunes = app('iTunes')
    for song in iTunes.sources.library_playlists[1].file_tracks.get():
        if song.location.get() == k.missing_value:
            delete_song(iTunes, song)
            continue
        if not os.path.exists(song.location.get().path):
            delete_song(iTunes, song)
            continue
        cur_songs.append(song.location.get().path)
        
    for root, subfolders, files in os.walk(args.dir):
        for filename in files:
            if os.path.splitext(filename)[1].lower() == '.mp3':
                full_path = os.path.join(root, filename)
                if not full_path in cur_songs:
                    if args.verbose:
                        print('Adding %s to library' % full_path)
                    iTunes.add(Alias(u'%s' % full_path))

