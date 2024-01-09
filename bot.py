import discord
from discord.ext import commands, tasks
from scheduleUpdaters import return_first_game, update_schedule
from webRequests.hockeyRequests import get_score
from botHelpers import get_seconds, next_game_info, get_sport, condition, get_date
from webRequests.soccerRequests import lafc_winner, lafc_game_over
from webRequests.basketballRequests import missed_freethrows, clippers_game_over

#add angels
#create archives

SECONDS_PER_MINUTE = 60
TOKEN = "TOKEN"
PREFIX = '!'
TEST_CHANNEL = 1187128458774585396
CHICKENWIN_CHANNEL = 1193355132075782209
ARCHIVES_CHANNEL = 1193379007996121150
INFO_CHANNEL = 1193359780606132235

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix = PREFIX, intents = intents)

#live scores from sofascores.com
#jsonLAFC schedule from jsonLAFC.com
#clippers schedule and live data from nba.com
#angels schedule from mlb.com
#ducks schedule from ?

@bot.event
async def on_ready():
    print(f'{bot.user.name} has logged on')
    # await send_both(TEST_CHANNEL,INFO_CHANNEL, MESSAGE )
    seconds_until_game = [get_seconds('jsonFiles/jsonDucks/ducksGamesUpdated.json',
                                      'jsonFiles/jsonLAFC/lafcGamesUpdated.json',
                                      'jsonFiles/jsonClippers/clippersGamesUpdated.json',
                                      'jsonFiles/jsonAngels/angelsGamesUpdated.json')]
    countdown_to_next_game.start(seconds_until_game)


@bot.event
async def on_member_join(member):
    await member.send(MESSAGE)


@bot.command(name = "nextGame")
async def nextGame(ctx):
    await ctx.send(next_game_info())


@tasks.loop(seconds = SECONDS_PER_MINUTE)
async def countdown_to_next_game(seconds_until_game):
    print(seconds_until_game[0])
    if seconds_until_game[0] <= 0:
        sport = get_sport("jsonFiles/jsonDucks/ducksGamesUpdated.json",
                          'jsonFiles/jsonLAFC/lafcGamesUpdated.json',
                          'jsonFiles/jsonClippers/clippersGamesUpdated.json',
                          'jsonFiles/jsonAngels/angelsGamesUpdated.json')

        if sport == "hockey":
            await send_both(CHICKENWIN_CHANNEL, TEST_CHANNEL,
                            'The Anaheim Ducks game has started! Support your local team and potentially win free chicken!')
            ducks_goals.start()
            update_schedule("jsonFiles/jsonDucks/ducksGamesUpdated.json")
        elif sport == "soccer":
            await send_both(TEST_CHANNEL, CHICKENWIN_CHANNEL,
                            'The LAFC game has started! Support your local team and potentially win free chicken!')
            lafc_win.start(False)
            update_schedule("jsonFiles/jsonLAFC/lafcGamesUpdated.json")
        elif sport == "basketball":
            await send_both(TEST_CHANNEL, CHICKENWIN_CHANNEL,
                            'The LA Clippers game has started! Support your local team and potentially win free chicken!')
            clippers_freethrows.start()
            update_schedule("jsonFiles/jsonClippers/clippersGamesUpdated.json")
        elif sport == "baseball":
            await send_both(TEST_CHANNEL, CHICKENWIN_CHANNEL,
                            'The Los Angeles Angels game has started! Support your local team and potentially win free chicken!')
            # angels_runs.start()
            update_schedule('jsonFiles/jsonAngels/angelsGamesUpdated.json')

        seconds_until_game[0] = get_seconds('jsonFiles/jsonDucks/ducksGamesUpdated.json',
                                            'jsonFiles/jsonLAFC/lafcGamesUpdated.json',
                                            'jsonFiles/jsonClippers/clippersGamesUpdated.json',
                                            'jsonFiles/jsonAngels/angelsGamesUpdated.json')
    else:
        seconds_until_game[0] -= SECONDS_PER_MINUTE


@tasks.loop(seconds = SECONDS_PER_MINUTE)
async def ducks_goals():
    score = get_score()
    if score == -1:
        ducks_goals.stop()
    else:
        if score >= 5:
            message = condition('Anaheim Ducks', 'scored 5 goals')
            await send_message(ARCHIVES_CHANNEL, f'**{get_date()}** - 🚨🦆 The Anaheim Ducks scored 5 goals! 🏒🔥 #freechicken')
            await send_both(TEST_CHANNEL, CHICKENWIN_CHANNEL, message)
            ducks_goals.stop()


@tasks.loop(seconds = SECONDS_PER_MINUTE)
async def lafc_win():
    if lafc_game_over():
        if lafc_winner():
            message = condition('LAFC', 'won at home')
            await send_message(ARCHIVES_CHANNEL, f'**{get_date()}** - 🚨⚽ LAFC conquered their home game with a win! ⚽🏆 #freechicken ')
            await send_both(TEST_CHANNEL, CHICKENWIN_CHANNEL, message)
        lafc_win.stop()


@tasks.loop(seconds = SECONDS_PER_MINUTE)
async def clippers_freethrows():
    gameId = return_first_game('jsonFiles/jsonClippers/clippersGamesUpdated.json')['gameId']
    if not clippers_game_over(gameId):
        if missed_freethrows():
            message = condition("Clippers'", 'missed two free throws in a row in the 4th quarter')
            await send_message(ARCHIVES_CHANNEL, f'**{get_date()}** - 🚨🏀 The Clippers opponent missed 2 free throws in a row during the 4th quarter! 🏀🏆 #freechicken')
            await send_both(TEST_CHANNEL, CHICKENWIN_CHANNEL, message)
            clippers_freethrows.stop()
    else:
        clippers_freethrows.stop()

async def send_message(channel_id, message):
    channel = bot.get_channel(channel_id)
    await channel.send(message)


async def send_both(channel_id, channel_id2, message):
    channel1 = bot.get_channel(channel_id)
    channel2 = bot.get_channel(channel_id2)
    await channel1.send(message)
    await channel2.send(message)


MESSAGE = """🌟 **Chicken Winner Socal ** 🌟

Welcome to the Chicken Winner Socal Discord Server! We're dedicated to bringing the thrill of local sports and free chicken to the Socal community! 🐔🏀⚽⚾🏀

**Reward Criteria:**
To score some delicious chicken rewards, your favorite local teams need to meet the following criteria during their home games:

1. 🏒 **Ducks Goals:** The Anaheim Ducks must score 5 or more goals.
2. ⚾ **Angels Runs:** The Los Angeles Angels must score 7 or more runs.
3. ⚽ **LAFC Dubs:** LA Football Club needs to secure a victory during a home game.
4. 🏀 **Clippers FTs:** The opposing team of the LA Clippers must miss 2 consecutive free throws during the 4th quarter.

**Note:** All conditions must be met during a home game.

**Claiming Your Reward:**
1. 🕐 After our bot sends the exciting news, it may take up to 30 minutes for the reward to appear in your cfa app.
2. 📲 To claim your reward, open the cfa app by midnight on the same day the message is sent.
3. ⏳ Keep in mind that rewards expire in 3 days.


**Check the Next Eligible Game:**
📅 Use the `!nextGame` command in our DMs to check when the next eligible game is.

**Channels:**
- **#chickenwin:** Announces when games start and @'s everyone when you can claim your free chicken.
- **#archive:** An archive of previous times we have claimed free chicken.
- **#bot-info:** Information about the bot and server.

**Stay Informed:**
🔔 To ensure you don't miss out on the winning moment, keep your @ notifications turned on. Our bot will ping you when it's time to open the app and enjoy your well-deserved reward!

**Community Support and Free Chicken:**
Our mission is to foster a supportive community for all local sports teams in LA and OC counties. Let's cheer for our teams, celebrate victories, and savor the taste of victory with free chicken! 🎉🍗

cwSC was made by Cory Yonemura. Feel free to ask questions via my DMs, and let's build a community that loves sports and delicious chicken! 🏆🎊
"""

bot.run(TOKEN)
