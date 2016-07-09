from get_cookies import get_cookies
import json,requests
from pprint import pprint

def get_movie_data(location):
	website="https://in.bookmyshow.com/"+location+"/movies" 
	cookies=get_cookies(website)
	url="https://in.bookmyshow.com/serv/getData?cmd=QUICKBOOK&type=MT"
	response=requests.get(url,cookies=cookies)
	response.raise_for_status()
	data=(json.loads(response.text))
	return data

def get_number_of_movies(location):
	movieData=get_movie_data(location)
	return len(movieData['moviesData']['BookMyShow']['arrEvents'])

def get_number_of_child_events(location,i):
	movieData=get_movie_data(location)
	return len(movieData['moviesData']['BookMyShow']['arrEvents'][i]['ChildEvents'])	

def get_movie_list(location):
	data=get_movie_data(location)
	mlist=[]
	nmovies=get_number_of_movies(location)
	for i in range(0,nmovies-1):
		movies={
			'Title': data['moviesData']['BookMyShow']['arrEvents'][i]['EventTitle'],
			'Duration':data['moviesData']['BookMyShow']['arrEvents'][i]['EventGrpDuration'],
			'Genre':data['moviesData']['BookMyShow']['arrEvents'][i]['EventGrpGenre'],
			'Censor':data['moviesData']['BookMyShow']['arrEvents'][i]['EventGrpCensor']	
		}
		movies['id']=i+1
		movies['Extra']=[]
		ch=get_number_of_child_events(location,i)
		if ch>0:
			for j in range(1,ch+1):
				extra={
					'Dimension':data['moviesData']['BookMyShow']['arrEvents'][i]['ChildEvents'][j-1]['EventDimension'],
					'Language':data['moviesData']['BookMyShow']['arrEvents'][i]['ChildEvents'][j-1]['EventLanguage'],
					'isNew':data['moviesData']['BookMyShow']['arrEvents'][i]['ChildEvents'][j-1]['isNewEvent']
				}
				movies['Extra'].append(extra)

		mlist.append(movies)
	return mlist

def get_rating():
	"""Implement RottenTomatoes api for ratings of movies"""
	pass

if __name__ == '__main__':
	location="kota"
	website="https://in.bookmyshow.com/"+location+"/movies"
	print get_number_of_movies(location)
	print get_number_of_child_events(location,0)
	pprint(get_movie_list(location))