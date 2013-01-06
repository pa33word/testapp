import os
import psycopg2
from bottle import route, run, template
## NEED below for encryption
from Crypto.Cipher import AES
from base64 import b64encode, b64decode
from datetime import datetime
from re import sub
import json


class aestest:
	'Optional class documentation string'
	BLOCK_SIZE = 32
	INTERRUPT = u'\u0001'
	PAD = u'\u0000'
	
	def __init__(self):
		xx = u'12345678abcdeggh'

	def EncryptWithAES(self, encrypt_cipher, plaintext_data):
		def AddPadding(data, interrupt, pad, block_size):
			new_data = ''.join([data, interrupt])
			new_data_len = len(new_data)
			remaining_len = block_size - new_data_len
			to_pad_len = remaining_len % block_size
			pad_string = pad * to_pad_len
			return ''.join([new_data, pad_string])
		plaintext_padded = AddPadding(plaintext_data, aestest.INTERRUPT, aestest.PAD, aestest.BLOCK_SIZE)
		encrypted = encrypt_cipher.encrypt(plaintext_padded)
		return b64encode(encrypted)
	def DecryptWithAES(self, decrypt_cipher, encrypted_data):
		def StripPadding(data, interrupt, pad):
			return data.rstrip(pad).rstrip(interrupt)
		decoded_encrypted_data = b64decode(encrypted_data)
		decrypted_data = decrypt_cipher.decrypt(decoded_encrypted_data)
		return StripPadding(decrypted_data, aestest.INTERRUPT, aestest.PAD)

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

@get('/addentry') # or @route('/login')
def addentry_form():
    return '''<form method="POST" action="/addentry">
        <label for="name">Name: <span class="required">*</span></label>
	<p> </p>  
       <input name="name"   placeholder="Name of Entry"  type="text" />
                <input name="url" placeholder="Site URL" type="text" />
				
       <input name="user"   placeholder="username"  type="text" />
                <input name="password" placeholder="password" type="password" />
                <input type="submit" name="submit" />
              </form>'''

@post('/addentry') # or @route('/login', method='POST')
def addentry_submit():
	name     = request.forms.get('name')
	url     = request.forms.get('url')
	user     = request.forms.get('user')
	pre = request.forms.get('password')
	encrypted_data = EncryptWithAES(cipher_for_encryption, pre)	
						#post_passwd = pre.encode('base64','strict')
						#decrypt = post_passwd.decode('base64','strict')	
	decrypted_data = DecryptWithAES(cipher_for_decryption, encrypted_data)
	
	return {'Entry: %s == THe username is: %s & the Password is : %s Decrypted: %s & of URL: %s' % (name,user,encrypted_data,decrypted_data,url)}
	
@post('/addjson') # or @route('/login', method='POST')
def addentry_submit():
#	name = json.dumps(request.json)
	name     = request.json.get('name')
	url     = request.json.get('url')
	user     = request.json.get('user')
	pre = request.json.get('password')
	encrypted_data = EncryptWithAES(cipher_for_encryption, pre)	
						#post_passwd = pre.encode('base64','strict')
						#decrypt = post_passwd.decode('base64','strict')	
	decrypted_data = DecryptWithAES(cipher_for_decryption, encrypted_data)
#	return json.dumps(request.json)	
#	return "th recieved data is: %s \n" % name

	return {'Entry: %s == THe username is: %s & the Password is : %s Decrypted: %s & of URL: %s' % (name,user,encrypted_data,decrypted_data,url)}
##
#
run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
