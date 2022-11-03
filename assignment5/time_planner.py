from bs4 import BeautifulSoup
import requests
import re
import os

"""
The URL used in this exercise links to the 2021/22 FIS alpine ski world cup, and may be different than
the one described in the latest iteration of the assignment. This is permitted, as @benjara said on october
29th at 12:46 pm:
'@helenwan because of the confusion, any FIS page from 2019-2020 to 2021-2022 will be accepted, 
as long as you make it clear which one you use.'
Link to quote: https://mattermost.uio.no/ifi-undervisning/pl/g9a1r6qx8jnc9y8i4s7rdtjeoa

Changing the link to a different FIS page may cause the script to no longer work.
"""
url = "https://en.wikipedia.org/wiki/2021-22_FIS_Alpine_Ski_World_Cup"

def extract_events(url):
    
    disciplines = {
        "DH": "Downhill",
        "SL": "Slalom",
        "GS": "Giant Slalom",
        "SG": "Super Giant Slalom",
        "AC": "Alpine Combined",
        "PG": "Parallel Giant Slalom",
    }
    
    # Get HTML
    response = requests.get(url)
    
    # Make soup
    soup = BeautifulSoup(response.text, "html.parser")

    # Find calendar
    calendar_header = soup.find(id="Calendar")
    
    # Find calendar table
    calendar_table = calendar_header.find_all_next("table")[0]
    
    # Find rows of table
    rows = calendar_table.find_all("tr")
    
    found_date = None
    found_venue = None
    found_discipline=None
    
    # Saving values to list
    events = []
    
    full_row_length = 11
    medium_row_length = full_row_length - 1
    short_row_length = full_row_length - 2

    """
    cells = rows[26].find_all("td")
    cell1 = cells[1].text.strip()
    cell2 = cells[2].text.strip()
    cell3 = cells[3].text.strip()
    cell4 = cells[4].text.strip()
    print(len(cells), cell1, cell2, cell3, cell4)
    for row in rows[36:]:
        cells = row.find_all("td")
        cell1 = cells[1].text.strip()
        cell2 = cells[2].text.strip()
        cell3 = cells[3].text.strip()
        cell4 = cells[4].text.strip()
        print(len(cells), cell1, cell2, cell3, cell4)
    
    exit()
    """

    for row in rows[1:]:
        cells = row.find_all("td")
        
        if len(cells) not in [full_row_length, medium_row_length, short_row_length]:
            continue
        
        date = cells[2]
        
        # Find event id
        if re.match(r"\d{1,2}\s\w+\s20\d{2}",date.text.strip()):
            found_date = date.text.strip()
        else :
            found_date = None
        if len(cells) == full_row_length :
            venue_cell = cells [3]
            found_venue = venue_cell.text.strip()
            discipline_index = 5
        elif len(cells) == medium_row_length:
            discipline_index = 4
        else:
            discipline_index = 3
        
        discipline = cells[discipline_index]
        discipline_regex = r"(?:DH|SL|GS|SG|AC|PG)"
        discipline_match = re.search(discipline_regex, discipline.text.strip())
        if discipline_match:
            found_discipline = disciplines[discipline_match.group(0)]
        else:
            discipline = cells[discipline_index + 1]
            discipline_match = re.search(discipline_regex, discipline.text.strip())
            if discipline_match:
                found_discipline = disciplines[discipline_match.group(0)]
            else:
                found_discipline = None
            
        if found_venue and found_date and found_discipline:
            events.append((found_date, found_venue, found_discipline))

    return events

def create_betting_slip(events, save_as):
    """
    Saves a markdown formatted betting slip to the location 
    './datetime_filter/<save_as>.md'
    Input:
    - events: List of events returned from the extract_events function
    - save_as: name of betting slip
    """
    output = os.path.join(os.getcwd(), "datetime_filter", save_as)

    with open(output, "w", encoding="utf-8") as outfile:
        outfile.write (f"# BETTING SLIP ({save_as})\n\nName:\n\n")
        outfile.write (" Date | Venue | Discipline | Who wins ?\n")
        outfile.write (" --- | --- | --- | --- \n")
        for e in events :
            date, venue, discipline = e
            outfile . write (f"{date} | {venue} | {discipline} | \n")

    

events = extract_events(url)
create_betting_slip(events, "betting_slip_empty.md")
