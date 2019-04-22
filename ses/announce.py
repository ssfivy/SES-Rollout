#!/usr/bin/env python3

# Announce jobs top-level API
import logging

import speech

def announceJob(job, serialout=None):
    '''Announce the details of a specific job'''
    logging.info(job)
    if serialout is not None:
        serialout.announce(job)
    #ethernet.announce(job)
    #https.announce(job)
    # Do speech last since vocal reading takes time
    speech.announce(job)

def announceStartup(isLive):
    '''Announce application startup, including warning if this is simply a training '''
    logging.info('Announcing application startup')
    #serialout.announceStartup(isLive)
    #ethernet.announceStartup(isLive)
    #https.announceStartup(isLive)
    # Do speech last since vocal reading takes time
    speech.announceStartup(isLive)
