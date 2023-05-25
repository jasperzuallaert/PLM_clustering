import streamlit as st
import pandas as pd
import plotly.express as px

# Read the CSV file
data = pd.read_csv('csv/data_with_ptms.csv')
language_models = ['ESM2_3B', 'ESM1b', 'ProtTransT5_XL_UniRef50']

# Create a checkbox for filtering categories
categories = data['category'].unique()
selected_categories = st.multiselect('Categories', categories, default=categories)

# Create a checkbox for filtering organisms
organisms = data['organism'].unique()
selected_organisms = st.multiselect('Organisms', organisms, default=organisms)

# Filter data based on selected categories
filtered_data = data[data['category'].isin(selected_categories)]

# Filter data based on organism
filtered_data = filtered_data[filtered_data['organism'].isin(selected_organisms)]

# Filter data based on prot_id
selected_prot_ids = st.multiselect('Protein IDs', filtered_data['prot_id'].unique(), default=filtered_data['prot_id'].unique())
filtered_data = filtered_data[filtered_data['prot_id'].isin(selected_prot_ids)]

# Create a checkbox for selecting x and y coordinates
selected_lm = st.selectbox('Language model', language_models)
color_columns = ['category', 'organism', 'prot_id']
color_columns += [x for x in list(filtered_data.columns)[list(filtered_data.columns).index('pos')+1:] if filtered_data[x].nunique()>1]
# Create a dropdown for selecting the column to color by
color_by = st.selectbox('Select Color By', color_columns)

# Create a scatter plot using Plotly
fig = px.scatter(filtered_data, x=f'{selected_lm}_x', y=f'{selected_lm}_y', color=color_by, hover_data=['info', 'ctxt'])
fig.update_layout(title='Scatter Plot')

st.plotly_chart(fig, use_container_width=True)
