#!/usr/bin/env python
import smtplib
import sys
import psycopg2

def DominioCliente():
        dbName='contactvox3'
	dbUser='postgres'
	dbPass='P@r@n01d'
        try:
                conexion=psycopg2.connect(database=dbName,user=dbUser,password=dbPass)
                rows=conexion.cursor()
                rows.execute("select value from private.sys_settings where id=1")
                for row in rows:
                        nameCliente=row[0]
                conexion.close()
        except:
                print 'Error en la conexion con la BD'
                sys.exit(1)
        return nameCliente

nameCliente=DominioCliente()
peer='Nombre de troncal'
ip='IP de troncal'
data='Data AMI'
pieCorreo="We really know IT !!!...\nCualquier novedad no dude en comunicarse con nosotros.Estamos gustosos en atenderle.\n\t\t\t\tContactVox Unified Communications System."

mensaje = """Contactvox te saluda!!\nCliente: %s \nEste es un mail generado automaticamente. \n\nEstado de la troncal SIP:\nTroncal:%s \nIP:%s\nEstado:Inalcanzable\n\nDetalle:\n%s \n\n\n%s""" % (nameCliente,peer,ip,data,pieCorreo)

remitente = "Contactvox UCS  <servicios@sidevox.com>"
destinatario = "Soporte <soporte@sidevox.com"
asunto = "Contactvox UCS Test Soporte"
email = """From: %s
To: %s
MIME-Version: 1.0
Content-type: text
Subject: %s

%s

""" % (remitente, destinatario, asunto,mensaje)
try:
	smtp = smtplib.SMTP('localhost')
        smtp.sendmail(remitente, destinatario, email)
        print "Correo enviado"
except:
	print """Error: el mensaje no pudo enviarse"""

