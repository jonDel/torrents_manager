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

filename = "/media/SAMSUNG/transmission-daemon/downloads/Hemlock.Grove.S01E01.720p.WEBRip.x264-QRUS.mkv"
#File hash is 953feed23f613636
filename = "/media/SAMSUNG/Seriados/Supernatural.S09E21.720p.HDTV.X264-DIMENSION.mkv"
#File hash is 2c631aa0fa454521
filename = "/media/SAMSUNG/transmission-daemon/downloads/Game.of.Thrones.S04E06.720p.HDTV.x264-DIMENSION[rarbg]/Game.of.Thrones.S04E06.720p.HDTV.x264-DIMENSION.mkv"
#File hash is 876f22be2407374a
filehash = '876f22be2407374a'
p =  OpenSubtitles.OpenSubtitles(None, None)
subfname = filename[:-3]+"srt"
subTempGz = '/tmp/subtitle.gz'
logging.info("Processing %s" % filename)
#subs = p.process(filename, ["en", "pt"])
lang='pt-br'
print 'lang is '+lang
#subs = p.process(filename, [lang], '876f22be2407374a')
#for i in subs:
#	print 'uploader is '+i['user']+' and his rank is ####'+(i['user_rank']).replace(' member','').replace(' plus', '')+'###'
#	print 'rating is '+i['rating']+' and his bad is '+i['bad']
#lang='pt'
#print 'lang is '+lang
#subs = p.process(filename, [lang])
#for i in subs:
#	print 'uploader is '+i['user']+' and his rank is ####'+(i['user_rank']).replace(' member','').replace(' plus', '')+'###'
#	print 'rating is '+i['rating']+' and his bad is '+i['bad']
#lang='en'
#print 'lang is '+lang
#subs = p.process(filename, [lang])
#for i in subs:
#	print 'uploader is '+i['user']+' and his rank is ####'+(i['user_rank']).replace(' member','').replace(' plus', '')+'###'
#	print 'rating is '+i['rating']+' and his bad is '+i['bad']

size = '1234244'
#size = os.path.getsize(filename)
subs = p.query_with_hash(filename,size,filehash, [lang]) #, size, [lang])(filename, [lang], '876f22be2407374a')
for i in subs:
	print 'uploader is '+i['user']+' and his rank is ####'+(i['user_rank']).replace(' member','').replace(' plus', '')+'###'
	print 'rating is '+i['rating']+' and his bad is '+i['bad']
##p.downloadFile(subs[0]['link'], subTempGz)
##inF = gzip.open(subTempGz, 'rb')
##outF = open(subfname, 'wb')
##outF.write( inF.read() )
##inF.close()
##outF.close()
##os.remove(subTempGz)
##print 'gravada legenda '+subfname
#
#
#print 'subs is:'
##print subs
#print 'subs 0 is:'
#print subs[0]['link']
#print 'subs 1 is:'
#print subs[1]['link']
#print 'subs 2 is:'
#print subs[2]['link']
#print 'subs 3 is:'
#print subs[3]['link']
#p.downloadFile('http://api.thesubdb.com/?action=download&hash=ffaea75b7402c1b1a2f22bf130c3b302&language=pt', "/home/jon/Downloads/teste.srt.gz")
#p.downloadFile(subs[0]['link'], subfname)


