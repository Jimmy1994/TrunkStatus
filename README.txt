PARA LA INSTALACION EJECUTAR PRIMERAMENTE EL SCRIP INSTALL
./install o sh install

UNA VEZ HAYA FINALIZADO PUEDE COMPROBAR EL SERVICIO CON
systemctl daemon-reload
systemctl status trunkStatus

REVISAR SI SE TIENE CREADO EL USUARIO EN ASTERISK AMI
Path= /etc/asterisk/manager.conf
[admin]
secret=paradise
permit=127.0.0.1
read=system
eventfilter=Event: PeerStatus
RECARGAR EL MODULO MANAGER EN ASTERISK

PARA PROBAR EL ENVIO DE CORREO EJECUTAR
./bin/test.py
EL CORREO SE ENVIARA A soporte@sidevox.com


PUEDE INICIAR EL SERVICIO CON 
systemctl start trunkStatus

CONFIRME EL ESTADO DEL SERVICIO CON
systemctl status trunkStatus

SI PRESENTA ALGUN ERROR AL INICIAR EL SERVICIO REVISAR CON
journalctl -u trunkStatus.service


