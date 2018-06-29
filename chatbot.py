import requests
import json
import aiml
import sqlite3 as sq
import webbrowser


conn = sq.connect("conv.db")
sql='create table if not exists '+'conversation'+'(id INT,user TEXT,bot TEXT)'
conn.execute(sql)
conn.commit()
cursor=conn.execute('SELECT id from conversation')
id=0;
for items in cursor:
	id=items[0]
id=id+1
def insert(u,b):
	conn.execute("INSERT INTO conversation (id,user,bot) VALUES (?,?,?) ",(id,u,b))
	conn.commit()
def location():
	send_url='http://freegeoip.net/json'
	r=requests.get(send_url)
	try:
		j=json.loads(r.text)
		s=str(j['city'])
		return s
	except ValueError:
		return 'Could not connect to internet'#internet error
def weather():
	send_url='http://api.openweathermap.org/data/2.5/weather?q='+location()+'&APPID=919c4a180d74e61b0dff5716c6fac999'
	r=requests.get(send_url)
	try:
		j=json.loads(r.text)
		try :
			l=j['weather'];
			for items in l:
				a=items['description']
			l=j["main"]
			b=(l['temp'])
			return a,b
		except KeyError:
			return "Error","Too many requests for weather service.Please ask again after a minute"
	except ValueError:
		return "Error","Internet error" 

kernel=aiml.Kernel()
kernel.learn("bot/start.aiml")
kernel.respond("learn ai")


while True:
	u=input(">>>")
	if str(u)[:6]=="google" or str(u)[:6]=="Google":
		url = "https://www.google.com.tr/search?q={}".format(str(u)[6:]);    
		webbrowser.open(url,2)
		insert(str(u),"")
		continue;
	s=kernel.respond(u)
	if s=="API WEATHER":
		desc,temp=weather()
		if desc=="Error":
			print(temp)
			insert(u,temp)
		else :
			print("Current Weather Conditions")
			print("Description:"+desc)
			print("Temperature:"+str(int(float(temp)-273.15)))
			v="Current Weather Conditions.Description:"+str(desc)+".Temperature:"+str(int(float(temp)-273.15))
			insert(u,v)
	elif s=="LOCATION API":
			k=location()
			print(k)
			insert(u,k)
	else :
		s=s.split('newline')
		ch=False
		v=""
		for item in s:
			print(str(item))
			v=v+str(item)
			if 'Bye' in item:
				ch=True
		insert(u,v)
		if ch :
			break
