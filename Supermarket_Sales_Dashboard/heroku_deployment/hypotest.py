import streamlit as st
import pandas as pd  
import scipy as sp
import numpy as np 
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import norm
from scipy import stats

def app():
    st.title('Hypothesis Testing')
    st.subheader('Welcome to Hypothesis Testing Section!')
    st.markdown('This section will show you an analysis of the significance between supermarket gross income during morning sales (10 AM - 3 PM) and supermarket gross income during evening sales (3 PM - 9 PM).')
    st.markdown('The dataset that will be used here is **Supermarket Sales** data')
    st.markdown('Our hypothesis in this case are:')
    st.markdown('**H0 : µ Gross income during morning sales = µ Gross income during evening sales**')
    st.markdown('**H1 : µ Gross income during morning sales != µ Gross income during evening sales**')
    st.write(' ')
    
    @st.cache
    def load_data():
        df = pd.read_csv('supermarket_sales_cleaned.csv')
        return df

    df=load_data()

################################# Variable Segregation #####################################################
    df_morning = df[(df['Time'] <= '15:00')][['Time','gross income']].sort_values('Time')
    df_morning = df_morning.set_index('Time') 

    df_evening = df[(df['Time'] > '15:00')][['Time','gross income']].sort_values('Time')
    df_evening = df_evening.set_index('Time')

    st.markdown('First thing first, we will define two new variables to segregate the **morning sales** and **evening sales** data')
    code1 = '''df_morning = df[(df['Time'] <= '15:00')][['Time','gross income']].sort_values('Time')
df_morning = df_morning.set_index('Time') 

df_evening = df[(df['Time'] > '15:00')][['Time','gross income']].sort_values('Time')
df_evening = df_evening.set_index('Time')'''

    expander1 = st.expander('Show code')
    expander1.code(code1, language='python')

##################################### P-value calculation ####################################################
    t_stat, p_val = stats.ttest_ind(df_morning, df_evening)

    st.markdown('Then we will calculate the p-value to see whether will the H0 be rejected or not.')
    code2 = '''t_stat, p_val = stats.ttest_ind(df_morning, df_evening)
print('P-value:',p_val[0])
print('t-statistics:',t_stat[0])'''
    
    expander2 = st.expander('Show code')
    expander2.code(code2, language='python')
    
    st.write('P-value =', p_val[0])
    st.write('t-statistics =', t_stat[0])


##################################### Plotting ####################################################
    morning_pop = np.random.normal(df_morning['gross income'].mean(),df_morning['gross income'].std(),5000)
    evening_pop = np.random.normal(df_evening['gross income'].mean(),df_evening['gross income'].std(),5000)

    ci = stats.norm.interval(0.95, df_morning['gross income'].mean(), df_morning['gross income'].std())

    fig_hypo = plt.figure(figsize=(16,5))
    sns.distplot(morning_pop, label='Morning Sales Gross Income',color='blue')
    sns.distplot(evening_pop, label='Evening Sales Gross Income',color='red')

    plt.axvline(df_morning['gross income'].mean(), color='blue', linewidth=2, label='Morning Sales mean')
    plt.axvline(df_evening['gross income'].mean(), color='red',  linewidth=2, label='Evening Sales mean')

    plt.axvline(ci[1], color='green', linestyle='dashed', linewidth=2, label='confidence threshold of 95%')
    plt.axvline(ci[0], color='green', linestyle='dashed', linewidth=2)

    plt.axvline(morning_pop.mean()+t_stat[0]*morning_pop.std(), color='black', linestyle='dashed', linewidth=2, label = 'Alternative Hypothesis')
    plt.axvline(morning_pop.mean()-t_stat[0]*morning_pop.std(), color='black', linestyle='dashed', linewidth=2)

    plt.legend()
    
    st.markdown('''Now let's see the visualization''')
    code3 = '''morning_pop = np.random.normal(df_morning['gross income'].mean(),df_morning['gross income'].std(),5000)
evening_pop = np.random.normal(df_evening['gross income'].mean(),df_evening['gross income'].std(),5000)

ci = stats.norm.interval(0.95, df_morning['gross income'].mean(), df_morning['gross income'].std())

fig_hypo = plt.figure(figsize=(16,5))
sns.distplot(morning_pop, label='Morning Sales Gross Income',color='blue')
sns.distplot(evening_pop, label='Evening Sales Gross Income',color='red')

plt.axvline(df_morning['gross income'].mean(), color='blue', linewidth=2, label='Morning Sales mean')
plt.axvline(df_evening['gross income'].mean(), color='red',  linewidth=2, label='Evening Sales mean')

plt.axvline(ci[1], color='green', linestyle='dashed', linewidth=2, label='confidence threshold of 95%')
plt.axvline(ci[0], color='green', linestyle='dashed', linewidth=2)

plt.axvline(morning_pop.mean()+t_stat[0]*morning_pop.std(), color='black', linestyle='dashed', linewidth=2, label = 'Alternative Hypothesis')
plt.axvline(morning_pop.mean()-t_stat[0]*morning_pop.std(), color='black', linestyle='dashed', linewidth=2)

plt.legend()'''

    expander3 = st.expander('Show code')
    expander3.code(code3, language='python')
    st.pyplot(fig_hypo)

    st.markdown('''The p-value is more than 0.05, that means the we **fail to reject the H0**. 
    Therefore, it can be concluded that the morning sales gross income is not significant from 
    the evening sales gross income. This analysis is also supported by the graph above. It can be 
    seen from the graph that there are not many differences between the morning sales distribution
    and evening sales distribution.  ''')
    st.markdown('''From the analysis, we can conclude that in the morning the Supermarkets have as much 
    gross income as in the evening.''')
