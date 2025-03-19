package com.muva.aiva.ps.service.impl;

import com.muva.aiva.ps.service.PlateRecognitionService;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

import java.io.*;
import java.util.ArrayList;
import java.util.List;
import java.util.Optional;

@Service
@Slf4j
public class PlateRecognitionServiceImpl implements PlateRecognitionService {

    @Override
    public Optional<String> recognizePlate(File imageFile) {
        log.info("Procesando la imagen {}", imageFile.getName());
        String detectedPlate = "ABC1234";

        return Optional.of(detectedPlate);
    }

    @Override
    public List<String> recognizePlateFromVideo(File videoFile) {
        log.info("Procesando video: {}", videoFile.getName());

        List<String> detectedPlates = new ArrayList<>();

        // Simulación de detección en distintos frames del video
        detectedPlates.add("ABC1234");
        detectedPlates.add("XYZ5678");

        return detectedPlates;
    }
}
