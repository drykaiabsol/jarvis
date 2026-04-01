import os
from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
TWITCH_CLIENT_ID = os.getenv("TWITCH_CLIENT_ID")
TWITCH_CLIENT_SECRET = os.getenv("TWITCH_CLIENT_SECRET")

STUDY_CHANNELS = {
    "25/5":  int(os.getenv("POMODORO_25_CHANNEL", "0")),
    "50/10": int(os.getenv("POMODORO_50_CHANNEL", "0")),
    "90/20": int(os.getenv("POMODORO_90_CHANNEL", "0")),
}
STUDY_TEXT_CHANNEL = int(os.getenv("STUDY_TEXT_CHANNEL", "0"))
TWITCH_ANNOUNCE_CHANNEL = int(os.getenv("TWITCH_ANNOUNCE_CHANNEL", "0"))

TWITCH_STREAMER = os.getenv("TWITCH_STREAMER", "drykai_")