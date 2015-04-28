#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    conn = connect()
    cur = conn.cursor()
    cur.execute("""delete  from matches""")
    conn.close


def deletePlayers():
    """Remove all the player records from the database."""
    conn = connect()
    cur = conn.cursor()
    cur.execute("""truncate players;""") 
    cur.execute("""truncate matches;""") 
    conn.commit()
    conn.close

def countPlayers():
    """Returns the number of players currently registered."""
    conn  = connect()
    cur = conn.cursor()
    cur.execute("""select count(*) from players;""")
    data = cur.fetchall()
    for dataOut in data:
        count =  dataOut[0] 
    return  count 

def registerPlayer(name):
    """Adds a player to the tournament database.
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    conn = connect()
    cur = conn.cursor()
    playerId = cur.execute("""INSERT INTO players ( playername ) values (%s) """,(name,))
    conn.commit()
    conn.close


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    conn = connect()
    cur = conn.cursor()
    cur.execute("""select playerid, playername, count(m.winnerid) as numberofwins, 
                 count(m.winnerid) + count(m2.loserid) as numberofmatches 
                  from players p left join matches m on m.winnerid = p.playerid 
                   left join matches m2 on m2.loserid = p.playerid 
                     group by p.playerid, p.playername;""")
    data = cur.fetchall()
    resultList = []
    for dataOut in data:
        resultList.append(dataOut) 
    conn.close
    return resultList


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.
    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    conn = connect()
    cur = conn.cursor()
    cur.execute("""INSERT INTO matches( winnerid, loserid) 
                    VALUES (%s, %s);""", (winner, loser) )

#    cur.execute("""UPDATE players set  numberofwins = numberofwins + 1, 
#                     numberofmatches = numberofmatches + 1 
#                   WHERE playerid = %s;""", (winner,))
# 
#
#    cur.execute("""UPDATE players set  numberofmatches = numberofmatches + 1
#                     WHERE playerid = %s;""", (loser,))
#
    conn.commit()

def swissPairings():
    """Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    conn = connect()
    cur = conn.cursor()
    cur.execute("""SELECT "winnerid", 
                          "winnername", 
                          "loserid", 
                          "losername" 
                   from view_swiss_pairings v; """)
    data = cur.fetchall()
    resultList = [] 
    for dataOut in data: 
        resultList.append(dataOut)
    return resultList

connect()


