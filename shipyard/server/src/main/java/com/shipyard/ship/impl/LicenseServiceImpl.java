package com.shipyard.ship.impl;

import com.shipyard.ship.shared.dto.License;
import com.shipyard.ship.shared.dto.Ship;
import com.shipyard.ship.shared.interfaces.LicenseService;
import com.shipyard.ship.shared.interfaces.ShipyardControlSystem;

import java.util.List;

public class LicenseServiceImpl implements LicenseService {

    @Override
    public License getLicenseInfo() {
        return new License(
                false,
                "Your license expired on 2031-09-28. Renew it to use advanced features."
        );
    }
}
