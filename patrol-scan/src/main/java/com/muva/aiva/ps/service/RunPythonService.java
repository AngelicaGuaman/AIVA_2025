package com.muva.aiva.ps.service;

import java.io.File;
import java.io.FileNotFoundException;

public interface RunPythonService {

    Object runner (File videoFile) throws FileNotFoundException;
}
