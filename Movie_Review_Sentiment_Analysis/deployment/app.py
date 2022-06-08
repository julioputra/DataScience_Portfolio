import streamlit as st
import tensorflow as tf
import pandas as pd
import numpy as np

st.set_page_config(
    page_title="Movie Review Sentiment Analysis",
    page_icon="🎬",
    layout="centered",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.google.com',
        'Report a bug': "https://www.github.com/julioputra",
        'About': "This is Julio's Milestone 2 in Phase 2",})

def app():
    st.title('Movie Review Sentiment Analysis')

    st.markdown('''
    This is a web application to classify the sentiment of movie reviews
    ''')

    review = st.text_area("Type your review here")

    data_new = {'review' : review}

    model_nlp = tf.keras.models.load_model('imdb_model')

    data_nlp = pd.DataFrame([data_new])  

    if st.button('Predict'):        
        predict_nlp = model_nlp.predict(data_nlp).argmax(axis=1)
        predict_nlp = np.where(predict_nlp < 0.5, 0, 1)
        if predict_nlp == 1:
            st.subheader('This is a POSITIVE review')
        elif predict_nlp == 0:
            st.subheader('This is a NEGATIVE review')
                
app()