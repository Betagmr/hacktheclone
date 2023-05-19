# HackTheClone

<p align="center">
<img src="assets\readmePhoto.png" alt="Esquema" width="full"/>
</p>

## Información del proyecto
HackTheClone es una herramienta que permite la creación de máquinas con diversas vulnerabilidades, esto permite construir entornos realistas y seguros para practicar y aprender sobre seguridad informática. Estas máquinas se desarrollan de manera intencional para contener vulnerabilidades conocidas y desafíos de seguridad, lo que permite a los participantes poner a prueba sus habilidades en un entorno controlado.

## Prerequisitos
* [Python](https://www.python.org/) 3.10 o superior.
* [Docker](https://www.docker.com/)

## Instrucciones de ejecución
```
git clone https://github.com/Betagmr/hacktheclone
cd hacktheclone
make install
make run
```
## Como crear máquinas

* Crear carpeta en `containers` con formato `snake_case`
* Crear `dockerfile` con la configuración que se desee.
* Tener un archivo `root.txt` con el *flag* por máquina.
* Posible añadir imagen con formato `.png`, de no ser así, se seleccionará una imagen aleatoria por defecto.
* Para más ejemplos, acceder a la carpeta `containers`.