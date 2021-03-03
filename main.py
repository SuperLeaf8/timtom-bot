import discord
from discord.ext import commands

### custom prefix
dpf = 't/'
def pf(bot,message):
    try:
        f = open('prefixes.json','r')
        prefixes = json.load(f)
        return prefixes[message.guild.id]
    except AttributeError:
        if message.channel.type is not discord.ChannelType.private:
            guild = message.guild
            f = open('prefixes.json','r')
            prefixes = json.load(f)
            prefixes[guild.id] = dpf
            f = open('prefixes.json','w')
            json.dump(prefixes,f)
        return dpf
    except KeyError:
        f = open('prefixes.json','r')
        prefixes = json.load(f)
        prefixes.update({message.guild.id:dpf})
        f = open('prefixes.json','w')
        json.dump(prefixes,f)
        return dpf
###

### initializing
intents = discord.Intents.default()
intents.members = True
intents.presences = True
bot = commands.Bot(command_prefix=pf,case_insensitive=True,intents=intents)
bot.remove_command('help')

###
