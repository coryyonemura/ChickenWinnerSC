import discord
from discord.ext import commands, tasks
from datetime import datetime
import pytz
from ducksScheduleUpdater import return_first_game, update_schedule
from hockeyRequests import get_score

#live scores from sofascores.com
#lafc schedule from lafc.com
#ducks schedule from ?

TOKEN = "TOKEN"
PREFIX = '!'

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=PREFIX, intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user.name} has logged on')
    global seconds_until_game
    seconds_until_game = [get_seconds(return_first_game('jsonFiles/ducksScheduleUpdated.json'),return_first_game('jsonFiles/lafcGamesUpdated.json'))]
    countdown_to_next_game.start()
    # count_goals.start()

@bot.command(name="nextGame")
async def nextGame(ctx):
    hockey_game = return_first_game("jsonFiles/ducksScheduleUpdated.json")
    soccer_game = return_first_game('jsonFiles/lafcGamesUpdated.json')

    game = get_closest_game(hockey_game, soccer_game)

    datetime_obj = datetime.strptime(game['date'], "%Y-%m-%d %H:%M:%S")
    written_date = datetime_obj.strftime('%B %d, %Y at %I:%M%p')

    opponent = game['opponent']
    if game == hockey_game:
        await ctx.send(f'the next eligible game is a hockey game. '
                   f'the Anaheim Ducks are playing against the {opponent}'
                   f' on {written_date} PT')
    else:
        await ctx.send(f'the next eligible game is a soccer game. '
                       f'LAFC are playing against the {opponent} '
                       f' on {written_date} PT')

def get_seconds(hockey, soccer):
    hockey_date = datetime.strptime(hockey['date'], "%Y-%m-%d %H:%M:%S")
    soccer_date = datetime.strptime(soccer['date'], "%Y-%m-%d %H:%M:%S")

    pt_timezone = pytz.timezone('US/Pacific')

    # Get the current time in Pacific Time (aware of the timezone)
    current_time_pt = datetime.now(pt_timezone)
    hockey_date = pt_timezone.localize(hockey_date)
    soccer_date = pt_timezone.localize(soccer_date)

    time_diff_hockey = int((hockey_date-current_time_pt).total_seconds())
    time_diff_soccer = int((soccer_date-current_time_pt).total_seconds())
    if time_diff_hockey <= time_diff_soccer:
        return time_diff_hockey
    else:
        return time_diff_soccer

def get_closest_game(hockey, soccer):
    hockey_date = datetime.strptime(hockey['date'], "%Y-%m-%d %H:%M:%S")
    soccer_date = datetime.strptime(soccer['date'], "%Y-%m-%d %H:%M:%S")

    pt_timezone = pytz.timezone('US/Pacific')

    # Get the current time in Pacific Time (aware of the timezone)
    current_time_pt = datetime.now(pt_timezone)
    hockey_date = pt_timezone.localize(hockey_date)
    soccer_date = pt_timezone.localize(soccer_date)

    time_diff_hockey = int((hockey_date-current_time_pt).total_seconds())
    time_diff_soccer = int((soccer_date-current_time_pt).total_seconds())
    if time_diff_hockey <= time_diff_soccer:
        return hockey
    else:
        return soccer

# def get_thirty_min():
#     pt_timezone = pytz.timezone('US/Pacific')
#
#     # Get the current time in Pacific Time (aware of the timezone)
#     current_time_pt = datetime.now(pt_timezone)
#     return int(current_time_pt).total_seconds()+1800

        
@tasks.loop(seconds=60)
async def countdown_to_next_game():
    global seconds_until_game
    print(seconds_until_game[0])
    if seconds_until_game[0] <= 0:
        channel_id = 1187128458774585396
        channel = bot.get_channel(channel_id)

        if channel:
            await channel.send(f'the game has started! support your local team and potentially win free chicken!')

        # call a new task function that calls the data from the live data and checks for goals scored
        count_goals.start()
        #update the json file
        update_schedule("jsonFiles/ducksScheduleUpdated.json")

        seconds_until_game = [get_seconds(get_seconds(return_first_game('jsonFiles/ducksScheduleUpdated.json'),return_first_game('jsonFiles/lafcGamesUpdated.json') ))]

    else:
        seconds_until_game[0] -= 60
#
@tasks.loop(seconds=60)
async def count_goals():
    print('hello')
    score = get_score()
    if score == -1:
        count_goals.stop()
    else:
        if score >= 5:
            channel_id = 1187128458774585396
            channel = bot.get_channel(channel_id)
            await channel.send(f'@everyone the Anaheim Ducks have scored 5 goals! '
                               f'Claim your free chicken on the cfa app before midnight! '
                               f'(rewards may take up to 30 minutes from this announcement to show up on the cfa app)')
            count_goals.stop()

bot.run(TOKEN)