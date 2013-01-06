import os
import psycopg2
from bottle import route, run, template

@route("/")
def hello_world():
        return "Hello World! TESTING push"

@route("/test")
def test_db():
	con = None
	con = psycopg2.connect(dbname="dd593v8qlv784t", host="ec2-54-243-217-241.compute-1.amazonaws.com", port="5432", user="wovsovccagcayo", password="ar47Vr0fsg86Hi_IwNcqLMcFSU")
	
#con = psycopg2.connect(database='mytestedb', user='postgres') 
	cur = con.cursor()
	cur.execute('SELECT * FROM usertestx;') 
	result = cur.fetchall()	
        #return "Hello World! TESTING push"
	output = template('make_table', rows=result)
	return output

run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
