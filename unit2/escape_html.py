# User Instructions
# 
# Implement the function escape_html(s), which replaces:
# > with &gt;
# < with &lt;
# " with &quot;
# & with &amp;
# and returns the escaped string
# Note that your browser will probably automatically 
# render your escaped text as the corresponding symbols, 
# but the grading script will still correctly evaluate it.
# 

import cgi

def escape_html(s):
    s = s.replace ("&", "&amp;")
    s = s.replace(">", "&gt;")
    s = s.replace("<", "&lt;")
    s = s.replace("\"", "&quot;")
    return s

def escape_html_cgi(s):
	return cgi.escape(s, quote = True)