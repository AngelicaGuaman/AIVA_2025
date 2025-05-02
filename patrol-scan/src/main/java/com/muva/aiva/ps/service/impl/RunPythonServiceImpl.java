package com.muva.aiva.ps.service.impl;

import com.muva.aiva.ps.configuration.PythonConfig;
import com.muva.aiva.ps.service.RunPythonService;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.StandardCopyOption;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashSet;
import java.util.List;
import java.util.Set;

@Service
@Slf4j
public class RunPythonServiceImpl implements RunPythonService {

    @Autowired
    private PythonConfig config;

    @Override
    public List<String> runner(File image, File video) throws FileNotFoundException {
        Set<String> detectedPlates = new HashSet<>();

        File tempScript = preparePythonScript();

        log.info("python path {}", config.getPath());
        log.info("model path {}", config.getModel());

        ProcessBuilder processBuilder = buildProcessBuilder(tempScript, image, video);
        processBuilder.redirectErrorStream(true);

        Process process = null;
        try {
            process = processBuilder.start();

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
        } catch (IOException | InterruptedException e) {
            log.error(e.getMessage());
            throw new RuntimeException(e);
        }

        return new ArrayList<>(detectedPlates);
    }

    @Override
    public List<String> runner(String base64Image) {
        Set<String> detectedPlates = new HashSet<>();
        File tempScript = preparePythonScript();

        log.info("python path {}", config.getPath());
        log.info("model path {}", config.getModel());

        try {

            ProcessBuilder processBuilder = new ProcessBuilder(config.getPath(),
                    tempScript.getAbsolutePath(), "--model", config.getModel());
            processBuilder.redirectErrorStream(true);

            Process process = processBuilder.start();

            // Enviar los bytes de la imagen
            try (OutputStream os = process.getOutputStream()) {
                os.write(base64Image.getBytes(StandardCharsets.UTF_8));
                os.flush();
                process.getOutputStream().close();
            }

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

        } catch (IOException e) {
            log.error(e.getMessage());
            throw new RuntimeException(e);
        } catch (InterruptedException e) {
            log.error(e.getMessage());
            throw new RuntimeException(e);
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

    private File preparePythonScript() {
        try (InputStream iSPythonScript = readResourceFile("core.py")) {
            File tempScript = File.createTempFile("core", ".py");
            tempScript.deleteOnExit();
            Files.copy(iSPythonScript, tempScript.toPath(), StandardCopyOption.REPLACE_EXISTING);
            return tempScript;
        } catch (IOException e) {
            log.error("Error preparando el script Python: {}", e.getMessage());
            throw new RuntimeException(e);
        }
    }


    private ProcessBuilder buildProcessBuilder(File script, File image, File video) {
        List<String> command = new ArrayList<>(List.of(config.getPath(), script.getAbsolutePath(), "--model", config.getModel()));
        if (image != null) {
            command.addAll(List.of("--image", image.getAbsolutePath()));
        } else if (video != null) {
            command.addAll(List.of("--video", video.getAbsolutePath()));
        }
        ProcessBuilder processBuilder = new ProcessBuilder(command);
        processBuilder.redirectErrorStream(true);
        return processBuilder;
    }
}
