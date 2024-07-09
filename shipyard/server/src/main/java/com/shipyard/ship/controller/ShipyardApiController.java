package com.shipyard.ship.controller;

import com.shipyard.ship.shared.interfaces.ShipyardControlSystem;
import com.shipyard.ship.shared.dto.Ship;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.ResponseBody;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.IOException;
import java.util.List;

@Controller
public class ShipyardApiController {


    private final ShipyardControlSystem shipyardControlSystem;

    public ShipyardApiController(ShipyardControlSystem shipyardControlSystem) {
        this.shipyardControlSystem = shipyardControlSystem;
    }

    @RequestMapping(value = "/api/ships", method = RequestMethod.GET)
    @ResponseBody
    public List<Ship> getShips() {
        return shipyardControlSystem.getShips();
    }

    @RequestMapping(value = "/api/contact", method = RequestMethod.POST)
    @ResponseBody
    public void contact(HttpServletRequest request, HttpServletResponse response) throws IOException {
        response.sendRedirect("/contact?success=true");
    }
}