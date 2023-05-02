import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title('My New Healthy Dinner')

streamlit.header('Breakfast Favourites')
streamlit.text('🥣 Omega 3 & Blueberry Oat meal')
streamlit.text('🥗 Kale , SPinach & Rocket Smoothie')
streamlit.text('🐔 Hard Boiled Free-Range egg')
streamlit.text('🥑🍞 Avacado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')


my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")

# Let's put a pick list here so they can pick the fruit they want to include 
my_fruit_list = my_fruit_list.set_index('Fruit')
fruits_selected = streamlit.multiselect("pick some fruits:",list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

streamlit.dataframe(fruits_to_show)

#Create the repetable code block
def get_fruityvice_data(this_fruit_choice):
     fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + this_fruit_choice)
        # write your own comment -what does the next line do? 
     fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
     return fruityvice_normalized
    

streamlit.header("Fruityvice Fruit Advice!")
try:
    fruit_choice = streamlit.text_input('What fruit would you like information about?')
    if not fruit_choice:
      streamlit.error("Please select a fruit to get the information")
    else:
       
        back_from_function = get_fruityvice_data(fruit_choice)
        streamlit.dataframe(back_from_function)
except URLError as e:
    streamlit.error()





streamlit.header("The Fruit load List COntains:")
def get_fruit_load_list():
     with my_cnx.cursor() as my_cur:
          my_cur.execute("SELECT * FROM fruit_load_list")
          return my_cur.fetchall()

# Add a button to load the fruit
if streamlit.button('get fruit load list'):
     my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
     my_data_rows = get_fruit_load_list()
     streamlit.dataframe(my_data_rows)

streamlit.stop()



fruit_choice = streamlit.text_input('What fruit would you like to add?','Jackfruit')
streamlit.write('Thanks for Adding ', fruit_choice)

my_cur.execute("insert into PC_RIVERY_DB.PUBLIC.FRUIT_LOAD_LIST values ('from streamlit')")
