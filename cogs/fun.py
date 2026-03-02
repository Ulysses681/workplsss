import discord
from discord.ext import commands
import random

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Coinflip
    @commands.command()
    async def coinflip(self, ctx):
        await ctx.send(random.choice(["Heads 🪙", "Tails 🪙"]))

    # 8ball
    @commands.command(name="8ball")
    async def eightball(self, ctx, *, question):
        responses = [
            "Yes.",
            "No.",
            "Maybe.",
            "Definitely.",
            "Ask again later.",
            "Absolutely not.",
            "100% yes."
        ]
        await ctx.send(random.choice(responses))

    # Say
    @commands.command()
    async def say(self, ctx, *, message):
        await ctx.send(message)

    # Dice roll
    @commands.command()
    async def dice(self, ctx):
        await ctx.send(f"🎲 You rolled: {random.randint(1,6)}")

    # Roll custom number
    @commands.command()
    async def roll(self, ctx, number: int):
        await ctx.send(f"🎯 Result: {random.randint(1, number)}")

    # Rock Paper Scissors
    @commands.command()
    async def rps(self, ctx, choice):
        options = ["rock", "paper", "scissors"]
        bot_choice = random.choice(options)

        if choice.lower() not in options:
            return await ctx.send("Choose rock, paper, or scissors.")

        if choice.lower() == bot_choice:
            result = "It's a tie!"
        elif (
            (choice == "rock" and bot_choice == "scissors") or
            (choice == "paper" and bot_choice == "rock") or
            (choice == "scissors" and bot_choice == "paper")
        ):
            result = "You win!"
        else:
            result = "You lose!"

        await ctx.send(f"I chose {bot_choice}. {result}")

    # Choose between options
    @commands.command()
    async def choose(self, ctx, *options):
        if len(options) < 2:
            return await ctx.send("Give at least 2 options.")
        await ctx.send(f"I choose: {random.choice(options)}")

    # Joke
    @commands.command()
    async def joke(self, ctx):
        jokes = [
            "Why did the programmer quit? Because he didn't get arrays.",
            "I would tell you a UDP joke, but you might not get it.",
            "Why do Java developers wear glasses? Because they don’t C#."
        ]
        await ctx.send(random.choice(jokes))

    # Roast
    @commands.command()
    async def roast(self, ctx, member: discord.Member):
        roasts = [
            "I'd say you're 'trash', but that's an insult to garbage.",
            "You don’t need GPS — you already lost.",
            "You're not stupid, just... creatively challenged."
        ]
        await ctx.send(f"{member.mention} {random.choice(roasts)}")

    # Ship
    @commands.command()
    async def ship(self, ctx, member1: discord.Member, member2: discord.Member):
        percentage = random.randint(1,100)
        await ctx.send(f"💞 {member1.mention} + {member2.mention} = {percentage}% compatibility!")

    # Poll
    @commands.command()
    async def poll(self, ctx, *, question):
        embed = discord.Embed(title="📊 Poll", description=question, color=discord.Color.blue())
        message = await ctx.send(embed=embed)
        await message.add_reaction("👍")
        await message.add_reaction("👎")

    # Random math problem
    @commands.command()
    async def math(self, ctx):
        a = random.randint(1,20)
        b = random.randint(1,20)
        await ctx.send(f"What is {a} + {b}? Answer: {a+b}")

    # Random quote
    @commands.command()
    async def quote(self, ctx):
        quotes = [
            "Stay hungry, stay foolish.",
            "Code is like humor. When you have to explain it, it’s bad.",
            "First, solve the problem. Then, write the code."
        ]
        await ctx.send(random.choice(quotes))

    # Animal fact
    @commands.command()
    async def animal(self, ctx):
        facts = [
            "Octopuses have three hearts.",
            "A group of flamingos is called a flamboyance.",
            "Honey never spoils."
        ]
        await ctx.send(random.choice(facts))

async def setup(bot):
    await bot.add_cog(Fun(bot))
