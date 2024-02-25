"""This module defines an app for the Alan Wake game."""

from typing import Dict, Iterator, List

from src import exceptions
from src.constants import STEAM_USERDATA
from src.models import CollectibleSeries, App

NAMED_SECTIONS_COUNT = 10
SECTION_TITLE_TO_SERIES_NAME: Dict[str, str] = {
    "CANPYRAMIDS": "can_pyramids",
    "CHESTS": "chests",
    "COCONUTSONGS": "coconut_songs",
    "DLC1_ALARMCLOCKS": "alarm_clocks",
    "DLC1_CARDBOARDCUTOUTS": "cardboard_cutouts",
    "DLC2_NIGHTSPRINGSVIDEOGAMES": "video_games",
    "RADIOSHOWS": "radio_shows",
    "SIGNS": "signs",
    "THERMOS": "thermos",
    "TVSHOWS": "tv_shows",
}


class AlanWake(App):
    name = "alanwake"
    series: Dict[str, CollectibleSeries] = {
        "can_pyramids": CollectibleSeries(
            name="Can pyramids",
            full_set=set(str(i) for i in range(1, 12 + 1)),
        ),
        "chests": CollectibleSeries(
            name="Chests",
            full_set=set(str(i) for i in range(1, 30 + 1)),
        ),
        "coconut_songs": CollectibleSeries(
            name="Coconuts songs",
            full_set=set(),
        ),
        "alarm_clocks": CollectibleSeries(
            name="Alarm clocks",
            full_set=set(str(i) for i in range(1, 10 + 1)),
        ),
        "cardboard_cutouts": CollectibleSeries(
            name="Cardboard cutouts",
            full_set=set(str(i) for i in range(1, 6 + 1)),
        ),
        "video_games": CollectibleSeries(
            name="Video games",
            full_set=set(str(i) for i in range(1, 10 + 1)),
        ),
        "radio_shows": CollectibleSeries(
            name="Radio shows",
            full_set=set(str(i) for i in range(1, 11 + 1)),
        ),
        "signs": CollectibleSeries(
            name="Signs",
            full_set=set(str(i) for i in range(1, 25 + 1)),
        ),
        "thermos": CollectibleSeries(
            name="Thermos",
            full_set=set(str(i) for i in range(1, 101 + 1) if i != 90),  # For some reason, there's no thermos 90 ?
            description="Mind the fact that the provided ID are in-game ID. Those may follow the logical progression "
                        "in the story but it's not proven. For example, thermos 77 is the 73rd in online guides, and "
                        "thermos 87 is 83rd.\n"
                        "Also, it seems that there's no thermos 90."
        ),
        "tv_shows": CollectibleSeries(
            name="TV shows",
            full_set=set(str(i) for i in range(1, 14 + 1)),
        ),
    }

    def parse(self) -> None:
        config_path = STEAM_USERDATA / r"128617914\108710\remote\config"
        try:
            content: bytes = config_path.read_bytes()
        except FileNotFoundError:
            raise exceptions.FileNotFoundException()

        # The file is full of gibberish, except ten titled sections for collectibles.
        # Those sections are defined like this :
        #   - 1 byte for the size of the title
        #   - 3 empty bytes
        #   - X bytes for the title
        #   - 1 byte for count of obtained collectibles
        #   - 1 byte for each ID of obtained collectibles

        # Let's find where to start
        # Using the title CANPYRAMIDS allow us to start rapidly.
        start_pos: int = content.find("CANPYRAMIDS".encode("ascii"))
        if start_pos == -1:
            raise exceptions.ParsingError("Could not find where to start")

        # Create a convenient iterator to consume the file byte-per-byte
        feed: Iterator[int] = iter(content)
        # Drop the start of the file
        # We leave four bytes before the title name, so we can consume the title size.
        for _ in range(start_pos - 4):
            next(feed)

        # Iterate on all the titled sections
        for i in range(NAMED_SECTIONS_COUNT):
            self._parse_section(feed)

    def _parse_section(self, feed: Iterator[int]) -> None:
        """Consume the byte feed to read just one section.
        Fill the CollectibleSeries objects with the relevant data.

        :param feed: the byte feed to read
        """
        # Consume the title size
        title_size = next(feed)

        # Consume the blank bytes
        for _ in range(3):
            next(feed)

        # Consume the title
        title = ""
        for _ in range(title_size):
            title += chr(next(feed))

        # Consume the obtained count
        obtained_count = next(feed)

        # Consume the obtained list
        obtained: List[str] = []
        for _ in range(obtained_count):
            obtained.append(str(next(feed)))

        # Update the series
        series_name = SECTION_TITLE_TO_SERIES_NAME.get(title)
        if series_name is None:
            print(f"Warning: Unknown {title=}")
            return
        collectible_series = self.series[series_name]
        collectible_series.mark_more_as_obtained(obtained)
