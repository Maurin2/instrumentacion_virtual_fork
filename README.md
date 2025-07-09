# instrumentacion_virtual

Este repositorio contiene las clases que implementan el VISA para la automatización de diversos instrumentos de medición. Actualmente en construcción...


# Instrucciones para la instalación en Ubuntu 

1. Instalar NI-visa y pyvisa:

```sh
sudo apt update
```


https://www.ni.com/es/support/downloads/drivers/download.ni-visa.html#565016

Descomprimir la carpeta e instalar los drivers (ubuntu 24.04):

```sh
sudo dpkg -i ni-ubuntu2404-drivers-2025Q2.deb
sudo dpkg -i ni-ubuntu2404-drivers-stream.deb
```


Ubuntu 24.04:
```sh
sudo apt install python3-pyvisa-py
```

2. Instalar entorno:

Opcion 1: Con poetry:

Instalar poetry:
```sh
curl -sSL https://install.python-poetry.org | python3 -
```

Instalar dependencias
```sh
poetry install --dev
```

Para activar la consola del python instalado por poetry deben copiar y ejecutar eel comando que se muestra al ejecutar:
```sh
poetry env activate
```

Opcion 2: Con lo que quieran usando el `requirements.txt`, por ejemplo pip:

```sh
pip3 install -r requirements.txt
```

3. Dar acceso al usb al usuario de python:
```sh
sudo nano  /etc/udev/rules.d/99-com.rules
```
--- Agregar la siguiente linea:
```sh
SUBSYSTEM=="usb", MODE="0666", GROUP="usbusers"
```
Crear el grupo y agregar al usuario
```sh
sudo groupadd usbusers
```
```sh
sudo usermod -a -G usbusers $USER
```

4. Reiniciar el equipo