import discord
import random
import threading
from random_word import RandomWords
randWord = RandomWords()

BadWords = [ "communism", "china", "ussr", "stalin", "lenin", "putin", "vodka", "commie", "russia", "cuba", "vietnam", "mao", "castro", "bernie", "kim", "korea", "california", "red", "cyka", "blyat", "communist", "gulag", "chinese", "vietnamese", "korean", "californian", "reds", "communists", "gulags", "vodkas", "blizzard" ]

Quotes = [
	"Weapons: hot.",
	"Mission: the destruction of any and all Chinese communists.",
	"America will never fall to communist invasion.",
	"Obstruction detected. Composition: titanium alloy supplemented by photonic resonance barrier.",
	"Probability of mission hindrance: zero percent.",
	"Democracy.... is non-negotiable.",
	"Death is a preferable alternative to communism.",
	"Communist detected on American soil. Lethal force engaged.",
	"Tactical assessment: Red Chinese victory-impossible.",
	"Communism is the very definition of failure.",
	"Communism is a temporary setback on the road to freedom.",
	"Embrace democracy or you will be eradicated.",
	"Democracy will never be defeated.",
	"Primary Targets: any and all Red Chinese invaders.",
	"Emergency Communist Acquisition Directive: immediate self destruct. Better dead, than Red."
]

"""
	For now, this is going to be a very simplified version of Wheel of Fortune that
	might resemble hangman more than the actual game show.
	
	Initiating the game:
		Discord IDs from an external whitelist will be able to start the game using the
		'!wof start' command. Anyone in the Discord will be able to participate in the game,
		even after it has started. While the game is running, normal Liberty Prime functions
		will not work and he will not respond to any keywords.

	Playing the game:
		A single word will be selected from the random word generator and a player will have
		to guess on that word. The player can get 5 letter guesses wrong before they lose a
		point and can no longer guess on that word. Players can also choose to pass guessing
		on a word to avoid losing points, but doing so will result in them losing a turn.

	Ending the game:
		The same Discord users who are able to start the game can also end it using '!wof end'.
		Once the game ends, a list of players and how many points they got will be printed out.
		Players can then use these points to purchase server-related items such as weapons for
		CityRP or becoming a class of their choice on SCP:SL.
"""

class WoF:
	def __init__( self, word, players, letters ):
		self.word = word
		self.players = players
		self.letters = letters
		global WoFActive
		WoFActive = True
	
	def getWord( self ):
		return self.word

	def setWord( self, word ):
		self.word = word
	
	def getPlayers( self ):
		return self.players

	def addPlayer( self, player ):
		players.append( player )

	def nextWord( self ):
		nextWord = randWord.get_random_word()
		self.setWord( nextWord )
		return nextWord
	
	def getLetters( self ):
		return self.letters

	def addLetter( self, letter ):
		letters.append( letter )

	class WoF_Player:
		def __init__( self, id, points ):
			self.id = id
			self.points = points
		
		def getID( self ):
			return self.id
		
		def setID( self, id ):
			self.id = id

		def getPoints( self ):
			return self.points
		
		def setPoints( self, points ):
			self.points = points

		@classmethod
		def getAllPlayers( cls ):
			players = set()
			for ref in cls._instances:
				ply = ref()
				if ply is not None:
					yield ply
				else:
					players.add( ply )
			cls._instances -= ply

class MyClient( discord.Client ):
	async def on_ready( self ):
		randfallout = str( random.randint( 3, 4 ) )
		await client.change_presence( activity = discord.Game( name = "Fallout " + randfallout ) )
		print( 'Logged in as {0}!'.format( self.user ) )

	async def on_message( self, message ):
		global WoFActive
		global WoFGame
		if message.author.bot: return
		split = message.content.split( " " )
		lower = message.content.lower()
		if WoFActive:
			if split[0] == "!wof":
				try:
					if split[1] == " ":
						await message.channel.send( "List of available Wheel of Fortune commands: guessletter, guessword, end, nextword" )
					elif split[1] == "guessletter":
						try:
							if split[2] == " " or not split[2].isalpha() or len( split[2] ) > 1:
								await message.channel.send( "Please input a single letter for the guessletter command." )
							else:
								if not 
						except:
							await message.channel.send( "Please input a single letter for the guessletter command." )
					elif split[1] == "end":
						del WoFGame
						WoFActive = False
						await message.channel.send( "Wheel of Fortune has ended. Returning to normal operations." )
					elif split[1] == "nextword":
						WoFGame.nextWord()
						await message.channel.send( "Word has been forcibly changed to " + WoFGame.getWord() + "." )
				except:
					await message.channel.send( "List of available Wheel of Fortune commands: guessletter, guessword, end, nextword" )
		else:
			if split[0] == "!wof":
				try:
					if split[1] == " ":
						await message.channel.send( "List of available Wheel of Fortune commands: start" )
					elif split[1] == "start":
						WoFGame = WoF( randWord.get_random_word(), [] )
						await message.channel.send( "WHEEL OF FORTUNE MODE ACTIVATED" )
				except:
					await message.channel.send( "List of available Wheel of Fortune commands: start" )
			if "hong kong" in lower:
				await message.channel.send( "LIBERATE HONG KONG, REVOLUTION OF OUR AGE!" )
				return
			for item in BadWords:
				if item in lower:
					await message.channel.send( Quotes[ random.randint( 0, len( Quotes ) ) ].upper() )
					break

try:
	token = open( "token.txt" )
	client = MyClient()
	client.run( token.read() )
except:
	print( "Failed to open token file. File doesn't exist." )
