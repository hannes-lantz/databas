from bottle import route, run, response, get, request
import sqlite3, json 

db = sqlite3.connect('movies.sqlite')
cursor = db.cursor()

@route('/ping')
def ping():
	response.status = 200
	return "Pong"

@route('/movies', method = 'GET')
@route('movies/')
def get_movies():
	title = request.query.['name']
	year = request.query.['year']
	with db: 
		if len(title) != 0:
			cursor.execute("SELECT * FROM movies WHERE tile = % AND year = %" (title, year))
		else: 
			cursor.execute("SELECT imdb_nbr, title, p_year FROM movies")
		s = [{"imdbKey": imdb_nbr, "title": title, "year": p_year}
			for (imdb_nbr, title, p_year) in cursor]
		return json.dumps({"data": s}, indent=3)


@route('/reset')
def reset():
	with open('reset.sql', 'r') as sql_reset:
	    sql_script = sql_reset.read()

	cursor.executescript(sql_script)
	db.commit()
	response.status = 200 
	return "OK"

run(host='localhost', port=7007, debug=True)