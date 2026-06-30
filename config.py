import os
from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
TWITCH_CLIENT_ID = os.getenv("TWITCH_CLIENT_ID")
TWITCH_CLIENT_SECRET = os.getenv("TWITCH_CLIENT_SECRET")
TWITCH_ANNOUNCE_CHANNEL = int(os.getenv("TWITCH_ANNOUNCE_CHANNEL", "0"))
TWITCH_STREAMER = os.getenv("TWITCH_STREAMER", "drykai_")
MEMBER_ROLE_NAME = os.getenv("MEMBER_ROLE_NAME", "membre")