import msvcrt

def getch():
	c=msvcrt.getch()
	if b'\xe0'==c:
		return '\xe0'+msvcrt.getch().decode()
	else:
		return c.decode()
