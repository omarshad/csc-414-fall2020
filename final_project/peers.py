import socket,sys
import threading
import multiprocessing
import time
import os
from threading import Thread

exit=0

host = sys.argv[2]

port=int(sys.argv[1])              

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.bind((host, port))


print(host)

s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

jobs=[];


def server():
	
	s.listen(5)   
	
	i=0
	
	while 1:
		c, addr = s.accept()
		
		t=Thread( work(c),args=(c))
	
		t.start()
		t.join()

	s.close()


def work(c):

	print('Im here ',os.getcwd())
	filename=c.recv(1024)
	print (filename)
	c.send('ACK')
	chunks=int(c.recv(3))
	c.send('ACK')
	size=int(c.recv(100))
	print(size)
	c.send('Ack')
	torrent=c.recv(1024)
	c.send('Ack')
	torrent=torrent+'.torrent'
	f=open(torrent,'r')
	for line in f:
		print(line,' Lines....')

	l=line.split()	
	chunk=int(l[1])	
	print('\n')
	print('in server ',filename)
	a_chunk=size/(chunks+1)
	file=open(filename,'rb')
	tosend=file.read(a_chunk)
	while tosend:
		c.send(tosend)
		tosend=file.read(a_chunk)
	
	print('Sent the file')
	file.close()
	c.close()	

	print chunks


def client():

	print('\nIn client')

	host1=raw_input+('Enter host ip you wish to connect to : ' )
	
	port1=int(raw_input('Enter port number : '))
	
	s1 = socket.socket()
	
	host1 = socket.gethostbyname('localhost')
	s1.connect((host1,port1))
	
	print 'Connected to peer'


		
	
def makeTorrentFile():

	name=raw_input('Enter File name: ')
	tor=raw_input('Enter File torrent name: ')
	type=raw_input('Enter the File type: ')+ ' '
	n_parts=(raw_input('Enter the number of parts the file is to be divided: '))

	curr_dir=os.getcwd()
	
	found = 0	
	for i in os.listdir(curr_dir):
		#print i
		if name in i:
			print 'Creating torrent'
			found = 1
			curr = i

	if found:
		size=os.path.getsize(name)
		print 'Size: ',size
		f=open(name,'r')
		path='/LocalUploadFolder'
		##print os.getcwd()
		path=os.getcwd()+path
		
		os.chdir(path)
		found2=0

		for obj in os.listdir(os.getcwd()):
			if obj==name:
				found2=1
				
		if(found2==0):
			f1=open(name,'w+')
			for line in f:
				f1.write(line)
			f1.close()	
		f.close()
		
		os.chdir('..')
		print('Status:',found2)
		#print os.getcwd()
		torrSocket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		torrSocket.connect(('127.0.0.1', 1231))
		torrSocket.send('torrent')
		tosend= 'Name: '+name+' ' +'type: '+type+'tor: '+tor 
		tosend2='port: ' +str(sys.argv[1])+ ' '+ 'Host: '+sys.argv[2]
		torrSocket.send(tosend)
		torrSocket.send(tosend2)

		
		print('\nSending Information to the Server.......')
		print(torrSocket.recv(1024))
		torrSocket.send(str(size))
		torrSocket.recv(3)
		torrSocket.send(str(n_parts))
		torrSocket.recv(3)
		torrSocket.send(tor)
		torrSocket.recv(3)
		torrSocket.close()
	else :
		print "Error : File not found!"


def download():

	filename=raw_input('Enter name of file ')
	d=open('loaded.txt','r')
	ff=0

	for line in d:
		if filename in d and host in line:
			chunky=line.split()
			chunks=int(chunky[2])
			ff=1
	d.close()		

	if not ff:
		chunks=0
		d=open('loaded.txt','a')
		d.write(filename+' '+host+' '+'0\n')
	d.close()	
	
	downloadingSocket= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	downloadingSocket.connect(('127.0.0.1',1231))
	downloadingSocket.send('downloa')
	downloadingSocket.send(filename)
	confirmation=0
	confirmation=downloadingSocket.recv(1)
	#print confirmation
	confirm=int(confirmation)
	if confirm:
		total_Chunks=1
	#	print os.getcwd()
		info0=(downloadingSocket.recv(1024)).split()
	#	print 'HERE',info0
	#	print info0[5]
		for i in os.listdir(os.getcwd()):
		#	print i
		#	print (info0[5] in i) 
			if info0[5] in i:
				f=open(i,'rb')
				for lines in f:
				#	print lines
					if 'n_parts' in lines:
						total_Chunks=lines.split()
					#	print total_Chunks, 'hereeererererer'
						total_Chunks=total_Chunks[1]
	#					print 'Chunks ========================================',total_Chunks				
		downloadingSocket.send('Ack')
	#	print 'Acked 123'
		info=downloadingSocket.recv(1024)
		downloadingSocket.send('Ack')
		info1=info.split()
		#print info1
		#print info1[3],info1[1]
		print("\nPress Enter to confirm that you want to download :")

		x=raw_input()
		
		otherPeer_ip=info1[3]
		otherPeer_port=int(info1[1])
		peer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		peer_socket.connect((otherPeer_ip,otherPeer_port))
		peer_socket.send(filename)
		peer_socket.recv(3)
		peer_socket.send(str(chunks))
		peer_socket.recv(3)
		peer_socket.send(str(os.path.getsize(filename)))
		peer_socket.recv(3)	
		peer_socket.send(info0[-1])
		peer_socket.recv(3)
		print '\n '
		print "Requested File : " + str(filename)
		#print chunks
		path='/Downloads'
		##print os.getcwd()
		sizeofEachChunk=(os.path.getsize(filename))/int(total_Chunks)
		sizef=os.path.getsize(filename)
		path=os.getcwd()+path
		
		os.chdir(path)
		newfile=open(filename,'wb')
		
		toadd=''
		toadd1=''
		count=0
	#	print sizeofEachChunk
		toadd='1'
		while(not 'Acked' in toadd and toadd):
			toadd=peer_socket.recv(sizeofEachChunk)
			if not 'Acked' in toadd and toadd:
				newfile.write(toadd)
				print('Downloading....')
				count=count+1
		#		print toadd
				

		print('\nSucessfully downloaded!!!!')

	

	else:
		print('No such file')
	downloadingSocket.close()
	peer_socket.close()
	os.chdir('..')

def list_peers():
	f = open('Peers.txt', 'r')
	print(f.read())
	f.close()


def list_content():
	f = open('search_content.txt', 'r')
	print f.read()
	f.close()


if __name__ == '__main__':
	
	print '================== Welcome =================='
	print "\nTHE CLIENT HAS BEEN LAUNCHED\n"
	print "You are conntected to : " + str(host) + " at port no : " + str(port) +"\n"
	print "1. Connect to a Peer \n2. Make a new torrent file \n3. Download a file \n4. List peers\n5. List of Files \n6. Exit"

	thread.start_new_thread ( server,())
	x=0;
	while x < 7:
		x=int(raw_input('Your choice : '))
	
		if x==1:
		
			t2=Thread( target=client(),args=())
			t2.start()
			t2.join
		
		if x==2: 

			t3= Thread(target=makeTorrentFile(),args=())
			t3.start()
			t3.join()	
			

		if x==3:
			try :
				t4=Thread(target=download(),args=())
			except :
				print ("The host is down!!!")
		if x== 4:
			list_peers()
		if x==5:
			list_content()
		if x==6 :

			#delete files from here
				
			sys.exit()
		if x > 6 : 
			print("Please choose an option between 1 - 6")

	s1.close()
	s.close()
	torrSocket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	torrSocket.connect(('127.0.0.1',1231))
	torrSocket.send('quit123')
	torrSocket.send(sys.argv[2])
	torrSocket.close
	
