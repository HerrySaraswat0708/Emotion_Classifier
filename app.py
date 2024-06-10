import streamlit as st
import tensorflow as tf
from tensorflow.keras.models import load_model
import numpy as np
from tensorflow.keras.preprocessing.sequence import pad_sequences
import pickle
import contractions

with open('tokenizer.pickle', 'rb') as handle:
    tokenizer = pickle.load(handle)


model = load_model('sent_attention.h5')

def clean(text):
  text=text.lower().strip()
  text=contractions.fix(text)
  text=re.sub('[^a-zA-Z]+',' ',text)
  text=re.sub('[ ]+',' ',text)
  tokens=[i for i in text.split() if i not in stop_words and len(i)>2]
  return ' '.join(tokens)


def text_pipeline(text):
  text=clean(text)
  text_tokens=tokenizer.texts_to_sequences([text])
  text_padded=pad_sequences(text_tokens,padding='post',maxlen=max_length)
  logits=model.predict([text_padded],verbose=0)
  return "Sentiment : "+le.inverse_transform([np.argmax(logits)])[0]

# Streamlit App
st.title("Sentiment Analyzer")

# Input text box for user input
input_sentence = st.text_input("Enter a sentence")

# Translate button
if st.button("Translate"):
    if input_sentence:
        output_sentence = text_pipeline(input_sentence)
        st.write("Translated Sentence:", output_sentence)
    else:
        st.write("Please enter a sentence.")