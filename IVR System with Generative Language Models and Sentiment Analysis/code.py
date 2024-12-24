#!/usr/bin/env python
# coding: utf-8

# In[1]:


import sounddevice as sd
import soundfile as sf

# Path to your audio file (e.g., 'audio.wav')
audio_file_path = 'greet.mp3'

# Load the audio file
data, samplerate = sf.read(audio_file_path)

# Play the audio file
sd.play(data, samplerate)
sd.wait()


# In[2]:


import sounddevice as sd
import numpy as np
import wavio

def record_audio(duration, sample_rate=44100):
    print("Recording...")
    audio_data = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype=np.int16)
    sd.wait()
    print("Recording done")
    return audio_data, sample_rate

# Record 3 seconds of audio
duration = 3  # seconds
audio_data, sample_rate = record_audio(duration)

# Save the audio to a file
file_path = 'recorded_audio.wav'
wavio.write(file_path, audio_data, sample_rate, sampwidth=2)
print(f"Audio saved to {file_path}")


# In[3]:


import speech_recognition as sr


def transcribe_audio(file_path):
    recognizer = sr.Recognizer()
    audio_file = sr.AudioFile(file_path)

    with audio_file as source:
        audio_data = recognizer.record(source)

    try:
        transcript = recognizer.recognize_google(audio_data)
        return transcript
    except sr.UnknownValueError:
        return "Speech recognition could not understand the audio"
    except sr.RequestError as e:
        return f"Error occurred during speech recognition: {e}"

# Path to your audio file (e.g., 'audio.wav')
user_response_audio_data = "recorded_audio.wav"

# Transcribe the audio file
user_response_transcript = transcribe_audio(user_response_audio_data)

print("Transcript:",user_response_transcript )


# In[5]:


#MarieAngeA13/Sentiment-Analysis-BERT
from transformers import pipeline
m='MarieAngeA13/Sentiment-Analysis-BERT'
classifier = pipeline('sentiment-analysis', model=m)
results=classifier(user_response_transcript)



# In[6]:


# Check if the label is very negative
if results[0]['label'] == 'negative' and results[0]['score'] > 0.9:  # Adjust the threshold as needed
    print("operator")
    exit()
else:
    print(results)


# In[9]:


import json
import ollama
# Define the categories
categories_list = ['Account related Enquiries', 'Technical Enquiries', 'New Enquiries', 'confused']
categories_list= '\n - '.join(categories_list)
# Assuming user_response_transcript contains the user's response

prompt = f"""here are the categories of a telecom operator company that you need to select from:
- {categories_list}
Based on that, select one category for this prompt
"""

# Generate a response using the Ollama model
user_response_transcript=json.dumps(user_response_transcript)
response = ollama.generate(model='gemma:2b', prompt=prompt + user_response_transcript, format='json')['response']
print(response)


# In[15]:


data = json.loads(response)
category_name = data.get("category", "")
category_name


# In[16]:


import sounddevice as sd
import soundfile as sf

# Path to your audio files
account_related_inquiry_audio_path = 'Account_related_inquiries.mp3'
technical_audio_path = 'Technical_audio.mp3'

new_enquiry_audio_path = 'sales_audio.mp3'
confused_audio_path = 'Confused_audio.mp3'


# Parse the JSON string into a dictionary
data = json.loads(response)



# Extract the category name
category_name = data.get("category", "")


# Determine the audio file path based on the predicted label
if category_name == 'Account related Enquiries':
    audio_file_path = account_related_inquiry_audio_path
elif category_name == 'Technical Enquiries':
    audio_file_path = technical_audio_path
elif category_name == 'New Enquiries':
    audio_file_path = new_enquiry_audio_path 
else:
    audio_file_path = confused_audio_path

# Load the audio file
data, samplerate = sf.read(audio_file_path)

# Play the audio file
sd.play(data, samplerate)
sd.wait()


# In[19]:




def record_audio(duration, sample_rate=44100):
    print("Recording...")
    audio_data = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype=np.int16)
    sd.wait()
    print("Recording done")
    return audio_data, sample_rate

# Record 3 seconds of audio
duration = 3  # seconds
audio_data, sample_rate = record_audio(duration)

# Save the audio to a file
file_path = 'recorded_audio_1.wav'
wavio.write(file_path, audio_data, sample_rate, sampwidth=2)
print(f"Audio saved to {file_path}")




import speech_recognition as sr



def transcribe_audio(file_path):
    recognizer = sr.Recognizer()
    audio_file = sr.AudioFile(file_path)

    with audio_file as source:
        audio_data = recognizer.record(source)

    try:
        transcript = recognizer.recognize_google(audio_data)
        return transcript
    except sr.UnknownValueError:
        return "Speech recognition could not understand the audio"
    except sr.RequestError as e:
        return f"Error occurred during speech recognition: {e}"

# Path to your audio file (e.g., 'audio.wav')
user_response_audio_data = "recorded_audio_1.wav"

# Transcribe the audio file
user_response_transcript_1 = transcribe_audio(user_response_audio_data)

print("Transcript:",user_response_transcript_1 )


# In[21]:


from transformers import pipeline

# Load the zero-shot classification pipeline
classifier = pipeline("zero-shot-classification")

# Sample transcript


# Classify the transcript using zero-shot learning
classification = classifier(user_response_transcript_1, ["affirmative", "negative"])

# Check if the response is affirmative
if classification["labels"][0] == "affirmative":
    print(response)
else:
    print("Confused")

closing_audio="Goodbye.mp3"
    
# Load the audio file
data, samplerate = sf.read(closing_audio)

# Play the audio file
sd.play(data, samplerate)
sd.wait()


# In[ ]:




