"""
Simple file to write information to post on my Instagram's bio in 'bio.txt'.
"""

import os
from datetime import datetime

from pyowm import OWM
from dotenv import load_dotenv

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
load_dotenv(dotenv_path=os.path.join(BASE_DIR, ".env"))


def main(owm_api_key):
    """Gets current weather data, build's IG bio, and writes IG bio to 'bio.txt'"""
    # Gets weather data from OpenWeatherMap.
    owm = OWM(owm_api_key)
    mgr = owm.weather_manager()
    toronto_weather = mgr.weather_at_place("Toronto,CA").weather

    # Gets current part of day (e.g., afternoon).
    current_hour = datetime.now().hour
    # Fetch sunrise and sunset times
    sunrise_hour = datetime.fromtimestamp(toronto_weather.sunrise_time()).hour
    sunset_hour = datetime.fromtimestamp(toronto_weather.sunset_time()).hour
    part_of_day = get_part_of_day(current_hour, sunrise_hour, sunset_hour)

    # Get sky condition and corresponding emoji
    sky_condition = toronto_weather.detailed_status
    sky_emoji = get_detailed_status_emoji(part_of_day, sky_condition)
    # Prepend emoji with whitespace if emoji was found.
    sky_emoji = " " + sky_emoji if sky_emoji else sky_emoji

    # Fetch temps
    temp = toronto_weather.temperature("celsius")
    temp_feel = int(round(temp["feels_like"], 0))

    # Updates IG bio and export bio to 'bio.txt'.
    ig_bio = build_ig_bio(part_of_day, sky_condition, sky_emoji, temp_feel)
    write_to_file(os.path.join(BASE_DIR, "bio.txt"), ig_bio)


def build_ig_bio(part_of_day, sky_cond, sky_emoji, temp_feel):
    """Builds IG bio."""
    return f"Back page of the internet.\n\nI look up this {part_of_day} and the Toronto sky looks like {sky_cond}{sky_emoji}.\nKinda feels like {temp_feel}\u00b0C."


def get_part_of_day(hour, sunrise_hour, sunset_hour):
    """Gets part of day from hour."""
    return (
        "morning"
        if sunrise_hour <= hour <= 11
        else "afternoon"
        if 12 <= hour <= sunset_hour
        else "evening"
        if sunset_hour + 1 <= hour <= 22
        else "night"
    )


def get_detailed_status_emoji(part_of_day, detailed_status):
    """Gets emoji from detailed weather status."""
    detailed_status = detailed_status.lower()
    # Stack most specific selectors near top.
    weather_key = (
        "clear"
        if "clear" in detailed_status
        else "partially-cloudy"
        if "broken cloud" in detailed_status or "scattered cloud" in detailed_status
        else "snow"
        if "snow" in detailed_status
        else "rain"
        if "rain" in detailed_status or "shower" in detailed_status
        else "cloudy"
        if "cloud" in detailed_status
        else ""
    )
    emoji_dict = {
        "morning": {
            "clear": "☀️",
            "partially-cloudy": "⛅️",
            "cloudy": "☁️",
            "rain": "🌧",
            "snow": "🌨",
        },
        "afternoon": {
            "clear": "☀️",
            "partially-cloudy": "⛅️",
            "cloudy": "☁️",
            "rain": "🌧",
            "snow": "🌨",
        },
        "evening": {
            "clear": "🌌",
            "partially-cloudy": "☁️🌌",
            "cloudy": "☁️",
            "rain": "🌧",
            "snow": "🌨",
        },
        "night": {
            "clear": "🌌",
            "partially-cloudy": "☁️🌌",
            "cloudy": "☁️",
            "rain": "🌧",
            "snow": "🌨",
        },
    }
    return emoji_dict[part_of_day].get(weather_key, "")


def write_to_file(filepath, content):
    """Writes content to filepath."""
    with open(filepath, "w") as file:
        file.write(content)


if __name__ == "__main__":
    main(os.environ["PYOWM_API"])
