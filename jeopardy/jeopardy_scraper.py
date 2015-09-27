from bs4 import BeautifulSoup
import requests
import re
import time
import pandas as pd

def getSeasonURLs(seasons_index): #pulls the URLs for the page for each season
    source = requests.get(seasons_index, 'xml').text
    seasons_list = BeautifulSoup(source, 'xml')
    seasons_urls = seasons_list.find_all('a', {'href': re.compile('')})
    seasons_urls = [url.get('href') for url in seasons_urls]
    seasons_urls = ['http://j-archive.com/' + url for url in seasons_urls if url[0] != 'h']
    return seasons_urls

def getGameURLs(games_page): #pulls the URLs for each game within a season
    source = requests.get(games_page, 'xml').text
    season = BeautifulSoup(source, 'xml')
    game_urls = season.find_all('a', {'href': re.compile('game_id')})
    game_urls = [url.get('href') for url in game_urls]
    return game_urls

def getHTML(gameurl): #pulls the HTML for an indivudiaul game
    source = requests.get(gameurl, 'xml').text
    return BeautifulSoup(source, 'xml')

def pullText(gameText, tag, attribute, value): #parses the relevant text
    return [item.get_text() for item in gameText.find_all(tag, {attribute: value})]

def getClues(gameText): #returns a series of cues for an individual game
    return pd.Series(pullText(gameText, 'td', 'class', 'clue_text'))

def getCats(gameText): #returns the names of each category from an individual game
    categories = pullText(gameText, 'td', 'class', 'category_name')
    return categories[0:6], categories[6:12], categories[-1]

def getOrder(gameText): #returns the order each clue was asked in
    return pd.Series(pullText(gameText, 'a', 'rel', 'nofollow'))

def getAnswers(gameText): #returns the answers to each clue
    answers = [str(x) for x in gameText.find_all('div', {'onmouseover': re.compile("toggle")})]
    return pd.Series([re.search('t_response.*/em', x).group()[20:-7] for x in answers])

def getGameInfo(gameText): #pulls the series number and air date of the game
    #splits string into game number and date aired
    gameNum, date = gameText.h1.string.split(' - ')
    gameNum = str(gameNum)
    date = str(date)
    date = re.search(' [A-Z].*', date).group().replace(',', '').lstrip()
    date = time.strptime(date, '%B %d %Y')[0:3]
    gameNum = re.search('[0-9]+$', gameNum).group()
    return gameNum, date
    

def getGrid(gameText): #pulls series of category, round, and value, to be matched with each clue
    coordlist = [tag.get('id') for tag in gameText.find_all('td') if tag.get('id') != None]
    gridlist = [coord for coord in coordlist if re.search('stuck', coord) == None]
    Jcats, DJcats, FJcat = getCats(gameText)
    
    cats = [Jcats[int(x[-3])-1] if x.find('_J') > 0 \
            else DJcats[int(x[-3])-1] if x.find('DJ') > 0 \
            else FJcat for x in gridlist]
    
    rounds = ['J' if x.find('_J') > 0 \
             else 'DJ' if x.find('DJ') > 0 \
             else 'FJ' for x in gridlist]
    
    values = [100 if x[-1] == '1' \
              else 200 if x[-1] == '2' \
              else 300 if x[-1] == '3' \
              else 400 if x[-1] == '4' \
              else 500 if x[-1] == '5' \
              else 'FJ' for x in gridlist]
    return pd.Series(cats), pd.Series(rounds), pd.Series(values)


def gameFrame(gameurl): #creates a dataframe with all of the above for each individual game
    game = getHTML(gameurl)
    clues = getClues(game)
    gameLength = len(clues)
    order = getOrder(game)
    answers = getAnswers(game)
    gameNum, date = getGameInfo(game)
    gameNum, date = pd.Series([gameNum]*gameLength), pd.Series([date]*gameLength)
    cats, rounds, values = getGrid(game)
    columns = [date, gameNum, cats, rounds, values, clues, answers, order]
    gameFrame = pd.DataFrame(columns).transpose()
    gameFrame.columns = ['Date(YMD)', 'Game_Number', 'Categories', 'Round', \
                    'Value', 'Clue', 'Answer', 'Order']
    return gameFrame
    

seasons_index = 'http://j-archive.com/listseasons.php' #list of seasons
seasons_list = getSeasonURLs(seasons_index) #
gameframeslist = [] #list to append each game's dataframe to.

for season in seasons_list:
    games_URLs = getGameURLs(season)
    games_URLs = [('http://www.j-archive.com/'+url) if url[0] != 'h' \ 
                  else url for url in games_URLs] #deals with hyperlink formatting

    for game in games_URLs:
        try:
            gameframeslist.append(gameFrame(game))
        except: #a few individual game pages were throwing up errors, so this will bypass them.
            continue

df = pd.concat(gameframeslist, ignore_index = True) #merge all individual games into a master dataframe



df.to_csv('Jeop.csv', encoding='utf=8') #save to csv




