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

        for div in soup.findAll('div', {'class': ['sgtvfullevening_divContent','sgtvfullfilmview_divCell']}):
            channel =  div.find('img', {'class': ['sgtvfullevening_logo','sgtvfullfilmview_logo']})
            try:
                key = channel.get('alt')
            except:
                continue

            #print key
            channelevent = []
            channelevent.append(key)
            # film
            if div.find('div', {'class':'sgtvfullfilmview_divContent'}):
                channelevent.append(div.find('span', {'class': 'sgtvfullfilmview_spanMovieDuration'}).getText().encode('utf-8'))
                channelevent.append(div.find('span', {'style': 'font-size: 14px !important;'}).getText().encode('utf-8'))
                channelevent.append(div.find('span', {'class': 'sgtvfullfilmview_spanTitleMovie'}).getText().encode('utf-8'))

                for filmdetails in div.findAll('span', {'class': 'sgtvfullfilmview_spanDirectorGenresMovie'}):
                    channelevent.append(filmdetails.getText())

                parental = div.find('div', {'class': 'sgtvfullfilmview_divContainerParentalLevel'})
                demo =  div.find('img', {'class':'sgtvfullfilmview_imageParentalControl'}).get('src')

                countfull = div.findAll('li', {'class':'sgtvfullfilmview_fullRatingDot'})

                half = 0
                if div.find('li', {'class':'sgtvfullfilmview_halfRatingDot'}):
                    half = 0.5

                channelevent.append('Rating: ' + str(len(countfull) + half) + '/5')

                tvguide[index] = channelevent
                index = index + 1

                if index >= 26:
                    break

            # serata
            else:
                for event in div.findAll('div', {'class':'sgtvfullevening_divProgram sgtvfullevening_displayTable'}):
                    channelevent.append(event.find('div', {'class':['sgtvfullevening_divHours',
                                                                    'sgtvfullfilmview_spanMovieDuration']}).getText())
                    channelevent.append(event.find('span', {'class': 'sgtvfullevening_spanTitle'}).getText())
                    channelevent.append(event.find('span', {'class': 'sgtvfullevening_spanEventType'}).getText())


                tvguide[index] = channelevent
                index = index + 1

                if index >= 26:
                    break

        return tvguide


if __name__  == "__main1__":

    hp = htmlparser("https://hyle.appspot.com/palinsesto/serata")

    programlist = hp.getPalimpsest()

    print programlist


if __name__  == "__main2__":

    hp = htmlprogrammitvparser("http://www.programmitv.it/stasera.html")

    hp.getPalimpsest()

if __name__  == "__main2__":

    hp = superguidatvtvparser("https://www.superguidatv.it/serata/")

    programlist = hp.getPalimpsest()

    print programlist

if __name__  == "__main__":

    hp = superguidatvtvparser("https://www.superguidatv.it/film-in-tv/oggi/nazionali/serata/")

    programlist = hp.getPalimpsest()

    print programlist


