import json
import time
import urllib
import random
import numpy as np
import smtplib
import imaplib
import email
import base64
from email.MIMEMultipart import MIMEMultipart
from email.Utils import COMMASPACE
from email.MIMEText import MIMEText

def BodyBuilder(recipeNames,recipeURL,ingredlist):
	#Feel the burn. Also builds the email body.
	weekDay = ('Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday')
	body = 'Recipes for this week are: \n \n'
	for count in range(len(recipeNames)):
		body += (weekDay[count%7] + ':\n' + recipeNames[count] + '\n' + recipeURL[count] + '\n \n')
	body += 'Ingedients List: \n \n'
	for count in range(np.shape(ingredlist)[0]-1):
		body += (ingredlist[count+1,0] + ' ' + ingredlist[count+1,1] + '\n')
	body += '\nEnjoy!'
	
	return body
	
def SendMail(person,user,server,body):
	fromaddr = 'velocity.recipe.master@gmail.com'
	tolist = person
	localtime = time.asctime( time.localtime(time.time()) )
	sub = 'Your recipes for '+ localtime
	msg = email.MIMEMultipart.MIMEMultipart()
	msg['From'] = fromaddr
	msg['To'] = tolist
	msg['Subject'] = sub
	msg.attach(MIMEText(body, 'plain'))
	n=42
	server.sendmail(user,tolist,msg.as_string())
	return

def NumpySearcher(nparray,value):
	#Expects a 1d numpy array, returns index of the first instance of a variable.
	count = 0
	for element in nparray[:,0]:
		if element == value:
			return count
		count += 1
	return False

def IsNotInList(L,value):
	try:
		L.index(value)
		return False
	except ValueError:
		return True

def IngredAdder(ingredList,recipList):
	for ingred in recipList:
		index = NumpySearcher(ingredList,ingred)
		if type(index) == int:
			ingredList[index][1] = str(int(ingredList[index][1])+1)
		else:
			foo = np.array(((ingred,1),))
			ingredList = np.append(ingredList,foo,axis = 0)
	return ingredList

def QueryEncoder(url,pref,search):
	if(isinstance(search,list)):
		if url != '':
			url += '&'
		counter = 1
		url += pref + '='
		for item in search:
			url += item
			if counter < len(search):
				url += ','
			counter += 1 
	else:
		url += pref + '=' + search
	return url


def ShowSome(name = '',ingred = ''):
	query = ''
	if name != '':
		query = QueryEncoder(query,'q',name)
	if ingred != '':
		query = QueryEncoder(query,'i',ingred)
	url = 'http://www.recipepuppy.com/api/?%s' % query
	searchResponse = urllib.urlopen(url)
	searchResults = searchResponse.read()
	results = json.loads(searchResults)
	results = results['results']
	num = random.randint(0,len(results)-1)
	recipe = results[num]
	return recipe
	
def RecipeSearch():
	kwargList = ("beef","chicken","fish","vegitarian","egg","curry","pasta","french","burger","steak","pork","rice")
	#kwargList = ("vegetarian",)
	ingredList = np.array((('',0),))
	recipeNames = []
	recipeURL = []
	for count in range(7):
		isRepeat = True
		count = 0
		while isRepeat:
			index = random.randint(0,len(kwargList)-1)
			recipe = ShowSome(kwargList[index])
			count += 1
			if IsNotInList(recipeNames,recipe['title']):
				recipeNames += [recipe['title']]
				recipeURL += [recipe['href']]
				ingredList = IngredAdder(ingredList,recipe['ingredients'].split(', '))
				isRepeat = False
			if count > 10:
				isRepeat = False
	body = BodyBuilder(recipeNames,recipeURL,ingredList[ingredList[:,0].argsort()])
	return body
		
def main():
	emailList = ('gkabbeke@telus.net','akabbeke@gmail.com','jakek.nielsen@gmail.com')
	
	user = 'velocity.recipe.master@gmail.com'
	passw = base64.b64encode('thisisthepassword')
	smtp_host = 'smtp.gmail.com'
	smtp_port = 587
	server = smtplib.SMTP()
	server.connect(smtp_host,smtp_port)
	server.ehlo()
	server.starttls()
	server.login(user,base64.b64decode(passw))
	imap_host = 'imap.gmail.com'
	mail = imaplib.IMAP4_SSL(imap_host)
	mail.login(user,base64.b64decode(passw))
	for person in emailList:
		print person
		body = RecipeSearch()
		print body
		SendMail(person,user,server,body)
		print 'Sent mail to '+person
	return

if __name__ == "__main__":
	main()
	