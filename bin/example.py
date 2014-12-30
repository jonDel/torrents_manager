#!/usr/bin/env python
# -*- coding: utf-8 -*-

import config,re,time
from tpb import TPB
from tpb import CATEGORIES, ORDERS
import OpenSubtitles
import logging
import gzip, os
import transmissionrpc

logging.basicConfig(level=logging.DEBUG)



uploaders = config.ConfigSectionMap("torrent_uploaders")
episode = config.ConfigSectionMap("series")['supernatural']
print "episode is "+episode
down_dir = config.ConfigSectionMap("dir")['series_dir']
print "down_dir is "+down_dir


def return_torrent_name(torrent_name):
	torrent= re.search('s([0-2][0-9])e([0-2][0-9]).*(720|1080)', torrent_name, re.I)
	ret = {}
	try:
		torrent_season  = torrent.group(1)
		torrent_episode = torrent.group(2)
		try:
			torrent.group(3)
			ret = {'is_valid':True,'hd_quality':True,'season':torrent_season,'episode':torrent_episode}
		except:
			#print 'Não tem torrent de boa qualidade'
			ret = ['False', 'False', torrent_season, torrent_episode]
			ret = {'is_valid':True,'hd_quality':False,'season':torrent_season,'episode':torrent_episode}
	except:
		ret = {'is_valid':False,'hd_quality':False}
		#print	'Não tem torrent com a temporada/episodio desejado'
	return ret

		
#t = TPB('https://thepiratebay.org')
#first_page = t.search('supernatural').order(ORDERS.SEEDERS.DES).page(0)

def get_torrent_from_page(page):
	for torrents in page:
		break_tor = False
		try:
			#print "torrent is "+str(torrents)
			ess
		except:
			pass
		torrent_reg = return_torrent_name(torrents.title)
		if (torrent_reg['is_valid'] and torrent_reg['hd_quality']):
			if episode == ('s'+torrent_reg['season']+'e'+torrent_reg['episode']):
				print 'Agora falta testar se o uploader é bagual'
				for uploader in uploaders:
					#print 'uploader is '+torrents.user
					#print 'uploader configured is '+uploader
					
					if uploader == torrents.user:
						print 'OK!!! torrent title is '+torrents.title
						print 'OK!!! torrent files is '+str(torrents.files)
						print 'uploader is '+torrents.user
						print 'number of leechers is '+ str(torrents.leechers)
						print 'number of seeders is '+ str(torrents.seeders)
						break_tor= True
						# achei o uploader certo, quebro o loop agora
						break
					else:
						print 'nao quero coisa de uploader desconhecido'
			else:
				#print 'Não corresponde ao episodio que queremos. TODO: pegar mais páginas'
				pass
		# achei o torrent certo, quebro o loop agora
		if break_tor:
			break
	return torrents

#for torrents in first_page:
#	print 'torrent is '+str(torrents)
#	print 'OK!!! torrent title is '+torrents.title
#	print 'OK!!! torrent files is '+str(torrents.files)
#	print 'uploader is '+torrents.user
#	print 'number of leechers is '+ str(torrents.leechers)
#	print 'number of seeders is '+ str(torrents.seeders)
#tor_chosen = get_torrent_from_page(first_page)
#print a[0].magnet_link
#for t in a:
#	print t
#	print t.magnet_link
#	print t.size
#	print t.user
#	print t.leechers
#	print t.seeders
#	break
#	#print a.file
# -*- coding: utf-8 -*-


tc = transmissionrpc.Client('localhost', port=9091)
print tc.get_torrents()
##tc.stop_torrent(1)
##tc.start_torrent(1)
#iny=0
for tor in tc.get_torrents():
	print tor.status
	print tor
	print tor.id
	#print tor.magnet_link
	#print tor.size
	#print tor.user
	#print tor.leechers
	#print tor.seeders
	#print tor.files()
	filesr = tor.files()
	print filesr
	print filesr[0]['name' ]
	for files in filesr:
		print filesr[files]['name']
		#print files
	#print a.file
#
##tc.remove_torrent(1)
##tc.remove_torrent(1)
#tc.add_torrent('magnet:?xt=urn:btih:7C9F535CC79E852B6C7707CA5FD6E44908EE4867&dn=the+big+bang+theory+s07e22+hdtv+x264+lol+ettv&tr=http%3A%2F%2Ftracker.trackerfix.com%2Fannounce&tr=udp%3A%2F%2Fopen.demonii.com%3A1337', download_dir = down_dir)
##tc.add_torrent(None,filename=tor_chosen.magnetLink, download_dir = down_dir)
#atr=tc.add_torrent(tor_chosen.magnet_link, download_dir = down_dir)
#for tor in tc.get_torrents():
#	print tor.status
#	id = tor.id
#print 'id is '+str(id)
#try:
#	tre = tc.get_torrent(id)
#	#print "transmission-dir = "+tre.comment
#	print "name = "+tre.name
#	print "commnet = "+tre.downloadDir
#	print 'files = '+str(tc.get_files())
#	#print "files = "+str(tre.files())
#	#for file in tre.files:
#	#	print 'file is '+str(file)
#except:
#	raise
#	pass
#print tc.get_torrents ()
#time.sleep(3)
##print tor.magnetLink
#for tor in tc.get_torrents():
#	tor.update()
#	print tor.status
##print tor.status # downloading, seeding


