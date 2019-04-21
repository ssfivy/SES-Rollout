#!/usr/bin/env python3

# Announce jobs top-level API

import serialout
import speech

def announceJob(job):
    '''Announce the details of a specific job'''
    print(job)
    speech.announce(job)
    serialout.announce(job)
    #ethernet.announce(job)
    #https.announce(job)

def announceStartup(isLive):
    '''Announce application startup, including warning if this is simply a training '''
    print('Announcing application startup')
    speech.announceStartup(isLive)
    #serialout.announceStartup(isLive)
    #ethernet.announceStartup(isLive)
    #https.announceStartup(isLive)
