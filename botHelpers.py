from datetime import datetime
import pytz
from scheduleUpdaters import return_first_game

def get_seconds(hockey_file, soccer_file, basketball_file, baseball_file):
    return min(time_conversions(hockey_file,soccer_file,basketball_file, baseball_file))


def get_closest_game(hockey_file, soccer_file, basketball_file,baseball_file):
    games = [return_first_game(hockey_file), return_first_game(soccer_file),return_first_game(basketball_file), return_first_game(baseball_file)]
    times = time_conversions(hockey_file, soccer_file, basketball_file, baseball_file)
    m = min(times)
    index = times.index(m)
    return games[index]

def get_sport(hockey_file, soccer_file, basketball_file,baseball_file):
    times = time_conversions(hockey_file, soccer_file, basketball_file, baseball_file)
    m = min(times)
    index = times.index(m)
    if index == 0:
        return "hockey"
    elif index == 1:
        return 'soccer'
    elif index == 2:
        return "basketball"
    elif index == 3:
        return "baseball"

def next_game_info():
    hockey_game = return_first_game("jsonFiles/jsonDucks/ducksGamesUpdated.json")
    soccer_game = return_first_game('jsonFiles/jsonLAFC/lafcGamesUpdated.json')
    basketball_game = return_first_game('jsonFiles/jsonClippers/clippersGamesUpdated.json')
    baseball_game = return_first_game('jsonFiles/jsonAngels/angelsGamesUpdated.json')

    game = get_closest_game("jsonFiles/jsonDucks/ducksGamesUpdated.json",
                            'jsonFiles/jsonLAFC/lafcGamesUpdated.json',
                            'jsonFiles/jsonClippers/clippersGamesUpdated.json',
                            'jsonFiles/jsonAngels/angelsGamesUpdated.json')

    datetime_obj = datetime.strptime(game['date'], "%Y-%m-%d %H:%M:%S")
    written_date = datetime_obj.strftime('%B %d, %Y at %I:%M%p')

    opponent = game['opponent']

    if game == hockey_game:
        return phrase('hockey', 'Anaheim Ducks', opponent, written_date)
    elif game == soccer_game:
        return phrase('soccer', 'LAFC', opponent, written_date)
    elif game == basketball_game:
        return phrase('basketball', 'LA Clippers', opponent, written_date)
    elif game == baseball_game:
        return phrase('baseball', 'Los Angeles Angels', opponent, written_date)
def time_conversions(hockey_file, soccer_file, basketball_file, baseball_file):
    hockey = return_first_game(hockey_file)
    soccer = return_first_game(soccer_file)
    basketball = return_first_game(basketball_file)
    baseball = return_first_game(baseball_file)

    hockey_date = datetime.strptime(hockey['date'], "%Y-%m-%d %H:%M:%S")
    soccer_date = datetime.strptime(soccer['date'], "%Y-%m-%d %H:%M:%S")
    basketball_date = datetime.strptime(basketball['date'], "%Y-%m-%d %H:%M:%S")
    baseball_date = datetime.strptime(baseball['date'], "%Y-%m-%d %H:%M:%S")

    pt_timezone = pytz.timezone('US/Pacific')

    # Get the current time in Pacific Time (aware of the timezone)
    current_time_pt = datetime.now(pt_timezone)
    hockey_date = pt_timezone.localize(hockey_date)
    soccer_date = pt_timezone.localize(soccer_date)
    basketball_date = pt_timezone.localize(basketball_date)
    baseball_date = pt_timezone.localize(baseball_date)

    time_diff_hockey = int((hockey_date - current_time_pt).total_seconds())
    time_diff_soccer = int((soccer_date - current_time_pt).total_seconds())
    time_diff_basketball = int((basketball_date - current_time_pt).total_seconds())
    time_diff_baseball = int((baseball_date-current_time_pt)).total_seconds()
    print(time_diff_hockey, time_diff_soccer, time_diff_basketball, time_diff_baseball)

    return [time_diff_hockey, time_diff_soccer, time_diff_basketball, time_diff_baseball]

def get_date():
    pacific_time = pytz.timezone("America/Los_Angeles")

    current_datetime_pacific = datetime.now(pacific_time)
    def get_ordinal_suffix(day):
        if 10 <= day % 100 <= 20:
            suffix = 'th'
        else:
            suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(day % 10, 'th')
        return suffix

    # Format the date with the ordinal suffix
    formatted_date_str = current_datetime_pacific.strftime("%B %d{}, %Y").format(get_ordinal_suffix(current_datetime_pacific.day))

    return formatted_date_str

def phrase(sport, team, opponent, date):
    return 'The next eligible game is a '+sport+' game. The '+team+' play against the '+opponent+' on '+date+' PT'

def condition(team, cond):
    return f'@everyone The {team} have {cond}! Claim your free chicken on the CFA app before midnight! (Rewards may take up to 30 minutes from this announcement to show up on the CFA app)'