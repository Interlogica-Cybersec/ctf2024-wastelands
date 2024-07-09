import numpy as np

def newtons_single(f, f_prime, x0, tol=1e-9, args=[]):
    n = 1
    dx = f(x0, args) / f_prime(x0, args)
    while abs(dx) > tol:
        x0 -= dx
        dx = f(x0, args) / f_prime(x0, args)
        n += 1

    return x0, n


# Two-body problem ordinary differential equation
def orbit_ode(t, y, mu):
    # Recall the orbit can be defined by two 3D vectors
    # The R vector is radius, V vector is velocity
    rx, ry, rz, vx, vy, vz = y

    # Convert position vector to numpy array
    r = np.array([rx, ry, rz])

    # Take the magnitude of r
    norm_r = np.linalg.norm(r)

    # Define the two-body acceleration
    # Recall this is derived from Newton's Universal Law of Gravitation
    ax, ay, az = -r*mu/norm_r**3

    return [vx, vy, vz, ax, ay, az]


# Gets the distance to the origin in an N-dimensional vector
def get_distance(row):
    tot = 0
    for num in row:
        tot += num**2
    return np.sqrt(tot)