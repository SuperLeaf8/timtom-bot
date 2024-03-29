import discord
from discord.ext import commands
import json
from channel_block import if_channel_allowed

class BasicCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def help(self, ctx, *section):
        help_color = 0x4ffff9
        with open ("commands.json","r") as f:
            data = json.load(f)
        sections = [x for x in data.keys()]
        # use json to get all keys of all sections
        if len(section) >= 1:
            section = section[0]
            section = section.lower()
            if section in sections:
                command_dict = data[section]
                embed = discord.Embed(
                    title=f"**{section}** commands:",
                    description=discord.Embed.Empty,
                    color=discord.Color(help_color)
                )
                for k, v in command_dict.items():
                    embed.add_field(name=k,value=v,inline=False)
                embed.set_footer(text="* means i havent coded the command yet")
                await ctx.send(embed=embed)
            else:
                commands_dict = {}
                for com_dict in data.values():
                    for command, explanation in com_dict.items():
                        commands_dict.update({command: explanation})
                if section in commands_dict.keys():
                    embed = discord.Embed(
                        title=f"**{section}**",
                        description=commands_dict[section],
                        color=discord.Color(help_color)
                    )
                    embed.set_footer(text="* means i havent coded the command yet")
                    await ctx.send(embed=embed)
                else:
                    await ctx.send("cuh idk what you mean")
        else:
            # commands_dict = {}
            # for com_dict in data.values():
            #     for command, explanation in com_dict.items():
            #         commands_dict.update({command: explanation})
            # embed = discord.Embed(
            #     title=f"**ALL of the commands:**",
            #     description=discord.Embed.Empty,
            #     color=discord.Color(0x4ffff9)
            # )
            # for k, v in commands_dict.items():
            #     embed.add_field(name=k,value=v,inline=False)
            # await ctx.author.send(embed=embed)
            for section_name, command_dict in data.items():
                embed = discord.Embed(
                    title=section_name,
                    description=discord.Embed.Empty,
                    color=discord.Color(help_color)
                )
                for com, explanation in command_dict.items():
                    embed.add_field(
                        name=com,
                        value=explanation,
                        inline=False
                    )
                embed.set_footer(text="* means i havent coded the command yet")
                await ctx.author.send(embed=embed)
    
    @commands.check(if_channel_allowed)
    @commands.command()
    async def test(self, ctx):
        await ctx.send("tested")
    
    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f"ping: {self.bot.latency}")

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        print(error)

    @test.error
    async def test_error(self, ctx, error):
        if isinstance(error,commands.CheckFailure):
            await ctx.send("disabled sorry bro")

        
