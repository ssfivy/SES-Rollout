
# core libraries
import logging
import time

# third party libraries
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup

# our imports
import announce


trainingURL = "https://trainbeacon.ses.nsw.gov.au"
trainingURL_login = "https://identitytrain.ses.nsw.gov.au/core/login"

liveURL = "" # TODO: Fill this infromation
liveURL_login = "" # TODO: Fill this information

initial_wait = 10
jobs_recent_enough = 30
jobs_refresh_delay = 10


def parse_jobs_table(browser):
    '''Parse the job register table and return a dict of jobs, with jobid as id'''
    # Refresh page required to ensure table is up to date
    browser.refresh()
    time.sleep(3) #FIXME: wait until things load. Should look into restructuing program flow for efficiency.
    JobRegisterTable = browser.find_element_by_id("jobRegisterTable")
    # TODO
    # handle exception if table isnt loaded yet
    time.sleep(3) #FIXME: wait until things load. Should look into restructuing program flow for efficiency.

    jobTable = BeautifulSoup(browser.page_source, "html.parser")
    jobRows = jobTable.find("table", id="jobRegisterTable").find("tbody").find_all("tr")

    jobs = {}
    for row in jobRows:
        cells = row.find_all("td")
        # Every second table row is 1 column wide and needs to be ignored
        if (len(cells) > 1):
            job = dict()
            job["id"] = cells[2].getText()
            job["received"] = cells[3].getText()
            job["priority"] = cells[4].getText()
            job["type"] = cells[5].getText()
            job["status"] = cells[6].getText()
            job["hq"] = cells[7].getText()
            job["parent"] = cells[8].getText()
            job["address"] = cells[9].getText()
            jobs[job["id"]] = job

    return jobs

def monitor_jobs(credentials, isLiveSite=False, isHeadless=False):
    '''Connect to web interface and parse jobs manually using Selenium'''


    if len(credentials['login']) < 1 or len(credentials['pass']) < 1:
        raise RuntimeError("No login credentials set.")

    if isLiveSite:
        #baseurl = liveURL
        #loginurl = liveURL_login
        raise NotImplementedError ('Live site not implemented until feature complete') #TODO duh.
    else:
        baseurl = trainingURL
        loginurl = trainingURL_login

    opts = Options()
    if isHeadless:
        opts.set_headless()
        assert opts.headless  # Operating in headless mode

    browser = Firefox(options=opts)
    browser.get(baseurl + "/Jobs")

    if (browser.current_url.split("?")[0] == loginurl):
        # Login
        user_form = browser.find_element_by_id('username')
        user_form.send_keys(credentials['login'])
        pass_form = browser.find_element_by_id('password')
        pass_form.send_keys(credentials['pass'])
        pass_form.submit()


    # Check if login was successful
    # Are we still on the login screen?
    logging.info(f"waiting {jobs_refresh_delay} seconds before checking login state")
    time.sleep(jobs_refresh_delay)
    if (browser.current_url.split("?")[0] == loginurl): 
         raise RuntimeError("Login error. Check username/password")

    # Try to get the initial list of jobs. We don't announce these.
    logging.info(f"waiting for {initial_wait} seconds to allow website to load")
    time.sleep(initial_wait)

    known_jobs = {}
    # Comment out the parse function below to make us announce all initial jobs (for testing)
    # Else, this will get an initial list of jobs which will not be announced
    known_jobs = parse_jobs_table(browser)

    # Check for further additional jobs
    while True:
        logging.info(f"waiting {jobs_refresh_delay} seconds")
        time.sleep(jobs_refresh_delay)

        # Hopefully the web page does not keep appending the jobs in the web page
        # so updated_job will not grow indefinitely
        updated_jobs = parse_jobs_table(browser)

        # Get new jobs by finding the diff between two sets, see https://stackoverflow.com/a/30986796
        new_job_ids = set(updated_jobs.keys()) - set(known_jobs.keys())

        # We don't need the old jobs anymore, replace with collection of new jobs
        known_jobs = updated_jobs

        # Announce all new jobs
        for job in new_job_ids:
            announce.announceJob(known_jobs[job])

