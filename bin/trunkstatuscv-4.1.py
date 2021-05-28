#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket
import smtplib 
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import datetime
import time
import psycopg2
import sys

#Funcion enviar correo	
def EnviarCorreo(data):
	print 'Ingreso a enviar correo:'
	print data
	global peer
	global nameCliente
	global ip
	remitente = "Contactvox UCS  <helpdesk@contactvox.com>"
	#destinatario = ["Cliente <workforce@happy-solutions.com.co>","Soporte <soporte@contactvox.com>"]
	destinatario = ["Soporte <eachig@contactvox.com>","Soporte <jpardo@contactvox.com>]
	asunto = "Contactvox UCS Aviso Troncal"
	msg=PreparCorreo(data)
	#print msg
	mensaje = MIMEMultipart()
 	mensaje['From'] = remitente
    	mensaje['To'] = ", ".join(destinatario)
    	mensaje['Subject'] = asunto
    	mensaje.attach(MIMEText(msg, 'html'))

	try:			
		smtp = smtplib.SMTP('localhost') 		
		smtp.sendmail(remitente, destinatario, mensaje.as_string())
		EscribirEnLog("\nCorreo enviado a: "+str(destinatario))
		print "Correo enviado"
	except:
		print """Error: el mensaje no pudo enviarse"""
		EscribirEnLog("\nFalla en envio de correo")

#Funcion para log
def EscribirEnLog(datos,archivo="/var/log/logtrunk.txt"):
	with open(archivo,"a") as miarchivo:
		miarchivo.write(datos)


#Funcion a bd
def BuscarPeer(data):
	
	global dbName
	global dbUser
	global dbPass
	global sqlQuery
	global ip
	global peer
	result=-1
	try:
		conexion=psycopg2.connect(database=dbName,user=dbUser,password=dbPass)
		rows=conexion.cursor()
		rows.execute(sqlQuery)
		for row in rows:
        		if result == -1:
				result=data.find(row[0])
				ip=row[1]
				peer=row[0]
			else:
				break
		conexion.close()
	except:
		print 'Error en la conexion con BD'
		EscribirEnLog('\nError en la conexion con la BD\n')
		sys.exit(1)
	return result

#Funcion Login Asterisk Call Manager Interface
def Login():
        global s
        global sizebuffer
        res=-1
        #s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        try:
		s.connect(("127.0.0.1",5038))
        	s.send("Action:Login\nUsername:admin\nSecret:paradise\n\n")
		while 1:
			con = s.recv(sizebuffer)
                	conex=str(con)
                	res=conex.find("Success")
			res2=conex.find("Error")
			if res!=-1:
				break
			if res2!=-1:
				print 'Error en Login'
				sys.exit(1)
		return res
	except:
		print 'Error en socket'
		sys.exit(1)



def DominioCliente():
	global dbName
	global dbUser
	global dbPass
	global nameCliente
	try:	
		conexion=psycopg2.connect(database=dbName,user=dbUser,password=dbPass)
		rows=conexion.cursor()
		rows.execute("select description from private.sys_settings where id=1")
		#rows.execute("select name from sys_users where id=2")
		for row in rows:
			nameCliente=row[0]
			print nameCliente
		conexion.close()
	except:
		print 'Error en la conexion con la BD'
		sys.exit(1)

def PreparCorreo(noti):
	global peer
	global nameCliente
	global ip
	color="303d45"
	email_content = """
	<html>
	<head>
	<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
    
   	<title>Notificación Email de Contactvox</title>
   	<style type="text/css">
	
    	a {color: #1c2745; text-decoration: none;}
 	 body, #header h1, #header h2, p {margin: 0; padding: 0;}
  	#main {border: 1px solid #cfcece;}
	img {display: block;}
  	#top-message p, #bottom p {color: #3f4042; font-size: 12px; font-family: Arial, Helvetica, sans-serif; }
  	#header h1 {letter-spacing: 2.5px; color: #ebc639 !important; font-family: "Lucida Grande",sans-serif;font-size: 16px; margin-bottom: 0!important; padding-bottom: 0; }
  	#header p {color: #000000 !important; font-family: "Lucida Grande", "Lucida Sans", "Lucida Sans Unicode", sans-serif; font-size: 12px;  }
  	h5 {margin: 0 0 0.8em 0;}
    	h5 {font-size: 24px; color: #1e2641 !important; font-family: "Lucida Grande",sans-serif; }
  	p {font-size: 16px; color: #1e2641; font-family: "Lucida Grande", "Lucida Sans", "Lucida Sans Unicode", sans-serif; line-height: 1.5;}
   
	</style>	
	</head>
 	
	<body>
 	
 	
	<table width="100%" cellpadding="0" cellspacing="0" bgcolor="e4e4e4"><tr><td>
	<table id="top-message" cellpadding="20" cellspacing="0" width="600" align="center">
    	<tr>
      	<td align="center">
       
      	</td>
    	</tr>
  	</table>
 	
	<table id="main" width="600" align="center" cellpadding="0" cellspacing="0" bgcolor="ffffff">
    	<tr>
      	<td>
        <table id="header" width="600" cellpadding="10" cellspacing="25" align="center" bgcolor="#"""+color+"""">
          <tr>    
              <td width="100%" align="left" bgcolor="#"""+color+"""" style="padding:5px;">
              <img src="http://186.4.249.199/img/cv-2.PNG" width="200" height="25" />
            </td>
       
            <td width="100%" align="right" bgcolor="#"""+color+""""><h1>NOTIFICACIÓN</h1></td>
          </tr>
        </table>
      	</td>
    	</tr>
 	
    	<tr>
      	<td>
        <table id="content-3" cellpadding="0" cellspacing="0" align="center">	
          <tr>
       
          </tr>
        </table>
      	</td>
    	</tr>
    	<tr>
      	<td>
        <table id="content-4" cellpadding="0" cellspacing="0" align="center">
          <tr>
            <td width="350" valign="top">
          	<br>
		<br>
		<br>    
	      <h5 align="center">Cliente: """+nameCliente+"""</h5>
              <br>
	      <p><b>El estado de la troncal:</b></p>
	      <p>Troncal: """+peer+"""</p>
              <p>IP: """+ip+"""</p>
              <p>Estado: Inalcanzable</p>
              <br>
	      <p><b>Detalle:</b></p>
              <p>"""+noti+"""</p>
            </td>
            <td width="15"></td>
          </tr>
	<br>
	<br>

        </table>
     	</td>
    	</tr>
	<tr>
	
	<td>
	<br>
	<br>
	
    	<p style="font-size: 13px;"  align="center"> <b>ContactVox Unified Communications System </b></p>
    	<p style="font-size: 13px;" align="center" style="text-decoration:none"> <b>www.contactvox.com </b></p>
	</td>

	</tr>
	
	
   	 <tr>
      	<td align="center">
        <table id="bottom" align="center" cellspacing="5">
		
		<tr>
			<td>
			<a href="https://www.facebook.com/contactvox/" target="_blank"><img alt="Siguenos en Facebook" src="http://186.4.249.199/img/fb.png" width=30 height=30  /></a>
			</td>
		

			<td>
			<a href="https://www.instagram.com/contactvox/" target="_blank"><img alt="Siguenos en Instagram" src="http://186.4.249.199/img/ins.png" width=30 height=30  /></a>
			</td>
	
			<td>
			<a href="https://www.linkedin.com/company/contactvox/" target="_blank"><img alt="Siguenos en Linkedin" src="http://186.4.249.199/img/link.png" width=30 height=30  /></a>	
			</td>
			<td>
			<a href="https://www.youtube.com/channel/UCsyXBnyN58msKU1JGw5TWDQ" target="_blank"><img alt="Siguenos en YouTube" src="http://186.4.249.199/img/youtube.png" width=30 height=30  /></a>

			</td>
		</tr>
	</table>
	</tr>


	<br>
	<br>
 
  	</table>

	<br>
	
  	<table id="bottom" cellpadding="20" cellspacing="0" width="600" align="center">
   	 <tr>
      	<td align="center">
        <table id="bottom" align="center">

	</table>
     
	</td>
    	</tr>
  	</table><!-- top message -->
	</td></tr></table><!-- wrapper -->
 	
	</body>
	</html>
	
	"""
	return email_content



#Definicion de variables
dbName='contactvox3'
dbUser='postgres'
dbPass='P@r@n01d'
nameCliente=''
sizebuffer=250
peer=""
ip=""
peerStatus="Unreachable"
sqlQuery="Select name,domain from private.tel_siptrunks order by name asc"
#sqlQuery="Select name,ipaddr from ast_sipregistrations"
s= socket.socket(socket.AF_INET,socket.SOCK_STREAM)   
from datetime import datetime
ahora=datetime.now()
fecha=ahora.strftime("%Y-%m-%d %H:%M:%S")


#Main
Login()
DominioCliente()
#EnviarCorreo('Prueba')
#sys.exit(0)


EscribirEnLog("\nSTART SCRIPT..........\nDate: "+fecha+"\n")
print 'Inicio Script'
#time.sleep(0.2)
i=1
while 1:		
	try:
		datos = s.recv(sizebuffer)
	except:
		'Error en socket conexion'
	dat=str(datos)
	resStatus=dat.find(peerStatus)
	resPeer=BuscarPeer(dat)
	
	if resPeer != -1:
		ahora=datetime.now()
		fecha=ahora.strftime("%Y-%m-%d %H:%M:%S")
		EscribirEnLog("\nDate:"+fecha+"....\n")
		EscribirEnLog(dat)

	if resStatus!=-1 and resPeer!=-1:
		EnviarCorreo(dat)
