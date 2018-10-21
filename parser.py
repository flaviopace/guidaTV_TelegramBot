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

        index = 1

        for channel in soup.findAll('div', {'class': ["g3", "g3 bet", "g3 ad"]}):
            try:
                key = channel.find('h3').contents[0]
            except:
                continue

            #print key
            channelevent = []
            channelevent.append(key)
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

            tvguide[index] = channelevent
            index = index + 1

        return tvguide

class htmlprogrammitvparser:

    def __init__(self, url):
        self.pageurl = url
        tvguide = {}

    def getPalimpsest(self):

        page = requests.get(self.pageurl)

        if page.status_code != 200:
            raise "HTML page error"

        soup = BeautifulSoup(page.text)

        index = 1

        for channel in soup.findAll('div', {'class': 'tab'}):
            try:
                key = channel.find('a').text
            except:
                continue

            print key
            channelevent = []
            channelevent.append(key)
            for event in channel.findAll('pre'):
                eventdetatails = event.findAll(text=True)
                print event.findAll('span')
                print eventdetatails
                link = event.find('a', href=True)
                print link.get('href')



            tvguide[index] = channelevent
            index = index + 1

            return tvguide

class superguidatvtvparser:

    def __init__(self, url):
        self.pageurl = url
        tvguide = {}

    def getPalimpsest(self):

        page = requests.get(self.pageurl)

        if page.status_code != 200:
            raise "HTML page error"

        soup = BeautifulSoup(page.text)

        index = 1

        for div in soup.findAll('div', {'class': 'sgtvfullevening_divContent'}):
            channel =  div.find('img', {'class': 'sgtvfullevening_logo'})
            try:
                key = channel.get('alt')
            except:
                continue

            #print key
            channelevent = []
            channelevent.append(key)
            for event in div.findAll('div', {'class':'sgtvfullevening_divProgram sgtvfullevening_displayTable'}):
                channelevent.append(event.find('div', {'class':'sgtvfullevening_divHours'}).getText())
                channelevent.append(event.find('span', {'class': 'sgtvfullevening_spanTitle'}).getText())
                channelevent.append(event.find('span', {'class': 'sgtvfullevening_spanEventType'}).getText())


            tvguide[index] = channelevent
            index = index + 1

        return tvguide


if __name__  == "__main1__":

    hp = htmlparser("https://hyle.appspot.com/palinsesto/serata")

    programlist = hp.getPalimpsest()

    print programlist


if __name__  == "__main2__":

    hp = htmlprogrammitvparser("http://www.programmitv.it/stasera.html")

    hp.getPalimpsest()

if __name__  == "__main__":

    hp = superguidatvtvparser("https://www.superguidatv.it/serata/")

    programlist = hp.getPalimpsest()

    print programlist


