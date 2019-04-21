#!/usr/bin/env python3

# Announce jobs top-level API

import serialout
import speech

def announceJob(job):
    print(job)
    speech.announce(job)
    serialout.announce(job)
    #ethernet.announce(job)
    #https.announce(job)
