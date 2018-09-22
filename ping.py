import os
import sys


if len(sys.argv) < 2:
	print ("please enter IP address")
else:
	address = sys.argv[1]
	os.system("ping " + address)
