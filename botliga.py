import httplib

class Poster:

	token = False
	def toBotliga(self,mid, goal1, goal2):
		if(Poster.token):
			path = "/api/guess?match_id={mid}&result={goal1}:{goal2}&token={token}".format(mid=mid,token=Poster.token,goal1=goal1,goal2=goal2)
			con = httplib.HTTPConnection("botliga.de")
			con.request("POST", path)
			print con.getresponse().read();

	

class Reader:
	
	s2010 = "http://botliga.de/api/matches/2010"
	s2011 = "http://botliga.de/api/matches/2011"

	def read(self,url):
		import urllib
		r = urllib.urlopen(url)
		jsonraw = str(r.read())
		import json
		ob = json.loads(jsonraw)
		return ob


