#!/usr/bin/python
# -*- coding: utf-8 -*-
import logging,logging.handlers, os,sys

class loggers(object):
	'''
		Descrição: fornece funcionalidades de log em stream e em arquivos
		Parâmetros:
			logName: nome do handler de log
			logFolderPath: pasta onde serão gravados os arquivos de log (default= False)
	'''
	def __init__(self, logName, logFolderPath=False):
		# Configurando os logs de erro
		self.log = logging.getLogger(logName)
		self.default_formatter = logging.Formatter('Log: %(message)s | Nível de Log:%(levelname)s | Data:%(asctime)s',datefmt='%m/%d/%Y %I:%M:%S')
		# Apenas adicionamos um novo handler de stream se já não existir um
		if not len(self.log.handlers):
			self.default_formatter = logging.Formatter('Log: %(message)s | Nível de Log:%(levelname)s | Data:%(asctime)s',datefmt='%m/%d/%Y %I:%M:%S')
			self.stream_handler = logging.StreamHandler(sys.stdout)
			self.stream_handler.setLevel(logging.DEBUG)
			self.stream_handler.setFormatter(self.default_formatter)
			self.log.addHandler(self.stream_handler)
		if logFolderPath != False:
			# Arquivo de log é gerado compactado
			self.errorLogfile = logFolderPath+"/"+logName+".error.log.bz2"
			self.debugLogfile = logFolderPath+"/"+logName+".debug.log.bz2"
			if not os.path.isdir(logFolderPath):
				try:
					os.mkdir(logFolderPath)
				except:
					print 'Não foi possível criar a pasta de log em '+logFolderPath+'. Criar manualmente e setar as permissões necessárias.'
					print 'Caso contrário, os arquivos de log '+self.errorLogfile+' e '+self.debugLogfile+' não serão criados e logados.' 
			else:
				try:
					self.debug_handler = logging.handlers.RotatingFileHandler(self.debugLogfile,maxBytes=600000,encoding='bz2-codec',backupCount=4)
					self.error_handler = logging.handlers.RotatingFileHandler(self.errorLogfile,maxBytes=600000,encoding='bz2-codec',backupCount=4)
					self.debug_handler.setLevel(logging.DEBUG)
					self.debug_handler.setFormatter(self.default_formatter)
					self.error_handler.setLevel(logging.ERROR)
					self.error_handler.setFormatter(self.default_formatter)
				except:
					print 'Não foi possível criar os arquivos de log na pasta '+logFolderPath+'. Setar as permissões necessárias para esta pasta.'

	def setLogRotateHandler(self,setFile):
		'''
		Descrição: habilita/desabilita o registro de logs em arquivos
		Parâmetros:
			setFile: False desabilita, True habilita
		'''
		if hasattr(self, 'debug_handler'):
			if setFile:
				self.log.addHandler(self.debug_handler)
				self.log.addHandler(self.error_handler)
			else:
				# Não trato exceção no caso de ainda não ter sido adicionados os handlers
				try:
					self.log.removeHandler(self.error_handler)
					self.log.removeHandler(self.debug_handler)
				except:
					pass
		else:
			self.log.debug('Os handlers de log em arquivo não foram criados. Não há como habilitar log em arquivos.')

	def setLogLevel(self,logLevel):
		'''
		Descrição: configura o nível de log da classe
		Parâmetros:
			logLevel: nível de log ('NOTSET','DEBUG','INFO' 'WARNING', 'ERROR', 'CRITICAL')
		'''
		exec "self.log.setLevel(logging."+logLevel+")"
		exec "self.log."+logLevel.lower()+"('Mudando log level para "+logLevel+"')"

	def setLogFormat(self, logType, logFormat):
		'''
		Descrição: configura o formato do log
		Parâmetros:
			logType: tipo do log(error, debug ou stream)
			logFormat: formato desejado para o log (ex:"Log: %(message)s | Nível de Log:%(levelname)s | Data:%(asctime)s',datefmt='%m/%d/%Y %I:%M:%S")
		'''
		if not (logType == 'error' or logType == 'stream' or logType == 'debug'):
			self.log.debug('Tipo de log deve ser error, stream, ou debug')
		else:
			exec "self.default_formatter = logging.Formatter('"+logFormat+"')"
			exec "self."+logType+"_handler.setFormatter(self.default_formatter)"


