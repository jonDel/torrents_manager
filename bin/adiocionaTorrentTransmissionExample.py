# -*- coding: utf-8 -*-

#   This file is part of periscope.
#   Copyright (c) 2008-2011 Patrick Dessalle <patrick@dessalle.be>
#
#    periscope is free software; you can redistribute it and/or modify
#    it under the terms of the GNU Lesser General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    periscope is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public License
#    along with periscope; if not, write to the Free Software
#    Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

import OpenSubtitles
import logging
import gzip, os

logging.basicConfig(level=logging.DEBUG)


import transmissionrpc

tc = transmissionrpc.Client('localhost', port=9091)
tc.get_torrents()
tc.stop_torrent(1)
tc.start_torrent(1)
tc.remove_torrent(1)
tc.add(None,filename='magnet:?xt=urn:btih:7C9F535CC79E852B6C7707CA5FD6E44908EE4867&dn=the+big+bang+theory+s07e22+hdtv+x264+lol+ettv&tr=http%3A%2F%2Ftracker.trackerfix.com%2Fannounce&tr=udp%3A%2F%2Fopen.demonii.com%3A1337', download_dir = down_dir)
tor = tc.get_torrent (1)
print tor.magnetLink
print tor.status # downloading, seeding
