# main.py
# Entry point

# main.py
from datetime import datetime
import time
from loguru import logger
from memory_profiler import profile

from gps_coordinate import GPSPoint, CircularGeofence
from managers import CANManager, GPSManager, MockGPSManager
from ship import ShipTaskManager, ShipPosition, ShipState

W = 17.6420
E = 17.6423
S = 46.7820
N = 46.7823

@profile
def main():
    logger.info(f"Starting application at {datetime.now()}")

    # --- Configuration ---
    LOOP_HZ = 5
    LOOP_INTERVAL = 1.0 / LOOP_HZ
    GEOFENCE_RADIUS_M = 100_000_000
    LELLE_LAT = 46.782290404768425
    LELLE_LON = 17.645052779259068

    ao_center = GPSPoint(LELLE_LAT, LELLE_LON)
    """Area of Operation - Geofence Center"""

    # NOTE: What to do when getting outside is unclear.
    #   TODO: the switch that toggles Autonomy modul control is unimplemented yet,
    #   maybe use that here as well?
    geofence = CircularGeofence(
        center=ao_center,
        radius_m=GEOFENCE_RADIUS_M  # 100m
    )

    # --- Init Modules ---
    gps_manager = MockGPSManager()
    ship_position = ShipPosition(geofence=geofence, gps_manager=gps_manager)
    ship_position.start_auto_update()

    can_manager = CANManager()
    ship_state = ShipState(ship_position)
    task_manager = ShipTaskManager(ship_state)

    # --- Main Loop ---
    try:
        while True:
            # Get latest CAN data (CANManager has a read interface)
            # expected: dict w/ u, v, r, rudder_angle, engine_rpm
            can_data = can_manager.read_state()  # returns { "u": float, "v": float, "r": float, "rudder_angle": float, "engine_rpm": float }

            # updates:
            #   self.position: ShipPosition u,v,r
            #   self.rudder_angle, self.engine_rpm
            ship_state.update_from_can(**can_data)

            # Get current route segment and compute control outputs
            # NOTE: shipstate does a lot of compute, hidden behind properties!
            segment = ship_state.current_segment
            if not segment:
                # insufficient, can lose control by soft-locking controls if the last point is not "port"!
                # TODO: we already store point of origin for Xb, Yb body referenced coords.
                #   maybe go back to point of origin?...
                logger.warning("No valid route segment available.")
                time.sleep(LOOP_INTERVAL)
                continue

            rudder_cmd, rpm_cmd = task_manager.update_control()

            # Send control commands via CAN
            can_manager.send_control(
                rudder=rudder_cmd,
                rpm=rpm_cmd
            )

            time.sleep(LOOP_INTERVAL)
            raise KeyboardInterrupt("One iter over.")

    except KeyboardInterrupt:
        logger.info("KeyboardInterrupt detected, shutting down...")
        ship_position.stop_auto_update()


if __name__ == "__main__":
    main()
