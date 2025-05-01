package com.muva.aiva.ps.service.impl;

import com.muva.aiva.ps.configuration.PythonConfig;
import com.muva.aiva.ps.service.RunPythonService;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.io.*;
import java.nio.file.Files;
import java.nio.file.StandardCopyOption;
import java.util.*;

@Service
@Slf4j
public class RunPythonServiceImpl implements RunPythonService {

    @Autowired
    private PythonConfig config;

    @Override
    public List<String> runner(File image, File video) throws FileNotFoundException {
        Set<String> detectedPlates = new HashSet<>();

        InputStream iSPythonScript = readResourceFile("core.py");

        try {

            File tempScript = File.createTempFile("core", ".py");
            tempScript.deleteOnExit();

            // Copiar contenido del script al archivo temporal
            Files.copy(iSPythonScript, tempScript.toPath(), StandardCopyOption.REPLACE_EXISTING);

            log.info("python path {}", config.getPath());
            log.info("model path {}", config.getModel());

            File modelFile = new File(config.getModel());
            if (!modelFile.exists()) {
                log.error("Modelo ONNX no encontrado en {}", config.getModel());
            }

            // Ejecutar Python con argumentos
            ProcessBuilder processBuilder = null;

            if (image != null) {
                processBuilder = new ProcessBuilder(config.getPath(),
                        tempScript.getAbsolutePath(), "--model", config.getModel(), "--image", image.getAbsolutePath());
            }

            if (video != null) {
                processBuilder = new ProcessBuilder(config.getPath(),
                        tempScript.getAbsolutePath(), "--model", config.getModel(), "--video", video.getAbsolutePath());
            }
            processBuilder.redirectErrorStream(true);

            Process process = processBuilder.start();
            BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream()));
            String line;
            while ((line = reader.readLine()) != null) {
                if (line.startsWith("[") && !line.equals("[]")) {
                    detectedPlates.addAll(Arrays.asList(line.replace("[", "").replace("]", "").replace("'", "").split(",\\s*")));
                }
            }

            log.info("Running Python command: {}", processBuilder.command());

            log.info("Matrículas detectadas: {}", detectedPlates);

            int exitCode = process.waitFor();
            log.info("Python script finalizado con código: {}", exitCode);

            BufferedReader errorReader = new BufferedReader(new InputStreamReader(process.getErrorStream()));
            String errorLine;
            while ((errorLine = errorReader.readLine()) != null) {
                log.error("Python error: {}", errorLine);
            }

        } catch (Exception e) {
            log.error(e.getMessage());
            e.printStackTrace();
        }
        return new ArrayList<>(detectedPlates);
    }

    private InputStream readResourceFile(String fileName) throws FileNotFoundException {
        InputStream inputStream = getClass().getClassLoader().getResourceAsStream(fileName);

        if (inputStream == null) {
            throw new FileNotFoundException("El archivo " + fileName + " no se encontró en resources");
        }

        return inputStream;
    }
}
