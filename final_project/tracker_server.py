#!/usr/bin/python           # This is server.py file
import socket 
import os
import threading
import sys
import multiprocessing
from threading import Thread
unique_id=0



def func(s):
	appendtoFile=s.recv(1024)
    ##appendtoHost=s.recv(1024)
	print appendtoFile
	appendSearch=''
	appendHostInfo=''
	iter=0
	index=0
	
	while iter < len(appendtoFile):

		if appendtoFile[iter]=='p' and appendtoFile[iter+1]=='o' and appendtoFile[iter+2]=='r' and appendtoFile[iter+3]=='t':
			index=iter
			break;

		else:
			appendSearch=appendSearch+appendtoFile[iter]
			iter=iter+1

	while index<len(appendtoFile):
		appendHostInfo=appendHostInfo+appendtoFile[index]
		index=index+1 
		
	print appendSearch
	
	print appendHostInfo
	#print 'PRINTING HERE'

	f=open('search_content.txt','a')
	fh=open('Peers.txt','a')
	f.write('\n'+appendSearch)
	fh.write('\n'+appendHostInfo)
	iter=0;
	name1=''

	while iter < len(appendtoFile):

		if appendtoFile[iter]=='t' and appendtoFile[iter+1]=='o' and appendtoFile[iter+2]=='r' and appendtoFile[iter+3]==':':
			index=iter+4
			current=appendtoFile[index]

			while not current==' ':
				name1=name1+current
				index=index+1
				current=appendtoFile[index]	
			break;

		else:
			iter=iter+1
	#print appendtoFile[index+1]

	s.send('Message From server : Torrent Information Recieved')
	size=s.recv(1024)
	s.send('Ack')
	n=s.recv(1024)
	s.send('Ack')
	name1=s.recv(1024)
	s.send('Ack')
	print 'Name',name1, n ,size
	name1=name1+'.torrent'
	ft=open(name1,'w+')
	
	line1='name: '+name1
	line2='\nkey: '+str(unique_id)
	line3='\nsize:'+size
	line4='\nn_parts: '+n
	ft.write(line1)
	ft.write(line2)
	ft.write(line3)
	ft.write(line4)
	ft.close()
	f.close()
	s.close()

def peerLeft(s):

	print'Updating info....'
	ip=s.recv(20)
	print ip
	f=open('search_content.txt','r')
	fh=open('Peers.txt','r')
	f2=open('Peers2.txt','w+')
	f1=open('search_content2.txt','w+')
	instances=[]
	count=0

	for lines in fh:
		count=count+1
		if not ip in lines:
			f2.write(lines)
		else:
			instances.append(count)


	count2=0;

	for lines in f:
		count2=count2+1
		if not count2 in instances:
			f1.write(lines)

	fh.close()
	f2.close()			
	f.close()
	f1.close()
	os.rename('search_content2.txt','search_content.txt')
	os.rename('Peers2.txt','Peers.txt')
	s.close()		


def download(c):

	print "=========== IN DOWNLOAD FUNCTION ================"
	filename=c.recv(20)
	
	print filename


	torrFIle = open('search_content.txt','r')
	hostInfo = open('Peers.txt')

	count1=0 
	count2=0

	information=[]
	instances=[]

	for line in torrFIle:
		count1=count1+1

		if filename in line:
			instances.append(count1)
			information.append(line)

	if len(instances)>0:
		c.send('1')

		c.send(information[0])

		
		print'Sent'
		a=c.recv(3)
		print a		
	else:

		c.send('0')	
	print'Here'

	for line in hostInfo:

		count2 = count2 +1 
		print count2

		if count2 in instances:
			c.send(line)
			print line
			print 'Sent again'

	if len(instances)> 0:		
		c.recv(3)

	c.send('Done')		

	print ('===============')
	print information
	print instances
	print ('===============')
	print 'File has been trasferred sucesfully!'
	c.close()



def peerService(c):
	
	choose=c.recv(7)
	
	#print 'torrent' in choose
	if 'torrent' in choose:
		t3= Thread(target=func(c),args=(c))
	elif 'downloa' in choose:
		t3=Thread(target=download(c),args=(c))
	elif 'quit' in choose:
		t3= Thread(target=peerLeft(c),args=(c))

		

def main():

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)      
	hostname = socket.gethostname();  
	host = socket.gethostbyname(hostname)

	print '================== Welcome =================='
	print "\nTHE SERVER HAS BEEN LAUNCHED\n"
	print "You are conntected to : " + str(host) + " at port no : " + str(1231) +"\n"
	

	
	port = 1231            
	s.bind((host, port))        
	s.listen(5)   
	i=0

	while 1:
		c, addr = s.accept()
		print 'Got connection from ' ,addr
		t=Thread(target=peerService(c),args=(c))




class myThread (threading.Thread):
    def __init__(self, threadID, c, addr):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.c = c
        self.addr = addr
    def run(self,):
    	func(self.c)



def giveCount():
	count=1;
if __name__ == '__main__':
	
	p1=multiprocessing.process(target=main())
	
	p2=multiprocessing.process(target=giveCount)
