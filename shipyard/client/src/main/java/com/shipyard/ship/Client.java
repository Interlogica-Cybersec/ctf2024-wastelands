package com.shipyard.ship;

import com.shipyard.ship.gui.GUI;
import com.shipyard.ship.logic.Logic;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import javax.swing.JOptionPane;

public class Client {
    private static final Logger log = LoggerFactory.getLogger(Client.class);

    public static void main(String[] args) {
        String host = JOptionPane.showInputDialog("Insert the hostname (format: \"hostname:port\")");
        if (host == null) {
            System.exit(0);
        }
        System.setProperty("HOST", host);
        Logic logic = new Logic();
        logic.init();
        GUI.showGUI(logic);
    }
}