#!/usr/bin/env python

#    This file is part of the Minecraft Overviewer.
#
#    Minecraft Overviewer is free software: you can redistribute it and/or
#    modify it under the terms of the GNU General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or (at
#    your option) any later version.
#
#    Minecraft Overviewer is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General
#    Public License for more details.
#
#    You should have received a copy of the GNU General Public License along
#    with the Overviewer.  If not, see <http://www.gnu.org/licenses/>.

import sys
if sys.version_info[0] != 2 and sys.version_info[1] < 6:
    print "Sorry, the Overviewer requires at least Python 2.6 to run"
    sys.exit(1)

import os
import os.path
from optparse import OptionParser
import re
import json

import world
import nbt

helptext = """
%prog [OPTIONS] <World # / Path to World> <tiles dest dir>"""

def main():
    parser = OptionParser(usage=helptext)

    options, args = parser.parse_args()

    if len(args) < 1:
        print "You need to give me your world number or directory"
        parser.print_help()
        list_worlds()
        sys.exit(1)
    worlddir = args[0]

    if not os.path.exists(worlddir):
        try:
            worldnum = int(worlddir)
            worlddir = world.get_worlds()[worldnum]['path']
        except (ValueError, KeyError):
            print "Invalid world number or directory"
            parser.print_help()
            sys.exit(1)

    if len(args) != 2:
        parser.error("Where do you want to save the tiles?")

    destdir = args[1]

    output = file(os.path.join(destdir, 'playermarkers.js'), 'w')
    playerdir = os.path.join(worlddir, 'players')
    output.write('playerMarkerData = [\n')
    for filename in os.listdir(playerdir):
        data = nbt.load(os.path.join(playerdir, filename))[1]
        playername = filename[0:-4]
        formatdata = ((playername,) + tuple(int(f) for f in data['Pos']))
        output.write('{"msg":"%s", "x":%d, "y":%d, "z":%d},\n' % formatdata)
    output.write(']\n')
    output.close()


def list_worlds():
    "Prints out a brief summary of saves found in the default directory"
    print 
    worlds = world.get_worlds()
    if not worlds:
        print 'No world saves found in the usual place'
        return
    print "Detected saves:"
    for num, info in sorted(worlds.iteritems()):
        timestamp = time.strftime("%Y-%m-%d %H:%M",
                                  time.localtime(info['LastPlayed'] / 1000))
        playtime = info['Time'] / 20
        playstamp = '%d:%02d' % (playtime / 3600, playtime / 60 % 60)
        size = "%.2fMB" % (info['SizeOnDisk'] / 1024. / 1024.)
        print "World %s: %s Playtime: %s Modified: %s" % (num, size, playstamp, timestamp)


if __name__ == "__main__":
    main()
