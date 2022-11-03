from bs4 import BeautifulSoup
import requests
import re
import matplotlib.pyplot as plt

url = "https://en.wikipedia.org/wiki/2021_NBA_playoffs"
base_url = "https://en.wikipedia.org"

def get_teams(url):
    """
    Function that finds all semifinal teams of 2021 NBA playoffs

    Returns:
    Dictionary, where keys are team names, values are team wikipedia article
    """

    response = requests.get(url)
    html_string = response.text

    soup = BeautifulSoup(html_string, "html.parser")

    # Find brackets
    bracket_header = soup.find(id="Bracket")

    # Find bracket table
    bracket_table = bracket_header.find_all_next("table")[0]

    # Find rows of table
    rows = bracket_table.find_all("tr")

    team_ids = []
    teams = []
    semifinal_teams = {}

    # Find all teams, url and score
    for row in rows[2:]:
        cells = row.find_all("td")
        if len(cells) < 4:
            continue
        team_id = cells[1]
        url_cell = cells[2]
        score = cells[3].text.strip()

        if re.match(r"[EW][1-8]", team_id.text.strip()):
            found_id = team_id.text.strip()
        else:
            continue

        if found_id in team_ids:
            continue
        team_ids.append(found_id)

        team_url = base_url + url_cell.find('a').attrs['href']
        team_name = url_cell.find('a').text
        # Change teams starting with LA -> L.A. for later use
        if re.match(r"^(LA)", team_name):
            team_name = re.sub(r"LA", r"L.A.", team_name)
        teams.append([team_name, team_url, score])
    
    # To get only semifinalists, we compare two and two team scores, and selects winner
    for i in range(0, len(teams)-1, 2):
        team1_name, team1_url, team1_score = teams[i]
        team2_name, team2_url, team2_score = teams[i+1]
        if int(team1_score) > int(team2_score):
            semifinal_teams[team1_name] = team1_url
        else:
            semifinal_teams[team2_name] = team2_url
    return semifinal_teams

def extract_players(url):
    """
    Function that finds all players of an NBA team

    Returns:
    Dictionary, where keys are player names and values are player wikipedia articles
    """
    response = requests.get(url)
    html_string = response.text

    soup = BeautifulSoup(html_string, "html.parser")

    #Find the roster header
    roster_header = soup.find(id="Roster")
    # Find first table
    roster_table = roster_header.find_all_next("table")[0]
    players = roster_table.find_all("td")[0]
    rows = players.find_all("tr")
    players = {}
    for row in rows[1:]:
        cells = row.find_all("td")
        url = base_url + cells[2].find('a').attrs['href']
        player = cells[2].find('a').text
        #last_name, first_name = player.split(", ")
        #player = first_name + " " + last_name
        #print(player, url)
        players[player] = url
    return players

def extract_player_statistics(url, team):
    """
    Function that takes a player url and their current team as input, and returns some player statistics if the player has any stats for the team.

    If the player has no recorded stats for their current team, all values in returned dictionary will be 0.

    Returns:
    Dictionary, where keys are abbreviations of different player statistics, and values are their respective values.
    """

    response = requests.get(url)
    html_string = response.text

    soup = BeautifulSoup(html_string, "html.parser")

    stats = {"rpg": 0,
             "bpg": 0, 
             "ppg": 0}

    nba_header = soup.find(id="NBA_career_statistics")
    if nba_header is None:
        nba_header = soup.find(id="NBA")
        try:
            regular_season_header = nba_header.find_next(id="Regular_season")
            nba_table = regular_season_header.find_next("table")
        except:
            try:
                nba_table = nba_header.find_next("table")
            except:
                return stats
    try:
        seasons = nba_table.find_all("tr")[1:]
        seasons.reverse()
        # Some players has Career and All-star stats. Others have only Career, which is why we're checking the bottom 3 rows
        for season in seasons[:3]:
            cells = season.find_all("td")
            if len(cells) == 13 and cells[1].text.rstrip() == team:
                rpg = cells[8].text.strip("*")
                bpg = cells[11].text.strip("*")
                ppg = cells[12].text.strip("*")
                stats["rpg"] = float(rpg)
                stats["bpg"] = float(bpg)
                stats["ppg"] = float(ppg)
                return stats
        return stats
    except UnboundLocalError:
        return stats

colors = ["red", "green", "purple", "yellow", "brown", "blue", "orange", "black"]
def plot_player_statistics(semi_teams):
    """
    Function that takes a dictionary of teams and urls, and plots the stats of the 3 best players in each of the following categories:
    - Rebounds per game
    - Blocks per game
    - Points per game

    Each plot is saved under a specified name in the /NBA_player_statistics folder
    """

    # Empty list to store values for plotting
    rpg_names, bpg_names, ppg_names = [], [], []
    rpg_scores, bpg_scores, ppg_scores = [], [], []
    teams = []

    # Loop to get highest rpg, bpg, ppg from each team
    for i, team in enumerate(semi_teams):
        print(f"Getting player stats for {team}")
        teams.append(team)
        team_dict = {}
        # Empty list for extracting highest values
        player_names, rpg, bpg, ppg = [], [], [], []
        roster = extract_players(semi_teams[team])
        for player in roster:
            team_dict[player] = extract_player_statistics(roster[player], team)
            player_names.append(player)
            rpg.append(team_dict[player]["rpg"])
            bpg.append(team_dict[player]["bpg"])
            ppg.append(team_dict[player]["ppg"])
        highest_rpg = sorted(zip(rpg, player_names), reverse=True)[:3]
        highest_bpg = sorted(zip(bpg, player_names), reverse=True)[:3]
        highest_ppg = sorted(zip(ppg, player_names), reverse=True)[:3]
        
        # Loop for storing info in "outer" lists
        for j in range(3):
            rpg_names.append(highest_rpg[j][1])
            rpg_scores.append(highest_rpg[j][0])
            bpg_names.append(highest_bpg[j][1])
            bpg_scores.append(highest_bpg[j][0])
            ppg_names.append(highest_ppg[j][1])
            ppg_scores.append(highest_ppg[j][0])

    # Plotting
    for names, scores in zip([rpg_names, bpg_names, ppg_names], [rpg_scores, bpg_scores, ppg_scores]):
        # Used for setting x-range of bars
        count = 0
        for i in range(8):
            # Setting team specific color
            color = colors[i]
            # Getting team name
            team = teams[i]
            # Setting range for bars
            x = range(count, count+3)
            count += 3
            # Storing values for specific portion of bar plot
            values = []
            for j in x:
                values.append(scores[j])
            # Setting bar values
            bars = plt.bar(x, values, color=color, label=team)
            plt.bar_label(bars)
        # Setting x labels as player names
        plt.xticks(range(len(names)), names, rotation=90)
        # Setting legend outside of plot to increase readability
        plt.legend(bbox_to_anchor=(1.05, 1.0), loc='upper left')
        plt.grid(False)
        # Making titles and saving files
        if names == rpg_names:
            plt.title("Rebounds per game")
            plt.tight_layout()
            plt.savefig("NBA_player_statistics/players_over_rpg.png")
        elif names == bpg_names:
            plt.title("Blocks per game")
            plt.tight_layout()
            plt.savefig("NBA_player_statistics/players_over_bpg.png")
        elif names == ppg_names:
            plt.title("Points per game")
            plt.tight_layout()
            plt.savefig("NBA_player_statistics/players_over_ppg.png")
        # Resetting plot figure for next plot
        plt.clf()    


semi_teams = get_teams(url)
plot_player_statistics(semi_teams)

