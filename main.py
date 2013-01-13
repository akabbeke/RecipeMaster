import json
import urllib
import random
import numpy as np

def NumpySearcher(nparray,value):
	#Expects a 1d numpy array, returns index of the first instance of a variable.
	count = 0
	for element in nparray:
		counter += 1
		if element == value:
			return count
	return "Not Found"

def IngredAdder(ingredList,recipList):
	for ingred in recipList:
		print 'LOL'
		#index = NumpySearcher(nparray,value)

def SearchEncoder(url,pref,search):
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


def Showsome(searchfor):
	query = SearchEncoder('','q',searchfor)
	url = 'http://www.recipepuppy.com/api/?%s' % query
	print url
	searchResponse = urllib.urlopen(url)
	searchResults = searchResponse.read()
	results = json.loads(searchResults)
	print results
	results = results['results']
	num = random.randint(0,len(results)-1)
	recipe = results[num]
	print recipe['title']
	print type(recipe['ingredients'])
	print recipe['href']
	#[0]['ingredients']
	#print ingred


Showsome('lunch')
