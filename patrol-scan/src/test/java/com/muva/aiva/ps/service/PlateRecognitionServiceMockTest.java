package com.muva.aiva.ps.service;

import com.muva.aiva.ps.service.impl.PlateRecognitionServiceImpl;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import java.io.File;
import java.io.FileNotFoundException;
import java.util.List;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.mockito.Mockito.*;

class PlateRecognitionServiceMockTest {

    private PlateRecognitionService plateRecognitionServiceMock;

    @BeforeEach
    void setUp() {
        plateRecognitionServiceMock = mock(PlateRecognitionServiceImpl.class);
    }

    @Test
    void testMockRecognizePlate() throws FileNotFoundException {
        File mockImage = new File("mock_image.jpg");
        List<String> mockPlates = List.of("5678XYZ");

        when(plateRecognitionServiceMock.recognizePlate(mockImage)).thenReturn(mockPlates);

        List<String> result = plateRecognitionServiceMock.recognizePlate(mockImage);

        assertFalse(result.isEmpty());
        assertEquals("5678XYZ", result.get(0));

        verify(plateRecognitionServiceMock, times(1)).recognizePlate(mockImage);
    }

    @Test
    void testMockRecognizePlateFromVideo() throws FileNotFoundException {
        File mockVideo = new File("mock_video.mp4");

        when(plateRecognitionServiceMock.recognizePlateFromVideo(mockVideo))
                .thenReturn(List.of("5678XYZ", "1234ABC"));

        List<String> results = plateRecognitionServiceMock.recognizePlateFromVideo(mockVideo);

        assertFalse(results.isEmpty());
        assertEquals(2, results.size());

        verify(plateRecognitionServiceMock, times(1)).recognizePlateFromVideo(mockVideo);
    }
}
