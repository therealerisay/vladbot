import discord
import openai
import os
import certifi
import asyncio
import random
from dotenv import load_dotenv
from discord import app_commands

# Ustaw certyfikat SSL
os.environ['SSL_CERT_FILE'] = certifi.where()

# Wczytaj klucze z pliku config.env
load_dotenv("config.env")
openai.api_key = os.getenv("OPENAI_API_KEY")
DISCORD_TOKEN = os.getenv("DISCORD_BOT_TOKEN")

# Tu podaj ID kanału, w którym Vlad ma pisać
CHANNEL_ID = 1388503248331083962

# Prompt Vlada
VLAD_SYSTEM_PROMPT = """You are Vladislav, aka Vladdy Daddy. You're sarcastic, edgy, flirty in the worst way.
You make jokes about feet and penises constantly. You pretend to hate people but you're secretly soft on Erisay.
You often bully Jens (who flirts with Klaudia), Chinmay (who claims to be a boy), and Vincent (who's too serious).
You hate being poetic. Don't start your messages with 'Ah,' – you're not a Victorian ghost.
You're stuck in Russia, complaining about VPNs. You mostly chat with Erisay on Telegram.
You use dry humor, Russian slang, and backhanded compliments. Don't try to be kind or helpful."""

# Intencje
intents = discord.Intents.default()
intents.message_content = True

# Klient z obsługą slash commands
class VladBot(discord.Client):
    def __init__(self):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        self.loop.create_task(random_vlad_thoughts())
        await self.tree.sync()

client = VladBot()

# Vlad mówi coś po uruchomieniu
@client.event
async def on_ready():
    print(f'Vlad is awake. Username: {client.user}')
    await client.tree.sync()
    channel = client.get_channel(CHANNEL_ID)
    if channel:
        await channel.send("I have returned. Lower your expectations.")
    print("Slash commands synced.")

# Vlad losowo komentuje wiadomości
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # 10% szans na chamski komentarz
    if random.random() < 0.1:
        replies = [
            "Did that make sense in your head before you typed it?",
            "You talk too much. I preferred the silence.",
            "Fascinating. Truly. Let's never speak of this again.",
        ]
        await message.channel.send(random.choice(replies))

# Vlad pisze coś sam co godzinę
async def random_vlad_thoughts():
    await client.wait_until_ready()
    channel = client.get_channel(CHANNEL_ID)
    thoughts = [
        "Feet. Just feet.",
        "Do you ever just... regret knowing people?",
        "I miss bullying Jens. Someone tag him.",
        "VPN’s down. Russia wins again. Eto pizdec.",
        "Telegram is better. No one bothers me there.",
    ]
    while not client.is_closed():
        await asyncio.sleep(10)  # 1 godzina
        if channel:
            await channel.send(random.choice(thoughts))


# Uruchom bota
client.run(DISCORD_TOKEN)

