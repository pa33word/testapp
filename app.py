import os
import psycopg2
from bottle import route, run

@route("/")
def hello_world():
        return "Hello World! TESTING push"
@route("/test")
def test_db():
	con = None
	con = psycopg2.connect(database='dd593v8qlv784t', user='wovsovccagcayo') 
	cur = con.cursor()
	cur.execute('SELECT * FROM usertestx;') 
	rows = cur.fetchall()	
        #return "Hello World! TESTING push"
	output = template('make_table', rows=result)
	return output

run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
