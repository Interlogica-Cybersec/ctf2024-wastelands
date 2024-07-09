import numpy as np
from scipy.integrate import ode
import foe_constants as fc
import ComputationalMethods as cm
from math import cos, sin

# Orbit Class

# TODO: failing to converge in a lot of cases (I don't notice a trend yet). Investigate


class Orbit():
    """A representation of an orbital trajectory at epoch.

    An Orbit is defined by a 6-variable Keplerian state vector
    with true anomaly defined at epoch. Information such as the
    orbital period, and position at some t after epoch can be
    extracted from an Orbit object. Information can be returned
    in terms of Keplerian orbital elements or a Cartesian state
    vector.

    """

    def __init__(self, sma, ecc, inc, raan, argp, tra, sgp=fc.MU_EARTH, epoch=0, radius=fc.R_EARTH):
        """Initializes a new two-body Keplerian orbit.

        Parameters
        ---------
        sma : float
            Semi-major axis (a)
        ecc : float
            Eccentricity (e)
        inc : float
            Inclination (i)
        raan : float 
            Right ascension of the ascending node (Omega)
        argp : float
            Argument of periapsis (omega)
        tra : float
            True Anomaly (theta) at epoch
        sgp : float, optional
            Standard Gravitaional Parameter (mu) (default Earth)
        epoch : float, optional
            The time for which these orbital elements are valid (default 0)
        """
        self.ecc = ecc
        self.sma = sma
        self.inc = inc
        self.raan = raan
        self.argp = argp
        self.tra = tra
        self.sgp = sgp
        self.epoch = epoch
        self.radius = radius

    def get_cartesian(self):
        """Returns the Cartesian state vector in geocentric-equatorial reference.

        Description
        --------
        get_cartesian() returns the Cartesian state vector in the geocentric-equatorial
        reference system at epoch. Essentially it converts the Keplerian state vector
        to a Cartesian state vector (say, for propagating orbits)

        Credit
        --------
        Credit to Thameur Chebbi who originally developed Kepler2Carts for MATLAB.
        https://www.mathworks.com/matlabcentral/fileexchange/80632-kepler2carts
        """
        p = self.sma*(1-self.ecc**2)
        r_0 = p / (1 + self.ecc * cos(self.tra))

        # Perifocal reference system coordinates
        x_ = r_0 * cos(self.tra)
        y_ = r_0 * sin(self.tra)

        Vx_ = -(self.sgp/p)**(1/2) * sin(self.tra)
        Vy_ = (self.sgp/p)**(1/2) * (self.ecc + cos(self.tra))

        # Geocentric-equatorial reference system
        # NOTE: must use \ to continue line in python
        x = (cos(self.raan) * cos(self.argp) - sin(self.raan) * sin(self.argp) * cos(self.inc)) * x_ \
            + (-cos(self.raan) * sin(self.argp) - sin(self.raan)
               * cos(self.argp) * cos(self.inc)) * y_
        y = (sin(self.raan) * cos(self.argp) + cos(self.raan) * sin(self.argp) * cos(self.inc)) * x_ \
            + (-sin(self.raan) * sin(self.argp) + cos(self.raan)
               * cos(self.argp) * cos(self.inc)) * y_
        z = (sin(self.argp) * sin(self.inc)) * x_ + \
            (cos(self.argp) * sin(self.inc)) * y_

        Vx = (cos(self.raan) * cos(self.argp) - sin(self.raan) * sin(self.argp) * cos(self.inc)) * Vx_ \
            + (-cos(self.raan) * sin(self.argp) - sin(self.raan)
               * cos(self.argp) * cos(self.inc)) * Vy_
        Vy = (sin(self.raan) * cos(self.argp) + cos(self.raan) * sin(self.argp) * cos(self.inc)) * Vx_ \
            + (-sin(self.raan) * sin(self.argp) + cos(self.raan)
               * cos(self.argp) * cos(self.inc)) * Vy_
        Vz = (sin(self.argp) * sin(self.inc)) * Vx_ + \
            (cos(self.argp) * sin(self.inc)) * Vy_

        return x, y, z, Vx, Vy, Vz

    def get_orbital_period(self):
        """Returns the period of this Orbit.
        """
        T = 2*np.pi*np.sqrt((self.sma**3)/self.sgp)
        return T

    def propagate(self, Nperiods=1, dt=60, integrator='dopri5'):
        """Propagates the orbit, returning a Cartesian state vector and time.

        Parameters
        --------
        Nperiods : int
            Defines the number of orbital periods to propagate (default 1)
        Nsteps : int
            Defines the number of steps per orbital period (default 100)
        integrator : string
            Defines which scipy integrator to use (default 'lsoda'). Other options
            include 'rk45', 'rk23', etc.
        """
        # Default one period with 100 steps per periods
        tspan = Nperiods*self.get_orbital_period()
        actual_steps = int(np.ceil(tspan/dt) + 1)

        self.ys = np.zeros((actual_steps, 6))  # State vector initialization
        self.ts = np.zeros((actual_steps, 1))  # Time vector initialization

        # Initial conditions
        x0, y0, z0, vx0, vy0, vz0 = self.get_cartesian()
        r0 = [x0, y0, z0]
        v0 = [vx0, vy0, vz0]

        y0 = r0 + v0  # Concatenate lists
        self.ys[0] = np.array(y0)  # Convert to Numpy array

        # Solve using scipy integration
        step = 1
        solver = ode(cm.orbit_ode)
        solver.set_integrator(integrator)
        solver.set_initial_value(y0, 0)
        solver.set_f_params(self.sgp)

        while solver.successful() and step < actual_steps:
            solver.integrate(solver.t + dt)
            self.ts[step] = solver.t
            self.ys[step] = solver.y
            step += 1
        self.ts = self.ts[:, 0]  # needed to avoid array of 1-element arrays

        return self.ys, self.ts

    def get_fov(self, dt=60):
        """
        Returns the satellite field of view in terms of arc length, angle, and cone r and h
        See documentation for definitions of:
        l_arc:  The arc length along the surface of the Earth of the satellite FOV
        theta:  The angle from the center of the Earth to the line from the center of the
                Earth to the 0 degree elevation points
        r_cone: The radius of a cone describing the FOV
        h_cone: The height of a cone describing the FOV
        """
        if self.ys is not None:
            self.ys, self.ts = self.propagate(dt=dt)
        # rs is R_E + h (i.e. the current distance from the satellite to the origin)
        rs = np.apply_along_axis(cm.get_distance, 1, self.ys)
        theta = np.arccos(self.radius / rs)
        l_arc = self.radius * theta
        h_cone = self.radius * (1 - np.cos(theta)) + (rs - self.radius)
        delta_h = self.radius * np.cos(theta)
        r_cone = np.sqrt(self.radius**2 - delta_h**2)

        return l_arc, theta, r_cone, h_cone, delta_h
