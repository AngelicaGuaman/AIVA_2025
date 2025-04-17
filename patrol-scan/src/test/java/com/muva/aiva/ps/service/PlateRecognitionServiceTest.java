package com.muva.aiva.ps.service;

import com.muva.aiva.ps.service.impl.PlateRecognitionServiceImpl;
import lombok.SneakyThrows;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.junit.jupiter.SpringExtension;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.InputStream;
import java.nio.file.Files;
import java.nio.file.StandardCopyOption;
import java.util.List;
import java.util.Optional;

import static org.junit.jupiter.api.Assertions.*;

//@ExtendWith(MockitoExtension.class)
@ExtendWith(SpringExtension.class)
@SpringBootTest
class PlateRecognitionServiceTest {

    //@InjectMocks
    @Autowired
    private PlateRecognitionServiceImpl plateRecognitionService;

    //@Mock
    //@Autowired
    //private RunPythonService runPythonService;

    @BeforeEach
    void setUp() {
        //runPythonService = new RunPythonServiceImpl();
        //plateRecognitionService = new PlateRecognitionServiceImpl(runPythonService);

    }

    @SneakyThrows
    @Test
    void testRecognizePlate_ValidImage() {

        InputStream inputStream = getClass().getClassLoader().getResourceAsStream("data/frame0076.png");

        if (inputStream == null) {
            throw new FileNotFoundException("El archivo no se encontró en resources");
        }

        File tempFile = File.createTempFile("data/frame0076", ".png");
        tempFile.deleteOnExit();

        Files.copy(inputStream, tempFile.toPath(), StandardCopyOption.REPLACE_EXISTING);

        Optional<String> result = plateRecognitionService.recognizePlate(tempFile);

        assertTrue(result.isPresent());
        assertEquals("1234ABC", result.get());
    }

    @Test
    @SneakyThrows
    void testRecognizePlate_InvalidImage() {
        File testImage = new File("empty.jpg");

        Optional<String> result = plateRecognitionService.recognizePlate(testImage);

        assertNull(result);
    }

    @Test
    void testRecognizePlateFromVideo() {
        File testVideo = new File("test_video.mp4");

        List<String> results = plateRecognitionService.recognizePlateFromVideo(testVideo);

        assertFalse(results.isEmpty());
        assertTrue(results.contains("1234ABC"));
    }
}
