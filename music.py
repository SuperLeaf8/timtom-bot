import discord
from discord.ext import commands
from discord.utils import get
import traceback

class MusicCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.loops = []


    @commands.command()
    async def join(self, ctx):
        try:
            channel = ctx.author.voice.channel
            await channel.connect()
        except AttributeError:
            await ctx.send("youre not in channel poopnose")
            
    
    @commands.command()
    async def leave(self, ctx):
        voice = get(self.bot.voice_clients,guild=ctx.guild)
        channel = voice.channel
        try:
            await voice.disconnect()
        except AttributeError as e:
            await ctx.send("im not in a channel")
            print(e)

    @commands.command()
    async def testplay(self,ctx):
        music = get(self.bot.voice_clients,guild=ctx.guild)
        def replay():
            if str(ctx.guild.id) in self.loops:
                music.play(discord.FFmpegPCMAudio("test.mp3"))
            else:
                pass
        music.play(discord.FFmpegPCMAudio("test.mp3"),after=lambda check: replay())
    
    @commands.command()
    async def loop(self, ctx): # can only loop when music play
        music = get(self.bot.voice_clients,guild=ctx.guild)
        channel = ctx.author.voice.channel
        print(type(music))
        if music:
            if not str(ctx.guild.id) in self.loops:
                self.loops.append(str(ctx.guild.id))
                await ctx.send("loop enabled")
            else:
                self.loops.remove(str(ctx.guild.id))
                await ctx.send("loop disabled")
        else:
            await ctx.send("im not in a channel")
    
    @commands.command()
    async def pause(self,ctx):
        music = get(self.bot.voice_clients,guild=ctx.guild)
        channel = ctx.author.voice.channel
        if not channel:
            await ctx.send("youre not in a channel")
        if not music:
            await ctx.send("am not in channel")
            return
        