import discord
from discord.ext import commands
from embedder import make_embed

class TestCommands(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
    
	@commands.command()
	async def intents(self, ctx):
		await ctx.send("if you see this then it works")
		await ctx.send(ctx.author.status)
	
	@commands.command()
	async def embedtest(self,ctx):
		embed = make_embed(title="hi",desc="there",color=discord.Color(0xf89e43))
		await ctx.send(embed=embed)
