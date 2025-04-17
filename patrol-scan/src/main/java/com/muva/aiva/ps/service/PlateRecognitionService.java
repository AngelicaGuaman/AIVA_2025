package com.muva.aiva.ps.service;

import java.io.File;
import java.io.FileNotFoundException;
import java.util.List;
import java.util.Optional;

public interface PlateRecognitionService {

    /**
     * Reconoce una matrícula en una imagen.
     *
     * @param imageFile Archivo de imagen que contiene la matrícula.
     * @return Un Optional con la matrícula detectada, vacío si no se detectó ninguna.
     */
    Optional<String> recognizePlate(File imageFile) throws FileNotFoundException;

    /**
     * Reconoce matrículas en un video procesando fotogramas.
     *
     * @param videoFile Archivo de video que contiene vehículos con matrículas.
     * @return Una lista de matrículas detectadas en distintos fotogramas.
     */
    List<String> recognizePlateFromVideo(File videoFile);
}
