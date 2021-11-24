import discord
from discord.ext import commands, tasks
from discord.ext.commands import cooldown
import json
import basics, capitalism, mod, music,tests
import screwaround

"""
Cogs   https://discordpy.readthedocs.io/en/latest/ext/commands/cogs.html
"""

team = [451900766958125076]



### prefix and initial stuff

dpf = 't/'

def get_dpf():
	return dpf

def pf(bot,message):
	try:
		f = open('prefixes.json','r')
		prefixes = json.load(f)
		return prefixes[str(message.guild.id)]
	except AttributeError:
		if message.channel.type is not discord.ChannelType.private:
			guild = message.guild
			f = open('prefixes.json','r')
			prefixes = json.load(f)
			prefixes[str(guild.id)] = dpf
			f = open('prefixes.json','w')
			json.dump(prefixes,f,indent=4)
		return dpf
	except KeyError:
		f = open('prefixes.json','r')
		prefixes = json.load(f)
		prefixes.update({message.guild.id:dpf})
		f = open('prefixes.json','w')
		json.dump(prefixes,f,indent=4)
		return dpf

intents = discord.Intents.default()
intents.members = True
intents.presences = True
bot = commands.Bot(command_prefix=pf,case_insensitive=True,intents=intents)
bot.remove_command('help')

with open("token.json","r") as f:
	token = json.load(f)

@bot.event
async def on_guild_join(guild):
	# prefix stuff
	f = open('prefixes.json','r')
	prefixes = json.load(f)
	prefixes[str(guild.id)] = dpf
	f = open('prefixes.json','w')
	json.dump(prefixes,f,indent=4)
	# mute stuff
	try:
		with open('muteroles.json','r') as f:
			data = json.load(f)
			roleID = data[str(guild.id)]
			role = guild.get_role(int(roleID))
			if isinstance(role,type(None)):
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
			
"""
HEYYY THOMAS

YE GOTTA REMEMBER TO MAKE THE EVENT on_guild_channel_update TO MAKE THE MUTE ROLE OVERRIDE!

check muteroles, make a role object with it, make the overrides for the new channel
if the server doesnt have a mute role, or the role is a NoneType, just forget it

actually i dont think i need it since i can make it so in fix_mute(), it redoes all the channel overrides
"""
# @bot.event
# async def on_guild_channel_update(channel):
#     with open("muteroles.json","r") as f:
#         data = json.load(f)
#         try:
#             roleID = data[str(channel.guild.id)]
#             role = channel.guild.get_role(int(roleID))
#             if not role:
#                 raise KeyError
#             perms = channel.overwrites_for(role)
#             perms.send_messages = False
#             perms.speak = False
#             perms.add_reactions = False
#             await channel.set_permissions(role, overwrite=perms)
#         except KeyError:
#             pass
@bot.event
async def on_ready():
	print("go time")
	for team_member_id in team:
		team_member = bot.get_user(team_member_id)
		embed = discord.Embed(
			title=f"hey, {team_member.name}",
			description="im online",
			color=discord.Color(0x4fff4f)
		)
		# await team_member.send(embed=embed)
	# await bot.change_presence(activity=discord.Activity(type=discord.Game,name="dm thomas if question"))
	

###

@bot.event
async def on_command_error(ctx, error):
	if isinstance(error, commands.CommandNotFound):
		await ctx.send(f"command not exist")

### cogs

cogs = [
		# tests.TestCommands(bot),
		basics.BasicCommands(bot),
		capitalism.CapitalistCommands(bot),
		mod.ModCommands(bot),
		music.MusicCommands(bot),
		screwaround.ScrewAround(bot),
		tests.TestCommands(bot)
	]
for cog in cogs:
	bot.add_cog(cog)

###



bot.run(token)