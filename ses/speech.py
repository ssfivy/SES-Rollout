# Speech synthesis API interface
# On windows, uses the SAPI tts engine
# On Linux, uses the 'festival' tts engine directly


# core python imports
import subprocess
import sys

# conditional imports
if sys.platform.startswith('win32'):
    import win32com.client

def sayText(sentence):
    if sys.platform.startswith('linux'):
        # Festival tts engine is written partly with Scheme so its syntax is a bit exotic
        cmd = ['festival', '-b', '(voice_cmu_us_slt_arctic_hts)',  f'(SayText "{sentence}")']
        subprocess.run(cmd)
    elif sys.platform.startswith('win32'):
        # Works just fine after the correct libraries are installed
        speaker = win32com.client.Dispatch("SAPI.SpVoice")
        speaker.Speak(sentence)
