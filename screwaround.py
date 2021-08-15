import discord
from discord.ext import commands

class ScrewAround(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
    
    @commands.command()
    async def addsc(self,ctx,user:discord.User ,points:int):
        embed = discord.Embed(
            title="FROM MINISTRY OF STATE",
            description=f"+{points} has been added to `{user.name}`'s account!\nGood work Citizen!",
            color=discord.Color(0xff0303)
        )
        embed.set_footer(text="中國共產黨萬歲")
        await ctx.send(embed=embed)
    @commands.command()
    async def subsc(self,ctx,user:discord.User ,points:int):
        embed = discord.Embed(
            title="FROM MINISTRY OF STATE",
            description=f"-{points} has been subtracted from `{user.name}`'s account...",
            color=discord.Color(0xff0303)
        )
        embed.set_footer(text="中國共產黨萬歲")
        await ctx.send(embed=embed)


    @commands.Cog.listener()
    async def on_command_error(self,ctx,error):
        print(error)
