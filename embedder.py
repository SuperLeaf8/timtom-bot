import discord
from discord.ext import commands
# instead of arg=None, maybe do arg=discord.Embed.Empty
def make_embed(*fields,title=discord.Embed.Empty,desc=discord.Embed.Empty,color=discord.Color(0xffffff),footer=discord.Embed.Empty,footer_icon=discord.Embed.Empty,author=None,avatar=discord.Embed.Empty,thumbnail=discord.Embed.Empty):
	embed = discord.Embed(
		title=title,
		description=desc,
		color=color
	)
	embed.set_footer(text=footer,icon_url=footer_icon)
	if author:
		embed.set_author(name=author,icon_url=avatar)
	embed.set_thumbnail(url=thumbnail)
	for i in fields:
		embed.add_field(
			name=i[0],
			value=i[1],
			inline=i[2]
		)
	return embed

