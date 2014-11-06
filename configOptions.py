import ConfigParser,logging, sys

class ConfigOptions():
	def __init__(self, configFile):
		self.Config = ConfigParser.ConfigParser()
		self.Config.optionxform = str
		self.Config.read(configFile)
		self.configFile = configFile
		self.logger = logging.getLogger(__name__)
		self.default_formatter = logging.Formatter('Log: %(message)s | Log level:%(levelname)s | Date:%(asctime)s',datefmt='%m/%d/%Y %I:%M:%S')
		stream_handler = logging.StreamHandler(sys.stdout)
		stream_handler.setLevel(logging.ERROR)
		stream_handler.setFormatter(self.default_formatter)
		self.logger.addHandler(stream_handler)

	def ConfigSectionMap(self, section):
		optionsDict = {}
		options = self.Config.options(section)
		for option in options:
			try:
				optionsDict[option] = self.Config.get(section, option)
				if optionsDict[option] == -1:
					self.logger.debug("Skip: %s with value = -1" % option)
			except:
				self.logger.error("Exception on option %s!" % option)
				optionsDict[option] = None
		return optionsDict

	def ConfigSetOption(self, section, option, value):
		self.Config.set(section,option,value)
		self.Config.write(self.configFile)
		
		
