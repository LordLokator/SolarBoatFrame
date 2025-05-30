# %pip install pygame -quiet

import threading
import pygame
from enum import Enum, auto
import numpy as np
from gps_coordinate.base import GPSPoint

from managers import GPSManager

from loguru import logger

from managers.can_bus.serial_manager import SerialParamReader
logger.remove()

# Constants
U = 1.1  # [m/s]
DT = 0.2  # [s]
MAX_STEPS = 1000

# Controller gains (from paper)
k1, k2, k3, k4 = 1.6, 19.92, 2.125, 92.1

# Constants
DT = 0.2  # timestep
ARRIVAL_TOL_M = 10.0
RUDDER_LIMIT_DEG = 35
MIN_SPEED = 0.1
CRUISE_SPEED = 2
SPEED_STEP = 0.01

class Mode(Enum):
    TRACKING = auto()
    TURNING = auto()


##########################################################################

serial_communication = SerialParamReader(
    port='/dev/ttyACM0',
    baudrate=115_200,
    timeout=2
)
sender_thread = threading.Thread(
    serial_communication.send_rudder_surge(),
    daemon=True
)
sender_thread.start()

##########################################################################

gps_manager = GPSManager(
    port='/dev/ttyUSB0',
    baudrate=115_200,
    timeout=3
)

##########################################################################

# Rectangle corners (latitude, longitude) - roughly 30x20 meter box
W, E = 17.642, 17.643
S, N = 46.782, 46.783

corner_1 = GPSPoint(N, W)
# corner_2 = GPSPoint(N, E)
# corner_3 = GPSPoint(S, E)
# corner_4 = GPSPoint(S, W)

BOGLAR_TEST_WP = GPSPoint(
    46.78077296310411,
    17.642497154244396
)

# Ordered loop of waypoints
waypoints = [BOGLAR_TEST_WP]

BOGLAR_DEFAULT_LAT = 46.78157378206975
BOGLAR_DEFAULT_LON = 17.643741699220094
boat_origin = GPSPoint(BOGLAR_DEFAULT_LAT, BOGLAR_DEFAULT_LON)


boat = GPSPoint(boat_origin.latitude, boat_origin.longitude)

def simulate_path_follower_fsm(boat: GPSPoint, waypoints: list[GPSPoint]):
    lat, lon, heading = gps_manager.get_live_location(timeout=1)
    boat.set_coordinates(GPSPoint(lat, lon))

    if not waypoints:
        return

    mode = Mode.TRACKING
    int_ey = 0
    error_psi_prev = 0
    psi = heading or np.pi / 2  # heading north


    U = 0.0

    current_wp = waypoints.pop(0)

    while True:
        dx = current_wp.Xn - boat.Xn
        dy = current_wp.Yn - boat.Yn
        dist = np.hypot(dx, dy)

        if dist < ARRIVAL_TOL_M:
            if not waypoints:
                logger.info("Reached final waypoint.")
                return
            current_wp = waypoints.pop(0)
            mode = Mode.TURNING
            int_ey = 0
            continue

        # Desired heading
        psi_d = np.arctan2(current_wp.Yn - boat.Yn, current_wp.Xn - boat.Xn)
        error_psi = np.arctan2(np.sin(psi - psi_d), np.cos(psi - psi_d))
        de_psi = (error_psi - error_psi_prev) / DT
        error_psi_prev = error_psi

        # Lateral error
        ey = np.sin(psi_d) * (boat.Xn - current_wp.Xn) - np.cos(psi_d) * (boat.Yn - current_wp.Yn)

        if mode == Mode.TURNING:
            U = max(U - SPEED_STEP, MIN_SPEED)
            delta = k1 * error_psi + k2 * de_psi
            rudder = np.clip(delta, -RUDDER_LIMIT_DEG, RUDDER_LIMIT_DEG)

            # Exit turning mode if aligned
            if np.abs(error_psi) < np.deg2rad(5) and np.abs(de_psi) < np.deg2rad(0.5):
                mode = Mode.TRACKING
                int_ey = 0

        elif mode == Mode.TRACKING:
            U = min(U + SPEED_STEP, CRUISE_SPEED)
            int_ey += ey * DT
            delta_PD = k1 * error_psi + k2 * de_psi
            delta_PI = k3 * ey + k4 * int_ey
            rudder = np.clip(delta_PD + delta_PI, -RUDDER_LIMIT_DEG, RUDDER_LIMIT_DEG)

        # Apply rudder effect
        rudder_rad = np.deg2rad(rudder)
        psi += -rudder_rad * 0.05  # simple model

        dx_local = U * np.cos(psi + rudder_rad) * DT
        dy_local = U * np.sin(psi + rudder_rad) * DT

        new_x = boat.Xn + dx_local
        new_y = boat.Yn + dy_local
        boat.set_from_Xn_Yn(new_x, new_y)


        serial_communication.rudder_angle = rudder
        serial_communication.surge_speed = 2000


simulate_path_follower_fsm(
    boat=boat,
    waypoints=waypoints
)


print("Done!")