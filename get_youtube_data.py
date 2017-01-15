import pandas as pd
import matplotlib as mpl
import numpy as np

from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser

import channel_details as cd

API_KEY = "AIzaSyBYq7UXn9VnF9JOLKEDHgU0N0u0U_zw3ps" 
API_NAME = "youtube"
API_VERSION = "v3"

"""
create array of search queries for data extraction
"""
search_query = "Manchester United"

def gather(search_query):
	argparser.add_argument("--q", help="Search term", default=search_query)
	argparser.add_argument("--max-results", help="Max results", default=25)
	arguments = argparser.parse_args()
	options = arguments

	youtube = build(API_NAME, API_VERSION, developerKey=API_KEY)

	search_response = youtube.search().list(
		q=options.q,
		type="video",
		part="id,snippet",
		maxResults=options.max_results
	).execute()

	videos = {}

	for search_result in search_response.get("items", []):
	    if search_result["id"]["kind"] == "youtube#video":
	    	videos[search_result["id"]["videoId"]] = search_result["snippet"]["title"]

	s = ','.join(videos.keys())

	videos_list_response = youtube.videos().list(
		id=s,
		part='id,statistics,snippet,status,contentDetails'
	).execute()

	res = []
	cnt = 0
	for i in videos_list_response['items']:
		temp_res = dict(v_id = i['id'], v_title = videos[i['id']])
		temp_res.update(i['statistics'])
		temp_res.update(i['status'])
		temp_res.update(i['contentDetails'])
		temp_res.update(i['snippet'])
		if cnt == 0:
			cnt = cnt + 1
			cd.get_all_data(temp_res['channelId'])
		res.append(temp_res)

	dataframe = pd.DataFrame.from_dict(res)
	# drop useless columns from dataframe
	dataframe.drop(['license', 'licensedContent', 'channelTitle', 'dimension', 'thumbnails', 'v_title', 'uploadStatus'], axis=1, inplace=True)

	"""
	below columns can be manipulated into being features
	"""
	dataframe.drop(['caption', 'embeddable'], axis=1, inplace=True)
	# print dataframe
	names = dataframe.columns.values 
	# print names
	count = 0
	for x in names:
		count = count + 1
	print count

gather(search_query)
cd.get_all_data("UCM9KEEuzacwVlkt9JfJad7g")

# print "id " + dataframe['v_id']

# f = open("data.csv", "a")
# f.write(str(dataframe))
