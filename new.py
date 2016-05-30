import socket
import sys
from thread import *
from datetime import datetime

HOST = '192.168.1.6'   # Symbolic name meaning all available interfaces
PORT = int(sys.argv[1])# Arbitrary non-privileged port
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print 'Socket created'
#Bind socket to local host and port
try:
    sock.bind((HOST, PORT))
except socket.error as msg:
    print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()

print 'Socket bind complete'

#Start listening on socket
sock.listen(10)
print 'Socket now listening'

def fileRead(fileName):
    filetext=''
    try:
        f=open(fileName,'rb')
    except IOError as e:
        print 'I/O error({0}):{1}'.format(e.errno, e.strerror)
    except:
        print 'unexpected error:',sys.exc_info()[0]
        raise
    character=''
    for word in f.read():
        if character==' ' and word== ' ' or character=='>' and word==' ' or character==' ' and word== '>' or word=='\n' or character=='<' and word==' ' or character==' ' and word=='<':
            continue
        else:
            filetext+=word
        character=word
        f.close()
    return filetext


while True:
    conn,addr=sock.accept()
    print 'connected from : '+addr[0]+':'+str(addr[1])
    requestheader=conn.recv(1024)
    print '***content starts***'+requestheader+'***content ends***'
    rf=requestheader[5:requestheader.find(' ',5)+1]
    print 'rf:'+rf
    if '.' not in rf:
        rf='index.html'
    print 'rf:'+rf
    rf=rf.strip()
    print rf.strip() 
    try:
        conn.send('HTTP/1.1 200 OK\r\n'
        'Connection: keep-alive\r\n'
        'Content-Length:'+str(len(fileRead(rf)))+'\r\n'
        'Content-Type: text/html\r\n'
        '\r\n')
        conn.send(fileRead(rf))
        conn.close()
    except IOError:
        conn.close()
        print 'you have closed the connecton'
sock.close()
