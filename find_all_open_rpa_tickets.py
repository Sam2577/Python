import requests, openpyxl, sys
from bs4 import BeautifulSoup
from lxml import html

login_url = "https://projects.markit.com/login.jsp"
url = 'https://jira.markit.com/browse/BRS-254'

all_tickets = []
all_urls = []
THE_FILE = 'C:\\users\\sam.walsh\\desktop\\ALL_TICKETS.xlsx'

wb = openpyxl.load_workbook(THE_FILE)
sheet = wb['Sheet1']

# Ticket class for representing each ticket scraped as a Ticket object
class Ticket:
    def __init__(self, key, assignee, summary, stat):
        self.key = key.strip()
        self.assignee = assignee.strip()
        self.summary = summary.strip()
        self.stat = stat.strip()
        
with requests.session() as s:

    payload = {
        "os_username": "sam.walsh", 
        "os_password": "" #removed
    }

    result = s.post(url, data=payload,headers={"referer":url, "X-Atlassian-Token":"no-check",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36"})

    print(result.status_code)
    
    res = s.get(url, cookies=result.cookies)
    print(result.status_code)
    
    soup = BeautifulSoup(res.content, "html.parser")
    issues = soup.select('tr.issuerow')

    for num, issue in enumerate(issues):

        # instantiate beautiful soup object to scrape page with
        newsoup = BeautifulSoup(str(issue), "html.parser")

        # scrape the ticket key
        key = newsoup.select('td a')[0].text.strip()
        
        # there may or may not be an assignee (and error thrown if there isnt), so try/except here.
        try:
            assignee = newsoup.select('td.assignee a')[0].text.strip()
        except:
            assignee = ""
            
        summary = str(newsoup.select('td.ghx-summary')[0].text.strip()).replace(',', '')

        # get ticket status
        stat = newsoup.select('td.status span')[0].text.strip()

        # set of all closed statuses
        closed = {"Closed - Complete", "Closed", "Resolved"}

        # if status of this ticket is not in the set of closed statuses, it is open
        if stat not in closed:
            # create a Ticket object from scraped info
            current_ticket = Ticket(key, assignee, summary, stat)
            
            # append Ticket object to all_tickets
            all_tickets.append(current_ticket)

# print all tickets info with a seperator between each item
for t in all_tickets:
    print(t.key, t.assignee, t.summary, t.stat, sep=" | ")

print("done.")
