package com.muva.aiva.ps.service;

import java.io.File;
import java.io.FileNotFoundException;
import java.util.List;

public interface RunPythonService {

    List<String> runner (File videoFile) throws FileNotFoundException;
}
