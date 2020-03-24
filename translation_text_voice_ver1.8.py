from __future__ import print_function
import pyaudio
from ibm_watson import SpeechToTextV1
from ibm_watson.websocket import RecognizeCallback, AudioSource
from threading import Thread
from tkinter import *
from pynput.keyboard import Key, Controller


selection=0
# def eng_btn():
def radio_btn():
    selection=lang.get()
    if selection==0:
        english.configure(foreground="#4285f4")
        spanish.configure(foreground="#757575")
        test = Label(window, text=selection, font=("Proxima Nova Thin",10), background="white", fg="#757575")
        test.place(relx=.5,rely=.8)
        txt.configure(state="normal")
        txt.delete(0,last=END)


    elif selection==1:
        spanish.configure(foreground="#4285f4")
        english.configure(foreground="#757575")
        test = Label(window, text=selection, font=("Proxima Nova Thin",10), background="white", fg="#757575")
        test.place(relx=.5,rely=.8)
        txt.configure(state="normal")
        txt.delete(0,last=END)
    return

#        Function to make window centered
def screen(width=1000, height=250):
    # get screen width and height
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    # calculate position x and y coordinates
    x = (screen_width/2) - (width/2)
    y = (screen_height/2) - (height/2)
    window.geometry('%dx%d+%d+%d' % (width, height, x, y))


window = Tk()
lang=IntVar()

window.title("Translate")
#               Invoke the window to be placed in the center as per the def screen above
screen()
# window.geometry('1000x250')
window.configure(background="white")


# lang = IntVar()
# lang.set(0)

    



english = Radiobutton(window, text="English to Spanish", font=("Proxima Nova Regular",18), variable=lang, value=0, indicatoron=0, background="white", fg="#757575", padx=10, relief="flat", border=0, command=radio_btn, foreground="#4285f4")
english.place(relx=.25,rely=.05)
# english.configure(background="white", padx=10, relief="flat", state="active", highlightcolor="blue")


spanish = Radiobutton(window, text="Spanish to English", font=("Proxima Nova Regular",18), variable=lang, value=1, indicatoron=0, background="white", fg="#757575", padx=10, relief="flat", border=0, command=radio_btn)
spanish.place(relx=.55,rely=.05)
# english.configure(background="white", padx=10, relief="flat", state="active", highlightcolor="blue")


header = Label(window, text="¿Qué quieres saber?", font=("Proxima Nova Bold", 50))
header.configure(background="white")
# header.grid(column=100, row=1)
header.place(relx=.5,rely=.4, anchor="center")

verion = Label(window, text="Version 1.70", font=("Proxima Nova Regular", 10))
verion.configure(background="white")
# header.grid(column=100, row=1)
verion.place(relx=.92,rely=.9)

 
txt = Entry(window,width=30, font=("Proxima Nova Thin",30))
txt.configure(border=0, background="#f5f5f5")
# txt.grid(column=1, row=2)
txt.place(relx=.5,rely=.7, anchor="center")
txt.focus()

 


def clicked(self):
    import os
    # Imports the Google Cloud client library
    from google.cloud import translate
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "" # your credentials, e.g. C:/gcloud/gappcred.json

    # Instantiates a client
    client = translate.Client()
    # text_var = "u"+txt.get()
    # The text to translate
    # text = text_var 
    text = txt.get()
    # The target language
    
    # target_lang = ''
    if lang.get()==0:
        target_lang = "es"
        
    elif lang.get()==1:
        target_lang = "en"
        

    target = target_lang
    # Translates some text
    translation = client.translate(
        text,
        target_language=target)

    print(u'Text: {}'.format(text))
    print(u'Translation: {}'.format(translation['translatedText']))
    res = (u'{}'.format(translation['translatedText']))
    # txt.grid_remove()
    txt.configure(background="white", state="disabled")
    # btn.grid_remove()
    header.configure(text= res)

window.bind('<Return>', clicked)

# btn = Button(window, text="Click Me", command=clicked)
# btn.grid(column=1, row=3)



def end_stt():
    # mic_photo_off = PhotoImage(file = r"images/Google Translate/mic-off-50.png")
    return
def start_stt():
    mic_photo_on = PhotoImage(file = r"images/mic-on-50.png")
    mic_on = Button(window, text="Mic", image=mic_photo_on, background="white", activebackground="white", border=0, command=end_stt)
    mic_on.place(x=900,y=148)
    # mic_off.grid()
    # import watson_tts
    # def quit():
    #     return
    # def stop_watson():
    #     return
    # window.bind('<Control-c>', stop_watson)
    def space_break():
        keyboard = Controller()
        # keyboard.press(Key.pause)
        # keyboard.release(Key.pause)
        with keyboard.pressed(Key.control):
          keyboard.press('c')
          keyboard.release('c')


    window.bind('<space>', space_break)
    try:
        from Queue import Queue, Full
    except ImportError:
        from queue import Queue, Full

    ###############################################
    #### Initalize queue / the thing to store the audio recordings ##
    ###############################################
    # CHUNK = 1024
    CHUNK=1500
    # *** if the websocket client isn't fast enough it will just discard
    # *** if that happens it said to try using a larger max size
    BUF_MAX_SIZE = CHUNK * 20
    # Buffer to store audio
    q = Queue(maxsize=int(round(BUF_MAX_SIZE / CHUNK)))

    # Create an instance of AudioSource
    audio_source = AudioSource(q, True, True)

    ###############################################
    #### Prepare Speech to Text Service ########
    ###############################################

    # initialize speech to text service
    speech_to_text = SpeechToTextV1(
        iam_apikey="ZAM8vwm2g3Dsnh1UPjOqyI-PloGvZ-PjSEAbjT_JHk1s",
        url="https://gateway-wdc.watsonplatform.net/speech-to-text/api")

    # define callback for the speech to text service
    class MyRecognizeCallback(RecognizeCallback):
        def __init__(self):
            RecognizeCallback.__init__(self)

        def on_transcription(self, transcript):
            print(transcript)
            # status = "Translating..."

        def on_connected(self):
            print('Connection was successful')
            # status = "Connected"

        def on_error(self, error):
            print('Error received: {}'.format(error))
            # status = "Error"

        def on_inactivity_timeout(self, error):
            print('Inactivity timeout: {}'.format(error))
            # status = "Timeout"

        def on_listening(self):
            print('Service is listening')
            # status = "Listening..."

        def on_hypothesis(self, hypothesis):
            print(hypothesis)
            # return

        def on_data(self, data):
            print(data)
            # text_translation = data
            # header.configure(text=text_translation)
            # return

        def on_close(self):
            print("Connection closed")
            # status = "Listening stopped"

    # this function will initiate the recognize service and pass in the AudioSource
    def recognize_using_weboscket(*args):
        mycallback = MyRecognizeCallback()
        speech_to_text.recognize_using_websocket(audio=audio_source,
                                                 content_type='audio/l16; rate=44100',
                                                 recognize_callback=mycallback,
                                                 interim_results=True)

    ###############################################
    #### Prepare the for recording using Pyaudio ##
    ###############################################

    # Variables for recording the speech
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100

    # define callback for pyaudio to store the recording in queue
    def pyaudio_callback(in_data, frame_count, time_info, status):
        try:
            q.put(in_data)
        except Full:
            pass # discard
        return (None, pyaudio.paContinue)

    # instantiate pyaudio
    audio = pyaudio.PyAudio()

    # open stream using callback
    stream = audio.open(
        format=FORMAT,
        channels=CHANNELS,
        rate=RATE,
        input=True,
        frames_per_buffer=CHUNK,
        stream_callback=pyaudio_callback,
        start=False
    )

    #########################################################################
    #### Start the recording and start service to recognize the stream ######
    #########################################################################

    print("Enter CTRL+C to end recording...")
    stream.start_stream()


    try:
        recognize_thread = Thread(target=recognize_using_weboscket, args=())
        recognize_thread.start()

        while True:
            pass
    except KeyboardInterrupt:
        # stop recording
        recognize_thread.stop()
        stream.stop_stream()
        stream.close()
        audio.terminate()
        audio_source.completed_recording()
    # end()

    # text = translate
    # header.configure(text=text)
    # clicked()
    

mic_photo_off = PhotoImage(file = r"images/mic-off-50.png")
mic_off = Button(window, text="Mic", image=mic_photo_off, background="white", activebackground="white", border=0, command=start_stt)
# btn.grid(column=1, row=3)
mic_off.place(x=900,y=148)








def close(event):
    window.withdraw() # if you want to bring it back
    sys.exit() # if you want to exit the entire thing

window.bind('<Escape>', close)

 
window.mainloop()



