from bottle import route, run, response, get, request
import sqlite3, json 

db = sqlite3.connect('movies.sqlite')
cursor = db.cursor()

def response(data):
    return json.dumps(data, indent=4) + "\n"

def get_by_imdb_nbr(imdb_nbr):
	c = cursor.execute(
		"""
		SELECT imdb_nbr, title, p_year
		FROM   movies
		WHERE  imdb_nbr = ?
		""",
		[imdb_nbr]
	)
	return c

@route('/ping')
def ping():
	response.status = 200
	return "Pong"


@get('/movies')
def get_movies():
	query =	"""
		SELECT imdb_nbr, title, p_year
		FROM   movies
		WHERE  1=1
		"""
	p = []
	if request.query.title:
		query += "AND title = ?"
		p.append(request.query.title)
	if request.query.p_year:
		query += "AND p_year = ?"
		p.append(request.query.p_year)
	cursor.execute(query, p)
	s = [{"imdb_nbr": imdb_nbr, "title": title, "year": p_year}
		for (imdb_nbr, title, p_year) in cursor]
	return response({"data": s})


@get('/movies/<imdb_nbr>')
def get_movie(imdb_nbr):
	c = get_by_imdb_nbr(imdb_nbr)
	s = [{"imdb_nbr": imdb_nbr, "title": title, "year": p_year}
		for (imdb_nbr, title, p_year) in cursor]
	return response({"data": s})

@route('/reset')
def reset():
	with open('reset.sql', 'r') as sql_reset:
	    sql_script = sql_reset.read()

	cursor.executescript(sql_script)
	db.commit()
	response.status = 200 
	return "OK"

run(host='localhost', port=7007, debug=True)