#!/usr/bin/python
#coding: utf-8
import subprocess, smtplib, email.utils, re, os
from email.mime.text import MIMEText
from datetime import datetime
import base64
from loggers import loggers

class userUtils(loggers):
	'''
	Descrição: fornece métodos úteis em geral
	'''
	def __init__(self):
		super(userUtils, self).__init__('userUtils')

	def sendMail(self,mailFrom,mailTo,subject,body,mailServer,serverVerbose=False):
		'''
		Descrição: envia email utilizando um servidor de smtp
		Parâmetros:
			mailfrom:      usuário que enviará o email
			mailto:        usuário para o qual será enviado o email
			subject:       campo assunto do email
			body:          corpo do email
			mailServer:    servidor de smtp  
			serverVerbose: se True, habilita log de comunicação com o servidor (default:False)
			logLevel: nível de log ('NOTSET','DEBUG','INFO' 'WARNING', 'ERROR', 'CRITICAL')
		'''
		start = datetime.now().strftime("%Y%m%d.%H%M%S")
		msg = MIMEText(body, 'plain', 'UTF-8')
		msg['To'] = email.utils.formataddr(('Recipient', mailTo ))
		msg['From'] = email.utils.formataddr(('Author', mailFrom ))
		msg['Subject'] = subject
		msg['message-id']= '<%s@'+mailServer+'.TODO.com.br>' % start
		mailto = mailTo.split(',')
		server = smtplib.SMTP(mailServer)
		if serverVerbose:
			server.set_debuglevel(True)
		try:
			server.sendmail(mailFrom, mailto, msg.as_string())
		except:
			self.log.error('Não foi possível enviar email para o destinatário '+mailTo)
		finally:
			server.quit()

	@staticmethod
	def getStdoutFromShellCmd(shellCmdList):
		'''
		Descrição: executa um comando no shell e retorna a saída padrão
		Parâmetros:
			shellCmdList: uma lista contendo cada um dos parametros de chamada do comando shell
		Retorno:
			proc.stdout.read(): a saída padrão do comando executado
		'''
		proc = subprocess.Popen(shellCmdList, stdout=subprocess.PIPE)
		proc.wait()
		return proc.stdout.read()

	@staticmethod
	def checkStringInFile(string,filePath):
		'''
		Descrição: busca a ocorrência de uma string em um arquivo
		Parâmetros:
			string: string desejada
			filePath: caminho do arquivo a ser pesquisado
		Retorno:
			True se existir a string no arquivo, False caso contrário
		'''
		with open(filePath, 'r') as f:
			fileData = f.read()
		if re.search(string,fileData) != None:
			return True
		else:
			return False

	@staticmethod
	def getFilesNames(dirPath, recursive=True, flag=''):
		'''
		Descrição: efetua uma busca pelo caminho completo de arquivos em diretórios
		Parâmetros:
			dirPath: caminho do diretório a ser buscado
			recursive: se True, faz uma busca recursiva nas subpastas da pasta (default: True)
			flag: se não for vazia, retorna apenas os arquivos com essa terminação(default: '')
		Retorno:
			filesList: lista com o caminho completo dos arquivos no diretório
		'''
		if recursive:
			filesList = [os.path.join(dirAbsPath, f) for dirAbsPath, dn, filenames in os.walk(dirPath) for f in filenames if f.endswith(flag)]
		else:
			filesList =[os.path.join(dirPath, fileName) for fileName in os.listdir(dirPath) if fileName.endswith(flag) if os.path.isfile(os.path.join(dirPath,fileName))]
		return filesList

	@staticmethod
	def replaceStringInFile(strToReplace, strToBeReplaced,filePath):
		'''
		Descrição: busca as ocorrências de uma string em um arquivo e as subsitui por outra string
		Parâmetros:
			strToBeReplaced: string a ser substituída
			strToReplace:    string que substituirá as ocorrências da string acima
		'''
		with open(filePath, 'r+b') as f:
			fileData = f.read()
		fileData = fileData.replace(strToBeReplaced, strToReplace)
		with open(filePath, 'w+b') as f:
			f.write(fileData)

	@staticmethod
	def getFuncParam(funcObj):
		'''
		Descrição: busca os parâmetros de uma determinada função
		Parâmetros:
			funcObj: objeto da função
		Retorno:
			paramList: lista com parâmetros da função passada
		'''
		paramList = []
		for argument in range(0,funcObj.func_code.co_argcount):
			if funcObj.func_code.co_varnames[argument] != 'self':
				paramList.append(funcObj.func_code.co_varnames[argument])
		return paramList

	@staticmethod
	def encriptFileField(fieldValue, field, separator, confFile):
		'''
		Descrição: encripta o valor de um campo e o insere/substitui em um campo em um arquivo
		Parâmetros:
			fieldValue: valor do campo a ser encriptado
			field: campo correspondente ao valor (ex: senhaUsuario=senha)
			separator: separador entre campo e o valor (no exemplo na linha acima seria o "=") - pode ser ' ',
				'=' ou ':'
			confFile: arquivo onde será gravado o campo e a senha
		'''
		newFieldValue = field+separator+base64.b64encode(fieldValue)
		with open (confFile, 'r') as confObj:
			confData = confObj.read()
		try:
			passLine = re.search('(^'+field+'?\s*(:|=| )\s*?.*?)$',confData, re.M).group(0)
			confData = confData.replace(passLine, newFieldValue)
		except:
			confData = confData+'\n'+newFieldValue
		with open (confFile, 'w') as confObj:
			confObj.write(confData)

	@staticmethod
	def getFieldValue(field, confFile, encrypted=False):
		'''
		Descrição: desencripta uma senha relativa a um campo em um arquivo
		Parâmetros:
			field: campo correspondente à senha (ex: senhaUsuario=senha)
			confFile: arquivo onde será gravado o campo e a senha
		Retorno:
			passwd: senha desencriptada
			separator: separador entre campo e senha (ex: em "campo=senha" o separador seria "=")
		'''
		with open (confFile, 'r') as confObj:
			confData = confObj.read()
		try:
			match = re.search('^'+field+'\s*(:|=| )\s*(.+)$',confData, re.M)
			fieldValue = match.group(2)
			separator = match.group(1)
		except:
			return 'Campo '+field+' não foi encontrado no arquivo '+confFile
		if encrypted:
			fieldValue = base64.b64decode(fieldValue)
		return fieldValue, separator


