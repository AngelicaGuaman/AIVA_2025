package com.muva.aiva.ps.service.impl;
import com.muva.aiva.ps.service.RunPythonService;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

import java.io.*;
import java.nio.file.Files;
import java.nio.file.StandardCopyOption;

@Service
@Slf4j
public class RunPythonServiceImpl implements RunPythonService {

    @Override
    public void runner(File videoFile) {
        try {
            InputStream inputStream = PlateRecognitionServiceImpl.class.getClassLoader().getResourceAsStream("script.py");

            if (inputStream == null) {
                throw new FileNotFoundException("El script no se encontró en resources");
            }

            File tempScript = File.createTempFile("script", ".py");
            tempScript.deleteOnExit();

            // Copiar contenido del script al archivo temporal
            Files.copy(inputStream, tempScript.toPath(), StandardCopyOption.REPLACE_EXISTING);

            // Argumentos para el script Python
            String arg1 = "hola";
            String arg2 = "mundo";

            // Ejecutar Python con argumentos
            ProcessBuilder processBuilder = new ProcessBuilder("python3", tempScript.getAbsolutePath(), arg1, arg2);
            processBuilder.redirectErrorStream(true);

            Process process = processBuilder.start();
            BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream()));

            // Leer la salida del script Python
            String line;
            while ((line = reader.readLine()) != null) {
                log.info(line);
            }

            int exitCode = process.waitFor();
            log.info("Python script finalizado con código: {}", exitCode);

        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
