package com.muva.aiva.ps.service.impl;

import com.muva.aiva.ps.configuration.PythonConfig;
import com.muva.aiva.ps.service.RunPythonService;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.io.*;
import java.nio.file.Files;
import java.nio.file.StandardCopyOption;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

@Service
@Slf4j
public class RunPythonServiceImpl implements RunPythonService {

    @Autowired
    private PythonConfig config;

    @Override
    public List<String> runner(File videoFile) throws FileNotFoundException {
        List<String> detectedPlates = new ArrayList<>();

        InputStream iSPythonScript = readResourceFile("main.py");
        InputStream iSLicenseModel = readResourceFile("license_plate_detector.onnx");

        try {

            File tempScript = File.createTempFile("main", ".py");
            tempScript.deleteOnExit();

            // Copiar contenido del script al archivo temporal
            Files.copy(iSPythonScript, tempScript.toPath(), StandardCopyOption.REPLACE_EXISTING);

            File tempModel = File.createTempFile("license_plate_detector", ".onnx");
            tempModel.deleteOnExit();

            // Copiar contenido del script al archivo temporal
            Files.copy(iSLicenseModel, tempModel.toPath(), StandardCopyOption.REPLACE_EXISTING);

            log.info("path {}",config.getPath());

            // Ejecutar Python con argumentos
            ProcessBuilder processBuilder = new ProcessBuilder(config.getPath(),
                    tempScript.getAbsolutePath(), tempModel.getAbsolutePath(), videoFile.getAbsolutePath());

            processBuilder.redirectErrorStream(true);

            Process process = processBuilder.start();
            BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream()));
            reader.readLine();
            detectedPlates = Arrays.asList(reader.readLine().replace("[", "").replace("]", "").replace("'", "").split(",\\s*"));
            log.info("Matrículas detectadas: {}", detectedPlates);

            int exitCode = process.waitFor();
            log.info("Python script finalizado con código: {}", exitCode);

        } catch (Exception e) {
            e.printStackTrace();
        }
        return detectedPlates;
    }

    private InputStream readResourceFile(String fileName) throws FileNotFoundException {
        InputStream inputStream = getClass().getClassLoader().getResourceAsStream(fileName);

        if (inputStream == null) {
            throw new FileNotFoundException("El archivo " + fileName + " no se encontró en resources");
        }

        return inputStream;
    }
}
