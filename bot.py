import os
import discord
import sqlite3
from discord.ext import commands
import asyncio

# ================= TOKEN =================
token = os.getenv("TOKEN")
if not token:
    raise ValueError("TOKEN environment variable missing!")

# ================= INTENTS =================
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(
    command_prefix="^",
    intents=intents,
    help_command=None  # Disable default help
)

# ================= DATABASE =================
conn = sqlite3.connect("database.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS economy (
    user_id INTEGER PRIMARY KEY,
    balance INTEGER DEFAULT 0
)
""")
conn.commit()

bot.db = conn  # allow cogs to access database

# ================= EVENTS =================
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    print("Bot is fully online.")

# ================= LOAD COGS =================
async def load_cogs():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")

async def main():
    async with bot:
        await load_cogs()
        await bot.start(token)

# ================= START =================
asyncio.run(main())
