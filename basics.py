import discord
from discord.ext import commands

class Basics(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
	
	@commands.command()
	async def help(self, ctx):
		await ctx.send("if you see this, then it worked!")
