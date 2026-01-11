# -----------------------------
# Import python packages
# -----------------------------
import streamlit as st
from snowflake.snowpark.functions import col
import requests

# -----------------------------
# App Header
# -----------------------------
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write("Choose the fruits you want in your custom Smoothie!")

# -----------------------------
# Name on Smoothie
# -----------------------------
name_on_order = st.text_input("Name on Smoothie:")
st.write("The name on your Smoothie will be:", name_on_order)

# -----------------------------
# Snowflake Connection (SniS)
# -----------------------------
cnx = st.connection("snowflake")
session = cnx.session()

# -----------------------------
# Fruit Options
# -----------------------------
fruit_df = (
    session
        .table("smoothies.public.fruit_options")
        .select(col("FRUIT_NAME"))
)

# -----------------------------
# Multiselect (max 5 fruits)
# -----------------------------
ingredients_list = st.multiselect(
    "Choose up to 5 ingredients:",
    fruit_df,
    max_selections=5
)

# -----------------------------
# Build Ingredients String
# -----------------------------
ingredients_string = ""

if ingredients_list:
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + " "

        # -----------------------------
        # SmoothieFroot Nutrition Info
        # -----------------------------
        smoothiefroot_response = requests.get(
            f"https://my.smoothiefroot.com/api/fruit/{fruit_chosen.lower()}"
        )

        st.dataframe(
            data=smoothiefroot_response.json(),
            use_container_width=True
        )

# -----------------------------
# Submit Button
# -----------------------------
submit_order = st.button("Submit Order")

# -----------------------------
# Insert Order
# -----------------------------
if submit_order:

    if not name_on_order or not ingredients_list:
        st.error("Please enter a name and select at least one ingredient.")
    else:
        insert_stmt = f"""
            INSERT INTO smoothies.public.orders
                (ingredients, name_on_order)
            VALUES
                ('{ingredients_string.strip()}', '{name_on_order}')
        """

        session.sql(insert_stmt).collect()

        st.success(
            f"Your Smoothie is ordered, {name_on_order}!",
            icon="✅"
        )
