import discord
from discord.ext import commands, tasks
from discord.ext.commands import BucketType
import json
from random import randint
from decimal import Decimal
from datetime import datetime
import math
import item

int_per = 5

class CapitalistCommands(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.interest.start()
		self.changeshop.start()
	class Villager:
		def __init__(self, start_debt, paid, balance):
			self.start_debt = start_debt
			self.paid = paid
			self.balance = balance
			self.ltp = self.start_debt - self.paid
			self.indebt = None
			if self.ltp > 0:
				self.indebt = True
			elif self.ltp == 0:
				self.indebt = False
		def add_bal(self, amount):
			self.balance += amount
		def sub_bal(self, amount):
			self.balance += amount
		def pay(self, amount):
			if amount > self.ltp:
				amount = self.ltp
			self.paid += amount
			self.balance -= amount
			self.__init__(self.start_debt,self.paid,self.balance)
		def recalculate(self):
			self.__init__(self.start_debt,self.paid,self.balance)
	
	@tasks.loop(seconds=10)
	async def interest(self):
		global int_per
		now = datetime.now()
		# here i would put a check to see when its time to apply interest
		# example:
		# if now.day == 1:
		with open("debt.json","r") as f:
			data = json.load(f)
			for user in data.keys():
				# await self.bot.wait_until_ready()
				# me = self.bot.get_user(451900766958125076)
				user_stats = data[user]
				villager = self.Villager(user_stats["start_debt"],user_stats["paid"],user_stats["balance"])
				if not villager.ltp:
					continue
				user_stats["start_debt"] = int(Decimal(str(user_stats["start_debt"])) * Decimal(str(1 + (int_per * 0.01))))
				data.update({user:data[user]})
		with open("debt.json","w") as f:
			json.dump(data,f,indent=4)
	
	@tasks.loop(seconds=60)
	async def changeshop(self):
		num_of_reg_items = 1
		musics = [i for i in item.all_items if i.itemtype == "music"]
		reg_items = [i for i in item.all_items if i.itemtype == "regular"]
		items = []
		items.append(musics[randint(0,len(musics)-1)])
		for i in range(num_of_reg_items):
			found = False
			while not found:
				reg_item = reg_items[randint(0,len(reg_items)-1)]
				if not reg_item in items:
					found = True
				else:
					print("fuck")
			items.append(reg_item)
		with open("shop.json","r") as f:
			data = json.load(f)
			data = []
			for i in items:
				data.append({"name":i.name,"type":i.itemtype,"price":i.price})
		with open("shop.json","w") as f:
			json.dump(data,f,indent=4)

	
	@commands.command()
	async def register(self, ctx):
		global int_per
		with open("debt.json","r") as f:
			data = json.load(f)
			if str(ctx.author.id) in data.keys():
				await ctx.send("bruh you already have debt")
				return
			random_debt = randint(500000,1500000)
			new_user = {
				str(ctx.author.id): {
					"start_debt": random_debt,
					"paid": 0,
					"balance": 0
				}
			}
			data.update(new_user)
			await ctx.send(f"aight g you got {random_debt} bells worth of debt by the end of the week it grows {int_per} percent")
		with open("debt.json","w") as f:
			json.dump(data, f, indent=4)
	
	@commands.command()
	async def stats(self, ctx, *pinged:discord.User):
		if len(pinged) > 0:
			user = pinged[0]
		else:
			user = ctx.author
		with open("debt.json","r") as f:
			data = json.load(f)
			if not str(user.id) in data.keys():
				if user == ctx.author:
					await ctx.send("bruh you arent registered")
				else:
					await ctx.send("bruh that dude isnt registered")
				return
			villager_stats = data[str(user.id)]
			villager = self.Villager(villager_stats["start_debt"],villager_stats["paid"],villager_stats["balance"])
			embed = discord.Embed(
				title=f"**{user.name}'s Debt Stats:**",
				description=discord.Embed.Empty,
				color=discord.Color(0xffe600)
			)
			embed.add_field(name="Initial debt:",value=villager.start_debt,inline=False)
			embed.add_field(name="Paid:",value=villager.paid,inline=False)
			embed.add_field(name="Left to pay:",value=villager.ltp,inline=False)
			embed.add_field(name="Balance:",value=villager.balance,inline=False)
			embed.set_author(name=user.name,icon_url=user.avatar_url)
			embed.set_footer(text="this post was made by nook gang")
			await ctx.send(embed=embed)
	
	@commands.command()
	async def pay(self, ctx, amount):
		with open("debt.json","r") as f:
			data = json.load(f)
			if not str(ctx.author.id) in data.keys():
				await ctx.send("BRUH how tf you gonna pay a debt that you dont have (t/register)")
				return
			villager_stats = data[str(ctx.author.id)]
			villager = self.Villager(villager_stats["start_debt"],villager_stats["paid"],villager_stats["balance"])
			try:
				amount = int(amount)
			except ValueError:
				if amount == "all":
					if villager.balance > villager.ltp:
						amount = villager.ltp
					else:
						amount = villager.balance
				else:
					raise commands.BadArgument
			if amount == 0:
				await ctx.send("bruh you really gonna pay nothing fr")
				return
			if amount > villager.balance:
				await ctx.send("you dont have that much cuh!")
				return
			if not villager.ltp:
				await ctx.send("yeah uhm you dont have debt idk what else to say")
				return
			villager.pay(amount)
			new_user = {
				str(ctx.author.id): {
					"start_debt": villager.start_debt,
					"paid": villager.paid,
					"balance": villager.balance
				}
			}
			data.update(new_user)
			await ctx.send(f"ok so you paid {amount} bells and now have {villager.ltp} bells left of debt")
		with open("debt.json","w") as f:
			json.dump(data,f,indent=4)
	
	@commands.command()
	@commands.cooldown(1,(60*60*24),BucketType.user)
	async def daily(self, ctx):
		# daily command because theres no other way of getting money
		with open("debt.json","r") as f:
			data = json.load(f)
			if not str(ctx.author.id) in data.keys():
				await ctx.send("cuh you arent registered")
				return
			user_stats = data[str(ctx.author.id)]
			random_daily = randint(10,1999)
			user_stats["balance"] = user_stats["balance"] + random_daily
			data.update({str(ctx.author.id):user_stats})
		with open("debt.json","w") as f:
			json.dump(data,f,indent=4)
		await ctx.send(f"ok heres your daily check you got {random_daily} bells")

	@daily.error
	async def dailyerror(self, ctx, error):
		if isinstance(error, commands.CommandOnCooldown):
			raw_sec = round(error.retry_after)
			hours = math.floor(raw_sec / 3600)
			minutes = math.floor((raw_sec % 3600) / 60)
			seconds = math.floor((raw_sec % 60))
			await ctx.send(f"cuh you gotta wait {hours} hours {minutes} minutes {seconds} seconds")
	@commands.command()
	async def give(self, ctx, person:discord.User, amount):
		with open("debt.json","r") as f:
			data = json.load(f)
			if not str(ctx.author.id) in data.keys():
				await ctx.send("you arent registered idiot")
			if not str(person.id) in data.keys():
				await ctx.send(f"{person.name} isnt registered")
				return
			p1 = data[str(ctx.author.id)]
			p2 = data[str(person.id)]
			try:
				amount = int(amount)
			except ValueError:
				if amount == "all":
					amount = p1["balance"]
				else:
					raise commands.BadArgument
			if amount > p1["balance"]:
				await ctx.send("you dont have that much money")
				return
			p1["balance"] = p1["balance"] - amount
			p2["balance"] = p2["balance"] + amount
			data.update({str(ctx.author.id):p1,str(person.id):p2})
		with open("debt.json","w") as f:
			json.dump(data,f,indent=4)
		await ctx.send(f"ok you gave {person.mention} {amount} bells")
