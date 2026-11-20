"""A small parcel tracker demo for a courier service (lab 5 version)."""

import secrets
import shutil
import subprocess  # nosec B404
import sys
import tempfile
from datetime import date

STATUS_FLOW = ["Booked", "Picked Up", "In Transit",
               "Out for Delivery", "Delivered"]
WITH_COURIER = ("Picked Up", "In Transit")
BASE_COST = 50  # flat base fee
EXTRA_RATE_PER_KG = 30
parcels = {}


def book_parcel(sender, receiver, weight_kg, history=None):
    """Register a new parcel and record its id in an optional history list."""
    if history is None:
        history = []
    tracking_id = f"TRK{10001 + len(parcels)}"
    parcels[tracking_id] = {
        "sender": sender,
        "receiver": receiver,
        "weight": weight_kg,
        "status": 0,
        "booked": str(date.today()),
    }
    history.append(tracking_id)
    return tracking_id


def advance_status(tracking_id):
    """Push a parcel to its next delivery stage and return that stage."""
    parcel = parcels[tracking_id]
    if parcel["status"] < len(STATUS_FLOW) - 1:
        parcel["status"] += 1
    return STATUS_FLOW[parcel["status"]]


def track_parcel(tracking_id):
    """Describe a parcel's route and current stage, or report an unknown id."""
    try:
        parcel = parcels[tracking_id]
    except KeyError:
        return f"Unknown tracking id {tracking_id}"
    route = f"{parcel['sender']} -> {parcel['receiver']}"
    return f"{route}: {STATUS_FLOW[parcel['status']]}"


def is_with_courier(tracking_id):
    """Tell whether a parcel is currently picked up or in transit."""
    status = STATUS_FLOW[parcels[tracking_id]["status"]]
    return status in WITH_COURIER


def shipping_cost(weight_kg):
    """Work out the shipping cost for a parcel weighing weight_kg."""
    cost = BASE_COST
    if weight_kg > 1:
        cost += (weight_kg - 1) * EXTRA_RATE_PER_KG
    return round(cost, 2)


def generate_otp():
    """Create a random 4-digit delivery OTP."""
    return secrets.randbelow(9000) + 1000


def label_path():
    """Create a temporary file for a parcel label and return its path."""
    # Helper kept for the lab: not called by the demo
    with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as label:
        return label.name


def ping_hub(hub_address):
    """Ping a courier hub once and return the raw command output."""
    # Helper kept for the lab: not called by the demo
    count_flag = "-n" if sys.platform == "win32" else "-c"
    ping_executable = shutil.which("ping")
    if ping_executable is None:
        raise FileNotFoundError("ping executable was not found on PATH")
    return subprocess.check_output(
        [ping_executable, count_flag, "1", hub_address],
        shell=False,  # nosec B603
    )


def main():
    """Run the parcel-tracking demonstration."""
    first = book_parcel("Bengaluru Books", "Ravi Kumar", 2.5)
    second = book_parcel("Gadget Hub", "Sneha Rao", 0.8)
    third = book_parcel("Spice Store", "Imran Khan", 4)
    for tracking_id, steps in ((first, 2), (second, 1), (third, 6)):
        for _ in range(steps):
            advance_status(tracking_id)
    for tracking_id in (first, second, third):
        print(track_parcel(tracking_id))
        print("  with courier:", is_with_courier(tracking_id))
        print("  cost:", shipping_cost(parcels[tracking_id]["weight"]))
    print(track_parcel("TRK00000"))  # unknown id
    print("Delivery OTP for", third, "is", generate_otp())
    print("Parcels booked today:", len(parcels))


if __name__ == "__main__":
    main()
