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

        List<String> result = plateRecognitionService.recognizePlate(tempFile);

        assertFalse(result.isEmpty());
        assertEquals("3999JFV", result.get(0));
    }

    @SneakyThrows
    //@Test
    void testRecognizePlate_ValidImage_two_cars() {

        InputStream inputStream = getClass().getClassLoader().getResourceAsStream("data/frame_134_compressed.jpg");

        if (inputStream == null) {
            throw new FileNotFoundException("El archivo no se encontró en resources");
        }

        File tempFile = File.createTempFile("data/frame_134_compressed", ".jpg");
        tempFile.deleteOnExit();

        Files.copy(inputStream, tempFile.toPath(), StandardCopyOption.REPLACE_EXISTING);

        List<String> result = plateRecognitionService.recognizePlate(tempFile);

        assertFalse(result.isEmpty());
        assertEquals(2, result.size());
        assertTrue(result.contains("6264LGR"));
        assertTrue(result.contains("9313JZT"));
    }

    @Test
    @SneakyThrows
    void testRecognizePlate_InvalidImage() {
        File testImage = new File("empty.jpg");

        List<String> result = plateRecognitionService.recognizePlate(testImage);

        assertNull(result);
    }

    @SneakyThrows
        // @Test
    void testRecognizePlateFromVideo()  {
        InputStream inputStream = getClass().getClassLoader().getResourceAsStream("data/20250203_132617.mp4");

        if (inputStream == null) {
            throw new FileNotFoundException("El archivo no se encontró en resources");
        }

        File tempFile = File.createTempFile("data/20250203_132617", ".mp4");
        tempFile.deleteOnExit();

        Files.copy(inputStream, tempFile.toPath(), StandardCopyOption.REPLACE_EXISTING);

        List<String> result = plateRecognitionService.recognizePlateFromVideo(tempFile);

        //assertFalse(result.isEmpty());
        assertTrue(result.contains("8846MLV"));
    }
}
