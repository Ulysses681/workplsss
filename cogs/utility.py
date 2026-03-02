import discord
from discord.ext import commands
import time
import datetime

class Utility(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.start_time = time.time()
        self.afk_users = {}
    # ================= HELP COMMAND =================
    @commands.command()
    async def help(self, ctx):
        embed = discord.Embed(
            title="📜 Bot Commands",
            description="Here are all available commands:",
            color=discord.Color.green()
        )

        embed.add_field(
            name="🛡 Moderation",
            value="""
^kick <user> - Kick a member
^ban <user> - Ban a member
^timeout <user> <minutes> - Timeout a member
^clear <amount> - Delete messages
""",
            inline=False
        )

        embed.add_field(
            name="💰 Economy",
            value="""
^balance - Check balance
^daily - Daily reward
^work - Earn coins
^leaderboard - Top users
""",
            inline=False
        )

        embed.add_field(
            name="🎉 Fun",
            value="""
^coinflip - Flip a coin
^8ball <question> - Ask the magic 8ball
^dice - Roll a dice
^roll <number> - Roll custom number
^rps <choice> - Rock Paper Scissors
^choose <options> - Bot chooses
^joke - Random joke
^roast <user> - Roast someone
^ship <user1> <user2> - Compatibility
^poll <question> - Create poll
^math - Random math problem
^quote - Random quote
^animal - Animal fact
""",
            inline=False
        )

        embed.add_field(
            name="🔧 Utility",
            value="""
^ping - Check latency
^userinfo <user> - User info
^serverinfo - Server info
^avatar <user> - Get avatar
^botinfo - Bot stats
^membercount - Server member count
^roleinfo <role> - Role details
^channelinfo - Channel details
^invite - Bot invite link
^uptime - Bot uptime
^afk <reason> - Set AFK status
""",
            inline=False
        )

        await ctx.send(embed=embed)

    # ================= BASIC UTILITY =================
    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f"🏓 Pong! {round(self.bot.latency * 1000)}ms")

    @commands.command()
    async def userinfo(self, ctx, member: discord.Member=None):
        member = member or ctx.author
        embed = discord.Embed(title="User Info", color=discord.Color.blue())
        embed.add_field(name="Name", value=member.name)
        embed.add_field(name="ID", value=member.id)
        embed.add_field(name="Joined Server", value=member.joined_at.strftime("%Y-%m-%d"))
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
    async def avatar(self, ctx, member: discord.Member=None):
        member = member or ctx.author
        embed = discord.Embed(title=f"{member.name}'s Avatar")
        embed.set_image(url=member.avatar.url)
        await ctx.send(embed=embed)

    @commands.command()
    async def botinfo(self, ctx):
        embed = discord.Embed(title="Bot Info", color=discord.Color.orange())
        embed.add_field(name="Servers", value=len(self.bot.guilds))
        embed.add_field(name="Users", value=len(self.bot.users))
        embed.add_field(name="Latency", value=f"{round(self.bot.latency * 1000)}ms")
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
        embed.add_field(name="Category", value=channel.category)
        await ctx.send(embed=embed)

    @commands.command()
    async def invite(self, ctx):
        await ctx.send("Add me using your bot invite link from Discord Developer Portal.")

    @commands.command()
    async def uptime(self, ctx):
        uptime_seconds = int(time.time() - self.start_time)
        uptime_string = str(datetime.timedelta(seconds=uptime_seconds))
        await ctx.send(f"⏳ Uptime: {uptime_string}")

    @commands.command()
    async def afk(self, ctx, *, reason="AFK"):
    self.afk_users[ctx.author.id] = reason
    await ctx.send(f"💤 {ctx.author.mention} is now AFK: {reason}")
    
    @commands.Cog.listener()
async def on_message(self, message):
    if message.author.bot:
        return

    # Remove AFK when user talks
    if message.author.id in self.afk_users:
        del self.afk_users[message.author.id]
        await message.channel.send("👋 Welcome back! AFK removed.")

    # Notify if mentioning AFK users
    for user in message.mentions:
        if user.id in self.afk_users:
            await message.channel.send(
                f"{user.name} is AFK: {self.afk_users[user.id]}"
            )

    await self.bot.process_commands(message)

async def setup(bot):
    await bot.add_cog(Utility(bot))
