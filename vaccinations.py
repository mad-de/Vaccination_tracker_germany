#!/usr/bin/python
# -*- coding: utf-8 -*-

import pandas as pd
import datetime
import requests
import os

url_vaccinations = 'https://www.rki.de/DE/Content/InfAZ/N/Neuartiges_Coronavirus/Daten/Impfquotenmonitoring.xlsx?__blob=publicationFile'
vacc_request = requests.get(url_vaccinations)

datapath = 'Impfquotenmonitoring.xlsx'

with open(datapath, 'wb') as f:
    f.write(vacc_request.content)

vaccinations_table = pd.read_excel(datapath, sheet_name=1)
vaccinations_date = pd.read_excel(datapath, sheet_name=0)

vaccination_ger_num = vaccinations_table.values.tolist()[16][2]
vaccination_ger_perc = vaccination_ger_num / 83002000 * 100
vaccination_ger_diff = vaccinations_table.values.tolist()[16][2]
vaccination_date = str(vaccinations_date.values.tolist()[1])
vaccination_date = vaccination_date.split('Impfungen_bis_einschl_', 1)[1]
vaccination_date = vaccination_date.split(')', 1)[0]

vaccinations_diff_table = pd.read_excel('Impfquotenmonitoring.xlsx', sheet_name="Impfungen_proTag").fillna("missing").values.tolist()
vaccinations_diff_dates = len(vaccinations_diff_table)

# fix random appearing numbers in the table
repl_string = 'Impfungen gesamt'
while vaccinations_diff_table[vaccinations_diff_dates-1][0] == 'missing' or vaccinations_diff_table[vaccinations_diff_dates-1][0] == repl_string:
   vaccinations_diff_dates = vaccinations_diff_dates - 1

vaccinations_diff = (float(vaccinations_diff_table[vaccinations_diff_dates-1][1]) - float(vaccinations_diff_table[vaccinations_diff_dates-2][1])) / float(vaccinations_diff_table[vaccinations_diff_dates-1][1]) * 100

vaccinations_diff_vorz = ""
if vaccinations_diff > 0:
   vaccinations_diff_vorz = "+"

vaccinations = "Aktuelle COVID-19-Impfungen in Deutschland: Es wurden " + str("{:,.0f}".format(vaccination_ger_num)) + " Personen (" + str("{:.2f}".format(vaccination_ger_perc)) + " % der Bevölkerung) bis zum " + str(format(vaccination_date)) + " geimpft. An diesem Tag wurden " + str("{:,.0f}".format(vaccinations_diff_table[vaccinations_diff_dates-2][1])) + " Personen geimpft (" + vaccinations_diff_vorz + str("{:.2f}".format(vaccinations_diff)) + " % im Vergleich zum Vortag)."

if os.path.exists(datapath):
  os.remove(datapath)

print(vaccinations)
