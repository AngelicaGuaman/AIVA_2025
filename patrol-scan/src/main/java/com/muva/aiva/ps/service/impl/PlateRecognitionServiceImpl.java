package com.muva.aiva.ps.service.impl;

import com.muva.aiva.ps.service.PlateRecognitionService;
import com.muva.aiva.ps.service.RunPythonService;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.io.*;
import java.util.ArrayList;
import java.util.List;
import java.util.Optional;

@Service
@Slf4j
public class PlateRecognitionServiceImpl implements PlateRecognitionService {

    private final RunPythonService runPythonService;

    @Autowired
    public PlateRecognitionServiceImpl(RunPythonService runPythonService) {
        this.runPythonService = runPythonService;
    }

    @Override
    public Optional<String> recognizePlate(File imageFile) throws FileNotFoundException {

        if (imageFile == null || !imageFile.exists() || !imageFile.isFile() || imageFile.length() == 0) {
            log.error("El fichero proporcionado no es válido: {}", imageFile);
            return null;
        }

        runPythonService.runner(imageFile);

        log.info("Procesando la imagen {}", imageFile.getName());
        String detectedPlate = "1234ABC";

        return Optional.of(detectedPlate);
    }

    @Override
    public List<String> recognizePlateFromVideo(File videoFile) {
        log.info("Procesando video: {}", videoFile.getName());

        List<String> detectedPlates = new ArrayList<>();

        // Simulación de detección en distintos frames del video
        detectedPlates.add("1234ABC");
        detectedPlates.add("5678XYZ");

        return detectedPlates;
    }
}
