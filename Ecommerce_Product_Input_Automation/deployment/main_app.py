import streamlit as st
import pickle
import sklearn
import pandas as pd
import numpy as np
import requests
from io import BytesIO
from PIL import Image, ImageOps
import base64
import tensorflow as tf
import keras, re, string, requests
from keras.preprocessing import image
from sklearn.preprocessing import MultiLabelBinarizer
import nltk
import difflib

st.set_page_config(
    page_title="Product Input Automation",
    page_icon="🎬",
    layout="centered",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.google.com',
        'Report a bug': "https://www.github.com/julioputra",
        'About': "Final Project Group 4 FTDS Batch 10"})

def app():
    header_img = Image.open('HEADER.jpeg')
    st.title('Product Input Automation')
    st.image(header_img, width=700)

#### Upload Image
    upload_file = st.file_uploader("Upload Product Image", type=["jpg", "png"])

#### Product tags 
    train_tags = ['beach', 'bikini', 'blouse', 'casual', 'cotton', 'dress', 'jumpsuit',
                    'lace', 'ladies', 'loose', 'pants', 'party', 'plus size', 'print',
                    'sexy', 'shirt', 'shorts', 'sleeveless', 'slim', 'sport', 'tank top',
                    'v-neck', 'vest', 'waist', 'women dress']
    if upload_file is None:   
        # Streamlit widgets untuk data kosong saat image belum di upload
        st.title('Product Information Form')
        st.text_input('Product Name', )
        st.multiselect('Product Tag', train_tags)
        col1,col2 = st.columns(2)
        col1.number_input('Inventory Total', 0, 1000000)
        col2.number_input('Retail Price', 0, 1000000)
        st.text_input('Estmated Product Price')

    if upload_file is not None:
        # Show product image
        img = Image.open(upload_file)
        st.image(img, width=200)
        
        # Generate tag recommendation 
        data = pd.read_csv('summer-products-with-rating-and-performance_2020-08.csv')
        df = pd.read_csv('recomender_data.csv')
        df.drop(['Unnamed: 0'], axis=1, inplace=True)
        df['tags']  = df['tags'].str.strip('[]')

        ## membuat tokenizer buat setiap kata
        sentence = []
        for i in range(len(df)):
            tokenizer = nltk.RegexpTokenizer(r"\w+")
            new_words = tokenizer.tokenize(df['tags'][i])
            sentence.append(new_words)
        df['tags'] = sentence

        ## Load model for product tagging
        model_cv = tf.keras.models.load_model('model')

        ## membuat skoring untuk setiap data terhadap data prediksi tagging
        img3 = ImageOps.fit(img, (224,224))
        img3 = tf.keras.preprocessing.image.img_to_array(img3)
        img3 = img3/255
        classes2 = np.array(train_tags)
        proba2 = model_cv.predict(img3.reshape(1,224,224,3))
        top_3a = np.argsort(proba2[0])[:-4:-1]
        tags2 = []
        for i in range(3):
            tags2.append("{}".format(classes2[top_3a[i]]))
        
        predict = tags2.copy() # ini yang jadi inputan dari model multi label classification
        similarity= []
        for i in range(len(df)):
            seq = difflib.SequenceMatcher(None,predict,df['tags'][i])
            d = seq.ratio()*100
            similarity.append(d)
        df['similarity'] = similarity
        df['index'] = df.index.copy()

        ## ambil similarity paling atas
        df_result = df.sort_values(by=['similarity'], ascending=False).head(1)

        ## di loc indexnya
        feature_result = data.iloc[df_result['index']]

        ## mengambil data lalu dimasukan ke variabel
        rec_retail_price = feature_result['retail_price']
        # rec_product_variation_inventory = feature_result['product_variation_inventory']
        # rec_shipping_option_name = feature_result['shipping_option_name']
        # rec_shipping_option_price = feature_result['shipping_option_price']
        # rec_shipping_is_express = feature_result['shipping_is_express']
        rec_inventory_total = feature_result['inventory_total']

        # product tag recommender
        img2 = ImageOps.fit(img, (224,224))
        img2 = tf.keras.preprocessing.image.img_to_array(img2)
        img2 = img2/255
        classes = np.array(train_tags)
        proba = model_cv.predict(img2.reshape(1,224,224,3))
        top_3 = np.argsort(proba[0])[:-4:-1]
        rec_tags = []
        for i in range(3):
            rec_tags.append("{}".format(classes[top_3[i]]))

        ## Streamlit Widgets
        st.title('Product Information Form')
        st.text_input('Product Name', value=feature_result['title_orig'].tolist()[0]) #value=rec_title_name
        st.multiselect('Product Tag', train_tags, rec_tags)
        col1,col2 = st.columns(2)
        inventory_total = col1.number_input('Inventory Total', value=rec_inventory_total.tolist()[0])
        retail_price = col2.number_input('Retail Price', 0, 1000000, value=(rec_retail_price.tolist()[0]*15471))
        
        # data_new = {'retail_price' : retail_price,
        #             'shipping_option_name' : rec_shipping_option_name.tolist()[0],
        #             'shipping_option_price' : rec_shipping_option_price.tolist()[0],
        #             'shipping_is_express' : rec_shipping_is_express.tolist()[0],
        #             'inventory_total' : inventory_total,
        #             'product_variation_inventory' : rec_product_variation_inventory.tolist()[0]}
        # st.dataframe(data_new)

        with open("summer_price_prediction.pkl", "rb") as f:
            price_prediction = pickle.load(f)

        # data_pred = pd.DataFrame([data_new])  
        # predict_price = price_prediction.predict(data_pred)
             
        predict_price = price_prediction.predict(feature_result[['retail_price', 'product_variation_inventory', 'shipping_option_name', 'shipping_option_price', 'shipping_is_express', 'inventory_total']])
        st.number_input('Estimated Product Price', 0, 1000000, value=round(predict_price.tolist()[0]))

    st.button('Submit')
    
app()