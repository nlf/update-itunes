# This script will update the iTunes library in the following ways:
#   Remove files that are in the library and iTunes has flagged as missing
#   Remove files that are in the library and the files are physically missing
#   Add files to the library in the specified path, if they aren't already in the library
#
# To install:
#   sudo easy_install pip
#   sudo pip install appscript
#
# To use:
#   python update_itunes.py -d /Users/yourusername/yourmusicfolder (a -v is optional and will display more detail)
#
# This can be added to cron or whatever task scheduler you like to keep your library up to date automatically
#
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

