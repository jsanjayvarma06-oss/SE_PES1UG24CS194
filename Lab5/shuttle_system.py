"""Campus Shuttle Timetable & Fleet Tracker.

Logs passenger counts per trip, computes average loads, flags
under-used routes and syncs fleet data to a JSON file.
"""

import json
import secrets
from datetime import datetime

MIN_CAPACITY = 10
MAX_CAPACITY = 60
DRIVERS = ["Prakash", "Leela", "Imran", "Tom"]

routes = {
    "R1": {"name": "Main Gate - Library", "trips": []},
    "R2": {"name": "Hostel - Sports Complex", "trips": []},
    "R3": {"name": "Admin Block - Metro", "trips": []},
}


def add_trip_log(route_id, passenger_count, logs=None):
    """Record a trip's passenger count and append a log entry."""
    if logs is None:
        logs = []
    if route_id not in routes:
        raise KeyError(f"Unknown route: {route_id}")
    if not isinstance(passenger_count, int) or isinstance(passenger_count,
                                                          bool):
        raise TypeError(f"Passenger count must be an int, "
                        f"got {passenger_count!r}")
    if not 0 <= passenger_count <= MAX_CAPACITY:
        raise ValueError(f"Passenger count {passenger_count} out of range "
                         f"0-{MAX_CAPACITY}")
    routes[route_id]["trips"].append(passenger_count)
    logs.append(f"{datetime.now()}: {route_id} carried {passenger_count}")
    return logs


def remove_route(route_id):
    """Remove a route if it exists; return True if removed."""
    return routes.pop(route_id, None) is not None


def average_load(route_id):
    """Return the average passenger load, or None if no trips."""
    if route_id not in routes:
        return None
    trips = routes[route_id]["trips"]
    if not trips:
        return None
    return sum(trips) / len(trips)


def underused_routes():
    """Return route IDs whose average load is below MIN_CAPACITY."""
    flagged = []
    for route_id in routes:
        avg = average_load(route_id)
        if avg is not None and avg < MIN_CAPACITY:
            flagged.append(route_id)
    return flagged


def assign_driver():
    """Pick a driver at random."""
    return secrets.choice(DRIVERS)


def sync_fleet_data(path="fleet.json"):
    """Write fleet data to disk and reload it to verify the round trip."""
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(routes, handle, indent=2)
    with open(path, "r", encoding="utf-8") as handle:
        loaded = json.load(handle)
    routes.clear()
    routes.update(loaded)


def safe_log(route_id, passenger_count, logs):
    """Log a trip, reporting invalid input instead of crashing."""
    try:
        add_trip_log(route_id, passenger_count, logs)
    except (KeyError, TypeError, ValueError) as err:
        print("Rejected trip:", err)


def main():
    """Run a demo of the shuttle tracker."""
    logs = []
    safe_log("R1", 32, logs)
    safe_log("R1", 28, logs)
    safe_log("R2", 4, logs)
    safe_log("R2", -6, logs)
    safe_log("R3", "full", logs)

    print("Driver for R1:", assign_driver())
    print("Underused:", underused_routes())
    print("R1 average:", average_load("R1"))

    sync_fleet_data()
    remove_route("R3")

    choice = input("Route to look up (Enter for R2): ").strip().upper()
    choice = choice or "R2"
    if choice in routes:
        print("Trips on", choice, ":", routes[choice]["trips"])
    else:
        print("No such route:", choice)

    r3_avg = average_load("R3")
    print("R3 average:", r3_avg if r3_avg is not None else "no data")


if __name__ == "__main__":
    main()
