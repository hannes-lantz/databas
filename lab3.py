from bottle import route, run, response, get, request, post
import sqlite3, json 

db = sqlite3.connect('movies.sqlite')
cursor = db.cursor()

def imdb_nbr_exist(imdb_nbr):
	c = get_movie_by_nbr(imdb_nbr)
	return c.fetchone() is not None


def theater_exist(name):
	cursor.execute(
		"""
		SELECT t_name
		FROM   theaters
		WHERE  t_name = ?
		""",
		[name]
	)
	return cursor.fetchone() is not None

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

@get('/performances')
def get_performances():
	cursor.execute(
		"""
		SELECT performance_nbr, start_date, start_time, imdb_nbr, t_name 
		FROM   performances
		"""
	)
	s = [{"performance_nbr": performance_nbr, "start_date": start_date, "start_time": start_time, "imdb_nbr": imdb_nbr, "t_name": t_name}
		for (performance_nbr, start_date, start_time, imdb_nbr, t_name) in cursor]
	return response({"data": s})

@post('/performances')
def add_performance():
	query =	"""
		INSERT
		INTO performances(imdb_nbr, t_name, start_date, start_time)
		VALUES (?,?,?,?)
		"""
	p = []
	if request.query.imdb_nbr and request.query.t_name and request.query.start_date and request.query.start_time:
		if imdb_nbr_exist(request.query.imdb_nbr) and theater_exist(request.query.t_name):
			p.append(request.query.imdb_nbr)
			p.append(request.query.t_name)
			p.append(request.query.start_date)
			p.append(request.query.start_time)
		else:
			response.status = 400
			return "No such movie or theater"
	else:
		response.status = 400
		return "Missing parameter"

	cursor.execute(query, p)
	db.commit()
	cursor.execute(
        """
        SELECT   performance_nbr
        FROM     performances
        
        """
    )
	performance_nbr = cursor.fetchone()[0]
	response.status = 200
	return "/performances/%s" % (performance_nbr)


run(host='localhost', port=7007, debug=True)