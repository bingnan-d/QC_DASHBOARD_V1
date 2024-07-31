import os
#import base64
import streamlit as st
import pandas as pd
#import altair as alt
import time
import plotly
#import common
#import folium
#import pydeck as pdk
from datetime import date, timedelta, datetime, timezone
#from folium.plugins import MarkerCluster
import streamlit.components.v1 as components
import plotly.graph_objects as go
from display_map import stationmap_show
from ftplib import FTP
import tempfile

#============================================================
#for setting the page title
st.set_page_config(
    page_title="SWAS-QC",
    page_icon=":material/satellite_alt:",
    layout="wide",#other options:" centered"
    initial_sidebar_state="expanded" #other options: "collapsed"
)
#===========================================================
#for setting the side bar
pages = ["", "Station Network", "Satellite World View", "Satellite Sky Plot","Daily Report","General Scanner", "Constellation Performance", "Station Performance"]

# Initialize the session state for current page
if 'current_page' not in st.session_state:
    st.session_state.current_page = pages[0]

#logopath = "C:\\Work\\Projects\\dashboard\\picture\\sidebar_logo.png"
#logopath =r"C:\Users\CHCUK-11\OneDrive - CHC Navigation\CodeList\dashboard\picture\sidebar_logo.png"

FTP_HOST = "3.9.58.243"
FTP_USER = "RSDQE"
FTP_PASS = "Gnss12345/"  # Replace with your actual password
FTP_FILE_PATH = "/Data_from_SH_to_download/dashboard/sidebar_logo.png"
ftp = FTP(FTP_HOST)
ftp.login(FTP_USER, FTP_PASS)

with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_file:
    ftp.retrbinary(f"RETR {FTP_FILE_PATH}", temp_file.write)
    logopath = temp_file.name
ftp.quit()

st.sidebar.image(logopath, width=200)

clicked = {page: st.sidebar.button(page) for page in pages}

for page, is_clicked in clicked.items():
    if is_clicked:
        st.session_state.current_page = page
        break
current_page = st.session_state.current_page
#=================================================================================
st.markdown(
    """
    <style>
    .center-text {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 60vh;
        flex-direction: column;
        font-size: 60px;
    }
    .utc-time {
        text-align: center;
        font-size: 30px;
        color: gray;
    }
    .stButton>button {
        border: none;
        background-color: transparent;
        padding: 10px;
        font-size: 16px;
        cursor: pointer;
    }
    .stButton>button:hover {
        background-color: #f0f0f0;
    }
    </style>
    """,
    unsafe_allow_html=True
)


#for showing html plots
def display_html_plot(filepath,pheight):
    with open(filepath, 'r') as f:
        plot_html = f.read()
    components.html(plot_html, height=pheight)
#for show UTC real time 
def get_utc_time():
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
#===================================================================================
if current_page=="Station Network":
    st.markdown("<h1 style='text-align: center; margin-top: -30px;'>Station Network</h1>", unsafe_allow_html=True)
    stcdpath = "stnList3000_selected_v20221116.xlsx"
    #stcdpath = r"C:\Users\CHCUK-11\OneDrive - CHC Navigation\CodeList\dashboard\stnList3000_selected_v20221116.xlsx"
    stationmap_show(stcdpath)
#=====================================
elif current_page==pages[0]:#welcome page
    st.markdown('<div class="center-text">Welcome to SWAS QC</div>', unsafe_allow_html=True)
    utc_placeholder = st.empty() #for 
    while True:
        current_utc_time = get_utc_time()
        utc_placeholder.markdown(f'<div class="utc-time">{current_utc_time}</div>', unsafe_allow_html=True)
        time.sleep(1)
#====================================
elif current_page=="Satellite World View":
    st.markdown("<h1 style='text-align: center; margin-top: -30px;'>Satellite World View</h1>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1,2,7])
    with col1:
        st.markdown(
        """
        <div style="display: flex; align-items: right; justify-content: right; height: 100%;">
            <span style="margin-top: 35px;">Day:</span>
        </div>
        """,
        unsafe_allow_html=True
        )
    with col2:
        selected_time = st.date_input('')
        #local_dir = r"D:\QC_DATA\"
elif current_page=="Satellite Sky Plot":
    st.markdown("<h1 style='text-align: center; margin-top: -30px;'>Satellite Sky View</h1>", unsafe_allow_html=True)

#====================================
elif current_page=="General Scanner":
    plotpath = "general_scanner_bars_2 - 20_mean.html"
    # #plotpath = r"C:\Users\CHCUK-11\OneDrive - CHC Navigation\CodeList\dashboard\plot_pool\general_scan_plots\general_scanner_bars_2 - 20_mean.html"
    # display_html_plot(plotpath,1000)
    with open(plotpath, 'r') as f:
        deck_html = f.read()
    # Render the HTML content in an iframe with specified height
    st.components.v1.html(deck_html, height=700)  # Adjust height as needed
#=============================================
elif current_page=="Constellation Performance":
    st.markdown("<h1 style='text-align: center; margin-top: -30px;'>Constellation Performance</h1>", unsafe_allow_html=True)
    col1, col2, col3, col4, col5,col6 = st.columns([1,1,1,1,1,1])
    with col1:
        st.markdown(
        """
        <div style="display: flex; align-items: right; justify-content: right; height: 100%;">
            <span style="margin-top: 35px;">Day:</span>
        </div>
        """,
        unsafe_allow_html=True
    )
    with col2:
        default_date = date.today() - timedelta(days=1)
        selected_date = st.date_input('', default_date)#''means no label
    with col3:
        st.markdown(
        """
        <div style="display: flex; align-items: right; justify-content: right; height: 100%;">
            <span style="margin-top: 35px;">Constellation:</span>
        </div>
        """,
        unsafe_allow_html=True
        )
    with col4:
        syslist = ['GPS','BDS','GAL']
        default_sys = 'GPS'
        selected_sys = st.selectbox('',syslist,index=syslist.index(default_sys))
    with col5:
        st.markdown(
        """
        <div style="display: flex; align-items: right; justify-content: right; height: 100%;">
            <span style="margin-top: 35px;">Availability:</span>
        </div>
        """,
        unsafe_allow_html=True
        )
    with col6:
        availability = ['Missing','Available']
        default_availability = 'Missing'
        selected_availability = st.selectbox('', availability,index=availability.index(default_availability))
    year = selected_date
    doy = selected_date.timetuple().tm_yday
    plotfolder = "plot_pool\missing_data_plots"
    #plotfolder = "C:\\Users\\CHCUK-11\\OneDrive - CHC Navigation\\CodeList\\dashboard\\plot_pool\\missing_data_plots"
    if selected_sys=='GPS':
        sysname = 1
    elif selected_sys=='BDS':
        sysname = 3
    elif selected_sys=='GAL':
        sysname = 4
    
    if selected_availability=='Available':
        pltname = f"constellation_available_daily_{sysname}.html"
        pltpath = os.path.join(plotfolder,pltname)
        display_html_plot(pltpath,1000)
    else:
        pltname = f"constellation_miss%_daily_{sysname}.html"
        pltpath = os.path.join(plotfolder,pltname)
        display_html_plot(pltpath,400)
        pltname2 = f"constellation_missing_daily_{sysname}.html"
        pltpath2 = os.path.join(plotfolder,pltname2)
        display_html_plot(pltpath2,400)
#================================
elif current_page=="Daily Report":
    st.markdown("<h1 style='text-align: center; margin-top: -30px;'>Daily Report</h1>", unsafe_allow_html=True)