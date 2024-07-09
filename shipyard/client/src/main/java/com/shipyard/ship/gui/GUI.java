package com.shipyard.ship.gui;

import com.shipyard.ship.logic.Logic;
import com.shipyard.ship.shared.dto.License;
import com.shipyard.ship.shared.dto.Ship;

import javax.swing.*;
import java.awt.*;
import java.util.List;

public class GUI extends JFrame {

    public static void showGUI(Logic logic) {
        final GUI gui = new GUI();
        gui.setTitle("Shipyard Management Desktop Application");
        gui.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);
        License license = logic.getLicense();
        JPanel shipsPanel = new JPanel(new BorderLayout());
        JPanel descriptionPanel = new JPanel(new BorderLayout());
        List<Ship> ships = logic.getShips();
        DefaultListModel<String> listModel = new DefaultListModel<>();
        for (Ship ship : ships) {
            if (ship.getReason() != null) {
                listModel.addElement(ship.getName() + " (" + (ship.isOnline() ? "online" : "offline") + " - " + (ship.getReason()) + ")");
            } else {
                listModel.addElement(ship.getName() + " (" + (ship.isOnline() ? "online" : "offline") + ")");
            }
        }
        JList<String> list = new JList<>(listModel);
        list.setMaximumSize(new Dimension(Integer.MAX_VALUE, Short.MAX_VALUE));
        JTextArea shipDescriptionTextArea = new JTextArea(15, 80);
        shipDescriptionTextArea.setLineWrap(true);
        shipDescriptionTextArea.setEditable(false);
        JButton pingButton = new JButton("Ping ship transponder");
        JButton reserveButton = new JButton("Reserve ship");
        pingButton.setEnabled(false);
        reserveButton.setEnabled(false);
        list.addListSelectionListener(e -> {
            int selectedIndex = list.getSelectedIndex();
            if (selectedIndex >= 0) {
                Ship ship = ships.get(selectedIndex);
                shipDescriptionTextArea.setText(ship.getDescription());
                pingButton.setEnabled(true);
                reserveButton.setEnabled(true);
            } else {
                pingButton.setEnabled(false);
                reserveButton.setEnabled(false);
            }
        });
        pingButton.addActionListener(e -> {
            int selectedIndex = list.getSelectedIndex();
            if (selectedIndex >= 0) {
                if (license.isValid()) {
                    Ship ship = ships.get(selectedIndex);
                    String result = logic.pingShip(ship.getId());
                    JOptionPane.showMessageDialog(null, result);
                } else {
                    JOptionPane.showMessageDialog(null, "You need a valid license to perform this action");
                }
            }
        });
        reserveButton.addActionListener(e -> {
            int selectedIndex = list.getSelectedIndex();
            if (selectedIndex >= 0) {
                if (license.isValid()) {
                    Ship ship = ships.get(selectedIndex);
                    String result = logic.reserveShip(ship.getId());
                    JOptionPane.showMessageDialog(null, result);
                } else {
                    JOptionPane.showMessageDialog(null, "You need a valid license to perform this action");
                }
            }
        });
        shipsPanel.setBorder(BorderFactory.createTitledBorder("Ships available for rent"));
        shipsPanel.add(new JScrollPane(list), BorderLayout.CENTER);
        JPanel pingButtonPanel = new JPanel();
        pingButtonPanel.setLayout(new BorderLayout());
        pingButtonPanel.add(pingButton, BorderLayout.CENTER);
        JPanel reserveButtonPanel = new JPanel();
        reserveButtonPanel.setLayout(new BorderLayout());
        reserveButtonPanel.add(pingButton, BorderLayout.CENTER);
        reserveButtonPanel.add(reserveButton, BorderLayout.SOUTH);
        descriptionPanel.setBorder(BorderFactory.createTitledBorder("Ship description"));
        descriptionPanel.add(new JScrollPane(shipDescriptionTextArea), BorderLayout.CENTER);
        Container contentPane = gui.getContentPane();
        contentPane.setLayout(new BoxLayout(contentPane, BoxLayout.Y_AXIS));
        contentPane.add(shipsPanel);
        contentPane.add(descriptionPanel);
        contentPane.add(pingButtonPanel);
        contentPane.add(reserveButtonPanel);
        gui.pack();
        gui.setLocationRelativeTo(null);
        gui.setVisible(true);
        if (!license.isValid()) {
            JOptionPane.showMessageDialog(null, license.getMessage());
        }

    }
}
