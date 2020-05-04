import discord
from discord.ext import commands
from wakeonlan import send_magic_packet
import json
import logging
import datetime
import random
import time

# setting up the logging to file called discord.log
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

config = json.load(open('./config.json', 'r'))
prefix = str(config["prefix"])

def is_admin(role, lvl):
	if discord.utils.get(role, name="Bot-lvl " + lvl):
		return True
	else:
		return False

def randomizer(answers):
	answer = ''.join(random.sample(answers,  1))
	return answer

class TeflonBot(discord.Client):
	async def on_ready(self):
		await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="'help"))
		print('Logged on as', self.user)

	async def on_message(self, message):
		# check if message starts with prefix and don't follow orders from filthy bots
		if message.content.startswith(prefix) and message.author.bot == False:
			command = message.content.lower().split(None,1)

# SEND AVAILABLE COMMANDS
			if command[0] == prefix + 'help':
				embed = discord.Embed(title="TeflonBot " + str(config["version"]) +  " - Commands:", description="What can the bot do? Commands are not case sensitive.", colour=discord.Colour(int(config["embed_colour"])))
				embed.add_field(name=prefix + "Jaa", value="Link the Nuuskis Jaa Video", inline = False)
				embed.add_field(name=prefix + "No", value="Link the Office Michael OH GO PLEASE NO! Video", inline = False)
				embed.add_field(name=prefix + "Booty", value="Link booty song ( ͡° ͜ʖ ͡° )", inline = False)
				embed.add_field(name=prefix + "Sale", value="Notify the server of the divine sales!", inline = False)
				embed.add_field(name=prefix + "Bday", value="Happy birthday somebody", inline = False)
				embed.add_field(name=prefix + "FreeGame [Game Name] [URL]", value="Notify for free games in the free-games channel", inline = False)
				embed.add_field(name=prefix + "8Ball [Question]", value="Ask from the magical eightball", inline = False)
				embed.add_field(name=prefix + "Coinflip [choise1] [choise2]", value="Flip the coin. Leave choises empty for default yes/no. Can also put more choises)", inline = False)
				embed.add_field(name=prefix + "F", value="Press F to pay respect", inline = False)
				await message.channel.send(content=None, embed=embed)

# CHANGE NAME TO FOOL REPEATEDELY
			elif command[0] == prefix + 'fool':
				for i in range(10):
					await message.author.edit(nick='Fool')
					time.sleep(0.5)
					await message.author.edit(nick=None)
					time.sleep(0.5)

# LINK NUUSKIS JAA VIDEO
			elif command[0] == prefix + 'jaa':
				await message.channel.send('https://www.youtube.com/watch?v=YF8W_2TJsKw&feature=youtu.be&t=2s')

# LINK THE OFFICE MICHAEL NOOOO! VIDEO
			elif command[0] == prefix + 'no':
				await message.channel.send('https://youtu.be/H07zYvkNYL8?t=3s')

# LINK BOOTY SONG VIDEO
			elif command[0] == prefix + 'booty':
				await message.channel.send('https://www.youtube.com/watch?v=NS7z0Ph668E\n( ͡° ͜ʖ ͡° )( ͡° ͜ʖ ͡° )( ͡° ͜ʖ ͡° )( ͡° ͜ʖ ͡° )( ͡° ͜ʖ ͡° ( ͡° ͜ʖ ͡° )( ͡° ͜ʖ ͡° ( ͡° ͜ʖ ͡° )( ͡° ͜ʖ ͡° )')

# NOTIFY OF STEAM SALE
			elif  command[0] == prefix + 'sale':
				await message.channel.send('https://www.youtube.com/watch?v=rP2MDtWu5t0\n@everyone :raised_hands: STEAM SALE HAS STARTED!!! ALL HAIL LORD GABEN!!! :raised_hands:')

# LINK BIRTHDAY SONG VIDEO
			elif  command[0] == prefix + 'bday':
				await message.channel.send(':tada: :balloon: :birthday: :gift: :confetti_ball: HAPPY BIRTHDAY!!! :confetti_ball: :gift: :birthday: :balloon: :tada:\nhttps://www.youtube.com/watch?v=rP2MDtWu5t0')

# FREE GAME PSA
			elif  command[0] == prefix + 'freegame':
				try:
					command[1]
				except IndexError:
					await message.author.send('You forgot the game name / url')
				else:
					game_details = command[1].split(None)
					free_games_channel = discord.utils.get(message.author.guild.channels, name = "free-games")
					if type(free_games_channel) == discord.channel.TextChannel:
						try:
							game_details[0] and game_details[1]
						except IndexError:
							await message.author.send('You forgot the game name / url')
						else:
							embed = discord.Embed(title="Free Game!", description=game_details[0] + ":\n" + game_details[1], colour=discord.Colour(int(config["embed_colour"])))
							embed.set_image(url="https://puu.sh/B8rUY.jpg")
							embed.set_thumbnail(url="https://puu.sh/AZxe5.png")
							await free_games_channel.send(content=None, embed=embed)
					else:
						await message.channel.send("There's no free-games channel available. Make sure to have one with the exact name and check that the bot can read and send messages to that channel")

# MAGIC 8BALL
			elif command[0] == prefix + '8ball':
				try:
					command[1]
				except IndexError:
					await message.channel.send('You forgot the question')
				else:
					choises = ['Maybe', 'Apsolutely not', 'I hope so', 'I your dreams', 'There\'s good chance of that', 'pretty surely', 'I think so', 'I hope not',
					'Never!', 'Ahaha! Really?!?', 'Pfft', 'Sorry', 'Fuck yeah!', 'Fuck no!','Stupid question lmao', 'The future is unclear',
					'I\'d prefer not to answer', 'Who cares?', 'Possibly', 'No way', 'There\'s a slight chance', 'Yes!', 'Ask again later']
					answer = randomizer(choises)
					if command[1].rfind('?') <= 0: # Add questionmark if there isn't one already. Just to be more fancy
						command[1] += "?"
					embed = discord.Embed(title=':8ball: ' + str(command[1]), description=answer, colour=discord.Colour(int(config["embed_colour"])))
					await message.channel.send(content=None, embed=embed)

# FLIP THE COIN
			elif command[0] == prefix + 'coinflip' or command[0] == prefix + 'flip':
				try:
					command[1]
				except IndexError:
					choises = ['Yes', 'No'] # Default choises for faster basic command
					embed = discord.Embed(title='<:coin:467302593870299146> Coinflip Result:', description=randomizer(choises), colour=discord.Colour(int(config["embed_colour"])))
					await message.channel.send(content=None, embed=embed)
				else:
					choises = command[1].split() # If there is user set choises use those instead
					embed = discord.Embed(title='<:coin:467302593870299146> Coinflip Result:', description=randomizer(choises), colour=discord.Colour(int(config["embed_colour"])))
					await message.channel.send(content=None, embed=embed)
# PAY RESPECT + RANDOM COLOURED HEART
			elif command[0] == prefix + 'f':
				choises = [':heart:', ':blue_heart:', ':yellow_heart:', ':green_heart:', ':purple_heart:', ':black_heart:']
				await message.channel.send("**" + message.author.mention + "** has paid their respects "+ randomizer(choises))
# WOL
			elif command[0] == prefix + 'wol':
				if is_admin(message.author.roles, "2"):
					send_magic_packet(config["MACEthernet"], ip_address='192.168.0.255', port=9) # ETHERNET
					send_magic_packet(config["MACWifi"], ip_address='192.168.0.255', port=9) # WIFI
					print('WOL done')
				else:
					await message.author.send('You don\'t have permission to do this')
					

# WRONG COMMAND
			else:
				await message.author.send('```Command ' + str(message.content.lower()) + ' Does not excist. Use ' + prefix + 'help to see available commands```')

# DELETE USER'S MESSAGE
			await message.delete()

bot = TeflonBot()
bot.run(config["token"])