package com.shipyard.ship.logic;

import com.shipyard.ship.shared.dto.License;
import com.shipyard.ship.shared.dto.Ship;
import com.shipyard.ship.shared.interfaces.LicenseService;
import com.shipyard.ship.shared.interfaces.ShipyardControlSystem;
import org.springframework.context.ApplicationContext;
import org.springframework.context.support.ClassPathXmlApplicationContext;

import java.util.List;

public class Logic {

    private ShipyardControlSystem shipyardControl;
    private LicenseService licenseService;

    public void init() {
        ApplicationContext context = new ClassPathXmlApplicationContext("client-beans.xml");
        shipyardControl = (ShipyardControlSystem) context.getBean("shipyardControlBean");
        licenseService = (LicenseService) context.getBean("licenseServiceBean");
        System.out.println(shipyardControl.getShips());
        System.out.println(licenseService.getLicenseInfo().getMessage());
    }

    public License getLicense() {
        return this.licenseService.getLicenseInfo();
    }

    public List<Ship> getShips() {
        return this.shipyardControl.getShips();
    }

    public String pingShip(String shipId) {
        return this.shipyardControl.pingShipTransponder(shipId);
    }

    public String reserveShip(String shipId) {
        return this.shipyardControl.reserveShip(shipId);
    }
}
