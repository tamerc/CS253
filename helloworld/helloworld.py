import webapp2
import cgi

form="""
<form method="post">
	What is your birthday?
	<br>
	<label> Day
		<input type="text" name="day" value="%(day)s">
	</label>
	
	<label> Month
		<input type="text" name="month" value="%(month)s">
	</label>
	
	<label> Year
		<input type="text" name="year" value="%(year)s">
	</label>
	
	<div style="color: red">%(error)s</div>
	
	<br>
	<br>
	<input type="submit">
	
</form>
"""

class MainPage(webapp2.RequestHandler):
	def write_form(self, error="", month="", day="", year=""):
		self.response.out.write(form % {"error":error,
										"month":month,
										"day":day,
										"year":year})

	def get(self):
		self.write_form()
      
	def post(self):
		user_month = self.request.get('month')
		user_day = self.request.get('day')
		user_year = self.request.get('year')
		
		month = valid_month(user_month)
		day = valid_day(user_day)
		year = valid_year(user_year)
		
		if not (month and day and year):
			self.write_form("That doesn't look valid to me, friend.", user_month,
			user_day, user_year)
		else:
			self.redirect("/thanks")
			
class ThanksHandler(webapp2.RequestHandler):
	def get(self):
		self.response.out.write("Thanks! that's a totally valid day!")


app = webapp2.WSGIApplication([('/', MainPage), ('/thanks', ThanksHandler)],
                              debug=True)
                              
def valid_year(year):
	if year and year.isdigit():
		yearValue = int(year)
		if yearValue >= 1900 and yearValue <= 2020:
			return yearValue
	return None;
	
def valid_day(day):
    if day and day.isdigit():
        try:
            validDay = int(day)
            if validDay > 0 and validDay < 32:
             return validDay
        except exceptions.ValueError:
         return None;
    return None;        

months = ['January',
          'February',
          'March',
          'April',
          'May',
          'June',
          'July',
          'August',
          'September',
          'October',
          'November',
          'December']

month_abbvs = dict((m[:3].lower(), m) for m in months)
          
def valid_month(month):
    if (month):
     short_month = month[:3].lower()
     return month_abbvs.get(short_month)      