
import streamlit as st
import pandas as pd
import pydeck as pdk    
#=================================================================================================
def stationmap_show(stcdpath):
    # stcddt = pd.read_excel(stcdpath)
    # stcddt.rename(columns={'Sta': 'station','Lat': 'latitude', 'Lon': 'longitude'}, inplace=True)
    # layer = pdk.Layer(
    #     'ScatterplotLayer', # Layer type
    #     stcddt,
    #     get_position='[longitude, latitude]',
    #     get_color='[0, 0, 255, 160]',
    #     get_radius=20000,# Point radius (20,000 pixels)
    #     pickable=True,
    #     auto_highlight=True
    # )
    #  # Set the viewport location
    # view_state = pdk.ViewState(
    #     latitude=stcddt['latitude'].mean(),
    #     longitude=stcddt['longitude'].mean(),
    #     zoom=3,
    #     pitch=0
    # )
    # # Define tooltips
    # tooltip = {
    #     "html": "<b>Station:</b> {station}<br/><b>Latitude:</b> {latitude}<br/><b>Longitude:</b> {longitude}",
    #     "style": {"backgroundColor": "steelblue", "color": "white"}
    # }
    # map_style = 'light'
    # r = pdk.Deck(layers=[layer], initial_view_state=view_state, tooltip=tooltip, map_style=map_style)
    # r.to_html('deck.html')
    # # Read the HTML content
    with open('deck.html', 'r') as f:
        deck_html = f.read()
    # Render the HTML content in an iframe with specified height
    st.components.v1.html(deck_html, height=700)  # Adjust height as needed
    return 
#==============================================================================================================