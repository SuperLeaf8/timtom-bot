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
        if not voice:
            await ctx.send("am not in channel")
            return
        await voice.disconnect()
        

    @commands.command()
    async def testplay(self,ctx):
        music = get(self.bot.voice_clients,guild=ctx.guild)
        channel = ctx.author.voice.channel
        if not channel:
            await ctx.send("youre not in a channel")
            return
        if not music:
            await ctx.send("am not in channel")
            return
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
        if not channel:
            await ctx.send("youre not in a channel")
            return
        if not music:
            await ctx.send("am not in channel")
            return
        if music.is_playing or music.is_paused: # if music is playing or music is PAUSED
            if not str(ctx.guild.id) in self.loops:
                self.loops.append(str(ctx.guild.id))
                await ctx.send("loop enabled")
            else:
                self.loops.remove(str(ctx.guild.id))
                await ctx.send("loop disabled")
        else:
            await ctx.send("music not playing")
            return
    
    @commands.command()
    async def pause(self,ctx):
        music = get(self.bot.voice_clients,guild=ctx.guild)
        channel = ctx.author.voice.channel
        if not channel:
            await ctx.send("youre not in a channel")
            return
        if not music:
            await ctx.send("am not in channel")
            return
        if music.is_playing:
            music.pause()
            await ctx.send("paused")
        else:
            await ctx.send("music not playing")
    
    @commands.command()
    async def stop(self,ctx):
        music = get(self.bot.voice_clients,guild=ctx.guild)
        channel = ctx.author.voice.channel
        if not channel:
            await ctx.send("youre not in a channel")
            return
        if not music:
            await ctx.send("am not in channel")
            return
        if music.is_playing or music.is_paused:
            music.stop()
            await ctx.send("stopped")
        else:
            await ctx.send("music not playing")