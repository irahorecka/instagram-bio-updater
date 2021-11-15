"""
Simple file to write information to post on my Instagram's bio in 'bio.txt'.
"""

import os
from datetime import datetime

from pyowm import OWM


def main(owm_api_key):
    """Gets current weather data, build's IG bio, and writes IG bio to 'bio.txt'"""
    # Gets current part of day (e.g., afternoon).
    current_hour = datetime.now().hour
    time_of_day = get_part_of_day(current_hour)

    # Gets weather data from OpenWeatherMap.
    owm = OWM(owm_api_key)
    mgr = owm.weather_manager()
    toronto_weather = mgr.weather_at_place("Toronto,CA").weather
    sky_condition = toronto_weather.detailed_status
    sky_emoji = get_detailed_status_emoji(sky_condition)
    # Prepend emoji with whitespace if emoji was found.
    sky_emoji = " " + sky_emoji if sky_emoji else sky_emoji
    temp = toronto_weather.temperature("celsius")
    temp_feel = int(temp["feels_like"])

    # Updates IG bio and export bio to 'bio.txt'.
    ig_bio = build_ig_bio(time_of_day, sky_condition, sky_emoji, temp_feel)
    write_to_file("bio.txt", ig_bio)


def build_ig_bio(time_of_day, sky_cond, sky_emoji, temp_feel):
    """Builds IG bio."""
    return f"Back page of the internet.\n\nI look up and the {time_of_day} sky in Toronto is {sky_cond}{sky_emoji}.\nRight now it feels like... oh, about {temp_feel}C\u00b0."


def get_part_of_day(hour):
    """Gets part of day from hour."""
    return (
        "morning"
        if 5 <= hour <= 11
        else "afternoon"
        if 12 <= hour <= 17
        else "evening"
        if 18 <= hour <= 22
        else "night"
    )


def get_detailed_status_emoji(detailed_status):
    """Gets emoji from detailed weather status."""
    detailed_status = detailed_status.lower()
    # Stack most specific selectors near top.
    return (
        "🌨"
        if "snow" in detailed_status
        else "🌧"
        if "rain" in detailed_status or "shower" in detailed_status
        else "⛅️"
        if "broken cloud" in detailed_status
        else "☁️"
        if "cloud" in detailed_status
        else "☀️"
        if "sun" in detailed_status
        else ""
    )


def write_to_file(filepath, content):
    """Writes content to filepath."""
    with open(filepath, "w") as file:
        file.write(content)


if __name__ == "__main__":
    main(os.environ["PYOWM_API"])
