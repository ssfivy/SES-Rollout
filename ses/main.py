
"""
SES Rollout
"""

__author__ = "mgf897, ssfivy"
__version__ = "0.1.0"
__license__ = "CC SA"

# core libraries
import argparse
import sys

# our imports
import monitor_ses_api
import monitor_ses_selenium
import serialout
import speech

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
    print('Saying speaker test...')
    #speech.sayText('This is the S E S Rollout speaker test message!')

    # List available serial ports
    serialout.list_ports()

    #monitor_ses_api.monitor_jobs(livesite)
    monitor_ses_selenium.monitor_jobs(livesite, args.headless)


