import socket,sys
from blessings import Terminal
from itertools import permutations
from threading import Thread, RLock

mutex = RLock()

t = Terminal()
req_counter =0
state_dict = {}
state_dict['delay'] = None
state_dict['bw']= None

def atomic_read():
	mutex.acquire()
	data = str(state_dict)
	mutex.release()
	return data

def atomic_write(data_type,data):
	mutex.acquire()
	if data_type == 'd':
		state_dict['delay'] = data
	else:
		state_dict['bw'] = data
	mutex.release()


def write_stuff_below(data_array,data_type):
	st = " ".join([str(item)[:5] for item in data_array])
	if data_type == "d":
		with t.location(0, t.height-2):
			sys.stdout.write("\r{}".format("DL: "+ st))
			sys.stdout.flush()
	else:
		with t.location(0, t.height -1):
			sys.stdout.write("\r{}".format("BW: "+ st))
			sys.stdout.flush()

def create_server(port_no):
	serversocket = socket.socket()
	host = ''
	port = port_no
	serversocket.bind((host, port))
	serversocket.listen(5)
	print ('server started and listening')
	return serversocket


def print_header():
	links = list(permutations(range(1,5),2))
	with t.location(0, t.height-3):
		print "   ","   ".join(["%d-%d" % (tup[0],tup[1]) for tup in links])

def collector(serversocket):
	delaysocket,_ = serversocket.accept()
	bwsocket,_ = serversocket.accept()
	links = list(permutations(range(1,5),2))
	print "Data collector connections accepted"
	while True:
		s = delaysocket.recv(1024)    
		if s != '':
			try:
				s = s.split(" d")[1]
				typ = "d"
				d =  eval(s)
				atomic_write(typ,d)
				array = [str(d[item])[:5] for item in links]
				write_stuff_below(array,typ)
			except:
				print "Error in evaluating delay %s",s
			

		s1 = bwsocket.recv(1024)
		if s1 != '':
			try:
				s1 = s1.split(" b")[1]
				typ = "b"
				d =  eval(s1)
				atomic_write(typ,d)
				array = [str(d[item])[:5] for item in links]
				write_stuff_below(array,typ)
			except:
				print "Error in evaluating bw %s",s1

def listener(serversocket):
	global req_counter
	state_socket,_ = serversocket.accept()
	print "State request connection accepted"
	while 1:		
		req = state_socket.recv(1024)
		if req != '':
			if req[:3] == "GET":
				req_counter +=1
				with t.location(0, t.height-6):
					print "State request %d" % req_counter
				string = atomic_read()
				state_socket.sendall(string)

if __name__ == '__main__':
	l_server_sock = create_server(9000)
	c_server_sock = create_server(7000)
	print_header()
	collectors = []
	collector = Thread(target = collector, args = (l_server_sock,))
	listeners = []
	for i in range(10):
		listeners.append(Thread(target = listener, args = (c_server_sock,)))
	collector.start()
	for l in listeners:
		l.start()