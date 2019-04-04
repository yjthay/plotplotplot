import os
import requests
import datetime
from PyPDF2 import PdfFileMerger, PdfFileReader
import getpass


def get_month_year(i):
    year = datetime.datetime.now().year
    if i > 12:
        month = datetime.date(1900, i - 12 * int((i - 1) / 12), 1).strftime('%B')
        year = year + int(i / 12)
    else:
        month = datetime.date(1900, i, 1).strftime('%B')
    return month, year


def create_calendar_pdf(number_of_months):
    os.chdir("C:/Users/{}/Documents".format(getpass.getuser()))
    url = "http://www.calendarpedia.co.uk/download/months/INPUT_YEAR/calendar-INPUT_MONTH-INPUT_YEAR-landscape.pdf"

    start_month = datetime.datetime.now().month
    start_year = datetime.datetime.now().year
    merger = PdfFileMerger()
    for i in range(start_month, start_month + number_of_months):
        month, year = get_month_year(i)
        url_temp = url.replace('INPUT_YEAR', str(year)).replace('INPUT_MONTH', month.lower())
        r = requests.get(url_temp, allow_redirects=True)
        with open(month + str(year) + '.pdf', 'wb') as f:
            f.write(r.content)
        merger.append(PdfFileReader(month + str(year) + '.pdf', 'rb'))
        os.remove(month + str(year) + '.pdf')
    merger.write('{} {} to {} {}.pdf'.format(datetime.datetime.now().strftime('%B'), start_year, month, year))


create_calendar_pdf(12)
