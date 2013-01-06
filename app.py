import os
import psycopg2
from bottle import route, run, template
## NEED below for encryption
from Crypto.Cipher import AES
from base64 import b64encode, b64decode
from datetime import datetime
from re import sub


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

@route("/en")
def test_en():
	our_data_to_encrypt = u'The Sample encrypt text901234567890abc'
	SECRET_KEY = u'a1b2c3d4e5f6g7h8a1b2c3d4e5f6g7h8' # possibly needs unicode conversion from input string
		
	IV = u'12345678abcdeggh' # possibly needs unicode conversion from input string
	cipher_for_encryption = AES.new(SECRET_KEY, AES.MODE_CBC, IV)
	cipher_for_decryption = AES.new(SECRET_KEY, AES.MODE_CBC, IV)
	test = aestest()
	encrypted_data = test.EncryptWithAES(cipher_for_encryption, our_data_to_encrypt)
	decrypted_data = test.DecryptWithAES(cipher_for_decryption, encrypted_data)
	return ('Encrypted string:', encrypted_data '& De:', decrypted_data)


#@route("/de")
#def test_de():
	#test2 = aestest()

	#return ('Decrypted string:', decrypted_data)
##
#
run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
