"""This module register all the apps of the project."""

from typing import List, Type

from src import exceptions
from src.alanwake.main import AlanWake
from src.models import App

APPS: List[Type[App]] = []


def register_app(app_class: Type[App]) -> None:
    """Register an app to use with the program.

    :param app_class: The app class to register
    """
    if not issubclass(app_class, App):
        raise exceptions.AppRegistrationException("The app must subclass App")
    if app_class in APPS:
        raise exceptions.AppRegistrationException("The app is already registered")
    if any(app.name == app_class.name for app in APPS):
        raise exceptions.AppRegistrationException(f"The name {app_class.name} is already taken")
    APPS.append(app_class)


register_app(AlanWake)
