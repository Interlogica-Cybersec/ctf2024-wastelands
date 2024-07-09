package com.shipyard.ship.shared.interfaces;

import com.shipyard.ship.shared.dto.Ship;

import java.util.List;

public interface ShipyardControlSystem {
    String getShipStartupKey(String shipId);

    List<Ship> getShips();

    String pingShipTransponder(String shipId);

    String reserveShip(String shipId);

    String scheduleForMaintenance(String shipId);

    String getReservationHistory(String shipId);

    String getAdditionalInformation(String shipId);
}
