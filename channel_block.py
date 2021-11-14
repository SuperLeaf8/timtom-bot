import json

async def if_channel_allowed(ctx):
    with open("channel_blacklist.json","r") as f:
        channels = json.load(f)
        try:
            if str(ctx.channel.id) in channels[str(ctx.guild.id)]:
                return False
            else:
                return True
        except:
            return True

	"""tabby"""