package com.shipyard.ship.shared.dto;

import java.io.Serial;
import java.io.Serializable;

public class Ship implements Serializable {
    @Serial
    private static final long serialVersionUID = 1L;
    private final String id;
    private final String name;
    private final String description;
    private final boolean online;
    private final String reason;
    private final String image;

    public Ship(String id, String name, String description, boolean online, String reason, String image) {
        this.id = id;
        this.name = name;
        this.description = description;
        this.online = online;
        this.reason = reason;
        this.image = image;
    }

    public String getId() {
        return id;
    }

    public String getName() {
        return name;
    }

    public String getDescription() {
        return description;
    }

    public boolean isOnline() {
        return online;
    }

    public String getReason() {
        return reason;
    }

    public String getImage() {
        return image;
    }
}
