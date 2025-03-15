# PatrolScan - Detección y Reconocimiento de Matrículas

## 🚓 Introducción
**PatrolScan** es un sistema avanzado de visión artificial diseñado para la **detección y reconocimiento de matrículas** en tiempo real. Se integra en coches patrulla y opera de forma autónoma, proporcionando información instantánea sobre vehículos a los agentes de la Dirección General de Tráfico (**DGT**)

## Descripción
El producto final es una librería usable en Java y Python que permite la detección y lectura de mátriculas en una o varias imágenes, devolviendo como resultado una lista de matrículas encontradas. Para ello se desarrolla un pipeline de procesamiento de imágenes que incluye:
- Detección de la matrícula en la imagen
- Extracción del texto de la matrícula
- Reconocimiento del texto de la matrícula
- Comparación del resultado con una base de datos de matrículas
El sistema principal se desarrolla en Python, y mediante el uso de un wrapper de Java se integra en el sistema operativo Android, permitiendo su uso en los coches patrulla de la DGT, sin la necesidad del guardado o envio de las imágenes a un servidor, o proceso externo. Esto permite un funcionamiento con poca latencia, y seguridad en el tratamiento de los datos.

## ✨ Características principales
- 📸 **Captura de imágenes en tiempo real** desde cámaras de distinta resolución instaladas en los coches patrulla.
- 🤖 **Reconocimiento óptico de caracteres (OCR)** mediante tecnologías de visión artificial.
- 🔍 **Cruce de datos** con bases de datos de la DGT.
- 🌐 **Funcionamiento en local**, sin necesidad de conexión a internet.
- ⚡ **Procesamiento rápido y eficiente**, con respuesta en tiempo real.
- 🎛 **Adaptable a distintas condiciones ambientales**, como baja luz o niebla.

## 🛠 Tecnologías utilizadas
- **Lenguajes:** Java (Android Auto), Python (procesamiento de imágenes)
- **Librerías:** OpenCV, YOLOv11, Tesseract OCR
- **Hardware:** Hardware instalado en el coche patrulla
- **Infraestructura:** Proceso ejecutando en local en el coche patrulla

## 🏗 Arquitectura del sistema
![Diagrama de arquitectura del sistema](images/diagramaPatrolScan.svg)

## 🚀 Instalación y uso
### Requisitos
[Próximamente]

### Instalación
[Próximamente]

### Uso
[Próximamente]


## 📸 Ejemplos de funcionamiento
[Próximamente]
