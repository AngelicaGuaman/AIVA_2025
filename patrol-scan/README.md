# PatrolScan - Java
Esta librería permite invocar algoritmos en Python para la detección y reconocimiento de las matrículas vehiculares.

La aplicación de la Dirección General de Tráfico (DGT) podrá integrar esta librería para procesar imágenes capturadas por cámaras de los coches patrulla.
A través de esta integración, la aplicación podrá analizar las imágenes en tiempo real o de manera offline para verificar si el vehículo tiene alguna incidencia como: multas, restricciones de circulación, etc.

## 🚀 Tecnologías utilizadas

- Java 21
- Maven
- Lombok
- JUnit / Mockito
- Spring Boot

## 📦 Instalación

Para instalar la librería, primero debemos clonar el repositorio e instalar el módulo de Java:

```bash
git clone https://github.com/AngelicaGuaman/AIVA_2025
cd AIVA_2025/patrol-scan
mvn clean install
```

### 🔬 Versión alpha

Actualmente, los tests unitarios son mocks. Para poder lanzarlos hay que ejecutar el siguiente comando:

```bash
mvn clean install
```

## 🚀 Uso
```xml
<dependency>
    <groupId>com.muva.aiva.ps</groupId>
    <artifactId>patrol-scan-lib</artifactId>
    <version>0.0.1-SNAPSHOT</version>
</dependency>
```

## 🏗 Diagramas UML

### Diagrama de clases

![Diagrama de clases del módulo Java](../documentation/diagram/clases/DiagramaClasesJava.jpg)

### Diagrama de secuencia

![Diagrama de secuencia del módulo Java](../documentation/diagram/secuencia/DiagramaDeSecuenciaPython.jpg)

### Diagrama de actividad

![Diagrama de actividad del módulo Java](../documentation/diagram/actividad/DiagramaActividadJava.jpg)