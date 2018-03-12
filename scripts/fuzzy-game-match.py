#!/usr/bin/python

# Perform a "fuzzy" match on game names

from difflib import SequenceMatcher

matches = []

i = 1

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

with open('/Raspberry Pi/RetroPie/snes-100.txt', 'r') as f:
    top_games = f.read().splitlines()

with open('/Raspberry Pi/RetroPie/snes-games.txt', 'r') as f:
    all_games = f.read().splitlines()

with open('/Raspberry Pi/RetroPie/best-snes-games.txt', 'w+') as out_file:

    for top in top_games:
        top = top.split(' ', 1)[1]
        for all in all_games:
            match_all = all.rsplit('(', 1)[0]
            pct = similar(top, match_all)
            if pct > 0.85:
                print i, top, all, pct
                i += 1
                matches.append(all)

    matches.sort()

    out_file.writelines("%s\n" % l for l in matches)

