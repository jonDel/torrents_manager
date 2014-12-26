import ConfigParser

class ConfigOptions():
	def __init__(self, configFile):
		self.Config = ConfigParser.ConfigParser()
		self.Config.optionxform = str
		self.Config.read(configFile)
		self.configFile = configFile

	def ConfigSectionMap(self, section):
		optionsDict = {}
		options = self.Config.options(section)
		for option in options:
			try:
				optionsDict[option] = self.Config.get(section, option)
				if optionsDict[option] == -1:
					print("Skip: %s with value = -1" % option)
			except:
				print ("Exception on option %s!" % option)
				optionsDict[option] = None
		return optionsDict

	def ConfigSetOption(self, section, option, value):
		self.Config.set(section,option,value)
		self.Config.write(self.configFile)
		
		
