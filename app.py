# app.py - Smart Viewing Scheduler (Laila's part: form, validation, routes)
from datetime import datetime
from flask import Flask, render_template, request

app = Flask(__name__)

MIN_DURATION = 5     # minutes
MAX_DURATION = 240   # minutes
MAX_PROPERTIES = 8


def blank_property():
    return {"title": "", "address": "", "duration": "30"}


def parse_tour_form(form):
    """Read the submitted form, validate it, and return (tour, properties, errors).

    tour       -> cleaned data (only useful when errors is empty)
    properties -> the rows exactly as typed, so we can refill the form
    errors     -> list of messages to show the user
    """
    errors = []

    start_location = form.get("start_location", "").strip()
    start_time = form.get("start_time", "").strip()

    # 1. Starting point
    if not start_location:
        errors.append("Enter a starting address or landmark.")

    # 2. Tour start time (HH:MM)
    try:
        datetime.strptime(start_time, "%H:%M")
    except ValueError:
        errors.append("Pick a valid tour start time.")

    # 3. Property rows (the form sends parallel lists)
    titles = form.getlist("title")
    addresses = form.getlist("address")
    durations = form.getlist("duration")

    properties = []
    cleaned_properties = []
    for number, (title, address, duration) in enumerate(
        zip(titles, addresses, durations), start=1
    ):
        title, address, duration = title.strip(), address.strip(), duration.strip()
        properties.append({"title": title, "address": address, "duration": duration})

        if not (title or address):          # completely empty row -> ignore it
            continue

        row_ok = True
        if not title:
            errors.append(f"Property {number}: add a title.")
            row_ok = False
        if not address:
            errors.append(f"Property {number}: add an address.")
            row_ok = False
        if not duration.isdigit():
            errors.append(f"Property {number}: viewing time must be a whole number of minutes.")
            row_ok = False
        elif not MIN_DURATION <= int(duration) <= MAX_DURATION:
            errors.append(
                f"Property {number}: viewing time must be between "
                f"{MIN_DURATION} and {MAX_DURATION} minutes."
            )
            row_ok = False

        if row_ok:
            cleaned_properties.append(
                {"title": title, "address": address, "duration": int(duration)}
            )

    if not any(p["title"] or p["address"] for p in properties):
        errors.append("Add at least one property to visit.")
    if len(properties) > MAX_PROPERTIES:
        errors.append(f"You can add up to {MAX_PROPERTIES} properties.")

    if not properties:
        properties = [blank_property()]

    tour = {
        "start_location": start_location,
        "start_time": start_time,
        "properties": cleaned_properties,
    }
    return tour, properties, errors


@app.route("/")
def index():
    return render_template(
        "index.html",
        tour=None,
        errors=[],
        form={"start_location": "", "start_time": "09:00"},
        properties=[blank_property()],
        max_properties=MAX_PROPERTIES,
    )


@app.route("/plan", methods=["POST"])
def plan():
    tour, properties, errors = parse_tour_form(request.form)

    if errors:
        return render_template(
            "index.html",
            tour=None,
            errors=errors,
            form=request.form,
            properties=properties,
            max_properties=MAX_PROPERTIES,
        ), 400

    # TODO (teammates): pass `tour` to Syazwan's Distance Matrix + route
    # optimisation code, then to Adha's timeline code.
    return render_template(
        "index.html",
        tour=tour,
        errors=[],
        form=request.form,
        properties=properties,
        max_properties=MAX_PROPERTIES,
    )


if __name__ == "__main__":
    app.run(debug=True)
