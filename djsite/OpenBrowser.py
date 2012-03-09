#http://docs.python.org/library/webbrowser.html
import webbrowser

url = 'http://localhost:80'

# Open URL in a new tab, if a browser window is already open.
try:
	webbrowser.open_new_tab(url)
except:
	# Open URL in new window, raising the window if possible.
	webbrowser.open_new(url)
