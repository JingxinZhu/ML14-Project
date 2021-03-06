'''
This code is a part of the final project for course Machine Learning 
and Computational Statistics at NYU for Fall 2014.

Author: Bowei Zhang and Jingxin Zhu
Date created: 23rd, Apr
'''

import urllib2

from BeautifulSoup import BeautifulSoup as BS

class Crawler_Celebrity_Accounts:
    def crawl(self, n, start_id = 1):
        if n > 1000:
            n = 100
            print 'N should be no greater than 1000. Set it to 100.'

        # current page on Twitaholic
        page = (start_id - 1) / 100 + 1
        page_offset = (start_id - 1) % 100
        # number of IDs acquired
        cnt = page_offset 

        # the list of IDs to return
        IDs = []

        n += page_offset
        while cnt < n:
            try:
                # request HTML (pure)
                html = urllib2.urlopen('http://twitaholic.com/top' +\
                        str((page * 100)) + '/followers/')
                # parse obtained html and save tabs for each celebrity
                elem = BS(html).findAll('td', {'class' : 'statcol_name'})

                # parse each tab
                for e in elem[page_offset:]:
                    # already done
                    if cnt >= n:
                        break;
                    list_elem = str(e)

                    # extract the field that stores Twitter ID
                    ID = list_elem[list_elem.find('@') + 1: list_elem.rfind\
                            ('<br')]
                    IDs.append(ID)
                    cnt += 1

                page_offset = 0

                # if all celebrities' IDs in the current web pages have been
                # crawled, turn to next page
                if cnt >= page * 100:
                    page += 1
            except:
                print 'Error on fetching and parsing HTML.'
                break
        return IDs
