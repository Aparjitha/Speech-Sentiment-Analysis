import speech_recognition as sr
from textblob import TextBlob
import re

recognizer = sr.Recognizer()

def get_voice_input():
    try:
        with sr.Microphone() as source:
            print("Adjusting for ambient noise... Please wait.")
            recognizer.adjust_for_ambient_noise(source, duration=1)
            print("Please speak now.")
            audio = recognizer.listen(source) 
            print("Processing your input...")
            text = recognizer.recognize_google(audio)
            return text
    except sr.UnknownValueError:
        print("Sorry, I could not understand your speech.")
        return None
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        return None

def analyze_sentiment(text):
    blob = TextBlob(text)
    sentiment_score = blob.sentiment.polarity
    return sentiment_score

def analyze_split_sentiment(text):
    conjunctions = r'\b(?:but|however|though|although|nevertheless|still|yet)\b'
    
    split_phrases = re.split(conjunctions, text, flags=re.IGNORECASE)
    
    sentiment_scores = []
    
    for phrase in split_phrases:
        sentiment_score = analyze_sentiment(phrase.strip())
        sentiment_scores.append(sentiment_score)
    
    if any(score > 0 for score in sentiment_scores) and any(score < 0 for score in sentiment_scores):
        return 0 
    else:
        return sum(sentiment_scores) / len(sentiment_scores)  

if __name__ == "__main__":
    print("Starting voice input sentiment analysis...")
    transcribed_text = get_voice_input()
    if transcribed_text:
        print(f"Transcribed Text: {transcribed_text}")
        sentiment = analyze_split_sentiment(transcribed_text)
        if sentiment > 0:
            print("Sentiment: Positive")
        elif sentiment < 0:
            print("Sentiment: Negative")
        else:
            print("Sentiment: Neutral")
    else:
        print("No valid speech input detected.")