from csv2fisxml import convert_results


src = []
src.append({'fname': 'a1.csv', 'codex': '7350', 'sex': 'L'})
src.append({'fname': 'a2.csv', 'codex': '2381', 'sex': 'M'})
src.append({'fname': 'a3.csv', 'codex': '7351', 'sex': 'L'})
src.append({'fname': 'a4.csv', 'codex': '2382', 'sex': 'M'})
src.append({'fname': 'b1.csv', 'codex': '7352', 'sex': 'L'})
src.append({'fname': 'b2.csv', 'codex': '2383', 'sex': 'M'})
src.append({'fname': 'b3.csv', 'codex': '7353', 'sex': 'L'})
src.append({'fname': 'b4.csv', 'codex': '2384', 'sex': 'M'})

race = {}
race['season'] = '2016'
race['discipline'] = 'GS'
race['date_d'] = '31'
race['date_m'] = '1'
race['date_y'] = '2016'
race['race_name'] = 'LEKI CUP'
race['place'] = 'Šachty - Vysoké nad Jizerou'
race['club'] = 'Český skiklub Vysoké nad Jizerou'

jury = []
jury.append({'fname': "Jiří", 'lname': "Lukáš", 'function': "Chiefrace"})
jury.append({'fname': "Jan", 'lname': "Pohanka", 'function': "Referee"})

for s in src:
    convert_results(race, jury, s)
