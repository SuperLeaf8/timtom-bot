import discord
from discord.ext import commands
import json
import tests, basics
from traceback import print_exc

"""
Cogs   https://discordpy.readthedocs.io/en/latest/ext/commands/cogs.html
"""

team = [451900766958125076]

### prefix and initial stuff

dpf = 't/'
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
        f = open('muteroles.json','r')
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
            perms.connect = False
            perms.add_reactions = False
            await c.set_permissions(role, overwrite=perms)
        f = open('muteroles.json','r')
        data = json.load(f)
        data.update({str(guild.id):str(role.id)})
        f = open('muteroles.json','w')
        json.dump(data,f,indent=4)

@bot.event
async def on_ready():
    print("go time")
    # embed = discord.Embed(
    #     title="hey",
    #     description="im up",
    #     color=discord.Color(0x4fff4f)
    # )
    for team_member_id in team:
        team_member = bot.get_user(team_member_id)
        embed = discord.Embed(
            title=f"hey, {team_member.name}",
            description="im online",
            color=discord.Color(0x4fff4f)
        )
        await team_member.send(embed=embed)
###



### cogs

cogs = [tests.TestCommands(bot),basics.BasicCommands(bot)]
for cog in cogs:
    bot.add_cog(cog)

###



bot.run(token)