import discord
from discord.ext import commands
import random

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

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

    @commands.command(name="8ball")
    async def eightball(self, ctx, *, question):
        responses = [
            "Yes.", "No.", "Maybe.",
            "Definitely.", "I don't think so.",
            "Ask again later."
        ]
        await ctx.send(f"🎱 {random.choice(responses)}")

    @commands.command()
    async def choose(self, ctx, *, options: str):
        choices = options.split(",")
        await ctx.send(f"I choose: {random.choice(choices).strip()}")

    @commands.command()
    async def say(self, ctx, *, message):
        await ctx.send(message)


async def setup(bot):
    await bot.add_cog(Fun(bot))
