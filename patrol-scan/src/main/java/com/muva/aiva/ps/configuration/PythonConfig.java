package com.muva.aiva.ps.configuration;

import lombok.Getter;
import lombok.Setter;
import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.stereotype.Component;

@Component
@ConfigurationProperties(prefix = "patrolscan.python")
@Getter
@Setter
public class PythonConfig {
    /**
     * Path to the Python executable.
     */
    private String path;

    /**
     * Path to the Python model.
     */
    private String model;
}

