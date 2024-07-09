package com.shipyard.ship.shared.dto;

import java.io.Serial;
import java.io.Serializable;

public class License implements Serializable {
    @Serial
    private static final long serialVersionUID = 1L;
    private final boolean isValid;
    private final String message;

    public License(boolean isValid, String message) {
        this.isValid = isValid;
        this.message = message;
    }

    public boolean isValid() {
        return isValid;
    }

    public String getMessage() {
        return message;
    }
}
