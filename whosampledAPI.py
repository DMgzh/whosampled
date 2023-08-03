import requests
from bs4 import BeautifulSoup
import pandas as pd

class Whosampled:
    headers = {'User-Agent':
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    def __init__(self):
        pass
    
    def get_samples(self, artist, track):
        url = f'https://www.whosampled.com/{artist}/{track}/'
        response = requests.get(url, headers=self.headers)
        
        samples_list = []

        if response.ok:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            n_str = soup.find('span', {'class': 'section-header-title'}).getText()
            n = int(''.join(filter(str.isdigit, n_str)))

            if n > 3:
                url = f'https://www.whosampled.com/{artist}/{track}/samples'
                response = requests.get(url, headers=self.headers)
                soup = BeautifulSoup(response.text, 'html.parser')
                
                tracks_info_list = soup.find_all('div', 'listEntry sampleEntry')
                
                for list_entry in tracks_info_list:
                    track_details = list_entry.find('div', {'class': 'trackDetails'})
                    track_name = track_details.find('a', {'class': 'trackName playIcon'}).getText()
                    artist_name = track_details.find('span', {'class': 'trackArtist'}).find('a').getText()
                    
                    samples_list.append({'artist': artist_name, 'track': track_name})
            else: 
                tracks_info_list = soup.find_all('div', 'listEntry sampleEntry')
                
                for list_entry in tracks_info_list:
                    track_details = list_entry.find('div', {'class': 'trackDetails'})
                    track_name = track_details.find('a', {'class': 'trackName playIcon'}).getText()
                    artist_name = track_details.find('span', {'class': 'trackArtist'}).find('a').getText()
                    samples_list.append({'artist': artist_name, 'track': track_name})
        else:
            return response

        return samples_list
    
    def get_tracks(self, artist):
        i = 1
        tracks_list = []
        while True:
            url = f'https://www.whosampled.com/{artist}/?sp={i}'
            response = requests.get(url, headers=self.headers)
            
            if response.ok:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                tracks = soup.find_all('h3', {'class': 'trackName'})
                for h3 in tracks:
                    track = h3.find('span').getText().replace(' ', '-')
                    track = track.replace('-/', '')
                        
                    tracks_list.append(track)
        
            else:
                return tracks_list
            i+=1
    
api = Whosampled()

tracks = api.get_tracks('N.W.A')
for track in tracks:        
    samples = api.get_samples('N.W.A', track)
    print(track, samples)
