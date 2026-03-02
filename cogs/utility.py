import discord
from discord.ext import commands
import time
import datetime
import asyncio
import platform

class Utility(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.start_time = time.time()
        self.afk_users = {}
        self.sniped_messages = {}
        self.welcome_enabled = False

    # ================= HELP =================
    @commands.command()
    async def help(self, ctx):
        embed = discord.Embed(
            title="📜 Bot Commands",
            description="Prefix: ^",
            color=discord.Color.green()
        )

        embed.add_field(
            name="🎉 Fun",
            value="""
^coinflip
^dice
^roll
^rps
^8ball
^choose
^say
""",
            inline=False
        )

        embed.add_field(
            name="🛡 Moderation",
            value="""
^lock
^unlock
^slowmode
^poll
""",
            inline=False
        )

        embed.add_field(
            name="🔧 Utility",
            value="""
^ping
^userinfo
^serverinfo
^avatar
^botinfo
^membercount
^uptime
^afk
^remind
""",
            inline=False
        )

        await ctx.send(embed=embed)

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f"🏓 Pong! {round(self.bot.latency * 1000)}ms")

    @commands.command()
    async def botinfo(self, ctx):
        embed = discord.Embed(title="Bot Info", color=discord.Color.orange())
        embed.add_field(name="Servers", value=len(self.bot.guilds))
        embed.add_field(name="Users", value=len(self.bot.users))
        embed.add_field(name="Latency", value=f"{round(self.bot.latency * 1000)}ms")
        embed.add_field(name="Python Version", value=platform.python_version())
        await ctx.send(embed=embed)

    @commands.command()
    async def uptime(self, ctx):
        uptime_seconds = int(time.time() - self.start_time)
        uptime_string = str(datetime.timedelta(seconds=uptime_seconds))
        await ctx.send(f"⏳ Uptime: {uptime_string}")

    @commands.command()
    async def afk(self, ctx, *, reason="AFK"):
        self.afk_users[ctx.author.id] = reason
        await ctx.send(f"💤 {ctx.author.mention} is now AFK: {reason}")

    @commands.command()
    async def remind(self, ctx, seconds: int, *, message):
        await ctx.send(f"⏰ Reminder set for {seconds} seconds.")
        await asyncio.sleep(seconds)
        await ctx.send(f"🔔 {ctx.author.mention} Reminder: {message}")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        if message.author.id in self.afk_users:
            del self.afk_users[message.author.id]
            await message.channel.send("👋 Welcome back! AFK removed.")

        for user in message.mentions:
            if user.id in self.afk_users:
                await message.channel.send(
                    f"{user.name} is AFK: {self.afk_users[user.id]}"
                )

        await self.bot.process_commands(message)


async def setup(bot):
    await bot.add_cog(Utility(bot))
