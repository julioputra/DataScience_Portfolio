import streamlit as st 
import matplotlib.pyplot as plt
import pandas as pd 
import numpy as np 
import seaborn as sns 

def app():
    st.title('Data Visualization')
    st.subheader('Welcome to Data Visualization Section!')

    st.markdown('This section will show you several interesting visualization of Supermarket data and surely will also help you to understand about the data easily.')

######################## Data Loading #################################
    @st.cache
    def load_data():
        df = pd.read_csv('supermarket_sales_cleaned.csv')
        return df

    df=load_data()

###################### Visualization 1 with Callback ###################################
    st.subheader('Visualization 1: Quantity of Purchased Product Line based on Customer Type')

    if st.checkbox('Show full diagram of Quantity of Purchased Product Line based on Customer Type'):
        fig_full = plt.figure(figsize=(12,6))
        sns.barplot(x='Product line', y='Quantity', data=df.sort_values('Product line'), estimator=sum, hue='Customer type')
        plt.title('Quantity of Purchased Product Line based on Customer Type', fontsize=18)
        plt.xlabel('Product Line', fontsize=16)
        plt.ylabel('Quantity', fontsize=16)
        st.pyplot(fig_full)

    selected_type = st.selectbox('Select customer type', options=('Member', 'Normal'), index = 0)
    fig = plt.figure(figsize=(12,6))
    sns.barplot(x='Product line', y='Quantity', data=df[df['Customer type']==selected_type].sort_values('Product line'), estimator=sum)
    plt.title('Quantity of Purchased Product Line based on Customer Type', fontsize=18)
    plt.xlabel('Product Line', fontsize=16)
    plt.ylabel('Quantity', fontsize=16)
    st.pyplot(fig)
    expander = st.expander("Analysis")
    expander.write("From the diagrams above, it appears that Electronic Accessories and Fashion Accessories products are purchased more by normal customers, which are non-membership customers.")
    expander.write("On the other hand, it appears that Food and Beverages, Health and Beauty, Home and lifesttyle, and Sports and Travel products are purchased more by membership customer.")

###################### Visualization 2 with Callback ###################################
    st.subheader('Visualization 2: Distribution of Gross Income in Each Branch')
    
    if st.checkbox('Show diagram of Distribution of Gross Income in All Branch'):
        figfull2, ax1 = plt.subplots(figsize=[12,6])
        sns.histplot(df['gross income'], color="teal")
        plt.title('Distribution of Gross Income in All Branch', fontsize=18)
        plt.xlabel('Gross Income', fontsize=16)
        plt.ylabel('Count', fontsize=16)
        st.pyplot(figfull2)

    selected_branch = st.radio('Select branch', ('Yangon','Naypyitaw','Mandalay'))
    fig1, ax1 = plt.subplots(figsize=[12,6])
    sns.histplot(df[df['City']==selected_branch]['gross income'], color="green")
    plt.title('Distribution of Gross Income in Each Branch', fontsize=18)
    plt.xlabel('Gross Income', fontsize=16)
    plt.ylabel('Count', fontsize=16)
    st.pyplot(fig1)
    expander1 = st.expander("Analysis")
    expander1.write("From the full diagram, it appears that the distribution of gross income data is not normal. The diagram shows that the distribution is positive skew")
    expander1.write("Same thing goes for the segregated diagram. The gross income data in all three branches show a positive skew distribution.")

###################### Visualization 3 ###################################
    st.subheader('Visualization 3: Proportion of Each Product Line')
    colors_list = ['teal', 'yellowgreen', 'palevioletred', 'lightsalmon', 'royalblue', 'tomato']
    fig2,ax2 = plt.subplots()
    df['Product line'].value_counts().plot(kind='pie', 
                                           figsize=(12,6),
                                           autopct='%1.1f%%', 
                                           startangle=90,
                                           labels=None,         
                                           pctdistance=1.12,  
                                           colors=colors_list,
                                           ax=ax2  
                                           )
    fig2.patch.set_facecolor('white')
    plt.title('Proportion of Product Line', fontsize=18)
    plt.axis('equal')
    plt.legend(labels=df['Product line'], loc='upper left')
    st.pyplot(fig2)
    expander2 = st.expander("Analysis")
    expander2.write("From the diagram above, we can see that all Product Lines are purchased almost evenly. The most purchased is in Health and Beauty line and the least is in Electronic Accessories line")

###################### Visualization 4 ###################################
    st.subheader('Visualization 4: Fluctuation of Gross Income in Each Branch')
    df_yangon = df[df['City']=='Yangon'][['Date','City','gross income']].groupby('Date').sum().sort_values('Date')
    df_naypyitaw = df[df['City']=='Naypyitaw'][['Date','City','gross income']].groupby('Date').sum().sort_values('Date')
    df_mandalay = df[df['City']=='Mandalay'][['Date','City','gross income']].groupby('Date').sum().sort_values('Date')

    fig4 = plt.figure()

    ax0 = fig4.add_subplot(3, 1, 1) # add subplot 1 (1 row, 2 columns, first plot)
    ax1 = fig4.add_subplot(3, 1, 2)
    ax2 = fig4.add_subplot(3, 1, 3)

    df_yangon.plot(kind='line',
               color='blue',
               figsize=(30,20),
               ax=ax0)

    df_naypyitaw.plot(kind='line',
                  color='green',
                  figsize=(12,10),
                  ax=ax1)

    df_mandalay.plot(kind='line',
                 color='red',
                 figsize=(12,10),
                 ax=ax2)

    ax0.set_title('Fluctuation of Gross income in Yangon Branch', fontsize=16) 
    ax1.set_title('Fluctuation of Gross income in Naypyitaw Branch', fontsize=16)
    ax2.set_title('Fluctuation of Gross income in Mandalay Branch', fontsize=16)   

    plt.subplots_adjust(left=0.1,
                    bottom=0.1, 
                    right=0.9, 
                    top=0.9, 
                    wspace=0.4, 
                    hspace=0.4)

    st.pyplot(fig4)                
    expander3 = st.expander("Analysis")
    expander3.write("From the graph above, we can see that the gross income is very fluctuative in every branch. Sometimes it reaches below 50, but sometimes it reaches above 150.")












