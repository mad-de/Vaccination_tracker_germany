#!/usr/bin/python
# -*- coding: utf-8 -*-

import pandas as pd
import datetime
import requests

url_vaccinations = 'https://www.rki.de/DE/Content/InfAZ/N/Neuartiges_Coronavirus/Daten/Impfquotenmonitoring.xlsx?__blob=publicationFile'
vacc_request = requests.get(url_vaccinations)

with open('Impfquotenmonitoring.xlsx', 'wb') as f:
    f.write(vacc_request.content)


vaccinations_table = pd.read_excel('Impfquotenmonitoring.xlsx', sheet_name=1)
vaccinations_date = pd.read_excel('Impfquotenmonitoring.xlsx', sheet_name=0)

vaccination_ger_num = vaccinations_table.values.tolist()[16][1]
vaccination_ger_perc = vaccination_ger_num / 83002000 * 100
vaccination_ger_perc = " (" + str("{:.2f}".format(vaccination_ger_perc)) + " %)"
vaccination_ger_diff = vaccinations_table.values.tolist()[16][2]
vaccination_date = vaccinations_date.values.tolist()[1][1]
vaccination_date_time = vaccinations_date.values.tolist()[1][2]
vaccination_date = vaccination_date.strftime("%m.%d.%Y")


vaccinations = "Aktuelle COVID-19-Impfungen in Deutschland: " + str("{:.0f}".format(vaccination_ger_num)) + vaccination_ger_perc + ". Stand: " + str(format(vaccination_date)) + " um " + str(format(vaccination_date_time)) + ". " + str("{:.0f}".format(vaccination_ger_diff)) + " Impfungen wurden am Vortag durchgeführt."


print(vaccinations)
