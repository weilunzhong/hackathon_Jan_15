from pytrends.pyGTrends import pyGTrends
import time
from random import randint
import json
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
import datetime
import sys
from numpy import NaN, Inf, arange, isscalar, asarray, array

import es_dao
import google_api

def csv2json(data):
    output={}
    sign=0
    for d in data:
        # print d
        if d.startswith('Web Search interest:'):
            output['query_title']=d.split(': ')[1]
            # print output
            continue
        if d.startswith('Interest over time'):
            output['query_overtime']=[]
            continue
        if (' - ' in d) and d.startswith('20'):
            # print d
            if ',' in d:
                query_time_info={}
                d_time,d_querycount=d.split(',')[0],d.split(',')[1]
                query_time_info['starttime']=d_time.split(' - ')[0]
                query_time_info['endtime']=d_time.split(' - ')[1]
                query_time_info['querycount']=d_querycount
                output['query_overtime'].append(query_time_info)
        elif ('-' in d) and d.startswith('20'):
            # print d
            if ',' in d:
                query_time_info={}
                d_time,d_querycount=d.split(',')[0],d.split(',')[1]
                query_time_info['starttime']=d_time.split('-')[0]
                query_time_info['endtime']=d_time.split('-')[1]
                query_time_info['querycount']=d_querycount
                output['query_overtime'].append(query_time_info)
            # break
        if sign is 1:
            sign=2
            output['query_us_states']=[]
            continue
        if d.startswith('Top regions') or d.startswith('Top metros') or d.startswith('Top subregions'):
            sign=1
        if sign is 2:
            if d=='':
                sign = 0
                break
            query_regioin_info={}
            query_regioin_info['region']=d.split(',')[0]
            query_regioin_info['querycount']=d.split(',')[1]
            output['query_us_states'].append(query_regioin_info)
    return output



def get_top_date(actor_name, peak_num):

    google_username = "zhongweilunmichael@gmail.com"
    google_password = "xxxxxx"

    fid = es_dao.get_actor_freebase_id_by_name(actor_name)
    print fid
    connector = pyGTrends(google_username, google_password)

    # make request
    connector.request_report(fid)
    res_json=csv2json(connector.decode_data.split('\n'))
    res_json['freebase_id']=fid
    #print "Here is result in json:", res_json
    overtime_data = []
    timestamp_start =[]
    timestamp_end =[]
    for weekly_data in res_json['query_overtime']:
        overtime_data.append(int(weekly_data['querycount']))
        timestamp_start.append(weekly_data['starttime'])
        timestamp_end.append(weekly_data['endtime'])
    #print res_json['query_overtime']
    # print timestamp
    # print overtime_data

    sorted_data = sorted(range(len(overtime_data)), key=lambda i: overtime_data[i])[-peak_num:]
    # print sorted_data

    for index in sorted_data:
        print "date:{}, count{}".format(timestamp_start[index], overtime_data[index])

    # array_data = np.asarray(overtime_data)
    # peakind =signal.find_peaks_cwt(array_data, np.arange(5,10))
    # print peakind

    # plt.plot(overtime_data)
    # plt.show()

    # wait a random amount of time between requests to avoid bot detection
    time.sleep(randint(5, 10))
    return sorted_data, overtime_data, timestamp_start, timestamp_end

if __name__ == "__main__":

    actor = 'rachel mcadams'
    top_dates, overtime_data, timestamp_start, timestamp_end = get_top_date(actor, 4)

    with open('output.json', 'wb') as f:
        for index in top_dates:
            start_date = timestamp_start[index]
            end_date = timestamp_end[index]
            print start_date, end_date
            date_format = '%Y-%m-%d'
            start_date, end_date = datetime.datetime.strptime(start_date, date_format), datetime.datetime.strptime(end_date,date_format)


            res = google_api.get_news(actor, start_date, end_date)

            f.write(json.dumps(res))
            f.write('\n')






