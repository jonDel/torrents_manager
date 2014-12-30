#!/usr/bin/env python
# -*- coding: utf-8 -*-

import configOptions,re, ast
from tpb import TPB, ORDERS
from pytvdbapi import api
import datetime
from logs import logs
import sqlite as sql

class videoManager(logs):
	'''
	Description: class to get torrents from piratebay for series and movies according
		to pre-configured config files
	'''
	def __init__(self, sqliteDb):
		super(videoManager, self).__init__('videosManager','/var/log/torrents_manager/videosManager')
		# Class atributes
		self.sqliteDb = sqliteDb
		# Getting conf files
		self.seriesConfig = configOptions.ConfigOptions('tv.conf')
		self.moviesConfig = configOptions.ConfigOptions('movies.conf')
		self.seriesTorrentPageUrl = self.seriesConfig.ConfigSectionMap("ignore")['torrentPageUrl']
		self.moviesTorrentPageUrl = self.moviesConfig.ConfigSectionMap("ignore")['torrentPageUrl']
		# Getting tvdb database
		self.tvdb = api.TVDB(self.seriesConfig.ConfigSectionMap("key")['tvdb'])

	def checkSeriesTorrent(self, torrentName, serie):
		'''
		Description: from torrent title, verifies if episode quality is acceptable
		Parameters:
			torrentName: torrent title 
			serie: serie name
		Return:
			True if torrent is acceptable, False otherwise
		'''
		con = sql.connect(self.sqliteDb)
		cur = con.cursor()
		cur.execute("SELECT SeriesConfig.IgnoreResolution FROM SeriesConfig WHERE Name='"+serie+"'");
		ignoreRes = cur.fetchone();ignoreRes = ast.literal_eval(ignoreRes[0])
		if not ignoreRes:
			cur.execute("SELECT SeriesConfig.Resolution FROM SeriesConfig WHERE Name='"+serie+"'")
			resolution = cur.fetchone();resolution=resolution[0]
			con.close()
			try:
				match = re.search('s[0-2][0-9]e[0-2][0-9].*?([0-9]{3,4})',torrentName, re.I)
				torrentRes = int(match.group(1))
				if torrentRes >= resolution: 
					self.log.info('Torrent: '+torrentName+' has an acceptable resolution: ('+resolution+')')
					return True
				else:
					self.log.info('Torrent: '+torrentName+' has resolution '+torrentRes+' lower than the acceptable resolution '+resolution)
			except:
					self.log.info('Torrent: '+torrentName+' does not seem to have resolution: ('+resolution+')')
			self.log.warning('There is no result for this series (season and episode):'+torrentName)
			return False
		else:
			con.close()
			self.log.info('Ignoring series episode:'+torrentName+' resolution.')
			return True

	def checkMoviesTorrent(self, torrentName):
		'''
		Description: from torrent title, verifies if movie quality is acceptable
		Parameters:
			torrentName: torrent title
		Return:
			True if torrent is acceptable, False otherwise
		'''
		if not  ast.literal_eval(self.moviesConfig.ConfigSectionMap("ignore")['videoResolution']):
			for rate, resolution in self.moviesConfig.ConfigSectionMap("resolution"):
				torrent= re.search('('+resolution+')', torrentName, re.I)
				try:
					torrent.group(1)
					self.log.info('Torrent: '+torrentName+' has an acceptable resolution: ('+resolution+')')
					return True
				except:
					self.log.info('Torrent: '+torrentName+' does not have resolution: ('+resolution+')')
			self.log.warning('There is no result for this movie: '+torrentName )
			return False
		else:
			self.log.info('Ignoring movie:'+torrentName+' resolution.')
			return True

	def getSeriesTorrentFromPage(self, fileName, serie):
		'''
		Description: from file name searches pirate bay for apropriate series torrent file
		Parameters:
			fileName: desired file name for a TV serie
			serie: serie name
		Return:
			torrent: torrent file downloaded from pirate bay
	'''
		torrentPage = TPB(self.seriesTorrentPageUrl)
		# Order by major number of seeders first
		torrentMultipage = torrentPage.search(fileName).order(ORDERS.SEEDERS.DES).multipage()
		for torrent in torrentMultipage:
			self.log.debug("Testing video resolution for torrent:"+str(torrent.title)+" from uploader "+str(torrent.user))
			if self.checkSeriesTorrent(str(torrent.title)):
				self.log.debug('Testing uploader`s '+torrent.user+' reputation:')
				if self.checkUploader(str(torrent.user), serie):
					#self.videoTitle = torrent.title
					#self.magnetLink = torrent.magnet_link
					self.log.debug('Chosen torrent`s title is: '+str(torrent.title))
					return torrent
				else:
					self.log.warning('I dont want anything from an untrusted uploader: '+torrent.user)
			else:
				self.log.debug('It doesnt correspond to the file I want: '+torrent.title)
		self.log.warning('It was not possible to find a reliable torrent.')
		return False

	def getMovieTorrentFromPage(self, fileName):
		'''
		Description: from file name searches pirate bay for apropriate movie torrent file
		Parameters:
			fileName: desired movie name
		Return:
			torrent: movie torrent file downloaded from pirate bay
		'''
		torrentPage = TPB(self.moviesTorrentPageUrl)
		# Order by major number of seeders first
		torrentMultipage = torrentPage.search(fileName).order(ORDERS.SEEDERS.DES).multipage()
		for torrent in torrentMultipage:
			self.log.debug("Testing video resolution for torrent:"+str(torrent.title)+" from uploader "+str(torrent.user))
			if self.checkMoviesTorrent(str(torrent.title)):
				self.log.debug("Testing uploader's quality:")
				if self.checkUploader(str(torrent.user), self.moviesConfig):
					self.log.debug('Torrent title is: '+str(torrent.title))
					self.log.debug('Torrent files are: '+str(torrent.files))
					self.log.debug('Uploader is: '+str(torrent.user))
					self.log.debug('The number of leechers is: '+ str(torrent.leechers))
					self.log.debug('The number of seeders is: '+ str(torrent.seeders))
					return torrent
				else:
					self.log.warning('I dont want anything from an untrusted uploader')
			else:
				self.log.debug('It doesnt correspond to the file I want')
		self.log.warning('It was not possible to find a reliable torrent.')
		return False

	def checkUploader(self, torrentUploader, serie):
		'''
		Description: verifies if torrent uploader is trusted
		Parameters:
			torrentUploader: torrent uploader
		Return:
			True if torrent uploader is trusted, False otherwise
		'''
		con = sql.connect(self.sqliteDb)
		cur = con.cursor()
		cur.execute("SELECT SeriesConfig.IgnoreUpReputation FROM SeriesConfig WHERE Name='"+serie+"'");
		ignoreUploader = cur.fetchone();ignoreUploader = ast.literal_eval(ignoreUploader[0])
		if not ignoreUploader:
			cur.execute("SELECT SeriesConfig.favTorUploader FROM SeriesConfig WHERE Name='"+serie+"'");
			favTorUploader = cur.fetchone();favTorUploader = favTorUploader[0]
			if torrentUploader == favTorUploader:
				self.log.debug('Torrent uploader '+torrentUploader+' is the favorite one for '+serie+' serie.')
				con.close()
				return True
			else:
				cur.execute('SELECT Name FROM torrentUploaders ORDER BY Ranking DESC');rows = cur.fetchall();
				for uploader in rows:
					if uploader == torrentUploader:
						con.close()
						self.log.debug('Uploader '+uploader+' is a trusted one.')
						return True
				self.log.warning('There uploader '+torrentUploader+'is not trusted.')
				con.close()
				return False
		else:
			self.log.info('Ignoring uploader reputation.')
			return True

	def updateAllSeries(self):
		'''
		Description: read from a config file and check if there are new episodes
			to download. The config file has the series and each last
			downloaded episode.
		Return:
			seriesDict dictionary with each serie and its episodes to download
		'''
		self.log.info('Checking if there are new episodes to be downloaded')
		for serie, lastEpisode in self.seriesConfig.ConfigSectionMap("last_episode").iteritems():
			seriesEpisodeList = self.getEpisodesToDownload(self, serie, lastEpisode)
			for episode in seriesEpisodeList:
				pass
				#getMovieTorrentFromPage
			#falta colocar pra pegar do piratebay
		return seriesEpisodeList

	def getEpisodesToDownload(self, serie, lastEpisode):
		'''
		Description: read from a config file and check if there are new episodes
			to download. The config file has the series and each last
			downloaded episode.
		Return:
			seriesDict dictionary with each serie and its episodes to download
		'''
		seriesEpisodeList = []
		self.log.info('Checking if there are new episodes to be downloaded')
		lastDownEp = int(lastEpisode[4:7])
		lastDownSeason = int(lastEpisode[1:3])
		self.log.debug('Tv serie is '+serie)
		self.log.debug('Last downloaded episode was '+lastEpisode)
		lastSeason,lastEp = self.checkLastEpisode(serie)
		# Search for all seasons above last downloaded season
		for season in range(lastSeason,lastDownSeason-1,-1):
			firstEpSeason, lastEpSeason = self.getSeasonLastFirstEpisodes(season, serie)
			# Search for all episodes above last downloaded episode
			self.log.debug('Searching in season '+str(season)+' from '+str(lastSeason)+' seasons')
			for episode in range(lastEpSeason,firstEpSeason-1,-1):
				if season <= lastDownSeason and episode <= lastDownEp:
					break
				else:
					seriesEpisodeList.append(serie+" s"+("%2s" % str(season)).replace(' ','0')+"e"+("%2s" % str(episode)).replace(' ','0'))
		return seriesEpisodeList

	def checkLastEpisode(self, serie):
		'''
		Description: from tvdb, discover last aired episode of the serie
		Parameters:
			serie: serie title
		Return:
			(lastSeason,lastEpisode): tuple last season and episode if successful, empty string otherwise
		'''
		self.log.debug('Connecting to TVDB site to search for the last episodes of serie '+serie)
		result = self.tvdb.search(serie, "en")
		show = result[0]
		# TODO: descobrir porque precisa desse try sem sentido
		try:
			dumm = result[0][1]
		except:
			dumm = result[1][1]

		dateToday = datetime.datetime.now().date()
		for season in reversed(show):
			for episode in reversed(season):
				if episode.FirstAired != '' and episode.FirstAired < dateToday:
					lastSeason  = ("%2s" % episode.SeasonNumber).replace(' ','0')
					lastEpisode = ("%2s" % episode.EpisodeNumber).replace(' ','0')
					self.log.debug('Last episode already aired is s'+lastSeason+'e'+lastEpisode+' in '+str(episode.FirstAired))
					return int(lastSeason), int(lastEpisode)
		return ''

	def getSeasonLastAndFirstEpisodes(self, season, serie):
		'''
		Description: from tvdb, discover first and last episode of the required season
		Parameters:
			season: serie season
			serie: serie title
		Return:
			(firstEpisode,lastEpisode): tuple of first and last episode of the required season
		'''
		self.log.debug('Connecting to TVDB site to search for the last episodes from season '+str(season)+' of serie '+serie)
		result = self.tvdb.search(serie, "en")
		show = result[0]
		firstEpisode = ("%2s" % next(iter(show[season])).EpisodeNumber).replace(' ','0')
		lastEpisode = ("%2s" % show[season][len(show[season])].EpisodeNumber).replace(' ','0')
		self.log.debug('First episode is '+firstEpisode+' and last episode:'+lastEpisode)
		return int(firstEpisode),int(lastEpisode)
		
#>> help(inotifyx)
#
#>>> from inotifyx import *
#>>> fd = init()
#>>> try: 
#...   wd = add_watch(fd, '/home/b40153/Downloads', IN_ALL_EVENTS)
#...   events = get_events(fd)
#...   print events
#...   rm_watch(fd, wd)
#... finally:
#...   os.close(fd)
