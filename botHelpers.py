from datetime import datetime
import pytz
from scheduleUpdaters import return_first_game

def get_seconds(hockey_file, soccer_file, basketball_file):
    return min(time_conversions(hockey_file,soccer_file,basketball_file))


def get_closest_game(hockey_file, soccer_file, basketball_file):
    games = [return_first_game(hockey_file), return_first_game(soccer_file),return_first_game(basketball_file)]
    times = time_conversions(hockey_file, soccer_file, basketball_file)
    m = min(times)
    index = times.index(m)
    return games[index]

def get_sport(hockey_file, soccer_file, basketball_file):
    times = time_conversions(hockey_file, soccer_file, basketball_file)
    m = min(times)
    index = times.index(m)
    if index == 0:
        return "hockey"
    elif index == 1:
        return 'soccer'
    elif index == 2:
        return "basketball"

def next_game_info():
    hockey_game = return_first_game("jsonFiles/jsonDucks/ducksGamesUpdated.json")
    soccer_game = return_first_game('jsonFiles/jsonLAFC/lafcGamesUpdated.json')
    basketball_game = return_first_game('jsonFiles/jsonClippers/clippersGamesUpdated.json')

    game = get_closest_game("jsonFiles/jsonDucks/ducksGamesUpdated.json",
                            'jsonFiles/jsonLAFC/lafcGamesUpdated.json',
                            'jsonFiles/jsonClippers/clippersGamesUpdated.json')

    datetime_obj = datetime.strptime(game['date'], "%Y-%m-%d %H:%M:%S")
    written_date = datetime_obj.strftime('%B %d, %Y at %I:%M%p')

    opponent = game['opponent']

    if game == hockey_game:
        return phrase('hockey', 'Anaheim Ducks', opponent, written_date)
    elif game == soccer_game:
        return phrase('soccer', 'LAFC', opponent, written_date)
    elif game == basketball_game:
        return phrase('basketball', 'LA Clippers', opponent, written_date)
def time_conversions(hockey_file, soccer_file, basketball_file):
    hockey = return_first_game(hockey_file)
    soccer = return_first_game(soccer_file)
    basketball = return_first_game(basketball_file)

    hockey_date = datetime.strptime(hockey['date'], "%Y-%m-%d %H:%M:%S")
    soccer_date = datetime.strptime(soccer['date'], "%Y-%m-%d %H:%M:%S")
    basketball_date = datetime.strptime(basketball['date'], "%Y-%m-%d %H:%M:%S")

    pt_timezone = pytz.timezone('US/Pacific')

    # Get the current time in Pacific Time (aware of the timezone)
    current_time_pt = datetime.now(pt_timezone)
    hockey_date = pt_timezone.localize(hockey_date)
    soccer_date = pt_timezone.localize(soccer_date)
    basketball_date = pt_timezone.localize(basketball_date)

    time_diff_hockey = int((hockey_date - current_time_pt).total_seconds())
    time_diff_soccer = int((soccer_date - current_time_pt).total_seconds())
    time_diff_basketball = int((basketball_date - current_time_pt).total_seconds())
    # print(time_diff_hockey, time_diff_soccer, time_diff_basketball)

    return [time_diff_hockey, time_diff_soccer, time_diff_basketball]

def phrase(sport, team, opponent, date):
    return 'the next eligible game is a '+sport+' game. the '+team+' play against the '+opponent+' on '+date+' PT'