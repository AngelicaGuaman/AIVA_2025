package com.muva.aiva.ps.service;

import java.io.File;
import java.io.FileNotFoundException;
import java.util.List;

public interface PlateRecognitionService {

    /**
     * Reconoce una matrícula en una imagen.
     *
     * @param imageFile Archivo de imagen que contiene la matrícula.
     * @return Las matrículas detectadas en la imagen.
     * @throws FileNotFoundException Si el archivo de imagen no se encuentra.
     */
    List<String> recognizePlate(File imageFile) throws FileNotFoundException;

    /**
     * Reconoce matrículas en un video procesando fotogramas.
     *
     * @param videoFile Archivo de video que contiene vehículos con matrículas.
     * @return Una lista de matrículas detectadas en distintos fotogramas.
     */
    List<String> recognizePlateFromVideo(File videoFile) throws FileNotFoundException;
}
