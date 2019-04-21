# SES-Rollout

Program to read new issues and announce them over the speaker

## Requirements

These requirements needs to be installed manually:
* Python 3.6+ (uses f-strings)
* Requires Firefox to be installed
* Requires Geckodriver to automate Firefox. [Geckodriver](https://github.com/mozilla/geckodriver/releases)
* On Linux, requires "festival" text to speech program: `sudo apt install festival festvox-us-slt-hts`

All other dependencies are in `requirements.txt` , install with:
* Windows: `pip install -r requirements.txt`
* Linux: `pip3 install -r requirements.txt`

TODO: Clarify which requirements are buildtime vs runtime

