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

import os, xmlrpclib,gzip, logging, struct, re,urllib2
import socket # For timeout purposes

USER_AGENT = 'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.1.3)'
log = logging.getLogger(__name__)

OS_LANGS ={ "en": "eng", 
            "fr" : "fre", 
            "hu": "hun", 
            "cs": "cze", 
            "pl" : "pol", 
            "sk" : "slo", 
            "pt" : "por", 
            "pt-br" : "pob", 
            "es" : "spa", 
            "el" : "ell", 
            "ar":"ara",
            'sq':'alb',
            "hy":"arm",
            "ay":"ass",
            "bs":"bos",
            "bg":"bul",
            "ca":"cat",
            "zh":"chi",
            "hr":"hrv",
            "da":"dan",
            "nl":"dut",
            "eo":"epo",
            "et":"est",
            "fi":"fin",
            "gl":"glg",
            "ka":"geo",
            "de":"ger",
            "he":"heb",
            "hi":"hin",
            "is":"ice",
            "id":"ind",
            "it":"ita",
            "ja":"jpn",
            "kk":"kaz",
            "ko":"kor",
            "lv":"lav",
            "lt":"lit",
            "lb":"ltz",
            "mk":"mac",
            "ms":"may",
            "no":"nor",
            "oc":"oci",
            "fa":"per",
            "ro":"rum",
            "ru":"rus",
            "sr":"scc",
            "sl":"slv",
            "sv":"swe",
            "th":"tha",
            "tr":"tur",
            "uk":"ukr",
            "vi":"vie"}

class OpenSubtitles():
    url = "http://www.opensubtitles.org/"
    site_name = "OpenSubtitles"
    
    def __init__(self, config, cache_folder_path, langs = OS_LANGS, revertlangs = None):
        self.langs = langs
        self.server_url = 'http://api.opensubtitles.org/xml-rpc'
        self.revertlangs = dict(map(lambda item: (item[1],item[0]), self.langs.items()))
        self.tvshowRegex = re.compile('(?P<show>.*)S(?P<season>[0-9]{2})E(?P<episode>[0-9]{2}).(?P<teams>.*)', re.IGNORECASE)
        self.tvshowRegex2 = re.compile('(?P<show>.*).(?P<season>[0-9]{1,2})x(?P<episode>[0-9]{1,2}).(?P<teams>.*)', re.IGNORECASE)
        self.movieRegex = re.compile('(?P<movie>.*)[\.|\[|\(| ]{1}(?P<year>(?:(?:19|20)[0-9]{2}))(?P<teams>.*)', re.IGNORECASE)


    def process(self, filepath, langs):
        ''' main method to call on the plugin, pass the filename and the wished 
        languages and it will query OpenSubtitles.org '''
        if os.path.isfile(filepath):
            if not filehash:
            	filehash = self.hashFile(filepath)
            log.debug('File hash is '+filehash)
            size = os.path.getsize(filepath)
            fname = self.getFileName(filepath)
            return self.query(moviehash=filehash, langs=langs, bytesize=size, filename=fname)
        else:
            fname = self.getFileName(filepath)
            return self.query(langs=langs, filename=fname)
        
    def query_with_hash(self, filepath, size, filehash, langs):
        ''' Makes a query with given hash and movie byte size on opensubtitles and returns info about found subtitles.
            Note: Since using moviehash, bytesize is necessary.    '''
        fname = self.getFileName(filepath)
        return self.query(moviehash=filehash, langs=langs, bytesize=size, filename=fname)

    def createFile(self, subtitle):
        '''pass the URL of the sub and the file it matches, will unzip it
        and return the path to the created file'''
        suburl = subtitle["link"]
        videofilename = subtitle["filename"]
        srtbasefilename = videofilename.rsplit(".", 1)[0]
        self.downloadFile(suburl, srtbasefilename + ".srt.gz")
        f = gzip.open(srtbasefilename+".srt.gz")
        dump = open(srtbasefilename+".srt", "wb")
        dump.write(f.read())
        dump.close()
        f.close()
        os.remove(srtbasefilename+".srt.gz")
        return srtbasefilename+".srt"

    def query(self, filename, imdbID=None, moviehash=None, bytesize=None, langs=None):
        ''' Makes a query on opensubtitles and returns info about found subtitles.
            Note: if using moviehash, bytesize is required.    '''
        log.debug('query')
        #Prepare the search
        search = {}
        sublinks = []
        if moviehash: search['moviehash'] = moviehash
        if imdbID: search['imdbid'] = imdbID
        if bytesize: search['moviebytesize'] = str(bytesize)
        if langs: search['sublanguageid'] = ",".join([self.getLanguage(lang) for lang in langs])
        if len(search) == 0:
            log.debug("No search term, we'll use the filename")
            # Let's try to guess what to search:
            guessed_data = self.guessFileData(filename)
            search['query'] = guessed_data['name']
            log.debug(search['query'])
            
        #Login
        self.server = xmlrpclib.Server(self.server_url)
        socket.setdefaulttimeout(10)
        try:
            log_result = self.server.LogIn("","","eng","periscope")
            log.debug(log_result)
            token = log_result["token"]
        except Exception:
            log.error("Open subtitles could not be contacted for login")
            token = None
            socket.setdefaulttimeout(None)
            return []
        if not token:
            log.error("Open subtitles did not return a token after logging in.")
            return []            
            
        # Search
        self.filename = filename #Used to order the results
        sublinks += self.get_results(token, search)

        # Logout
        try:
            self.server.LogOut(token)
        except:
            log.error("Open subtitles could not be contacted for logout")
        socket.setdefaulttimeout(None)
        return sublinks
        
        
    def get_results(self, token, search):
        log.debug("query: token='%s', search='%s'" % (token, search))
        try:
            if search:
                results = self.server.SearchSubtitles(token, [search])
        except Exception, e:
            log.error("Could not query the server OpenSubtitles")
            log.debug(e)
            return []
        log.debug("Result: %s" %str(results))

        sublinks = []
        if results['data']:
            log.debug(results['data'])
            # OpenSubtitles hash function is not robust ... We'll use the MovieReleaseName to help us select the best candidate
            for r in sorted(results['data'], self.sort_by_moviereleasename):
                # Only added if the MovieReleaseName matches the file
                result = {}
                result["release"] = r['SubFileName']
                result["link"] = r['SubDownloadLink']
                result["user"] = r['UserNickName']
                result["user_rank"] = r['UserRank']
                result["page"] = r['SubDownloadLink']
                result["bad"] = r['SubBad']
                result["rating"] = r['SubRating']
                result["downloadsCnt"] = r['SubDownloadsCnt']
                result["IDMovieImdb"] = r['IDMovieImdb']
                result["MovieImdbRating"] = r['MovieImdbRating']
                result["languageName"] = r['LanguageName']
                result["lang"] = self.getLG(r['SubLanguageID'])
                if search.has_key("query") : #We are using the guessed file name, let's remove some results
                    if r["MovieReleaseName"].startswith(self.filename):
                        sublinks.append(result)
                    else:
                        log.debug("Removing %s because release '%s' has not right start %s" %(result["release"], r["MovieReleaseName"], self.filename))
                else :
                    sublinks.append(result)
        return sublinks

    def sort_by_moviereleasename(self, x, y):
        ''' sorts based on the movierelease name tag. More matching, returns 1'''
        #TODO add also support for subtitles release
        xmatch = x['MovieReleaseName'] and (x['MovieReleaseName'].find(self.filename)>-1 or self.filename.find(x['MovieReleaseName'])>-1)
        ymatch = y['MovieReleaseName'] and (y['MovieReleaseName'].find(self.filename)>-1 or self.filename.find(y['MovieReleaseName'])>-1)
        #print "analyzing %s and %s = %s and %s" %(x['MovieReleaseName'], y['MovieReleaseName'], xmatch, ymatch)
        if xmatch and ymatch:
            if x['MovieReleaseName'] == self.filename or x['MovieReleaseName'].startswith(self.filename) :
                return -1
            return 0
        if not xmatch and not ymatch:
            return 0
        if xmatch and not ymatch:
            return -1
        if not xmatch and ymatch:
            return 1
        return 0

    def getFileName(self, filepath):
        if os.path.isfile(filepath):
            filename = os.path.basename(filepath)
        else:
            filename = filepath
        if filename.endswith(('.avi', '.wmv', '.mov', '.mp4', '.mpeg', '.mpg', '.mkv')):
            fname = filename.rsplit('.', 1)[0]
        else:
            fname = filename
        return fname

    def hashFile(self, name):
        ''' 
        Calculates the Hash à-la Media Player Classic as it is the hash used by OpenSubtitles.
        By the way, this is not a very robust hash code.
        ''' 
        longlongformat = 'Q'  # unsigned long long little endian
        bytesize = struct.calcsize(longlongformat)
        format= "<%d%s" % (65536//bytesize, longlongformat)
     
        f = open(name, "rb") 
        filesize = os.fstat(f.fileno()).st_size
        hash = filesize 
     
        if filesize < 65536 * 2:
            log.error('File is too small')
            return "SizeError" 
     
        buffer= f.read(65536)
        longlongs= struct.unpack(format, buffer)
        hash+= sum(longlongs)
     
        f.seek(-65536, os.SEEK_END) # size is always > 131072
        buffer= f.read(65536)
        longlongs= struct.unpack(format, buffer)
        hash+= sum(longlongs)
        hash&= 0xFFFFFFFFFFFFFFFF
     
        f.close() 
        returnedhash =  "%016x" % hash
        return returnedhash

    def downloadFile(self, url, filename):
        ''' Downloads the given url to the given filename '''
        content = self.downloadContent(url)
        dump = open(filename, "wb")
        dump.write(content)
        dump.close()
        log.debug("Download finished to file %s. Size : %s"%(filename,os.path.getsize(filename)))

    def getLG(self, language):
        ''' Returns the short (two-character) representation of the long language name'''
        try:
            return self.revertlangs[language]
        except KeyError, e:
            log.warn("Ooops, you found a missing language in the config file of %s: %s. Send a bug report to have it added." %(self.__class__.__name__, language))

     
    def guessFileData(self, filename):
        filename = unicode(self.getFileName(filename).lower())
        matches_tvshow = self.tvshowRegex.match(filename)
        if matches_tvshow: # It looks like a tv show
            (tvshow, season, episode, teams) = matches_tvshow.groups()
            tvshow = tvshow.replace(".", " ").strip()
            teams = teams.split('.')
            return {'type' : 'tvshow', 'name' : tvshow.strip(), 'season' : int(season), 'episode' : int(episode), 'teams' : teams}
        else:
            matches_tvshow = self.tvshowRegex2.match(filename)
            if matches_tvshow:
                (tvshow, season, episode, teams) = matches_tvshow.groups()
                tvshow = tvshow.replace(".", " ").strip()
                teams = teams.split('.')
                return {'type' : 'tvshow', 'name' : tvshow.strip(), 'season' : int(season), 'episode' : int(episode), 'teams' : teams}
            else:
                matches_movie = self.movieRegex.match(filename)
                if matches_movie:
                    (movie, year, teams) = matches_movie.groups()
                    teams = teams.split('.')
                    part = None
                    if "cd1" in teams :
                        teams.remove('cd1')
                        part = 1 
                    if "cd2" in teams :
                        teams.remove('cd2')
                        part = 2
                    return {'type' : 'movie', 'name' : movie.strip(), 'year' : year, 'teams' : teams, 'part' : part}
                else:
                    return {'type' : 'unknown', 'name' : filename, 'teams' : [] }

     
    def getLanguage(self, lg):
        ''' Returns the long naming of the language on a two character code '''
        try:
            return self.langs[lg]
        except KeyError, e:
            log.warn("Ooops, you found a missing language in the config file of %s: %s. Send a bug report to have it added." %(self.__class__.__name__, lg))

    def downloadContent(self, url, timeout = None):
        ''' Downloads the given url and returns its contents.'''
        try:
            log.debug("Downloading %s" % url)
            req = urllib2.Request(url, headers={'Referer' : url, 'User-Agent' : USER_AGENT})
            if timeout:
                socket.setdefaulttimeout(timeout)
            f = urllib2.urlopen(req)
            content = f.read()
            f.close()
            return content
        except urllib2.HTTPError, e:
            log.warning("HTTP Error: %s - %s" % (e.code, url))
        except urllib2.URLError, e:
            log.warning("URL Error: %s - %s" % (e.reason, url))

