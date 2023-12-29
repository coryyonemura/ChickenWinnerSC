from datetime import datetime
import pytz
from scheduleUpdaters import return_first_game

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

def get_sport(hockey, soccer):
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
        return "hockey"
    else:
        return "soccer"




def next_game_info():
    hockey_game = return_first_game("jsonFiles/ducksGamesUpdated.json")
    soccer_game = return_first_game('jsonFiles/lafcGamesUpdated.json')

    game = get_closest_game(hockey_game, soccer_game)

    datetime_obj = datetime.strptime(game['date'], "%Y-%m-%d %H:%M:%S")
    written_date = datetime_obj.strftime('%B %d, %Y at %I:%M%p')

    opponent = game['opponent']
    if game == hockey_game:
        return "the next eligible game is a hockey game. the Anaheim Ducks play against the "+opponent+" on "+written_date+" PT"
    return "the next eligible game is a soccer game. LAFC plays against the "+opponent+" on "+written_date+" PT"
