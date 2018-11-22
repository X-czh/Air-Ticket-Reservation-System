from air_ticket import app

"""
Run the app on localhost port 5000
debug = True -> you don't have to restart flask
for changes to go through, TURN OFF FOR PRODUCTION
"""
app.run('127.0.0.1', 5000, debug = True)
