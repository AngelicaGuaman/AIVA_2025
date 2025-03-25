package com.muva.aiva.ps.service;

import com.muva.aiva.ps.service.impl.PlateRecognitionServiceImpl;
import com.muva.aiva.ps.service.impl.RunPythonServiceImpl;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import java.io.File;
import java.util.List;
import java.util.Optional;

import static org.junit.jupiter.api.Assertions.*;

//@ExtendWith(MockitoExtension.class)
class PlateRecognitionServiceTest {

  //  @InjectMocks
    private PlateRecognitionServiceImpl plateRecognitionService;

    //@Mock
    private RunPythonService runPythonService;

    @BeforeEach
    void setUp() {
        runPythonService = new RunPythonServiceImpl();
        plateRecognitionService = new PlateRecognitionServiceImpl(runPythonService);

    }

    @Test
    void testRecognizePlate_ValidImage() {
        File testImage = new File("test_image.jpg");

        Optional<String> result = plateRecognitionService.recognizePlate(testImage);

        assertTrue(result.isPresent());
        assertEquals("1234ABC", result.get());
    }

    @Test
    void testRecognizePlate_InvalidImage() {
        File testImage = new File("empty.jpg");

        Optional<String> result = plateRecognitionService.recognizePlate(testImage);

        assertFalse(result.isEmpty());
    }

    @Test
    void testRecognizePlateFromVideo() {
        File testVideo = new File("test_video.mp4");

        List<String> results = plateRecognitionService.recognizePlateFromVideo(testVideo);

        assertFalse(results.isEmpty());
        assertTrue(results.contains("1234ABC"));
    }
}
