package com.muva.aiva.ps.service;

import com.muva.aiva.ps.service.impl.PlateRecognitionServiceImpl;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import java.io.File;
import java.util.List;
import java.util.Optional;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

class PlateRecognitionServiceMockTest {

    private PlateRecognitionService plateRecognitionServiceMock;

    @BeforeEach
    void setUp() {
        plateRecognitionServiceMock = mock(PlateRecognitionServiceImpl.class);
    }

    @Test
    void testMockRecognizePlate() {
        File mockImage = new File("mock_image.jpg");

        when(plateRecognitionServiceMock.recognizePlate(mockImage)).thenReturn(Optional.of("5678XYZ"));

        Optional<String> result = plateRecognitionServiceMock.recognizePlate(mockImage);

        assertTrue(result.isPresent());
        assertEquals("5678XYZ", result.get());

        verify(plateRecognitionServiceMock, times(1)).recognizePlate(mockImage);
    }

    @Test
    void testMockRecognizePlateFromVideo() {
        File mockVideo = new File("mock_video.mp4");

        when(plateRecognitionServiceMock.recognizePlateFromVideo(mockVideo))
                .thenReturn(List.of("5678XYZ", "1234ABC"));

        List<String> results = plateRecognitionServiceMock.recognizePlateFromVideo(mockVideo);

        assertFalse(results.isEmpty());
        assertEquals(2, results.size());

        verify(plateRecognitionServiceMock, times(1)).recognizePlateFromVideo(mockVideo);
    }
}
