import json
import urllib
import random
import numpy as np

def NumpySearcher(nparray,value):
	#Expects a 1d numpy array, returns index of the first instance of a variable.
	count = 0
	for element in nparray[:,0]:
		if element == value:
			return count
		count += 1
	return "Not Found"

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


def Showsome(name = '',ingred = ''):
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

kwargList = ("beef","chicken","fish","vegitarian","egg","curry","pasta","french","burger","steak","pork","rice")
ingredList = np.array((('',0),))
for count in range(7):
	index = random.randint(0,len(kwargList)-1)
	recipe = Showsome(kwargList[index])
	print recipe['title']
	print recipe['href']
	print "/n"
	ingredList = IngredAdder(ingredList,recipe['ingredients'].split(', '))
print ingredList

	