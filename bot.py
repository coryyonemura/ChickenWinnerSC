import discord
from discord.ext import commands, tasks
from scheduleUpdaters import return_first_game, update_schedule
from webRequests.hockeyRequests import get_score
from botHelpers import get_seconds, next_game_info, get_sport
from webRequests.soccerRequests import lafc_game, lafc_game_over
from webRequests.basketballRequests import missed_freethrows, clippers_game_over, game_over


#live scores from sofascores.com
#jsonLAFC schedule from jsonLAFC.com
#clippers schedule from nba.com
#angels schedule from ?
#ducks schedule from ?

SECONDS_PER_MINUTE = 60
TOKEN = "TOKEN"
PREFIX = '!'
TEST_CHANNEL = 1187128458774585396
TRUE_CHANNEL = 1193355132075782209

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix=PREFIX, intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user.name} has logged on')
    seconds_until_game = [get_seconds('jsonFiles/jsonDucks/ducksGamesUpdated.json',
                                      'jsonFiles/jsonLAFC/lafcGamesUpdated.json',
                                      'jsonFiles/jsonClippers/clippersGamesUpdated.json')]
    countdown_to_next_game.start(seconds_until_game)

@bot.event
async def on_member_join(member):
    await member.send(MESSAGE)

@bot.command(name="nextGame")
async def nextGame(ctx):
    await ctx.send(next_game_info())
        
@tasks.loop(seconds=SECONDS_PER_MINUTE)
async def countdown_to_next_game(seconds_until_game):
    print(seconds_until_game[0])
    if seconds_until_game[0] <= 0:
        sport = get_sport("jsonFiles/jsonDucks/ducksGamesUpdated.json",
                          'jsonFiles/jsonLAFC/lafcGamesUpdated.json',
                          'jsonFiles/jsonClippers/clippersGamesUpdated.json')

        if sport == "hockey":
            await send_both(TRUE_CHANNEL, TEST_CHANNEL,'the Anaheim Ducks game has started! support your local team and potentially win free chicken!')
            ducks_goals.start()
            update_schedule("jsonFiles/jsonDucks/ducksGamesUpdated.json")
        elif sport == "soccer":
            await send_both(TEST_CHANNEL, TRUE_CHANNEL, 'the LAFC game has started! support your local team and potentially win free chicken!')

            lafc_win.start(False)
            update_schedule("jsonFiles/jsonLAFC/lafcGamesUpdated.json")
        elif sport == "basketball":
            await send_both(TEST_CHANNEL, TRUE_CHANNEL, 'the LA Clippers game has started! support your local team and potentially win free chicken!')

            clippers_freethrows.start()
            update_schedule("jsonFiles/jsonClippers/clippersGamesUpdated.json")

        seconds_until_game[0] = get_seconds('jsonFiles/jsonDucks/ducksGamesUpdated.json',
                                            'jsonFiles/jsonLAFC/lafcGamesUpdated.json',
                                            'jsonFiles/jsonClippers/clippersGamesUpdated.json')
    else:
        seconds_until_game[0] -= SECONDS_PER_MINUTE
#
@tasks.loop(seconds=SECONDS_PER_MINUTE)
async def ducks_goals():
    score = get_score()
    if score == -1:
        ducks_goals.stop()
    else:
        if score >= 5:
            message = """@everyone the Anaheim Ducks have scored 5 goals!
                                    Claim your free chicken on the cfa app before midnight!
                                    (rewards may take up to 30 minutes from this announcement to show up on the cfa app)"""
            await send_both(TEST_CHANNEL, TRUE_CHANNEL, message)
            ducks_goals.stop()

@tasks.loop(seconds=SECONDS_PER_MINUTE)
async def lafc_win(winner):
    if lafc_game_over():
        if winner:
            message = """@everyone LAFC has won at home!
                        Claim your free chicken on the cfa app before midnight!
                        (rewards may take up to 30 minutes from this announcement to show up on the cfa app)"""
            await send_both(TEST_CHANNEL, TRUE_CHANNEL, message)
        lafc_win.stop()
    else:
        winner = lafc_game()

@tasks.loop(seconds=SECONDS_PER_MINUTE)
async def clippers_freethrows():
    gameId = return_first_game('jsonFiles/jsonClippers/clippersGamesUpdated.json')['gameId']
    if not clippers_game_over(gameId):
        if missed_freethrows():
            message = """@everyone the Clippers opponent have missed two free throws in a row! 
                        Claim your free chicken on the cfa app before midnight!
                        (rewards may take up to 30 minutes from this announcement to show up on the cfa app)"""
            await send_both(TEST_CHANNEL, TRUE_CHANNEL, message)
            clippers_freethrows.stop()
    else:
        clippers_freethrows.stop()

# @tasks.loop(seconds=SECONDS_PER_MINUTE)
# async def test_freethrows():
#     print('working')
#     gameId = '0022300493'
#     if game_over(gameId) == False:
#         if missed_freethrows():
#             channel_id = 1187128458774585396
#             channel = bot.get_channel(channel_id)
#             await channel.send(f'@everyone a team missed 2 freethrows in a row')
#             test_freethrows.stop()
#     else:
#         test_freethrows.stop()

# async def send_message(channel_id, message):
#     channel = bot.get_channel(channel_id)
#     await channel.send(message)

async def send_both(channel_id, channel_id2, message):
    channel1 = bot.get_channel(channel_id)
    channel2 = bot.get_channel(channel_id2)
    await channel1.send(message)
    await channel2.send(message)

MESSAGE = """🌟 **Chicken Winner Socal ** 🌟

Welcome to the Chicken Winner Socal Discord Server! We're dedicated to bringing the thrill of local sports and free chicken to the Socal community! 🐔🏀⚽⚾🏀

Here's some information about our server:

**Reward Criteria:**
To score some delicious Chicken rewards, your favorite local teams need to meet the following criteria during their home games:

1. 🏒 **Ducks Goals:** The Anaheim Ducks must score 5 or more goals.
2. ⚾ **Angels Runs:** The Los Angeles Angels must score 7 or more runs.
3. ⚽ **LAFC Dubs:** LA Football Club needs to secure a victory during a home game.
4. 🏀 **Clippers FTs:** The opposing team of the LA Clippers must miss 2 consecutive free throws during the 4th quarter.

**Note:** All conditions must be met during a home game for the rewards to activate.

**Claiming Your Reward:**
1. 🕐 After our bot sends the exciting news, please be patient as it may take up to 30 minutes for the reward to appear in your Chick-fil-A app.
2. 📲 To claim your reward, open the Chick-fil-A app by midnight on the same day the message is sent.

**Check the Next Eligible Game:**
📅 Use the `!nextGame` command in our DMs to check when the next eligible game is.

**Stay Informed:**
🔔 To ensure you don't miss out on the winning moment, keep your @ notifications turned on. Our bot will ping you when it's time to open the app and enjoy your well-deserved reward!

**Community Support and Free Chicken:**
Our bot's mission is to foster a supportive community for all local sports teams in LA and OC counties. Let's cheer for our teams, celebrate victories, and savor the taste of victory with free Chick-fil-A! 🎉🍗

cwSC was made by Cory Yonemura (the_flash125). Feel free to ask any questions or leave suggestions via my dms and let's build a community that loves sports and delicious chicken! 🏆🎊
"""


bot.run(TOKEN)