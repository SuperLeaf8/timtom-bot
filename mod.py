
import discord
from discord.ext import commands
import json
import traceback
from embedder import make_embed

class ModCommands(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
	
	async def fixmute(self, guild):
		try:
			with open('muteroles.json','r') as f:
				data = json.load(f)
				roleID = data[str(guild.id)]
				role = guild.get_role(int(roleID))
				if not role:
					raise KeyError
		except KeyError:
			mperms = discord.Permissions(send_messages=False, read_messages=True)
			role = await guild.create_role(name='TimTom Mute',permissions=mperms)
		for c in guild.channels:
			perms = c.overwrites_for(role)
			perms.send_messages = False
			perms.speak = False
			perms.add_reactions = False
			await c.set_permissions(role, overwrite=perms)
		with open('muteroles.json','r') as f:
			data = json.load(f)
			data.update({str(guild.id):str(role.id)})
		with open('muteroles.json','w') as f:
			json.dump(data,f,indent=4)

	# look at this
	def check_if_allowed(self,ctx,member):
		mod = ctx.author
		return not ((mod.top_role <= member.top_role and not mod.guild_permissions.administrator) or (mod != ctx.guild.owner) or (member.guild_permissions.administrator))

	# I SWEAR IM NOT KEEPING THIS, THIS WAS JUST TO SEE IF I CAN IDAGH DOSHG IH
	# def check_if_allowed(self,ctx,member):
	# 	mod = ctx.author
	# 	declined = [
	# 		(mod.top_role <= member.top_role and not mod.guild_permissions.administrator),
	# 		(mod != ctx.guild.owner),
	# 		(member.guild_permissions.administrator)
	# 	]
	# 	[return True for reasob in declined if not reason]
	# 	return False

	@commands.has_permissions(kick_members=True)
	@commands.command()
	async def kick(self, ctx, member: discord.Member,*,reason="no reason lol"):
		allowed = self.check_if_allowed(ctx,member)
		if not allowed:
			await ctx.send("you cant do that")
			return
		await member.kick(reason=reason)
		embed = make_embed(
			title=f"Kicked {member.name}",
			desc=f"Reason: {reason}",
			color=discord.Color(0xffea08),
			author=f"{member.name}#{member.discriminator}",
			avatar=member.avatar_url,
			footer="lol"
		)
		await ctx.send(embed=embed)
		# embed = discord.Embed(
		# 	title="Kicked",
		# 	description=f"kicked because: {reason}",
		# 	color=discord.Color(0xffea08)
		# )
		# embed.set_author(name=f"{member.name}#{member.discriminator}",icon_url=member.avatar_url)

	@commands.has_permissions(kick_members=True)
	@commands.command()
	async def mute(self, ctx, member: discord.Member,*,reason="shut up"):
		if (ctx.author.top_role <= member.top_role and not ctx.author.guild_permissions.administrator) or (ctx.author != ctx.guild.owner):
			await ctx.send("you cant do that")
			return
		await self.fixmute(ctx.guild)
		with open("muteroles.json","r") as f:
			muteroles = json.load(f)
			roleID = muteroles[str(ctx.guild.id)]
			muterole = ctx.guild.get_role(int(roleID))
			if muterole in member.roles:
				await ctx.send("this guy is already muted")
				return
			await member.add_roles(muterole,reason=reason)
		embed = discord.Embed(
			title="trolled",
			description=f"muted because: {reason}",
			color=discord.Color(0xa6a6a6)
		)
		embed.set_author(name=f"{member.name}#{member.discriminator}",icon_url=member.avatar_url)
		embed.set_footer(text="1984... big brother is watch...")
		await ctx.send(embed=embed)

	@commands.has_permissions(kick_members=True)
	@commands.command()
	async def unmute(self, ctx, member: discord.Member):
		if ctx.author.top_role <= member.top_role:
			await ctx.send("you cant do that")
			return
		await self.fixmute(ctx.guild)
		with open("muteroles.json","r") as f:
			data = json.load(f)
			roleID = data[str(ctx.guild.id)]
			muterole = ctx.guild.get_role(int(roleID))
			if not muterole in member.roles:
				await ctx.send("member not muted")
				return
			await member.remove_roles(muterole)
		embed = discord.Embed(
			title="Unmuted",
			description="you can talk now",
			color=discord.Color(0x8cff00) 
		)
		embed.set_author(name=f"{member.name}#{member.discriminator}",icon_url=member.avatar_url)
		embed.set_footer(text="ok now stop being annoying")
		await ctx.send(embed=embed)


	@commands.has_permissions(ban_members=True)
	@commands.command()
	async def ban(self, ctx, user:discord.User,*, reason="blocked"):
		try:
			member = ctx.guild.get_member(user.id)
			if member == None: # member isnt in server
				raise discord.NotFound # prevents role check (that wouldve caused error)
			if (ctx.author.top_role <= member.top_role and not ctx.author.guild_permissions.administrator) or (ctx.author != ctx.guild.owner): # role check if user was in server
				await ctx.send("you cant do that")
				return
		except discord.NotFound:
			pass
		try:
			await ctx.guild.fetch_ban(user)
			await ctx.send("user already banned")
			return
		except discord.NotFound:
			await ctx.guild.ban(user=user,reason=reason,delete_message_days=0)
		embed = discord.Embed(
			title="mass amounts of trolling",
			description=f"banned because: {reason}",
			color=discord.Color(0xff0000)
		)
		embed.set_author(name=f"{user.name}#{user.discriminator}",icon_url=user.avatar_url)
		embed.set_footer(text=":gifKingCry:")
		await ctx.send(embed=embed)

	@commands.has_permissions(ban_members=True)
	@commands.command()
	async def unban(self, ctx, user:discord.User):
		# try:
		#     member = await ctx.guild.get_member(user.id)
		#     if member == None: # member isnt in server
		#         raise discord.NotFound # prevents role check (that wouldve caused error)
		#     if ctx.author.top_role <= member.top_role: # role check if user was in server
		#         await ctx.send("you cant do that")
		#         return
		# except discord.NotFound:
		# pass
		try:
			await ctx.guild.fetch_ban(user)
			await ctx.guild.unban(user=user)
		except discord.NotFound:
			await ctx.send("not banned")
			return
		embed = discord.Embed(
			title="unbanned",
			description=f"shut up",
			color=discord.Color(0x00ff11)
		)
		embed.set_author(name=f"{user.name}#{user.discriminator}",icon_url=user.avatar_url)
		embed.set_footer(text="uncry")
		await ctx.send(embed=embed)

	@commands.has_permissions(manage_channels=True)
	@commands.command()
	async def disable(self, ctx):
		with open("channel_blacklist.json","r") as f:
			data = json.load(f)
			try:
				channels = data[str(ctx.guild.id)]
			except KeyError:
				data.update({str(ctx.guild.id):[]})
			channels = data[str(ctx.guild.id)]
			if str(ctx.channel.id) in channels:
				await ctx.send("already disabled")
			else:
				channels.append(str(ctx.channel.id))
				data.update({str(ctx.guild.id):channels})
				await ctx.send("disabled")
		with open("channel_blacklist.json","w") as f:
			json.dump(data,f,indent=4)
	@commands.has_permissions(manage_channels=True)
	@commands.command()
	async def enable(self, ctx):
		with open("channel_blacklist.json","r") as f:
			data = json.load(f)
			try:
				channels = data[str(ctx.guild.id)]
			except KeyError:
				data.update({str(ctx.guild.id):[]})
			channels = data[str(ctx.guild.id)]
			if not str(ctx.channel.id) in channels:
				await ctx.send("not disabled")
			else:
				channels.remove(str(ctx.channel.id))
				data.update({str(ctx.guild.id):channels})
				await ctx.send("enabled")
		with open("channel_blacklist.json","w") as f:
			json.dump(data,f,indent=4)

	@commands.has_permissions(manage_channels=True)
	@commands.command()
	async def setprefix(self, ctx, new_pf: str):
		with open("prefixes.json","r") as f:
			data = json.load(f)
			if new_pf == "default":
				try:
					del data[str(ctx.guild.id)]
				except KeyError:
					await ctx.send("its already set as default")
					return
			else:
				try:
					prefix = data[str(ctx.guild.id)]
				except KeyError:
					data.update({str(ctx.guild.id):"t/"})
				data[str(ctx.guild.id)] = new_pf
		with open("prefixes.json","w") as f:
			json.dump(data,f,indent=4)
		if new_pf == "default":
			await ctx.send("prefix set to default (t/)")
		else:
			await ctx.send(f"set prefix to: `{new_pf}`")

	@kick.error
	@mute.error
	@unmute.error
	@ban.error
	@unban.error
	@disable.error
	@enable.error
	@setprefix.error
	async def mod_error(self,ctx,error):
		s = ", "
		if isinstance(error,commands.MissingPermissions):
			await ctx.send(f"you cant do that because you cant: {s.join(error.missing_perms)}")
		if isinstance(error,commands.BotMissingPermissions):
			print(type(error))
			print(error)
			await ctx.send(f"i cant do that because i cant: {s.join(error.missing_perms)}")
		if isinstance(error,commands.CommandInvokeError):
			if isinstance(error.original,discord.errors.Forbidden):
				await ctx.send("didnt work, my role is too low probably")