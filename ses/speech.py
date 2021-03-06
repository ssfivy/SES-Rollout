# Speech synthesis API interface
# On windows, uses the SAPI tts engine
# On Linux, uses the 'festival' tts engine directly


# core python imports
import logging
import subprocess
import sys

# conditional imports
if sys.platform.startswith('win32'):
    import pythoncom
    import win32com.client

def sayText(sentence):
    logging.debug('Speaking text: "'+sentence+'"')
    if sys.platform.startswith('linux'):
        # Festival tts engine is written partly with Scheme so its syntax is a bit exotic
        cmd = ['festival', '-b', '(voice_cmu_us_slt_arctic_hts)',  f'(SayText "{sentence}")']
        subprocess.run(cmd)
    elif sys.platform.startswith('win32'):
        # Works just fine after the correct libraries are installed
        pythoncom.CoInitialize()
        speaker = win32com.client.Dispatch("SAPI.SpVoice")
        speaker.Speak(sentence)

def announce(job):
    # Generate sentence to speak
    words = []
    words.append('There is an incident requiring ')
    words.append(job['priority'])
    words.append(' response! ')

    words.append(' It is a ')
    words.append(job['type'])
    words.append(' !')

    words.append(' Location is ')
    words.append(job['address'])
    words.append(' !')


    # Say it!
    announcement = ' '.join(words)
    # Repeat announcement twice so they can be heard a bit clearly
    sayText(announcement)
    sayText("I repeat,")
    sayText(announcement)
    #sayText('S E S, Rollout!')

def announceStartup(isLive):
    if isLive:
        announcement = 'This is the LIVE speaker test message! I repeat, LIVE test message!'
    else:
        announcement = 'This is the Training speaker test message! I repeat, Training test message!'

    sayText(announcement)



