# Proyecto 1

**Curso:** ST0263 - Tópicos Especiales en Telemática
<br>**Profesor:** Edwin Montoya - emontoya@eafit.edu.co
<br>**Estudiantes:**
- Miguel Ángel Calvache Giraldo
- Mauricio David Correa Hernandez
- Miguel Angel Martinez Garcia
- Salomon Velez Perez
- Simon Botero

<br>**Título:** Proyecto 2 - Cluster kubernetes
<br>**Objetivo:** El objetivo es desplegar una aplicación en un clúster Kubernetes de alta disponibilidad utilizando la distribución MicroK8s en una infraestructura como servicio (IaaS) proporcionada por AWS.

## 1. Descripción general de la actividad

Este proyecto consiste en la implementación de un sistema de archivos distribuido basado en el modelo de HDFS (Hadoop Distributed File System) para manejar grandes volúmenes de datos con alta disponibilidad y tolerancia a fallos. La arquitectura requiere del NameNode para gestionar los metadatos y coordinar la replicación de los bloques de archivos en múltiples DataNodes.

### 1.1 Aspectos cumplidos

* Cluster de kubernetes con microk8s
* Un master y dos workers
* Servidor NFS para almacenar los datos
* ingress con microk8s
* Dominio propio (proyecto2.miguapa.tech)
* Certificado SSL
* wordpress 2 nodos
* mysql

### 1.2 Aspectos no desarrollados

Se cumplió con todo.

## 2. Arquitectura del sistema

A continuación se observa el diagrama de la arquitectura usada para nuestro proyecto.

<br>

## 3. Descripción del ambiente de desarrollo

### 3.1 EC2 en AWS

Se crearon 4 instancias EC2 en AWS, una para el master, dos para los workers, y una para el NFS Se utilizó la imagen de Ubuntu 20.04. 

### 3.2 Configuración de las instancias

### 3.3 Conectar workers con master

### 3.4 Crear NFS y agregar CSI en el master para el NFS

### 3.5 Manifestos

* NFS

* mysql

* wordpress

* Ingress

* Certificado SSL

 ## 4. Descripción del ambiente de ejecución (Resultados)

 ## Referencias
