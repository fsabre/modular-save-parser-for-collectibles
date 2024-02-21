"""This module defines exceptions for the project."""


class MoSaPException(Exception):
    """Base exception for MoSaP"""


class AppRegistrationException(MoSaPException):
    """Raised when an error occur on app registration."""
    pass


class FileNotFoundException(MoSaPException):
    """Raised when a needed file is not found."""
    pass


class ParsingError(MoSaPException):
    """Raised when the parsing of a save file failed."""
    pass
