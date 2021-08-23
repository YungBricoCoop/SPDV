import sqlite3
from sqlite3 import Error
from rich import print
from rich.console import Console
console = Console()
conn = None
def connect(db_file):
    console.rule(f"[bold cyan]Connecting to DB {db_file}[/bold cyan]",style="cyan")
    try:
        global conn
        conn = sqlite3.connect(db_file)
        print("DB connection | [bold green]OK")
    except Error as e:
        print("DB connection | [bold red]KO")
        print(e)
        conn.close()

def create_table(erase):
    try:
        if erase:
            conn.execute('''DROP TABLE IF EXISTS T_History;''')  
        conn.execute('''CREATE TABLE T_History (endTime text, artistName text, trackName text, msPlayed real)''')    
        conn.commit()
    except Error as e:
        print(e)
def insert_line(endTime,artistName,trackName,msPlayed):
    try:
        conn.execute(f"INSERT INTO T_History (endTime,artistName,trackName,msPlayed) VALUES ('{endTime}', '{artistName}', '{trackName}', {msPlayed} )");    
        
    except Error as e:
        print(e)
def insert_lines(lines):
    for l in lines:
        insert_line(l[0],l[1],l[2],l[3])
    conn.commit()
def get_all_history():
    """Get all the history """
    cur = conn.cursor()
    cur.execute("SELECT * FROM T_History")
    rows = cur.fetchall()
    return rows

def get_sorted_history(order):
    """Get all the history but can be order by date with ASC or DESC"""
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM T_History ORDER BY date(endTime) {order}")  
    return cur.fetchall()        

def get_filtered_history(fil,name):
    """Filter the history by artist or by song"""
    rows = None
    if fil == "artist":
        cur = conn.cursor()
        cur.execute("SELECT * FROM T_History WHERE artistName=?",(name,))  
        rows = cur.fetchall()        
    if fil == "song":
        cur = conn.cursor()
        cur.execute("SELECT * FROM T_History WHERE trackName=?",(name,))  
        rows = cur.fetchall()
    return rows

def get_filtered_grouped_history(name,order):
    """Filter the history by artist and group tracks"""
    cur = conn.cursor()
    cur.execute(f"SELECT trackName,SUM(msPlayed),COUNT(msPlayed) FROM T_History WHERE artistName=? group by trackName order by SUM(msPlayed) {order}",(name,))  
    return cur.fetchall()  

def get_total_time():     
    """Get the total played time in ms"""  
    cur = conn.cursor()
    cur.execute("SELECT SUM(msPlayed) FROM T_History")     
    return cur.fetchall()[0][0] 

def get_total_time_by(fil,name):
    """Get total time,count per artist or song"""
    if fil == "artist":
        cur = conn.cursor()
        cur.execute("SELECT artistName,SUM(msPlayed),COUNT(msPlayed) FROM T_History WHERE artistName=? group by artistName ",(name,))     
        return cur.fetchall()[0] 
    if fil == "song":
        cur = conn.cursor()
        cur.execute("SELECT trackName,SUM(msPlayed),COUNT(msPlayed) FROM T_History WHERE trackName=? group by trackName",(name,))     
        return cur.fetchall()[0] 

def get_total_time_group_by(fil,order):
    """Get total time,count grouped by artist or song"""
    if fil == "artist":
        cur = conn.cursor()
        cur.execute(f"SELECT artistName,SUM(msPlayed),COUNT(msPlayed) FROM T_History group by artistName order by SUM(msPlayed) {order}")     
        return cur.fetchall()
    if fil == "song":
        cur = conn.cursor()
        cur.execute(f"SELECT trackName,SUM(msPlayed),COUNT(msPlayed) FROM T_History group by trackName order by SUM(msPlayed) {order}")     
        return cur.fetchall()

def get_fav(fil):
    """Get favorite artist or song"""
    if fil == "artist":
        cur = conn.cursor()
        cur.execute(f"SELECT artistName,SUM(msPlayed),COUNT(msPlayed) FROM T_History group by artistName order by SUM(msPlayed) DESC LIMIT 1")     
        return cur.fetchall()[0]
    if fil == "song":
        cur = conn.cursor()
        cur.execute(f"SELECT trackName,SUM(msPlayed),COUNT(msPlayed) FROM T_History group by trackName order by SUM(msPlayed) DESC LIMIT 1")     
        return cur.fetchall()[0]    

def close():
    """Close database connection"""

    console.rule("[bold cyan]Disconnecting from DB [/bold cyan]",style="cyan")
    try:
        conn.close()
        print("DB disconnection | [bold green]OK")
    except Error as e:
        print("DB disconnection | [bold red]KO")



