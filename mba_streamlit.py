import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from mlxtend.frequent_patterns import association_rules, apriori
from datetime import datetime

# Streamlit < 0.65
from streamlit.ReportThread import get_report_ctx

# Streamlit > 0.65
from streamlit.report_thread import get_report_ctx

# Streamlit > ~1.3
from streamlit.script_run_context import get_script_run_ctx as get_report_ctx

# Streamlit > ~1.8
from streamlit.scriptrunner.script_run_context import get_script_run_ctx as get_report_ctx

# Streamlit > ~1.12
from streamlit.runtime.scriptrunner.script_run_context import get_script_run_ctx as get_report_ctx

try:
    # Streamlit < 0.65
    from streamlit.ReportThread import get_report_ctx

except ModuleNotFoundError:
    try:
        # Streamlit > 0.65
        from streamlit.report_thread import get_report_ctx

    except ModuleNotFoundError:
        try:
            # Streamlit > ~1.3
            from streamlit.script_run_context import get_script_run_ctx as get_report_ctx

        except ModuleNotFoundError:
            try:
                # Streamlit > ~1.8
                from streamlit.scriptrunner.script_run_context import get_script_run_ctx as get_report_ctx

            except ModuleNotFoundError:
                # Streamlit > ~1.12
                from streamlit.runtime.scriptrunner.script_run_context import get_script_run_ctx as get_report_ctx




data_bread= pd.read_csv(r'C:\Users\fakhr\Desktop\vsCode\bread basket.csv')

import pandas as pd

# Assuming data_waktu is a column in a DataFrame
data_bread['date_time'] = pd.to_datetime(data_bread['date_time'], format='%d-%m-%Y %H:%M', errors='coerce')

#memecah data variaebl date_time
data_bread['month'] = data_bread['date_time'].dt.month
data_bread['day'] = data_bread['date_time'].dt.weekday

#mengganti nama bulann dan hari dataset 
data_bread['month'].replace([i for i in range(1, 12+1)], ["January", "February", "March", "April", "Mei", "June", "July", "Agust","September", "October", "November", "December"], inplace= True)
data_bread['day'].replace([i for i in range(6+1)], ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"], inplace= True)

st.title("MBA dengan algoritma Apriori")

#kelompok inputan
def get_data(period_day= '', weekday_weekend= '', month= '', day= ''):
    data= data_bread.copy()
    filtered= data.loc[
        (data["period_day"].str.contains(period_day))&
        (data["weekday_weekend"].str.contains(weekday_weekend))&
        (data["month"].str.contains(month.title()))&
        (data["day"].str.contains(day.title()))
    ]
    return filtered if filtered.shape[0] else "No Result!"

def User_input_features():
    item= st.selectbox("item", ["Bread", "Scandinavian", "Hot chocolate", "Jam", "Cookies", "Muffin", "Coffe", "Pastry", "Medialuna", "Farm House", "Mineral water", "Fudge", "Basket", "Tea", "Juice", "Ella s Kitchen Pouches", "Victorian Sponge", "Hearty & Seasonal", "Soup", "Pick and Mix Bowls", "Tartine", "Mighty Protein", "Frittata", "Sandwich", "Brownie", "Alfajores", "Scone", "Tacos Fajita"])
    period_day= st.selectbox("Period_day", ["Morning", "Afternoon", "Evening", "Night"])
    weekday_weekend= st.selectbox("Weekday/weekend", ['Weekday', 'Weekend'])
    month= st.select_slider("Month", ["Jan", "Feb", "Mar", "Apr", "Mei", "Jun", "Jul", "Ags","Sep", "Oct", "Nov", "Dec"])
    day= st.select_slider("Day", ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"], value= "Saturday")

    return item, period_day, weekday_weekend, month, day

item, period_day, weekday_weekend, month, day= User_input_features()

data= get_data(period_day.lower(), weekday_weekend.lower(), month, day)

def encode(x):
    if x <= 0:
        return 0
    elif x >= 1:
        return 1

if type(data)!= type("No Result"):
    item_count= data_bread.groupby(["Transaction", "Item"])["Item"].count().reset_index(name="Count")
    item_count_pivot= item_count.pivot_table(index='Transaction', columns='Item', values='Count', aggfunc='sum').fillna(0)
    item_count_pivot= item_count_pivot.applymap(encode) 
    
    support= 0.01
    frequent_items= apriori(item_count_pivot, min_support= support, use_colnames=True)
    metric= "lift"
    min_threshold= 1
    rules= association_rules(frequent_items, metric= metric, min_threshold= min_threshold)[["antecedents", "consequents", "support", "confidence", "lift"]]
    rules.sort_values('confidence', ascending= False, inplace= True)

def parse_list(x):
    x= list(x)
    if len(x)== 1:
        return x[0]
    elif len(x)> 1:
        return ", ".join(x)

def return_item_data_bread(item_antecedents):
    data= rules[["antecedents", "consequents"]].copy()

    data["antecedents"]= data["antecedents"].apply(parse_list)
    data["consequents"]= data["consequents"].apply(parse_list)

    return list(data.loc[data["antecedents"]== item_antecedents].iloc[0,:])

if type(data)!= type("No Result!"):
    st.markdown("HASIL REKOMENDASI : ")
    st.success(f"Jika konsumen membeli **{item}**, maka membeli **{return_item_data_bread(item)[1]}** secara bersamaan")





