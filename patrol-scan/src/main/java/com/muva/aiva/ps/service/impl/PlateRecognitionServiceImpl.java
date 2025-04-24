package com.muva.aiva.ps.service.impl;

import com.muva.aiva.ps.service.PlateRecognitionService;
import com.muva.aiva.ps.service.RunPythonService;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.io.File;
import java.io.FileNotFoundException;
import java.util.ArrayList;
import java.util.List;

@Service
@Slf4j
public class PlateRecognitionServiceImpl implements PlateRecognitionService {

    private final RunPythonService runPythonService;

    @Autowired
    public PlateRecognitionServiceImpl(RunPythonService runPythonService) {
        this.runPythonService = runPythonService;
    }

    @Override
    public List<String> recognizePlate(File imageFile) throws FileNotFoundException {

        if (imageFile == null || !imageFile.exists() || !imageFile.isFile() || imageFile.length() == 0) {
            log.error("El fichero proporcionado no es válido: {}", imageFile);
            return null;
        }

        log.info("Procesando la imagen {}", imageFile.getName());

        List<String> detectedPlates = runPythonService.runner(imageFile, null);

        return detectedPlates;
    }

    @Override
    public List<String> recognizePlateFromVideo(File videoFile) throws FileNotFoundException {
        log.info("Procesando video: {}", videoFile.getName());

        if (videoFile == null || !videoFile.exists() || !videoFile.isFile() || videoFile.length() == 0) {
            log.error("El fichero proporcionado no es válido: {}", videoFile);
            return null;
        }

        List<String> detectedPlates = runPythonService.runner(null, videoFile);

        return detectedPlates;
    }
}
