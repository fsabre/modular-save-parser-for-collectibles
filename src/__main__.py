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
    missing = series.find_missing()
    missing_count = len(missing)
    print(f"{series.name} : {missing_count} missing ({', '.join(missing)})")
