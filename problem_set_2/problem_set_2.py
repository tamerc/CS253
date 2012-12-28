import webapp2
import cgi
import re

rot13_form="""
  <body>
    <h2>Enter some text to ROT13:</h2>
    <form method="post">
      <textarea name="text"
                style="height: 100px; width: 400px;">%(value)s</textarea>
      <br>
      <input type="submit">
    </form>
  </body>
"""

signup_form="""
<form method="post">
    Signup form
	<br>
	<label> Username
		<input type="text" name="username" value="%(username)s">
	</label>
	<div style="color: red">%(errorusername)s</div>
	
	<br>
	
	<label> Password
		<input type="password" name="password" value="%(password)s">
	</label>
	<div style="color: red">%(errorpw)s</div>
	
	<br>
	
	<label> Verify
		<input type="password" name="verify" value="%(verify)s">
	</label>
	<div style="color: red">%(errorverify)s</div>
	
	<br>
	
	<label> Email
		<input type="text" name="email" value="%(email)s">
	</label>
	<div style="color: red">%(erroremail)s</div>
	
	<br>

	<br>
	<br>
	<input type="submit">
	
</form>
"""


class Rot13(webapp2.RequestHandler):
	def write_form(self, text=""):
		self.response.out.write(rot13_form % {"value":text})

	def get(self):
		self.write_form()
      
	def post(self):
		text = self.request.get('text')
		rot13_text = rot13(text)
		self.write_form(cgi.escape(rot13_text, quote = True))
		
class Signup(webapp2.RequestHandler):
	def write_form(self, username="", password="", verify="", email="", errorusername="",
				   errorpw="", errorverify="", erroremail=""):
		self.response.out.write(signup_form % {"username":username,
											   "password":password,
											   "verify":verify,
											   "email":email,
											   "errorusername":errorusername,
											   "errorpw":errorpw,
											   "errorverify":errorverify,
											   "erroremail":erroremail})

	def get(self):
		self.write_form()
      
	def post(self):
		username = self.request.get('username')
		pw = self.request.get('password')
		verify = self.request.get('verify')
		email = self.request.get('email')
		error = False
		errorusername = ""
		errorpw = ""
		errorverify= ""
		erroremail = ""

		if not valid_username(username):
			errorusername = "That's not a valid username."
			error = True

		if not valid_password(pw):
			errorpw = "That wasn't a valid password."
			error = True
		elif pw != verify:
			errorverify = "Your passwords didn't match."
			error = True
		
		if not valid_email(email):
			erroremail = "That's not a valid email."
			error = True
            
		if error:
			self.write_form(username, pw, verify, email, errorusername,
			               errorpw, errorverify, erroremail)
		else:
			self.redirect('/unit2/welcome?username=' + username)
			
class WelcomeHandler(webapp2.RequestHandler):
	def get(self):
		username = self.request.get('username')
		if valid_username(username):
			self.response.out.write("Welcome " + username + "!")
		else:
			self.redirect('/unit2/signup')
		

			
app = webapp2.WSGIApplication([('/unit2/rot13', Rot13),('/unit2/signup', Signup)
							  ,('/unit2/welcome', WelcomeHandler)],
                              debug=True)

def rot13(input):
	output_string = ""
	for i in input:
		if i.isalpha():
			new_char = ord(i)
			
			if new_char >= 97 and new_char <= 122:
				new_char -= 97 + 13
				new_char = (new_char % 26)
				new_char += 97
			else:
				new_char -= 65 + 13
				new_char = (new_char % 26)
				new_char += 65
			
			output_string += str(chr(new_char))
		else:
			output_string += i	
	return output_string
	
USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return username and USER_RE.match(username)

PASS_RE = re.compile(r"^.{3,20}$")
def valid_password(password):
    return password and PASS_RE.match(password)

EMAIL_RE  = re.compile(r'^[\S]+@[\S]+\.[\S]+$')
def valid_email(email):
    return not email or EMAIL_RE.match(email)