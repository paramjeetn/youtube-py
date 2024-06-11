import streamlit as st
import requests
import json
import isodate
from datetime import timedelta

st.title("YouTube Playlist Analyzer")

# Get user input for API key, playlist ID, start video number, and end video number
yt_api = st.text_input("Enter your YouTube API key:")
playlist_id = st.text_input("Enter the YouTube playlist ID:")
startcount = st.number_input("Enter the starting video number:", value=1)
endcount = st.number_input("Enter the ending video number:", value=10)

if st.button("Analyze Playlist"):
    URL1 = 'https://www.googleapis.com/youtube/v3/playlistItems?part=contentDetails&maxResults=50&fields=items/contentDetails/videoId,nextPageToken&key={}&playlistId={}&pageToken='.format(yt_api, playlist_id)
    URL2 = 'https://www.googleapis.com/youtube/v3/videos?&part=contentDetails&key={}&id={}&fields=items/contentDetails/duration'.format(yt_api, '{}')

    next_page = '' 
    cnt = 0
    a = timedelta(0)
    total_cnt = 1

    while True:
        vid_list = []

        results = json.loads(requests.get(URL1 + next_page).text)

        for x in results['items']:
            vid_list.append(x['contentDetails']['videoId'])

        url_list = ','.join(vid_list)
        cnt = len(vid_list)

        op = json.loads(requests.get(URL2.format(url_list)).text)
        
        for x in op['items']:
            if startcount <= total_cnt <= endcount:
                a += isodate.parse_duration(x['contentDetails']['duration'])
                st.write(f"Video {total_cnt}: {isodate.parse_duration(x['contentDetails']['duration'])}")
            total_cnt += 1
        if 'nextPageToken' in results:
            next_page = results['nextPageToken']
        else:
            st.write(f"No of videos: {total_cnt-1}")
            st.write(f"Average length of video: {a/(total_cnt-1)}" if total_cnt > 1 else "0")
            st.write(f"Total length of playlist: {a}")
            st.write(f"At 1.25x: {a/1.25}" if total_cnt > 1 else "0")
            st.write(f"At 1.50x: {a/1.5}" if total_cnt > 1 else "0")
            st.write(f"At 1.75x: {a/1.75}" if total_cnt > 1 else "0")
            st.write(f"At 2.00x: {a/2}" if total_cnt > 1 else "0")
            break
