"""This module defines models for the project."""

import abc
from dataclasses import dataclass, field
from typing import Set, Iterable, Dict


@dataclass
class CollectibleSeries:
    """The entire collection of a kind of collectibles.

    Each one is represented by a distinct string. Then, some of them can be marked as obtained.
    """
    name: str
    full_set: Set[str]
    obtained_set: Set[str] = field(default_factory=set)

    def mark_as_obtained(self, collectible: str) -> None:
        """Mark one collectible as obtained.

        :param collectible: the string identifying the collectible
        """
        self.obtained_set.add(collectible)

    def mark_more_as_obtained(self, collectibles: Iterable[str]) -> None:
        """Mark multiple collectibles as obtained.

        :param collectibles: the collection of strings identifying each collectible
        """
        self.obtained_set.update(collectibles)

    def find_missing(self) -> Set[str]:
        """Return a set containing the non-obtained collectibles.

        :return: a set of the collectibles that are not in the obtained set"""
        return self.full_set.difference(self.obtained_set)


class App(abc.ABC):
    # The name of the app
    name: str = NotImplemented
    # A dict mapping their name to the collectible series provided by the app
    series: Dict[str, CollectibleSeries] = NotImplemented

    @abc.abstractmethod
    def parse(self) -> None:
        """Parse the save file and populate the series dict with obtained collectibles."""
        pass
