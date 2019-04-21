
"""
SES Rollout
"""

__author__ = "mgf897, ssfivy"
__version__ = "0.1.0"
__license__ = "CC SA"

# core libraries
import argparse
import os
import sys

# our imports
import announce
import monitor_ses_api
import monitor_ses_selenium
import serialout

# version number check: Require 3.6
if sys.version_info < (3, 6) :
    raise NotImplementedError('This script requires Python version 3.6 or later')


def parseinput():
    helptext = 'Script that parses SES alerts site and announces it through the station'
    parser = argparse.ArgumentParser(description=helptext)

    # Select between training and live site. Argument mandatory;
    # we don't want default to live site (us developers should not mess with live system by accident)
    # but we also don't want SES guys to accidentally set this monitor to training site (which can cause people to die)
    target_livesite = parser.add_mutually_exclusive_group(required=True)
    target_livesite.add_argument('--live', action='store_true', help='Parse the live SES site')
    target_livesite.add_argument('--training', action='store_true', help='Parse the training SES site')

    # Use headless browser
    parser.add_argument('--headless', action='store_true', default=False, help='Use headless browser instead of popping a Firefox window')

    return parser.parse_args()


if __name__ == "__main__":
    """ This is executed when run from the command line """
    args = parseinput()
    if args.live:
        livesite = True
    if args.training:
        livesite = False

    # allows the operator to verify the speaker is working
    announce.announceStartup(livesite)

    # List available serial ports
    serialout.list_ports()

    # get credentials from system variables
    credentials = {}
    credentials['login'] = os.environ.get("SES_LOGIN") or ''
    credentials['pass'] = os.environ.get("SES_PASS") or ''

    if len(credentials['login']) < 1 or len(credentials['pass']) < 1:
        raise RuntimeError("No login credentials set. Set SES_LOGIN and SES_PASS environment variables")

    #monitor_ses_api.monitor_jobs(livesite)
    monitor_ses_selenium.monitor_jobs(credentials, livesite, args.headless)


