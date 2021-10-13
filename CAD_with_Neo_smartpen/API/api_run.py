import api

positions = api.run()

for (x, y) in positions():
	print("x: {0} y: {1}".format(x, y))
