import csv
import xml.etree.ElementTree as etree
import xml.dom.minidom as minidom


k_name = 'Jméno'
k_fiscode = 'Id'
k_rc = 'Rodné číslo'
k_bib = 'Stč'
k_time = 'Čas'
k_rank = 'Poř'


def prettify(elem):
    """Return a pretty-printed XML string for the Element.
    """
    rough_string = etree.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")


def add_competitor(parent, c):
    competitor = etree.SubElement(parent, "Competitor")
    etree.SubElement(competitor, "Lastname").text = c[k_name].split()[0]
    givenname = c[k_name].split()[1:]
    givenname = " ".join(givenname)
    etree.SubElement(competitor, "Firstname").text = givenname

    fiscode = 0
    try:
        fiscode = int(c[k_fiscode])
    except:
        fiscode = 0

    etree.SubElement(competitor, "Fiscode").text = str(fiscode)

    year = int(c[k_rc][:2])
    year = year + 1900 if year > 50 else year + 2000
    sex = 'L' if c[k_rc][2] == '5' else 'M'

    etree.SubElement(competitor, "Sex").set("Sex", sex)
    # etree.SubElement(competitor, "Sex").text = sex
    etree.SubElement(competitor, "Yearofbirth").text = str(year)
    etree.SubElement(competitor, "Nation").text = 'CZE'


def add_ranked(parent, c):
    ranked = etree.SubElement(parent, "AL_ranked")
    ranked.set("Status", "QLF")
    etree.SubElement(ranked, "Rank").text = c[k_rank]
    etree.SubElement(ranked, "Bib").text = c[k_bib]
    add_competitor(ranked, c)
    result = etree.SubElement(ranked, "AL_result")
    etree.SubElement(result, "Timerun1").text = c[k_time]
    etree.SubElement(result, "Totaltime").text = c[k_time]
    etree.SubElement(result, "Racepoints").text = '0.0'


def add_notranked(parent, c, st):
    notranked = etree.SubElement(parent, "AL_notranked")
    notranked.set("Status", st)
    etree.SubElement(notranked, "Bib").text = c[k_bib]
    add_competitor(notranked, c)
    # if st == 'DSQ':
    etree.SubElement(notranked, "Gate").text = '99'
    etree.SubElement(notranked, "Run").text = '1'


def add_jury(parent, person):
    j = etree.SubElement(parent, "Jury")
    j.set('Function', person['function'])
    etree.SubElement(j, "Jurylastname").text = person['lname'].upper()
    etree.SubElement(j, "Juryfirstname").text = person['fname']
    etree.SubElement(j, "Jurynation")


def convert_results(raceinfo, jury, results):
    csvresults = []
    with open(results['fname']) as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            row = {k: v.strip() for k, v in row.items()}
            csvresults.append(row)

    fisresults = etree.Element('Fisresults')
    rhead = etree.SubElement(fisresults, "Raceheader")
    race = etree.SubElement(fisresults, "AL_race")

    rhead.set('Sector', 'AL')
    rhead.set('Sex', results['sex'])
    etree.SubElement(rhead, "Season").text = raceinfo['season']
    etree.SubElement(rhead, "Codex").text = results['codex']
    etree.SubElement(rhead, "Discipline").text = raceinfo['discipline']
    etree.SubElement(rhead, "Category").text = 'FIS'
    etree.SubElement(rhead, "Nation")
    rdate = etree.SubElement(rhead, "Racedate")
    etree.SubElement(rdate, "Day").text = raceinfo['date_d']
    etree.SubElement(rdate, "Month").text = raceinfo['date_m']
    etree.SubElement(rdate, "Year").text = raceinfo['date_y']
    etree.SubElement(rhead, "Eventname").text = raceinfo['race_name']
    etree.SubElement(rhead, "Place").text = raceinfo['place']
    etree.SubElement(rhead, "Clubname").text = raceinfo['club']

    td = etree.SubElement(rhead, "TD")
    td.set('Function', 'Delegate')
    etree.SubElement(td, "Tdnumber").text = '999'
    etree.SubElement(td, "Tdlastname")
    etree.SubElement(td, "Tdfirstname")
    etree.SubElement(td, "Tdnation")

    for ju in jury:
        add_jury(race, ju)

    rinfo = etree.SubElement(race, "AL_raceinfo")
    etree.SubElement(rinfo, "Snow")
    etree.SubElement(rinfo, "Weather")
    etree.SubElement(rinfo, "Temperatureatstart")
    etree.SubElement(rinfo, "Temperatureatfinish")
    etree.SubElement(rinfo, "Timingby")
    etree.SubElement(rinfo, "Dataprocessingby")
    etree.SubElement(rinfo, "Softwarecompany")
    etree.SubElement(rinfo, "Softwarename")
    etree.SubElement(rinfo, "Version")
    etree.SubElement(rinfo, "Usedfislist")
    etree.SubElement(rinfo, "Appliedpenalty")
    etree.SubElement(rinfo, "Calculatedpenalty")
    etree.SubElement(rinfo, "Fvalue")

    classified = etree.SubElement(race, "AL_classified")
    notclassified = etree.SubElement(race, "AL_notclassified")

    for r in csvresults:
        if r[k_time] == 'Diskval.':
            add_notranked(notclassified, r, 'DSQ')
        elif r[k_time] == 'Nestart.':
            add_notranked(notclassified, r, 'DNS')
        elif r[k_time] == 'Odstoupil':
            add_notranked(notclassified, r, 'DNF')
        else:
            add_ranked(classified, r)

    ofname = 'CZE' + results['codex'] + '.xml'
    with open(ofname, 'w') as xmlfile:
        xmlfile.write(prettify(fisresults))
    # print(prettify(fisresults), file='1.xml')

