package com.shipyard.ship.config;

import com.shipyard.ship.impl.LicenseServiceImpl;
import com.shipyard.ship.shared.interfaces.LicenseService;
import com.shipyard.ship.shared.interfaces.ShipyardControlSystem;
import com.shipyard.ship.impl.ShipyardControlSystemImpl;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.remoting.httpinvoker.HttpInvokerServiceExporter;

@Configuration
public class HttpInvokerConfig {

    @Bean
    public ShipyardControlSystem shipyardControlBean() {
        return new ShipyardControlSystemImpl();
    }

    @Bean
    public LicenseService licenseServiceBean() {
        return new LicenseServiceImpl();
    }

    @Bean(name = "/remote/shipyardControl.http")
    public HttpInvokerServiceExporter shipyardControlHttpInvokerServiceExporter() {
        HttpInvokerServiceExporter exporter = new HttpInvokerServiceExporter();
        exporter.setService(shipyardControlBean());
        exporter.setServiceInterface(ShipyardControlSystem.class);
        return exporter;
    }

    @Bean(name = "/remote/licenseService.http")
    public HttpInvokerServiceExporter licenseServiceHttpInvokerServiceExporter() {
        HttpInvokerServiceExporter exporter = new HttpInvokerServiceExporter();
        exporter.setService(licenseServiceBean());
        exporter.setServiceInterface(LicenseService.class);
        return exporter;
    }
}

