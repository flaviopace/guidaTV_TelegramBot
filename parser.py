from BeautifulSoup import BeautifulSoup
import requests

tvguide = {}

class htmlparser:

    def __init__(self, url):
        self.pageurl = url
        tvguide = {}

    def getPalimpsest(self):

        page = requests.get(self.pageurl)

        if page.status_code != 200:
            raise "HTML page error"

        soup = BeautifulSoup(page.text)

        #print(soup.prettify())

        for channel in soup.findAll('div', {'class': 'g3'}):
            key = channel.find('h3').contents[0]
            #print key
            channelevent = []
            for event in channel.findAll('li'):
                value = event.span.b.text
                #print value
                channelevent.append(value)
                value = event.span.contents[1].strip()
                if not value:
                    value = event.span.strong.text.strip()
                channelevent.append(value)
                #print value
                #print ""

            tvguide[key] = channelevent

        return tvguide

if __name__  == "__main__":

    hp = htmlparser("https://hyle.appspot.com/palinsesto/serata")

    programlist = hp.getPalimpsest()

    print programlist


