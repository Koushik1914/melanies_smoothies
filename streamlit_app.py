# -----------------------------
# Import python packages
# -----------------------------
import streamlit as st
from snowflake.snowpark.functions import col
import requests
import pandas as pd

# -----------------------------
# Snowflake Connection
# -----------------------------
cnx = st.connection("snowflake")
session = cnx.session()

# -----------------------------
# Load Fruit Options
# -----------------------------
my_dataframe = (
    session
        .table("smoothies.public.fruit_options")
        .select(col("FRUIT_NAME"), col("SEARCH_ON"))
)

# Convert to Pandas
pd_df = my_dataframe.to_pandas()

# -----------------------------
# UI Inputs
# -----------------------------
name_on_order = st.text_input("Name on Smoothie:")

ingredients_list = st.multiselect(
    "Choose up to 5 ingredients:",
    my_dataframe,
    max_selections=5
)

# -----------------------------
# Process Selected Fruits
# -----------------------------
if ingredients_list:

    ingredients_string = ""

    for fruit_chosen in ingredients_list:

        ingredients_string += fruit_chosen + " "

        search_on = pd_df.loc[
            pd_df['FRUIT_NAME'] == fruit_chosen,
            'SEARCH_ON'
        ].iloc[0]

        st.write(
            'The search value for ',
            fruit_chosen,
            ' is ',
            search_on,
            '.'
        )

        st.subheader(fruit_chosen + " Nutrition Information")

        response = requests.get(
            "https://my.smoothiefroot.com/api/fruit/" + search_on
        )

        st.dataframe(
            data=response.json(),
            use_container_width=True
        )
