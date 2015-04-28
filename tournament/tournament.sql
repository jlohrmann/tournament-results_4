-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

DROP TABLE IF EXISTS players CASCADE;

CREATE TABLE players (
   playerid serial PRIMARY KEY,
   playername  varchar(100)
);


DROP TABLE IF EXISTS matches CASCADE; 
 
CREATE TABLE matches (
     matchId serial PRIMARY KEY,
     winnerid integer,
     loserid integer
);


CREATE VIEW view_swiss_pairings AS 
 SELECT DISTINCT winnerid, winnername, loserid, losername
   FROM 
   ( SELECT p.playerid as winnerid, p.playername as winnername, count(m.winnerid) as wins
      FROM players p
         LEFT JOIN matches m on m.winnerid = p.playerid 
          Group By p.playerid, p.playername
            ORDER BY wins DESC ) as junk,
   ( SELECT p2.playerid as loserid, p2.playername as losername, 
        count(m2.winnerid) as wins2
        FROM players p2
         LEFT JOIN matches m2 on m2.winnerid = p2.playerid
            Group By p2.playerid, p2.playername 
              ORDER BY wins2 DESC ) as junk2
    WHERE junk.wins = junk2.wins2 AND winnerid > loserid;

