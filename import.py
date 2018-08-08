# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# import.py
#
# Web Programming with Python and Javascript
# Leony Brok
#
# Takes information from a csv with currency codes, names and symbols
# and imports it into a database.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "expensetracker.settings")
django.setup()
from tracker.models import Currency

import csv

# Open csv with zip codes.
with open('currency.csv', newline='') as csvfile:

    datareader = csv.DictReader(csvfile)

    # Read every line, add and save data.
    for i, row in enumerate(datareader):

        unicode_decimals = row['unicode-decimal'].split(', ')
        unicode_html = []
        for code in unicode_decimals:
            code = f"&#{code};"
            unicode_html.append(code)

        unicode_html = ''.join(unicode_html)

        c = Currency.objects.create(
            name = row['text'],
            code = row['code'],
            unicode_html = unicode_html,
        )
        c.save

        print(i, c)