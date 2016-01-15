import pprint
import json
from jdcal import gcal2jd, jd2gcal
from googleapiclient.discovery import build
import datetime


def get_news(actor, start_date, end_date):
    service = build("customsearch", "v1",
                    developerKey="AIzaSyBdV1Emfi7Zd-T8_PQ1tr_Av7G4WuGpHOo")
    start_date_j = int(sum(gcal2jd(start_date.year, start_date.month, start_date.day)))
    end_date_j = int(sum(gcal2jd(end_date.year, end_date.month, end_date.day)))
    res = service.cse().list(
        q='{0} daterange:{1}-{2}'.format(actor, start_date_j, end_date_j),
        cx='012147580588716782987:kvx5v_ad2jk'
    ).execute()
    return res


def main(date):
    # Build a service object for interacting with the API. Visit
    # the Google APIs Console <http://code.google.com/apis/console>
    # to get an API key for your own application.

    date_format = '%Y-%m-%d'
    start_date, end_date = datetime.datetime.strptime(data_start, date_format), datetime.datetime.strptime('20100201',date_format)


    res = get_news(start_date, end_date)
    with open('output.json', 'wb') as f:
        f.write(json.dumps(res))



if __name__ == '__main__':
    main()
