from bottle import route, run, response, get, request, post
import sqlite3, json 

db = sqlite3.connect('movies.sqlite')
cursor = db.cursor()

def imdb_nbr_exist(imdb_nbr):
	c = get_by_imdb_nbr(imdb_nbr)
	return c.fetchone() is not None

def username_exist(username):
	cursor.execute(
		"""
		SELECT username
		FROM   customers
		WHERE  username = ?
		""",
		[username]
	)
	return cursor.fetchone() is not None

def performance_exist(performance_nbr):
	cursor.execute(
		"""
		SELECT performance_nbr
		FROM   performances
		WHERE  performance_nbr = ?
		""",
		[performance_nbr]
	)
	return cursor.fetchone() is not None


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

def tickets_left(performance_nbr):
	cursor.execute(
		"""
		SELECT (capacity - count(id))
		FROM   performances
		JOIN   theaters
		USING  (t_name)
		LEFT JOIN tickets
		USING  (performance_nbr)
		WHERE  performance_nbr = ?
		""",
		[performance_nbr]
	)
	return cursor.fetchone()[0]

def check_password(username, password):
	cursor.execute(
		"""
		SELECT password
		FROM   customers
		WHERE  username = ?
		""",
		[username]
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
	return "pong"


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
		p.append(request.query.year)
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

@post('/reset')
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
		SELECT performance_nbr, start_date, start_time, title, p_year, t_name, (capacity - count(id)) AS remaining_seats
		FROM   performances
		JOIN   movies
		USING  (imdb_nbr)
		JOIN   theaters
		USING  (t_name)
		LEFT JOIN tickets
		USING  (performance_nbr)
		GROUP BY performance_nbr		
		"""
	)
	s = [{"performance_nbr": performance_nbr, "start_date": start_date, "start_time": start_time, "imdb_nbr": imdb_nbr, "t_name": t_name, "reminingSeats": reminingSeats}
		for (performance_nbr, start_date, start_time, imdb_nbr, t_name, reminingSeats) in cursor]
	return response({"data": s})

@post('/performances')
def add_performance():
	query =	"""
		INSERT
		INTO performances(imdb_nbr, t_name, start_date, start_time)
		VALUES (?,?,?,?)
		"""
	p = []
	if request.query.imdb and request.query.theater and request.query.date and request.query.time:
		if imdb_nbr_exist(request.query.imdb) and theater_exist(request.query.theater):
			p.append(request.query.imdb)
			p.append(request.query.theater)
			p.append(request.query.date)
			p.append(request.query.time)

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

@post('/tickets')
def post_tickets():
	p = []
	if not (request.query.user and request.query.performance and request.query.pwd):
		response.status = 400
		return "Missing parameter"
	elif not (performance_exist(request.query.performance) and username_exist(request.query.user)):
		response.status = 400
		return "No such performance or user"
	elif not check_password(request.query.user, request.query.pwd):
		response.status = 401
		return "Wrong password"
	elif not tickets_left(request.query.performance):
		response.status = 403
		return "No tickets left"
	else:
		p.append(request.query.performance)
		p.append(request.query.user)
	
	
	query =	"""
		INSERT
		INTO tickets(performance_nbr, username)
		VALUES (?, ?);
		"""
	cursor.execute(
		query,
		p
	)
	db.commit()
	cursor.execute(
        """
        SELECT   id
        FROM     tickets
        WHERE    rowid = last_insert_rowid()
        """
    )
	id = cursor.fetchone()[0]
	response.status = 200
	return "/tickets/%s" % (id)

@get('/customers/<username>/tickets')
def get_tickets(username):
	print(username)
	cursor.execute(
		"""
		SELECT start_date, start_time, t_name, title, p_year, count() AS nbr_of_tickets
		FROM   tickets
		JOIN   performances
		USING  (performance_nbr)
		JOIN   movies
		USING  (imdb_nbr)
		WHERE username = ?
		""",
		[username]
	)
	s = [{"date": start_date, "startTime": start_time, "theater" : t_name, "title" : title, "year" : p_year, "nbrOfTickets" : nbr_of_tickets}
		for (start_date, start_time, t_name, title, p_year, nbr_of_tickets) in cursor]
	return response({"data": s})



run(host='localhost', port=7007, debug=True)