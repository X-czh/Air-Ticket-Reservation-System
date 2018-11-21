#Import Flask Library
from flask import Flask, render_template, request, session, url_for, redirect
import pymysql.cursors

#Initialize the app from Flask
app = Flask(__name__)

#Configure MySQL
conn = pymysql.connect(host='localhost',
                       user='root',
                       password='password',
                       db='air_ticket',
                       charset='utf8mb4',
                       cursorclass=pymysql.cursors.DictCursor)

#Define a route to hello function
@app.route('/')
def hello():
	return render_template('index.html')

@app.route('/upcoming', methods=['GET', 'POST'])
def checkUpcoming():
	#grabs information from the forms
	departure_airport = request.form['departure_airport']
	departure_date = request.form['departure_date']
	arrival_airport = request.form['arrival_airport']
	arrival_date = request.form['arrival_date']

	#cursor used to send queries
	cursor = conn.cursor()
	#executes query
	query = 'SELECT * FROM flight WHERE departure_airport = %s AND DATE(departure_time) = %s \
		arrival_airport = %s AND DATE(arrival_time) = %s'
	print(query)
	cursor.execute(query, (departure_airport, departure_date, arrival_airport, arrival_date))
	#stores the results in a variable
	data = cursor.fetchall()
	error = None
	if data:
		return render_template('index.html', result = data)
	else:
		return render_template('index.html', error = error) 

@app.route('/status', methods=['GET', 'POST'])
def checkStatus():
	#grabs information from the forms
	flight_num = request.form['flight_num']
	departure_date = request.form['departure_date']
	arrival_date = request.form['arrival_date']

	#cursor used to send queries
	cursor = conn.cursor()
	#executes query
	query = 'SELECT status FROM flight WHERE flight_num = %s AND \
		DATE(departure_time) = %s AND DATE(arrival_time) = %s'
	cursor.execute(query, (flight_num, departure_date, arrival_date))
	#stores the results in a variable
	data = cursor.one()
	#use fetchall() if you are expecting more than 1 data row
	error = None
	if data:
		#If the previous query returns data, then user exists
		error = 'This user already exists'
		return render_template('register.html', error = error)

#Define route for login
@app.route('/login')
def login():
	return render_template('login.html')

#Define route for register
@app.route('/register')
def register():
	return render_template('register.html')

#Authenticates the login
@app.route('/loginAuth', methods=['GET', 'POST'])
def loginAuth():
	#grabs information from the forms
	usertype = request.form['usertype']
	username = request.form['username']
	password = request.form['password']

	#cursor used to send queries
	cursor = conn.cursor()
	#executes query
	attr_username = 'username' if usertype == 'airline_staff' else 'email'
	query = 'SELECT * FROM {} WHERE {} = %s and password = %s'.format(usertype, attr_username)
	cursor.execute(query, (username, password))
	#stores the results in a variable
	data = cursor.fetchone()
	#use fetchall() if you are expecting more than 1 data row
	cursor.close()
	error = None
	if data:
		#creates a session for the the user
		#session is a built in
		session['username'] = username
		return render_template('index.html')
	else:
		#returns an error message to the html page
		error = 'Invalid login or username'
		return render_template('login.html', error=error)

#Authenticates the register
@app.route('/registerAuth', methods=['GET', 'POST'])
def registerAuth():
	#grabs usertype
	usertype = request.form['usertype']
	print(usertype)
	if usertype == 'customer':
		#grabs information from the forms
		email = request.form['email']
		password = request.form['password']
		name = request.form['name']
		passport_expiration = request.form['passport_expiration']
		passport_country = request.form['passport_country']
		#cursor used to send queries
		cursor = conn.cursor()
		#executes query
		attr_username = 'email'
		query = 'SELECT * FROM {} WHERE {} = %s'.format(usertype, attr_username)
		cursor.execute(query, (email))
		#stores the results in a variable
		data = cursor.fetchone()
		#use fetchall() if you are expecting more than 1 data row
		error = None
		if data:
			#If the previous query returns data, then user exists
			error = 'This user already exists'
			return render_template('register.html', error = error)
		else:
			ins = 'INSERT INTO user VALUES(%s, %s)'
			cursor.execute(ins, (email, password))
			conn.commit()
			cursor.close()
			return render_template('index.html')
	elif usertype == 'booking_agent':
		#grabs information from the forms
		email = request.form['email']
		password = request.form['password']
		booking_agent_id = request.form['booking_agent_id']

		#cursor used to send queries
		cursor = conn.cursor()
		#executes query
		attr_username = 'email'
		query = 'SELECT * FROM {} WHERE {} = %s'.format(usertype, attr_username)
		print(query)
		cursor.execute(query, (email))
		#stores the results in a variable
		data = cursor.fetchone()
		#use fetchall() if you are expecting more than 1 data row
		error = None
		if data:
			#If the previous query returns data, then user exists
			error = 'This user already exists'
			return render_template('register.html', error = error)
		else:
			ins = 'INSERT INTO {} VALUES(%s, %s, %s)'.format(usertype)
			cursor.execute(ins, (email, password, booking_agent_id))
			conn.commit()
			cursor.close()
			return render_template('index.html')
	else:
		#if usertype is airline staff
		pass

@app.route('/home')
def home():
    
    username = session['username']
    cursor = conn.cursor()
    query = 'SELECT ts, blog_post FROM blog WHERE username = %s ORDER BY ts DESC'
    cursor.execute(query, (username))
    data1 = cursor.fetchall() 
    for each in data1:
        print(each['blog_post'])
    cursor.close()
    return render_template('home.html', username=username, posts=data1)

@app.route('/post', methods=['GET', 'POST'])
def post():
	username = session['username']
	cursor = conn.cursor()
	blog = request.form['blog']
	query = 'INSERT INTO blog (blog_post, username) VALUES(%s, %s)'
	cursor.execute(query, (blog, username))
	conn.commit()
	cursor.close()
	return redirect(url_for('home'))

@app.route('/logout')
def logout():
	session.pop('username')
	return redirect('/')

app.secret_key = 'some key that you will never guess'
#Run the app on localhost port 5000
#debug = True -> you don't have to restart flask
#for changes to go through, TURN OFF FOR PRODUCTION
if __name__ == "__main__":
	app.run('127.0.0.1', 5000, debug = True)
