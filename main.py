import os
import sys
import json
from rich import print
from rich.console import Console
console = Console()

STREAMING_HISTORY_FOLDER = "./streamingHistory/"
OUTPUT_FOLDER = "output/"
OUTPUT_FILE = "result.html"

import output as o
import database as db

def ms_to_time(ms):
	"""Transform millisecond to humain readable time"""

	minutes=  int(ms/60000)
	hours= 	  int(ms/3600000)
	day = 	  int(ms/86400000)
	return f"{day} Days = {hours} Hours = {minutes} Minutes"

def populate_database():
	"""Populate database with data contained in JSON files"""

	console.rule(f"[bold cyan]Populating Database[/bold cyan]",style="cyan")
	db.create_table(True)
	inserted_lines = 0
	if len(os.listdir(STREAMING_HISTORY_FOLDER)) > 0:
		for f in os.listdir(STREAMING_HISTORY_FOLDER):
			file = open(STREAMING_HISTORY_FOLDER + f,encoding='UTF-8')
			history = json.load(file)
			lines = [[x["endTime"],x["artistName"].replace("\'"," "),x["trackName"].replace("\'"," "),int(x["msPlayed"])] for x in history]	
			db.insert_lines(lines)
			inserted_lines+=len(lines)
		print(f"Populating Database | [bold green]OK[/bold green] ({inserted_lines} Inserted Lines)")
	else:
		print(f"Populating Database | [bold red]KO[/bold red], there is no history file inside {STREAMING_HISTORY_FOLDER}")
	
def render_html():
	"""Render fav song, fav artist, history, grouped song, grouped artist"""
	history = db.get_sorted_history("ASC")
	if len(history)>0:
		artists = [list(x) for x in db.get_total_time_group_by("artist","DESC")]
		for x in artists:
			x[1] = ms_to_time(x[1])

		songs = [list(x) for x in db.get_total_time_group_by("song","DESC")]
		for x in songs:
			x[1] = ms_to_time(x[1])

		total = ms_to_time(db.get_total_time())
		favorite_artist = list(db.get_fav("artist"))
		favorite_artist[1] = ms_to_time(favorite_artist[1])
		favorite_song = list(db.get_fav("song"))
		favorite_song[1] = ms_to_time(favorite_song[1])

		context = {
		"total":total,
		"favorite_artist":favorite_artist,
		"favorite_song":favorite_song,
		"history":history,
		"artists":artists,
		"songs":songs
		}

		o.render(context,OUTPUT_FOLDER,OUTPUT_FILE)
	else:
		o.render({},OUTPUT_FOLDER,OUTPUT_FILE)

def show_help():
	print("")
	console.rule(f"[bold green]HELP[/bold green]",style="green")
	print(f"1) Put your spotify [bold green]StreamingHistory(number).json[/bold green] files in the [bold green]{STREAMING_HISTORY_FOLDER}[/bold green] folder")
	print(f"2) Use [bold green]-db[/bold green] to load history data inside database")
	print(f"3) Use [bold green]-generate[/bold green] to generate a pretty html file for visualizing your data")
if __name__ == "__main__":
	for arg in sys.argv[1:]:
		if arg == "-help":
			show_help()
		elif arg == "-db":
			db.connect("spotify.db")
			populate_database()
			db.close()

		elif arg == "-render":
			db.connect("spotify.db")
			render_html()
			db.close()
		else:
			show_help()