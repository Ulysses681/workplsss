import discord
from discord.ext import commands
import random
import time

class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.cooldowns = {}

    def get_balance(self, user_id):
        cursor = self.bot.db.cursor()
        cursor.execute("SELECT balance FROM economy WHERE user_id=?", (user_id,))
        result = cursor.fetchone()
        if result is None:
            cursor.execute("INSERT INTO economy (user_id, balance) VALUES (?, 0)", (user_id,))
            self.bot.db.commit()
            return 0
        return result[0]

    def update_balance(self, user_id, amount):
        cursor = self.bot.db.cursor()
        cursor.execute("UPDATE economy SET balance = balance + ? WHERE user_id=?", (amount, user_id))
        self.bot.db.commit()

    @commands.command()
    async def balance(self, ctx):
        bal = self.get_balance(ctx.author.id)
        await ctx.send(f"You have {bal} coins.")

    @commands.command()
    async def daily(self, ctx):
        now = time.time()
        if ctx.author.id in self.cooldowns and now - self.cooldowns[ctx.author.id] < 86400:
            return await ctx.send("Come back tomorrow!")

        self.cooldowns[ctx.author.id] = now
        reward = random.randint(50,150)
        self.update_balance(ctx.author.id, reward)
        await ctx.send(f"You received {reward} coins!")

    @commands.command()
    async def work(self, ctx):
        reward = random.randint(10,50)
        self.update_balance(ctx.author.id, reward)
        await ctx.send(f"You worked and earned {reward} coins!")

    @commands.command()
    async def leaderboard(self, ctx):
        cursor = self.bot.db.cursor()
        cursor.execute("SELECT user_id, balance FROM economy ORDER BY balance DESC LIMIT 5")
        rows = cursor.fetchall()

        text = ""
        for i, row in enumerate(rows, 1):
            user = await self.bot.fetch_user(row[0])
            text += f"{i}. {user.name} - {row[1]}\n"

        await ctx.send(f"Top 5:\n{text}")

async def setup(bot):
    await bot.add_cog(Economy(bot))
