package com.muva.aiva.ps.service;

import java.io.File;
import java.io.FileNotFoundException;
import java.util.List;

public interface RunPythonService {

    /**
     * Ejecuta un script de Python para procesar una imagen y devolver la matrícula detectada.
     *
     * @param image Archivo de imagen que contiene la matrícula.
     * @return Las matrículas detectadas en la imagen.
     * @throws FileNotFoundException Si el archivo de imagen no se encuentra.
     */
    List<String> runner (File image, File video) throws FileNotFoundException;
}
