#!/usr/bin/env python2.5

# Copyright 2010 bjweeks, MZMcBride

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import codecs
import datetime
import MySQLdb, MySQLdb.cursors
import re
import wikitools
import settings

skipped_pages = []
skipped_file = codecs.open('/home/mzmcbride/scripts/predadurr/skipped_pages.txt', 'r', 'utf-8')
for i in skipped_file.read().strip('\n').split('\n'):
    skipped_pages.append(i)
skipped_file.close()

excluded_titles = [
'^USS_',
'_[Ff]amily$',
'_[Mm]odel$',
'^FBI_',
'^The_',
'_School$',
'_Station$',
'_Band$',
'_Canada$',
'_Church$',
'_Tigers$',
'^List(s)?_of',
'^Numbers_in',
'^\d',
'\d$',
'_of_',
'_and_',
'_\&_',
'\(band\)',
'_FC$',
'_\([Ff]ilm\)$',
'_transmission$',
'_\(miniseries\)$',
'_College$',
'album\)$',
'song\)$',
'[Dd]isambiguation\)$',
'_Awards?$',
'_[Ss]chool',
'_team$',
'_[Hh]ighway',
]

jobs = [
'Athletes[,\n]',
'Accountants[,\n]',
'Actors[,\n]',
'Actresses[,\n]',
'Administrators[,\n]',
'Aerospace engineers[,\n]',
'Air traffic controllers[,\n]',
'Ambassadors[,\n]',
'Anesthetists[,\n]',
'Anchormen[,\n]',
'Animators[,\n]',
'Animal trainers[,\n]',
'Archaeologists[,\n]',
'Architects[,\n]',
'Art dealers[,\n]',
'Artists[,\n]',
'Astronauts[,\n]',
'Astronomers[,\n]',
'Athletic trainers[,\n]',
'Attorneys[,\n]',
'Authors[,\n]',
'Auditors[,\n]',
'Babysitters[,\n]',
'Bakers[,\n]',
'Bank tellers[,\n]',
'Bankers[,\n]',
'Barbers[,\n]',
'Baristas[,\n]',
'Barristers[,\n]',
'Bartenders[,\n]',
'Bassoonists[,\n]',
'Batmen[,\n]',
'Beauty therapists[,\n]',
'Beekeepers[,\n]',
'Bellhops[,\n]',
'Blacksmiths[,\n]',
'Boilermakers[,\n]',
'Bookkeepers[,\n]',
'Booksellers[,\n]',
'Brewers[,\n]',
'Builders[,\n]',
'Butchers[,\n]',
'Butlers[,\n]',
'Brain surgeons[,\n]',
'Cab drivers[,\n]',
'Calligraphers[,\n]',
'Cameramen[,\n]',
'Car designers[,\n]',
'Cardiologists[,\n]',
'Carpenters[,\n]',
'Cartoonists[,\n]',
'Cartographers[,\n]',
'Cashiers[,\n]',
'Cellists[,\n]',
'Chaplains[,\n]',
'Chess players[,\n]',
'Chief compliance officers[,\n]',
'Chief executive officers[,\n]',
'Chief information officers[,\n]',
'Chief financial officers[,\n]',
'Chief technology officers[,\n]',
'Chief privacy officers[,\n]',
'Chauffeurs[,\n]',
'Cheesemakers[,\n]',
'Chefs[,\n]',
'Chemists[,\n]',
'Chief of polices[,\n]',
'Chimney sweeps[,\n]',
'Cinematographers[,\n]',
'Civil servants[,\n]',
'Civil engineers[,\n]',
'Clarinetists[,\n]',
'Cleaners[,\n]',
'Clerks[,\n]',
'Clockmakers[,\n]',
'Clowns[,\n]',
'Coachs[,\n]',
'Coachmen[,\n]',
'Coast guards[,\n]',
'Cobblers[,\n]',
'Columnists[,\n]',
'Comedians[,\n]',
'Company secretaries[,\n]',
'Compasssmiths[,\n]',
'Composers[,\n]',
'Computer programmers[,\n]',
'Conductors[,\n]',
'Construction engineers[,\n]',
'Construction workers[,\n]',
'Consuls[,\n]',
'Consultants[,\n]',
'Contractors[,\n]',
'Cooks[,\n]',
'Coroners[,\n]',
'Corrections officers[,\n]',
'Cosmonauts[,\n]',
'Costume designers[,\n]',
'Couriers[,\n]',
'Cryptographers[,\n]',
'Cryptozoologists[,\n]',
'Curriers[,\n]',
'customer service advisors[,\n]',
'Customer service representatives[,\n]',
'Customs officers[,\n]',
'Dancers[,\n]',
'Dentists[,\n]',
'Deputies[,\n]',
'Dermatologists[,\n]',
'Detectives[,\n]',
'Dictators[,\n]',
'Disc jockeys[,\n]',
'Underwater divers[,\n]',
'Divers[,\n]',
'Doctors[,\n]',
'Dog walkers[,\n]',
'Doormen[,\n]',
'Dressmakers[,\n]',
'Croupiers[,\n]',
'Dealers[,\n]',
'Dummies[,\n]',
'Electricians[,\n]',
'Entertainers[,\n]',
'Escorts[,\n]',
'Engineers[,\n]',
'Falconers[,\n]',
'Farmers[,\n]',
'Farriers[,\n]',
'Fashion designers[,\n]',
'Film directors[,\n]',
'Film producers[,\n]',
'Financial advisers[,\n]',
'Fire marshals[,\n]',
'Fire Safety Officers[,\n]',
'Firefighters[,\n]',
'First Mates[,\n]',
'Fishmongers[,\n]',
'Fishermen[,\n]',
'Machinists[,\n]',
'Fitters[,\n]',
'Flavorists[,\n]',
'Fletchers[,\n]',
'Flight attendants[,\n]',
'Flight instructors[,\n]',
'Florists[,\n]',
'Flautists[,\n]',
'Food critics[,\n]',
'Footballers[,\n]',
'Foresters[,\n]',
'Fortune tellers[,\n]',
'Funeral directors[,\n]',
'Gamekeepers[,\n]',
'Game designers[,\n]',
'Game wardens[,\n]',
'Gardeners[,\n]',
'Gemcutters[,\n]',
'Genealogists[,\n]',
'Generals[,\n]',
'Geologists[,\n]',
'Gigolos[,\n]',
'Goldsmiths[,\n]',
'Government agents[,\n]',
'Governors[,\n]',
'Graphic designers[,\n]',
'Gravediggers[,\n]',
'Greengrocers[,\n]',
'Grocers[,\n]',
'Guides[,\n]',
'Guitarists[,\n]',
'Gunsmiths[,\n]',
'Hairdressers[,\n]',
'Hairstylists[,\n]',
'Handymen[,\n]',
'Harbourmasters[,\n]',
'Harpists[,\n]',
'Hatters[,\n]',
'Historians[,\n]',
'Homeopaths[,\n]',
'Hotel managers[,\n]',
'Housekeepers[,\n]',
'Housewifes[,\n]',
'Limners[,\n]',
'Illuminators[,\n]',
'Illusionists[,\n]',
'Illustrators[,\n]',
'Image consultants[,\n]',
'Importers[,\n]',
'Industrial engineers[,\n]',
'Industrialists[,\n]',
'Information Technologists[,\n]',
'Inkers[,\n]',
'Innkeepers[,\n]',
'Teachers[,\n]',
'Instructors[,\n]',
'Interior designers[,\n]',
'Interpreters[,\n]',
'Interrogators[,\n]',
'Inventors[,\n]',
'Investigators[,\n]',
'Investment bankers[,\n]',
'Investment brokers[,\n]',
'Ironmongers[,\n]',
'Ironmasters[,\n]',
'Ironworkers[,\n]',
'Jailers[,\n]',
'Janitors[,\n]',
'Jewellers[,\n]',
'Journalists[,\n]',
'Jurists[,\n]',
'Judges[,\n]',
'Jockeys[,\n]',
'Jogglers[,\n]',
'Karate masters[,\n]',
'Kinesiologists[,\n]',
'Kickboxers[,\n]',
'Kings[,\n]',
'kindergarten teachers[,\n]',
'Loan officers[,\n]',
'Laborers[,\n]',
'Landlords[,\n]',
'Landladies[,\n]',
'Laundresses[,\n]',
'Lavendars[,\n]',
'Law enforcement agents[,\n]',
'Lawyers[,\n]',
'Leadworkers[,\n]',
'Leatherers[,\n]',
'Leather workers[,\n]',
'Lecturers[,\n]',
'Level designers[,\n]',
'Mappers[,\n]',
'Librarianships[,\n]',
'Librettists[,\n]',
'Lifeguards[,\n]',
'Lighthouse keepers[,\n]',
'Lighting technicians[,\n]',
'Linemen[,\n]',
'Linguisticss[,\n]',
'Linguists[,\n]',
'Loan officers[,\n]',
'Lobbyists[,\n]',
'Locksmiths[,\n]',
'Logisticians[,\n]',
'Lumberjacks[,\n]',
'Lyricists[,\n]',
'Magistrates[,\n]',
'Magnates[,\n]',
'Maids[,\n]',
'Postmen[,\n]',
'Mailman or Mail carriers[,\n]',
'Make-up artists[,\n]',
'Management consultants[,\n]',
'Managers[,\n]',
'Manicurists[,\n]',
'Manufacturers[,\n]',
'Marine biologists[,\n]',
'Market gardeners[,\n]',
'Martial artists[,\n]',
'Masonries[,\n]',
'Masons[,\n]',
'Master of business administrators[,\n]',
'Massage therapists[,\n]',
'masseuses[,\n]',
'masseurs[,\n]',
'Matadors[,\n]',
'Mathematicians[,\n]',
'Mechanics[,\n]',
'Mechanical Engineers[,\n]',
'Mechanicians[,\n]',
'Mediators[,\n]',
'Medics[,\n]',
'Medical billers[,\n]',
'Medical Laboratory Scientists[,\n]',
'Medical Transcriptionists[,\n]',
'Mesmerists[,\n]',
'Bicycle messengers[,\n]',
'Messengers[,\n]',
'Mid-wifes[,\n]',
'Milkmen[,\n]',
'Milkmaids[,\n]',
'Millers[,\n]',
'Miners[,\n]',
'Missionaries[,\n]',
'Models[,\n]',
'Modellers[,\n]',
'Moneychangers[,\n]',
'Moneylenders[,\n]',
'Monks[,\n]',
'Mortgage brokers[,\n]',
'Mountaineers[,\n]',
'Muralists[,\n]',
'Music educators[,\n]',
'Musicians[,\n]',
'Navigators[,\n]',
'Negotiators[,\n]',
'Netmakers[,\n]',
'Neurologists[,\n]',
'Newscasters[,\n]',
'Night auditors[,\n]',
'Nightwatchmens[,\n]',
'Notary publics[,\n]',
'Notaries[,\n]',
'Novelists[,\n]',
'Numerologists[,\n]',
'Numismatists[,\n]',
'Nuns[,\n]',
'Nursemaids[,\n]',
'Nurses[,\n]',
'Nutritionists[,\n]',
'Oboists[,\n]',
'Obstetricians[,\n]',
'Occupational therapists[,\n]',
'Odontologists[,\n]',
'Oncologists[,\n]',
'Ontologists[,\n]',
'Operators[,\n]',
'Ophthalmologists[,\n]',
'Opticians[,\n]',
'Optometrists[,\n]',
'Oracles[,\n]',
'Ordinary Seamen[,\n]',
'Organizers[,\n]',
'Orthodontists[,\n]',
'Ornithologists[,\n]',
'Hostlers[,\n]',
'Ostlers[,\n]',
'Otorhinolaryngologists[,\n]',
'Optometrists[,\n]',
'Ocularists[,\n]',
'Painters[,\n]',
'Paleontologists[,\n]',
'Paralegals[,\n]',
'Paramedics[,\n]',
'Park rangers[,\n]',
'Parole Officers[,\n]',
'Pastors[,\n]',
'Patent attorneys[,\n]',
'Patent examiners[,\n]',
'Pathologists[,\n]',
'Pawnbrokers[,\n]',
'Peddlers[,\n]',
'Pediatricians[,\n]',
'Pedologists[,\n]',
'Percussionists[,\n]',
'Perfumers[,\n]',
'Personal Trainers[,\n]',
'Pharmacists[,\n]',
'Philanthropists[,\n]',
'Philologists[,\n]',
'Philosophers[,\n]',
'Photographers[,\n]',
'Physical Therapists[,\n]',
'Physicians[,\n]',
'Physician Assistants[,\n]',
'Physicists[,\n]',
'Physiognomists[,\n]',
'Physiotherapists[,\n]',
'Pianists[,\n]',
'Piano tuners[,\n]',
'Pilots[,\n]',
'Aviators[,\n]',
'Pirates[,\n]',
'Plumbers[,\n]',
'Podiatrists[,\n]',
'Poets[,\n]',
'Police inspectors[,\n]',
'Politicians[,\n]',
'Porters[,\n]',
'Presenters[,\n]',
'Presidents[,\n]',
'Press officers[,\n]',
'Priests[,\n]',
'Princesss[,\n]',
'Principals[,\n]',
'Printers[,\n]',
'Prison officers[,\n]',
'Private detectives[,\n]',
'Probation Officers[,\n]',
'Proctologists[,\n]',
'Product designers[,\n]',
'Professors[,\n]',
'Professional dominants[,\n]',
'Programmers[,\n]',
'Project Managers[,\n]',
'Proofreaders[,\n]',
'Prostitutes[,\n]',
'Psychiatrists[,\n]',
'Psychodramatists[,\n]',
'Psychologists[,\n]',
'Press officers[,\n]',
'Public Relations Officers[,\n]',
'Public speakers[,\n]',
'Publishers[,\n]',
'Porn stars[,\n]',
'Queen consorts[,\n]',
'Queen regnants[,\n]',
'Quilters[,\n]',
'Rabbis[,\n]',
'Radiologists[,\n]',
'Radiographers[,\n]',
'Real estate brokers[,\n]',
'Real estate investors[,\n]',
'Real estate developers[,\n]',
'Receptionists[,\n]',
'Record producers[,\n]',
'Referees[,\n]',
'Refuse collectors[,\n]',
'Registrars[,\n]',
'Registered Nurses[,\n]',
'Reporters[,\n]',
'Researchers[,\n]',
'Respiratory Therapists[,\n]',
'Restaurateurs[,\n]',
'Retailers[,\n]',
'Rubbish Collectors[,\n]',
'Sexologists[,\n]',
'Sex Slaves[,\n]',
'Sailmakers[,\n]',
'Sailors[,\n]',
'Salesmens[,\n]',
'Sanitation workers[,\n]',
'Sauciers[,\n]',
'Saxophonists[,\n]',
'Sawyers[,\n]',
'Scientists[,\n]',
'School superintendents[,\n]',
'Reconnaissances[,\n]',
'Scouts[,\n]',
'Screenwriters[,\n]',
'Scribes[,\n]',
'Scriveners[,\n]',
'Seamstresss[,\n]',
'Second Mates[,\n]',
'Secret service agents[,\n]',
'Secretary generals[,\n]',
'Security guards[,\n]',
'Senators[,\n]',
'Search engine optimizers[,\n]',
'Sextons[,\n]',
'Sheepshearers[,\n]',
'Sheriffs[,\n]',
'Sheriff officers[,\n]',
'Shoemakers[,\n]',
'Shoeshiners[,\n]',
'Shop assistants[,\n]',
'Singers[,\n]',
'Skydivers[,\n]',
'Sleepers[,\n]',
'Sleuths[,\n]',
'Social workers[,\n]',
'Socialites[,\n]',
'Software engineers[,\n]',
'Soil scientists[,\n]',
'Soldiers[,\n]',
'Solicitors[,\n]',
'Sommeliers[,\n]',
'Sonographers[,\n]',
'Sound Engineers[,\n]',
'Special agents[,\n]',
'Speech therapists[,\n]',
'Sportsmen[,\n]',
'Spies[,\n]',
'Statisticians[,\n]',
'Street artists[,\n]',
'Street musicians[,\n]',
'Stevedores[,\n]',
'Street sweepers[,\n]',
'Street vendors[,\n]',
'Structural engineers[,\n]',
'Stunt doubles[,\n]',
'Stunt performers[,\n]',
'Surgeons[,\n]',
'Supervisors[,\n]',
'Surveyors[,\n]',
'Swimmers[,\n]',
'Switchboard operators[,\n]',
'System administrators[,\n]',
'Systems analysts[,\n]',
'Students[,\n]',
'Tailors[,\n]',
'Tanners[,\n]',
'Tapestrymakers[,\n]',
'Tapicers[,\n]',
'Tapesters[,\n]',
'Tax collectors[,\n]',
'Tax lawyers[,\n]',
'Taxidermists[,\n]',
'Taxicab drivers[,\n]',
'Taxonomists[,\n]',
'Tea ladies[,\n]',
'Teachers[,\n]',
'Technicians[,\n]',
'Technologists[,\n]',
'Technical writers[,\n]',
'Telegraphists[,\n]',
'Telegraphers[,\n]',
'Telephone operators[,\n]',
'Tennis players[,\n]',
'Terminators[,\n]',
'Test developers[,\n]',
'Test pilots[,\n]',
'Thatchers[,\n]',
'Theatre directors[,\n]',
'Therapists[,\n]',
'Thimblers[,\n]',
'Tilers[,\n]',
'Toolmakers[,\n]',
'Tour Guides[,\n]',
'Trademark attorneys[,\n]',
'Merchants[,\n]',
'Traders[,\n]',
'Tradesmen[,\n]',
'Trainers[,\n]',
'Transit planners[,\n]',
'Translators[,\n]',
'Transport Planners[,\n]',
'Treasurers[,\n]',
'Truck drivers[,\n]',
'Turners[,\n]',
'Tutors[,\n]',
'Tylers[,\n]',
'Typists[,\n]',
'Undertakers[,\n]',
'Ufologists[,\n]',
'Undercover agents[,\n]',
'Underwriters[,\n]',
'Upholsterers[,\n]',
'Urban planners[,\n]',
'Urologists[,\n]',
'Ushers[,\n]',
'Underwear models[,\n]',
'Valets[,\n]',
'Sextons[,\n]',
'Vergers[,\n]',
'Veterinarians[,\n]',
'Vibraphonists[,\n]',
'Vicars[,\n]',
'Video editors[,\n]',
'Video game developers[,\n]',
'Vintners[,\n]',
'Violinists[,\n]',
'Violists[,\n]',
'Voice Actors[,\n]',
'Waiting staff[,\n]',
'Watchmakers[,\n]',
'Weaponsmiths[,\n]',
'weather forecasters[,\n]',
'Weathermen[,\n]',
'Weavers[,\n]',
'Web designers[,\n]',
'Web developers[,\n]',
'Wedding planners[,\n]',
'Welders[,\n]',
'Wet nurses[,\n]',
'Winemakers[,\n]',
'Wood cutters[,\n]',
'Woodcarvers[,\n]',
'Wranglers[,\n]',
'Writers[,\n]',
'Xylophonists[,\n]',
'X-ray Operators[,\n]',
'Yodelers[,\n]',
'Yinder Hos[,\n]',
'zen masters[,\n]',
'zoo veternarians[,\n]',
'Zookeepers[,\n]',
'Zoologists[,\n]',
'NULL',
]

excluded_categories = [
'_clubs[,\n]',
'-century',
'_phrases[,\n]',
'_organizations_',
'_pseudonyms[,\n]',
'_bc_(deaths',
'births)',
'political_parties',
'companies_',
'_species[,\n]',
'_software[,\n]',
'communes_of_',
'_(dis)?establishments[,\n]',
'television_series[,\n]',
'_cathedrals_',
'_lists[,\n]',
'needing_coordinates',
'organizations_based_in',
'roller_coasters_in',
'_singles[,\n]',
'_albums',
'(artist',
'geography)_stubs',
'year_of_death',
'living_people',
'[\ds]_births',
'[\ds]_deaths',
'(rock',
'music',
'musical)_groups',
'record_labels',
'fictional',
'disambiguation',
'_films[,\n]',
'Geography_of',
'Districts_of',
'_songs[,\n]',
'_books[,\n]',
'_novels[,\n]',
'_films[,\n]',
]

excluded_templates = [
'infobox_single',
'infobox_book',
'infobox_television',
'infobox_stadium',
'infobox_company',
'infobox_motorsport_venue',
'infobox_album',
'infobox_tv_channel',
'infobox_film',
'infobox_television_film',
'infobox_software',
'infobox_television_season',
'infobox_scotus_case',
'infobox_golf_tournament',
'infobox_website',
'infobox_vg',
'infobox_university',
'infobox_podcast',
'infobox_bus_transit',
'infobox_shopping_mall',
'infobox_dotcom_company',
'infobox_painting',
'infobox_football_club',
's-rail-start',
]

excluded_titles_re = re.compile(r'(%s)' % '|'.join(str(i) for i in excluded_titles))
jobs_re = re.compile(r'(%s)' % '|'.join(str(i.replace(' ', '_')) for i in jobs), re.I|re.U)
excluded_categories_re = re.compile(r'(%s)' % '|'.join(str(i) for i in excluded_categories), re.I|re.U)
excluded_templates_re = re.compile(r'(%s)' % '|'.join(str(i) for i in excluded_templates), re.I|re.U)
capital_letters_re = re.compile(r'[A-Z]')

report_title = settings.rootpage + 'Potential biographies of living people (4)'

report_template = u'''
Articles that potentially need to be in [[:Category:Living people]] (limited to the first 2000 \
entries). List generated mostly using magic; data as of <onlyinclude>%s</onlyinclude>.

{| class="wikitable sortable plainlinks" style="width:100%%; margin:auto;"
|- style="white-space:nowrap;"
! No.
! Biography
|-
%s
|}
'''

wiki = wikitools.Wiki(settings.apiurl)
wiki.login(settings.username, settings.password)

conn = MySQLdb.connect(host=settings.host, db=settings.dbname, read_default_file='~/.my.cnf', cursorclass=MySQLdb.cursors.SSCursor)
cursor = conn.cursor()
cursor.execute('SET SESSION group_concat_max_len = 1000000;')
cursor.execute('''
/* potenshblps4.py SLOW_OK */
SELECT
  page_title,
  GROUP_CONCAT(cl_to),
  GROUP_CONCAT(tl_title)
FROM page
LEFT JOIN templatelinks
ON tl_from = page_id
LEFT JOIN categorylinks
ON cl_from = page_id
WHERE page_namespace = 0
AND page_is_redirect = 0
GROUP BY page_id
ORDER BY page_id DESC
LIMIT 200000;
''')

i = 1
output = []
while True:
    row = cursor.fetchone()
    if i > 2000:
        break
    if row == None:
        break
    page_title = u'%s' % unicode(row[0], 'utf-8')
    if page_title in skipped_pages:
        continue
    if row[1] is not None:
        cl_to = u'%s' % unicode(row[1], 'utf-8')
    else:
        cl_to = 'NULL'
    if row[2] is not None:
        tl_title = u'%s' % unicode(row[2], 'utf-8')
    else:
        tl_title = ''
    if (
        not excluded_categories_re.search(cl_to) and
        not excluded_titles_re.search(page_title) and
        page_title.find('_') != -1 and
        jobs_re.search(cl_to) and
        len(capital_letters_re.findall(page_title)) > 1 and
        not excluded_templates_re.search(tl_title)
        ):
        table_row = u'''| %d
| [[%s]]
|-''' % (i, page_title)
        output.append(table_row)
        i += 1

cursor.close()

cursor = conn.cursor()
cursor.execute('SELECT UNIX_TIMESTAMP() - UNIX_TIMESTAMP(rc_timestamp) FROM recentchanges ORDER BY rc_timestamp DESC LIMIT 1;')
rep_lag = cursor.fetchone()[0]
current_of = (datetime.datetime.utcnow() - datetime.timedelta(seconds=rep_lag)).strftime('%H:%M, %d %B %Y (UTC)')

report = wikitools.Page(wiki, report_title)
report_text = report_template % (current_of, '\n'.join(output))
report_text = report_text.encode('utf-8')
report.edit(report_text, summary=settings.editsumm, bot=1)

cursor.close()
conn.close()
