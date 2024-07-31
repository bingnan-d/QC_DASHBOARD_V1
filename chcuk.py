
import io
import streamlit as st
import pandas as pd
from datetime import date, timedelta, datetime, timezone
import streamlit.components.v1 as components
from display_map import stationmap_show
from ftplib import FTP
import tempfile
import ftplib
from PIL import Image
import time


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
ftp = FTP(FTP_HOST)
ftp.login(FTP_USER, FTP_PASS)

FTP_FILE_PATH = "/Data_from_SH_to_download/dashboard/sidebar_logo.png"
with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_file:
    ftp.retrbinary(f"RETR {FTP_FILE_PATH}", temp_file.write)
    logopath = temp_file.name

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

def list_png_on_ftp(ftp, date_str):
    """
    List text files for a given date on the FTP server.
    """
    try:
        FTP_DIR="/Data_from_SH_to_download/dashboard/"
        ftp.cwd(FTP_DIR)
        files = ftp.nlst()  # List all files in the directory
        return [file for file in files if date_str in file and file.endswith('.png')]
    except ftplib.error_perm as e:
        st.error(f"FTP error: {e}")
        return []


def list_files_on_ftp(ftp, date_str):
    """
    List text files for a given date on the FTP server.
    """
    try:
        FTP_DIR="/Data_from_SH_to_download/dashboard/"
        ftp.cwd(FTP_DIR)
        files = ftp.nlst()  # List all files in the directory
        return [file for file in files if date_str in file and file.endswith('.txt')]
    except ftplib.error_perm as e:
        st.error(f"FTP error: {e}")
        return []
   
def fetch_file_from_ftp(ftp, file_name):
    """
    Fetch the content of a file from the FTP server.
    """
    buffer = io.BytesIO()
    try:
        ftp.retrbinary(f"RETR {file_name}", buffer.write)
        buffer.seek(0)
        if file_name.endswith('.png'):
            return Image.open(buffer)
        else:
            return buffer.getvalue().decode('utf-8')
    except ftplib.error_perm as e:
        st.error(f"FTP error: {e}")
        return None


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
    plotpath = "/Data_from_SH_to_download/dashboard/general_scanner_bars_2 - 20_mean.html"
    with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as temp_file:
        ftp.retrbinary(f"RETR {plotpath}", temp_file.write)
        temp_file_path = temp_file.name
    # #plotpath = r"C:\Users\CHCUK-11\OneDrive - CHC Navigation\CodeList\dashboard\plot_pool\general_scan_plots\general_scanner_bars_2 - 20_mean.html"
    display_html_plot(temp_file_path,1000)

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
    #plotfolder = "plot_pool\missing_data_plots"
    #plotfolder = "C:\\Users\\CHCUK-11\\OneDrive - CHC Navigation\\CodeList\\dashboard\\plot_pool\\missing_data_plots"
    if selected_sys=='GPS':
        sysname = 1
    elif selected_sys=='BDS':
        sysname = 3
    elif selected_sys=='GAL':
        sysname = 4
    
    if selected_availability=='Available':
        # pltname = f"constellation_available_daily_{sysname}.html"
        # pltpath = os.path.join(plotfolder,pltname)
        FTP_FILE_PATH = f"/Data_from_SH_to_download/dashboard/missing_data_plots/constellation_available_daily_{sysname}.html"
        with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as temp_file:
            ftp.retrbinary(f"RETR {FTP_FILE_PATH}", temp_file.write)
            pltpath = temp_file.name
        display_html_plot(pltpath,1000)
    else:
        # pltname = f"constellation_miss%_daily_{sysname}.html"
        # pltpath = os.path.join(plotfolder,pltname)
        FTP_FILE_PATH = f"/Data_from_SH_to_download/dashboard/missing_data_plots/constellation_available_daily_{sysname}.html"
        with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as temp_file:
            ftp.retrbinary(f"RETR {FTP_FILE_PATH}", temp_file.write)
            pltpath = temp_file.name
        display_html_plot(pltpath,400)
        # pltname2 = f"constellation_missing_daily_{sysname}.html"
        # pltpath2 = os.path.join(plotfolder,pltname2)
        FTP_FILE_PATH2 = f"/Data_from_SH_to_download/dashboard/missing_data_plots/constellation_missing_daily_{sysname}.html"
        with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as temp_file:
            ftp.retrbinary(f"RETR {FTP_FILE_PATH2}", temp_file.write)
            pltpath2 = temp_file.name
        display_html_plot(pltpath2,400)
#================================
elif current_page=="Daily Report":
    st.markdown("<h1 style='text-align: center; margin-top: -30px;'>Daily Report</h1>", unsafe_allow_html=True)
    selected_date = st.date_input("Select a date", datetime.today()-timedelta(days=6))
    year = selected_date.year
    doy = selected_date.timetuple().tm_yday
    
    st.markdown("<h2>Obs Section</h2>", unsafe_allow_html=True)
    st.markdown(f"<h3>{selected_date} </h3>", unsafe_allow_html=True)
    file1 = list_files_on_ftp(ftp, f"{year}_{doy}_obs_satellite_report")
    file2 = list_files_on_ftp(ftp, f"{year}_{doy}_obs_station_report")
    if len(file1)!=0:
        content = fetch_file_from_ftp(ftp, file2[0])
        lines = content.strip().split('\n')
        svalues = lines[0].split(':')[1].strip().split(' ')
        total_missing_rate = lines[1].split(':')[1].strip()
        st.markdown(f"<h5>Obs Total missing rate: {total_missing_rate}, Total Station number: {svalues[0]}, Actual Station number: {svalues[1]}, Stations with missing data: {svalues[2]}</h5>" , unsafe_allow_html=True)
        col1, col2 = st.columns([1,1])
        with col1:
            top_worst_stations = []
            for line in lines[4:]:
                parts = line.split()
                top_worst_stations.append({
                    'Station': parts[0],
                    'Missing Rate': parts[1]
                })
            df = pd.DataFrame(top_worst_stations)
            df.index = df.index + 1  
            st.markdown(lines[2])
            st.table(df)
        with col2:
            content1 = fetch_file_from_ftp(ftp, file1[0])
            lines1 = content1.strip().split('\n')
            top_worst_satellites = []
            for line in lines1[3:]:
                parts = line.split()
                top_worst_satellites.append({
                    'SYS': parts[0][0],
                    'PRN':parts[0][1:],
                    'Missing Rate': parts[1]
                })
            df1 = pd.DataFrame(top_worst_satellites)
            df1.index = df1.index + 1  
            st.markdown(lines1[1])
            st.table(df1)
    else:
        st.markdown(f"<h3>No report found {year}_{doy}_obs_satellite_report </h3>", unsafe_allow_html=True)

    st.markdown("<h2>Clk Section</h2>", unsafe_allow_html=True)
    st.markdown(f"<h3>{selected_date}</h3>", unsafe_allow_html=True)
    clkfile = list_files_on_ftp(ftp, f"{year}_{doy}_clk_obs_report")
    if len(clkfile)!=0:
        content = fetch_file_from_ftp(ftp, clkfile[0])
        lines = content.strip().split('\n')
        total_missing_rate = lines[0].split(':')[1].strip()
        st.markdown(f"<h5>Clk Total missing rate: {total_missing_rate}</h5>" , unsafe_allow_html=True)
        col1, col2 = st.columns([1,1])
        with col1:
            top_worst_stations = []
            for line in lines[3:]:
                parts = line.split()
                top_worst_stations.append({
                    'SYS': parts[0],
                    'PRN': parts[1],
                    'Clk Missing Rate': parts[2],
                    'Obs Missing Rate': parts[3]
                })
            df = pd.DataFrame(top_worst_stations)
            df.index = df.index + 1  
            st.markdown(lines[2])
            st.table(df)
    
    else:
        st.markdown(f"<h3>No report found {year}_{doy}_clk_obs_report </h3>", unsafe_allow_html=True)
    #st.markdown(f"<h4>Clk Total Missing Rate:{} </h4>", unsafe_allow_html=True)
    st.markdown("<h2>RES Section</h2>", unsafe_allow_html=True)
    st.markdown(f"<h3>{selected_date}</h3>", unsafe_allow_html=True)
    resfile = list_png_on_ftp(ftp, f"{year}{doy}")
    if len(resfile)!=0:
        
        col1, col2, col3 = st.columns([1,1,1])
        with col1:
            image = fetch_file_from_ftp(ftp, resfile[0])
            st.image(image, caption=resfile[0], use_column_width=True)
        with col2:
            image = fetch_file_from_ftp(ftp, resfile[1])
            st.image(image, caption=resfile[1], use_column_width=True)
        with col3:
            image = fetch_file_from_ftp(ftp, resfile[2])
            st.image(image, caption=resfile[2], use_column_width=True)
    else:
        st.markdown(f"<h3>No report found res plot {year}{doy} </h3>", unsafe_allow_html=True)



    st.markdown("<h2>QI Section</h2>", unsafe_allow_html=True)
    st.markdown(f"<h3>{selected_date}</h3>", unsafe_allow_html=True)
    qifile = list_files_on_ftp(ftp, f"QI_DailyReport_{year}{doy}")
    if len(qifile)!=0:
        content = fetch_file_from_ftp(ftp, qifile[0])
        lines = content.strip().split('\n')
        col1, col2 = st.columns([1,1])
        with col1:
            st.markdown(f"<h5>{lines[0][2:]} </h5>" , unsafe_allow_html=True)
            st.markdown(f"<h5>{lines[1][2:]} </h5>" , unsafe_allow_html=True)
            st.markdown(f"<h5>{lines[2][2:]} </h5>" , unsafe_allow_html=True)
            st.markdown(f"<h5>{lines[3]} </h5>" , unsafe_allow_html=True)
    else:
        st.markdown(f"<h3>No report found QI_DailyReport_{year}{doy} </h3>", unsafe_allow_html=True)

#=================================
elif current_page=="Station Performance":
    st.markdown("<h1 style='text-align: center; margin-top: -30px;'>Constellation Performance</h1>", unsafe_allow_html=True)
    col1, col2, col3, col4, col5, col6 = st.columns([1,1,1,1,1,1])
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
            <span style="margin-top: 35px;">Availability:</span>
        </div>
        """,
        unsafe_allow_html=True
        )
    with col4:
        availability = ['Missing','Available']
        default_availability = 'Missing'
        selected_availability = st.selectbox('', availability,index=availability.index(default_availability))
    year = selected_date
    doy = selected_date.timetuple().tm_yday
    #plotfolder = "plot_pool\missing_data_plots"
    #plotfolder = "C:\\Users\\CHCUK-11\\OneDrive - CHC Navigation\\CodeList\\dashboard\\plot_pool\\missing_data_plots"

    if selected_availability=='Available':
        # pltname = f"constellation_available_daily_{sysname}.html"
        # pltpath = os.path.join(plotfolder,pltname)
        FTP_FILE_PATH = f"/Data_from_SH_to_download/dashboard/missing_data_plots/ref_network_performance_available_daily.html"
        with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as temp_file:
            ftp.retrbinary(f"RETR {FTP_FILE_PATH}", temp_file.write)
            pltpath = temp_file.name
        display_html_plot(pltpath,1000)
    else:
        # pltname = f"constellation_miss%_daily_{sysname}.html"
        # pltpath = os.path.join(plotfolder,pltname)
        FTP_FILE_PATH = f"/Data_from_SH_to_download/dashboard/missing_data_plots/ref_network_performance_missing_daily.html"
        with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as temp_file:
            ftp.retrbinary(f"RETR {FTP_FILE_PATH}", temp_file.write)
            pltpath = temp_file.name
        display_html_plot(pltpath,400)
        # pltname2 = f"constellation_missing_daily_{sysname}.html"
        # pltpath2 = os.path.join(plotfolder,pltname2)
        FTP_FILE_PATH2 = f"/Data_from_SH_to_download/dashboard/missing_data_plots/ref_network_performance_miss%_daily.html"
        with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as temp_file:
            ftp.retrbinary(f"RETR {FTP_FILE_PATH2}", temp_file.write)
            pltpath2 = temp_file.name
        display_html_plot(pltpath2,400)
