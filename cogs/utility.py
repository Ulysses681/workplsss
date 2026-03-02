import discord
from discord.ext import commands
import time
import datetime
import random
import asyncio
import platform

class Utility(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.start_time = time.time()
        self.afk_users = {}
        self.sniped_messages = {}
        self.welcome_enabled = False

    # ================= HELP COMMAND =================
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
^roll <number>
^rps <choice>
^choose <option1, option2>
^8ball <question>
^say <message>
""",
            inline=False
        )

        embed.add_field(
            name="🔧 Utility",
            value="""
^ping
^userinfo <user>
^serverinfo
^avatar <user>
^botinfo
^membercount
^roleinfo <role>
^channelinfo
^uptime
^afk <reason>
^remind <seconds> <message>
^calc <math>
^timestamp
""",
            inline=False
        )

        embed.add_field(
            name="🛡 Moderation",
            value="""
^lock
^unlock
^slowmode <seconds>
^poll <question>
^snipe
^welcome
""",
            inline=False
        )

        await ctx.send(embed=embed)

    # ================= FUN =================
    @commands.command()
    async def coinflip(self, ctx):
        await ctx.send(f"🪙 {random.choice(['Heads', 'Tails'])}")

    @commands.command()
    async def dice(self, ctx):
        await ctx.send(f"🎲 You rolled: {random.randint(1,6)}")

    @commands.command()
    async def roll(self, ctx, number: int):
        if number <= 0:
            return await ctx.send("Number must be greater than 0.")
        await ctx.send(f"🎲 You rolled: {random.randint(1, number)}")

    @commands.command()
    async def rps(self, ctx, choice: str):
        options = ["rock", "paper", "scissors"]
        bot_choice = random.choice(options)
        choice = choice.lower()

        if choice not in options:
            return await ctx.send("Choose rock, paper, or scissors.")

        await ctx.send(f"You chose {choice}, I chose {bot_choice}!")

    @commands.command()
    async def choose(self, ctx, *, options: str):
        choices = options.split(",")
        await ctx.send(f"I choose: {random.choice(choices).strip()}")

    @commands.command(name="8ball")
    async def eightball(self, ctx, *, question):
        responses = [
            "Yes.", "No.", "Maybe.",
            "Definitely.", "I don't think so.",
            "Ask again later."
        ]
        await ctx.send(f"🎱 {random.choice(responses)}")

    @commands.command()
    async def say(self, ctx, *, message):
        await ctx.send(message)

    # ================= UTILITY =================
    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f"🏓 Pong! {round(self.bot.latency * 1000)}ms")

    @commands.command()
    async def userinfo(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        embed = discord.Embed(title="User Info", color=discord.Color.blue())
        embed.add_field(name="Name", value=member.name)
        embed.add_field(name="ID", value=member.id)
        embed.add_field(name="Joined", value=member.joined_at.strftime("%Y-%m-%d"))
        if member.avatar:
            embed.set_thumbnail(url=member.avatar.url)
        await ctx.send(embed=embed)

    @commands.command()
    async def serverinfo(self, ctx):
        guild = ctx.guild
        embed = discord.Embed(title="Server Info", color=discord.Color.purple())
        embed.add_field(name="Name", value=guild.name)
        embed.add_field(name="Members", value=guild.member_count)
        embed.add_field(name="Owner", value=guild.owner)
        if guild.icon:
            embed.set_thumbnail(url=guild.icon.url)
        await ctx.send(embed=embed)

    @commands.command()
    async def avatar(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        embed = discord.Embed(title=f"{member.name}'s Avatar")
        if member.avatar:
            embed.set_image(url=member.avatar.url)
        await ctx.send(embed=embed)

    @commands.command()
    async def botinfo(self, ctx):
        embed = discord.Embed(title="Bot Info", color=discord.Color.orange())
        embed.add_field(name="Servers", value=len(self.bot.guilds))
        embed.add_field(name="Users", value=len(self.bot.users))
        embed.add_field(name="Latency", value=f"{round(self.bot.latency * 1000)}ms")
        embed.add_field(name="Python Version", value=platform.python_version())
        await ctx.send(embed=embed)

    @commands.command()
    async def membercount(self, ctx):
        await ctx.send(f"👥 Members: {ctx.guild.member_count}")

    @commands.command()
    async def roleinfo(self, ctx, role: discord.Role):
        embed = discord.Embed(title="Role Info", color=role.color)
        embed.add_field(name="Name", value=role.name)
        embed.add_field(name="ID", value=role.id)
        embed.add_field(name="Members", value=len(role.members))
        await ctx.send(embed=embed)

    @commands.command()
    async def channelinfo(self, ctx):
        channel = ctx.channel
        embed = discord.Embed(title="Channel Info", color=discord.Color.teal())
        embed.add_field(name="Name", value=channel.name)
        embed.add_field(name="ID", value=channel.id)
        embed.add_field(name="Category", value=str(channel.category))
        await ctx.send(embed=embed)

    @commands.command()
    async def uptime(self, ctx):
        uptime_seconds = int(time.time() - self.start_time)
        uptime_string = str(datetime.timedelta(seconds=uptime_seconds))
        await ctx.send(f"⏳ Uptime: {uptime_string}")

    @commands.command()
    async def calc(self, ctx, *, expression):
        try:
            result = eval(expression)
            await ctx.send(f"🧮 Result: {result}")
        except:
            await ctx.send("Invalid math expression.")

    @commands.command()
    async def timestamp(self, ctx):
        now = int(time.time())
        await ctx.send(f"<t:{now}:F>")

    # ================= MODERATION =================
    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def lock(self, ctx):
        await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
        await ctx.send("🔒 Channel locked.")

    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def unlock(self, ctx):
        await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
        await ctx.send("🔓 Channel unlocked.")

    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def slowmode(self, ctx, seconds: int):
        await ctx.channel.edit(slowmode_delay=seconds)
        await ctx.send(f"🐢 Slowmode set to {seconds} seconds.")

    @commands.command()
    async def poll(self, ctx, *, question):
        embed = discord.Embed(title="📊 Poll", description=question)
        message = await ctx.send(embed=embed)
        await message.add_reaction("👍")
        await message.add_reaction("👎")

    # ================= AFK =================
    @commands.command()
    async def afk(self, ctx, *, reason="AFK"):
        self.afk_users[ctx.author.id] = reason
        await ctx.send(f"💤 {ctx.author.mention} is now AFK: {reason}")

    # ================= REMINDER =================
    @commands.command()
    async def remind(self, ctx, seconds: int, *, message):
        await ctx.send(f"⏰ Reminder set for {seconds} seconds.")
        await asyncio.sleep(seconds)
        await ctx.send(f"🔔 {ctx.author.mention} Reminder: {message}")

    # ================= SNIPE =================
    @commands.Cog.listener()
    async def on_message_delete(self, message):
        self.sniped_messages[message.channel.id] = (message.content, message.author)

    @commands.command()
    async def snipe(self, ctx):
        msg = self.sniped_messages.get(ctx.channel.id)
        if not msg:
            return await ctx.send("Nothing to snipe.")

        content, author = msg
        embed = discord.Embed(description=content, color=discord.Color.red())
        embed.set_author(name=str(author))
        await ctx.send(embed=embed)

    # ================= WELCOME =================
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def welcome(self, ctx):
        self.welcome_enabled = not self.welcome_enabled
        status = "enabled" if self.welcome_enabled else "disabled"
        await ctx.send(f"Welcome messages {status}.")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if self.welcome_enabled:
            channel = member.guild.system_channel
            if channel:
                await channel.send(f"👋 Welcome {member.mention}!")

    # ================= MESSAGE LISTENER =================
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
