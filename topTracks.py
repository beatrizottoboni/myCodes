'''
This script search for an artist on spotify and then save his or hers top tracks on a Excel Sheet
'''

from selenium import webdriver
import requests, openpyxl, sys
from datetime import datetime

def saveTopTracks(path, artist, topTracks):

    newWorkbook = openpyxl.Workbook()
    newWorkbook[newWorkbook.get_sheet_names()[0]].title = 'Track List'
    trackList = newWorkbook['Track List']

    trackList.sheet_view.showGridLines = False

    sheetHeader = [
            {'cell':'A1', 'text':'Position'},
            {'cell':'B1', 'text':'Music Name'},
            {'cell':'C1', 'text':'Album Name'},
            {'cell':'D1', 'text':'Release Date'}]

    color = openpyxl.styles.colors.Color(rgb="004BACC6")

    for item in sheetHeader:
        cell = item['cell']
        trackList[cell] = item['text']
        trackList[cell].fill = openpyxl.styles.fills.PatternFill(patternType='solid', fgColor=color)
        trackList[cell].font = openpyxl.styles.Font(name='Calibri', size=12, bold=True, italic=False, strike=False, underline='none', color='FFFFFF')

    for item in topTracks:
        row = trackList.max_row
        track = item['name']
        album = item['album']['name']
        releaseDate = item['album']['release_date']

        trackList[f'A{row+1}'] = row
        trackList[f'B{row+1}'] = track
        trackList[f'C{row+1}'] = album
        trackList[f'D{row+1}'] = '{}/{}/{}'.format(releaseDate[8:], releaseDate[5:7], releaseDate[:4])

    newWorkbook.save(f'{path}/Top Tracks {artist}.xlsx')
    newWorkbook.close()

user = 'beatriz.ribeiro'

browser = webdriver.Chrome(f'C:/Users/{user}/AppData/Local/Programs/Python/Python310/Lib/site-packages/selenium/webdriver/chrome/chromedriver.exe')

artist = 'Taylor Swift'
browser.get(f'https://open.spotify.com/search/{artist}]')
linkElement = browser.find_element_by_link_text(artist).get_attribute('href')
browser.quit()
artistId = linkElement.split('/')[4]

token = 'BQAhGh5JXOqWvpNt10Mlm_yh-DBzQH0BxxVjohNv0025GEXUnv3R7WgK7neSSyjqWfuVEH8eH5auifynFx6FuLx28ElvZhuoRPFG0R7vcSvLK7RE6gh6W2JUzMCj__wwSgUDhau34_DPA2i8AmU9ia_sTDb9ekdEVfEAvEQ4AK9i'
head = {'Authorization':f'Bearer {token}', 'Content-type': 'application/json'}
url = f'https://api.spotify.com/v1/artists/{artistId}/top-tracks?market=BR'
r = requests.get(url, headers=head)

try:
    r.raise_for_status()
except:
    print(f'There was an error and the script could not get to the artist page on spotify.')
    sys.exit()

topTracks = [item for item in r.json()['tracks']]

path = f'C:/Users/{user}/Documents'

saveTopTracks(path, artist, topTracks)
