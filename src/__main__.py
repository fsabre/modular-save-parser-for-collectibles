"""This module defines the main entrypoint for the project."""

import sys

from src.apps import APPS

if len(sys.argv) != 2:
    sys.exit("Usage: python -m src APP_NAME")
chosen_app_name: str = sys.argv[1]

# Choose the app to use

app_class = next((app for app in APPS if app.name == chosen_app_name), None)
if app_class is None:
    msg = f"No app with name '{chosen_app_name}' in {[app.name for app in APPS]}"
    sys.exit(msg)

app = app_class()

# Run the parsing script

app.parse()

# Display the result

for series in app.series.values():
    print(f"=== {series.name} ===")
    if series.description != "":
        print(series.description)
    total_count: int = len(series.full_set)
    obtained_count: int = len(series.obtained_set)
    print(f"Completion : {obtained_count}/{total_count}")
    missing_list = list(series.find_missing())
    if len(missing_list) > 0:
        if all(id.isdigit() for id in missing_list):
            missing_list.sort(key=lambda id: int(id))
        else:
            missing_list.sort()
        print(f"The missing ones are : {', '.join(missing_list)}")
