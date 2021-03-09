import discord
from discord.ext import commands

class TestCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def intents(self, ctx):
        await ctx.send("if you see this then it works")
        await ctx.send(ctx.author.status)