import streamlit as st
import numpy as np
import pandas as pd
from streamlit_autorefresh import st_autorefresh
import account
from pymongo import MongoClient
from streamlit_extras.stylable_container import stylable_container
from datetime import datetime
import pytz


mongo_client = MongoClient('mongodb://localhost:27017')

capture_db = mongo_client["Park_Camera"]
capture_detect_evts = capture_db.capture_evts

def read_db():
    data_ZoneA, data_ZoneB,timeA,timeB = [],[],[],[]

    #Find Latest Record
    latest = capture_detect_evts.find_one(sort=[('$natural', -1)])

    current_zoneA, current_zoneB = 0,0
    if latest['location'] == 'Zone A':
        current_zoneA = latest['count']
    else:
        current_zoneB = latest['count']

    total_zoneA = 0
    total_zoneB = 0

    for x in capture_detect_evts.find():
        if x['location'] == 'Zone A':
            total_zoneA += x['count']
            data_ZoneA.append(x['count'])
            timeA.append(x['time'])

        else:
            total_zoneB += x['count']
            data_ZoneB.append(x['count'])
            timeB.append(x['time'])
    
    return current_zoneA,current_zoneB,total_zoneA,total_zoneB,data_ZoneA,timeA,data_ZoneB,timeB


# pymongo configuration
# mongo_host = os.getenv('MONGO_HOST', None)
# if mongo_host is None:
#     logging.error('MONGO_HOST undefined.')
#     sys.exit(1)
# mongo_port = os.getenv('MONGO_PORT', None)
# if mongo_port is None:
#     logging.error('MONGO_PORT undefined.')
#     sys.exit(1)
# mongo_client = MongoClient(mongo_host)

# capture_db = mongo_client.Park_Camera
# capture_col = capture_db.captures
# capture_detect_evtsA = capture_db.capture_evts
# capture_detect_evtsB = capture_db.capture_evts

account.st.session_state.signout = False

def app():
                       
    if account.st.session_state.signout:


        #Autorefresh:
        count = st_autorefresh(interval=1000, limit=1000, key="fizzbuzzcounter")

        current_zoneA,current_zoneB,totalA,totalB,data_ZoneA,timeA,data_ZoneB,timeB =  read_db()

        # recentA = capture_detect_evtsA.find_one({'location':"Zone A"},sort=[('$natural',-1)])
        # recentB = capture_detect_evtsB.find_one({'location':"Zone B"},sort=[('$natural',-1)])

        # all_capture_evtsA = capture_detect_evtsA.find({'location':"Zone A"},{'new_capture':1})
        # all_capture_evtsB = capture_detect_evtsB.find({'location':"Zone B"},{'new_capture':1})
        
        # totalA, totalB = 0,0

        # for x in all_capture_evtsA:
        #     totalA += x['new_capture']

        # for x in all_capture_evtsB:
        #     totalB += x['new_capture']

        # Define a CSS class for metrics background
        custom_css = """
        <style>
        .metric-bg-zoneA {
            background-color: #ff0000; /* Change background color as per your preference */
            padding: 20px; /* Increase padding to increase box size */
            border-radius: 15px; /* Add border radius for rounded corners */
            # display: flex;
            # flex-direction: column;
            # # justify-content: center;
            # align-items: center;
            height: 150px; /* Set a fixed height for all metric boxes */
        }

        .metric-bg-zoneB {
            background-color: #0be300; /* Change background color as per your preference */
            padding: 20px; /* Increase padding to increase box size */
            border-radius: 15px; /* Add border radius for rounded corners */
            # display: flex;
            # flex-direction: column;
            # justify-content: left;
            # align-items: left;
            height: 150px; /* Set a fixed height for all metric boxes */
        }

        .metric-bg-all {
            background-color: #0233f7; /* Change background color as per your preference */
            padding: 20px; /* Increase padding to increase box size */
            border-radius: 10px; /* Add border radius for rounded corners */
            # display: flex;
            # flex-direction: column;
            # justify-content: left;
            # align-items: left;
            height: 150px; /* Set a fixed height for all metric boxes */
        }

        .metric-bg-lightA {
            background-color: #0233f7; /* Change background color as per your preference */
            padding: 50px; /* Increase padding to increase box size */
            border-radius: 10px; /* Add border radius for rounded corners */
            # display: flex;
            # flex-direction: column;
            # justify-content: left;
            # align-items: left;
            height: 200px; /* Set a fixed height for all metric boxes */
        }

        .metric-text {
            font-weight: bold; /* Make the text bold */
            font-size: 22px; /* Adjust font size */
            color: #ffffff; /* Adjust text color */
            margin-top: -5px; /* Adjust margin to move text upwards */
        }
        .metric-text-lightA {
            font-weight: bold; /* Make the text bold */
            font-size: 22px; /* Adjust font size */
            color: #ffffff; /* Adjust text color */
            margin-top: -30px; /* Adjust margin to move text upwards */
        }

        .metric-value {
            font-weight: bold;
            font-size: 20px; /* Adjust font size for temperature value */
            color: #ffffff; /* Adjust text color */
            margin-top: 20px; /* Adjust margin to move text upwards */
        }

        .metric-total {
            font-weight: bold;
            font-size: 20px; /* Adjust font size for temperature value */
            color: #ffffff; /* Adjust text color */
            margin-top: -10px; /* Adjust margin to move text upwards */
        }

        .metric-total-all {
            font-weight: bold;
            font-size: 20px; /* Adjust font size for temperature value */
            color: #ffffff; /* Adjust text color */
            margin-top: 55px; /* Adjust margin to move text upwards */
        }

        .metric-arrow {
            font-size: 24px; /* Adjust font size for arrow */
            color: green; /* Default arrow color */
        }
        </style>
        """
        st.markdown(custom_css, unsafe_allow_html=True)
        
        st.title("Dashboard")
        st.write("          ")
        a1, a2, a3 = st.columns(3)
        # a1.markdown(f'<div class="metric-bg-zoneA"><p class="metric-text">Zone A</p><p class="metric-value">Current Visitors: {recentA}</p><p class="metric-total">Total Visitors: {totalA}</p></div>', unsafe_allow_html=True)
        # a2.markdown(f'<div class="metric-bg-zoneB"><p class="metric-text">Zone B</p><p class="metric-value">Current Visitors: {recentB}</p><p class="metric-total">Total Visitors: {totalB}</p></div>', unsafe_allow_html=True)
        # a3.markdown(f'<div class="metric-bg-all"><p class="metric-text">ALL ZONES</p><p class="metric-value"></p><p class="metric-total-all">Total Visitors: {recentA+recentB}</p></div>', unsafe_allow_html=True)
        a1.markdown(f'<div class="metric-bg-zoneA"><p class="metric-text">Zone A</p><p class="metric-value">Current Visitors: {current_zoneA}</p><p class="metric-total">Total Visitors: {totalA}</p></div>', unsafe_allow_html=True)
        a2.markdown(f'<div class="metric-bg-zoneB"><p class="metric-text">Zone B</p><p class="metric-value">Current Visitors: {current_zoneB}</p><p class="metric-total">Total Visitors: {totalB}</p></div>', unsafe_allow_html=True)
        a3.markdown(f'<div class="metric-bg-all"><p class="metric-text">ALL ZONES</p><p class="metric-value"></p><p class="metric-total-all">Total Visitors: {totalA+totalB}</p></div>', unsafe_allow_html=True)
        
        st.write("                                  ")
        st.write("                                  ")
        timezone = pytz.timezone('Asia/Bangkok')
        bkk_time = datetime.now(timezone)
        original_title_date = f'<p style="font-family:Arial Black; color:Black; font-size: 30px; font-weight:normal;">{bkk_time.strftime("%A %d %B, %Y")}<br>{bkk_time.strftime("%H:%M:%S")}</p>'
        st.markdown(original_title_date, unsafe_allow_html=True)

        # Row C
        # C1 being the graph, C2 The Table.
        c_css = """
        <style>
        .metric-bg-lightA {
            background-color: #dbf7ff; /* Change background color as per your preference */
            padding: 50px; /* Increase padding to increase box size */
            border-radius: 10px; /* Add border radius for rounded corners */
            # display: flex;
            # flex-direction: column;
            # justify-content: center;
            # align-items: center;
            height: 300px; /* Set a fixed height for all metric boxes */
        }

        .material-icons{
            margin-top:50px;
            margin-left:60px;
        }

        .metric-text-label {
            font-weight: bold; /* Make the text bold */
            font-size: 22px; /* Adjust font size */
            color: #545454; /* Adjust text color */
            margin-top: -30px; /* Adjust margin to move text upwards */
            margin-left: -30px; /* Adjust this value as needed */
            text-align: left;
        }
        .metric-text-lightA {
            font-weight: bold; /* Make the text bold */
            font-size: 22px; /* Adjust font size */
            color: #545454; /* Adjust text color */
            margin-top: -30px; /* Adjust margin to move text upwards */
        }
        .metric-text-light {
            font-weight: thin;
            font-size: 20px; /* Adjust font size for temperature value */
            color: #545454; /* Adjust text color */
            margin-top: 20px; /* Adjust margin to move text upwards */
        }
        .metric-text-status {
            font-weight: thin;
            font-size: 20px; /* Adjust font size for temperature value */
            color: #545454; /* Adjust text color */
            margin-top: -20px; /* Adjust margin to move text upwards */
        }
        .metric-text-light-brightness {
            font-weight: thin;
            font-size: 20px; /* Adjust font size for temperature value */
            color: #545454; /* Adjust text color */
            margin-top: 0px; /* Adjust margin to move text upwards */
            margin-left: 185px;
        }
        [role="light-bar"] {
            --percentage: 45deg;
            --primary: #369;
            --secondary: #adf;
            --size: 50px;
            # margin-left: 23
            width: 175px;
            height: 50px;
            aspect-ratio: 2 / 1;
            border-radius: 50% / 100% 100% 0 0;
            position: relative;
            overflow: hidden;
            animation: light 2s 0.5s forwards ;
            animation-play-state: running;
            margin-left: 150px; /* Adjusted margin */
            margin-top:50px;
            margin-bottom:-80px;
        }

        [role="light-bar"]::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: conic-gradient(from 0.75turn at 50% 100%, var(--primary) calc(var(--percentage) * 1% / 2), var(--secondary) calc(var(--percentage) * 1% / 2 + 0.1%));
            mask: radial-gradient(at 50% 100%, white 55%, transparent 55.5%);
            mask-mode: alpha;
            -webkit-mask: radial-gradient(at 50% 100%, #0000 55%, #000 55.5%);
            -webkit-mask-mode: alpha;
        }
        [role="light-bar"]::after{
            counter-reset: percentage 13;
            content: counter(percentage) '%';
            font-family: Helvetica, Arial, sans-serif;
            font-size: calc(var(--size) / 5);
            color: #0000000;
        }
        @keyframes light {
            0% { --percentage: 0; }
            100% { --percentage: 30; }
        }
        @property --percentage {
            syntax: '<number>';
            inherits: true;
            initial-value: 0;
        }
        </style>
        """

        st.markdown(c_css, unsafe_allow_html=True)

        c1, c2 = st.columns((6, 4))
        
        # Graph
        with c1:
            data = {"Time": timeA, "Zone A":data_ZoneA}
            chart_data = pd.DataFrame(data)
            st.line_chart(chart_data, x="Time", y="Zone A")

        # # The fake nonsens table
        # with c2:
        #     df = pd.DataFrame(
        #         np.random.randn(7, 5),
        #         columns=('Paris', 'Malta', 'Stockholm', 'Peru', 'Italy')
        #     )
        #     st.table(df)
        # Add the link to the Google Fonts Icons CSS stylesheet
        # st.markdown('<link href="https://fonts.googleapis.com/css2?family=Material+Icons" rel="stylesheet">', unsafe_allow_html=True)

        # percentage_value = 32
        # # Add the Markdown content with the icon
        # c2.markdown(
        #     f'''
        #     <div class="metric-bg-lightA">
        #         <p class="metric-text-label">Zone A</p>
        #         <div role="light-bar">
        #         </div><i class="material-icons">light</i>
        #         <p class="metric-text-light-brightness">30%</p>
        #         <p class="metric-text-light">Light 1</p>
        #         <p class="metric-text-status">Status: ON</p>
        #     </div>
        #     ''', 
        #         unsafe_allow_html=True
        # )
        # # 
        # c2.toggle("Emergency Light Zone A")

        with c2:
            with stylable_container(
                key="light_containerA",
                css_styles=[
                    """
                    {
                        display: flex;
                        justify-content: space-between;
                        align-items: center;
                        background-color: #dbf7ff;
                        padding: 40px;
                        border-radius: 10px;
                        height:50px;
                    }
                    """,
                    """
                    /* Define a class for the icon */
                    .material-icons {
                        font-family: 'Material Icons';
                        font-weight: normal;
                        font-style: normal;
                        font-size: 24px;  /* Adjust the font size as needed */
                        display: inline-block;
                        line-height: 1;
                        text-transform: none;
                        letter-spacing: normal;
                        word-wrap: normal;
                        white-space: nowrap;
                        direction: ltr;
                        margin-left: 50px;
                        margin-top: 30px;  
                    }
                    .metric-text-label {
                        font-weight: bold; /* Make the text bold */
                        font-size: 22px; /* Adjust font size */
                        color: #545454; /* Adjust text color */
                        margin-top: -30px; /* Adjust margin to move text upwards */
                        margin-left: 30px; /* Adjust this value as needed */
                        text-align: left;
                    }
                    .metric-text-lightA {
                        font-weight: bold; /* Make the text bold */
                        font-size: 22px; /* Adjust font size */
                        color: #545454; /* Adjust text color */
                        margin-top: -30px; /* Adjust margin to move text upwards */
                    }
                    .metric-text-light {
                        font-weight: thin;
                        font-size: 18px; /* Adjust font size for temperature value */
                        color: #545454; /* Adjust text color */
                        margin-top: -40px; /* Adjust margin to move text upwards */
                        margin-left:30px;
                    }
                    .metric-text-status {
                        font-weight: thin;
                        font-size: 18px; /* Adjust font size for temperature value */
                        color: #545454; /* Adjust text color */
                        margin-top: -20px; /* Adjust margin to move text upwards */
                        margin-left:30px;
                    }
                    """
                    
                ]
            ): 
                st.markdown(
                    f'''
                    <div>
                    <p class="metric-text-label">Zone A</p>
                    </div>
                    ''',unsafe_allow_html=True
                )
                with stylable_container(
                    key="light_container_za",
                    css_styles=[
                    # """
                    # {
                    #     border: 1px hidden;
                    #     padding: 30px;
                    #     width: 20px;
                    #     height:20px;
                    #     margin-left:-140px;
                    # }

                    # """,
                    """
                    .material-icons {
                        margin-left:-100px;
                    }
                    """,
                    ]
                ):
                    # Add the Material Icons CSS to Streamlit
                    st.markdown(
                        f'<link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">',
                        unsafe_allow_html=True
                    )
                    st.markdown(
                        f'''
                        <div>
                        <i class="material-icons">light</i>
                        </div>
                        ''', unsafe_allow_html=True
                    )

                with stylable_container(
                    key="light_container_zab",
                    css_styles=[
                    """
                    [role="light-bar"] {
                        --percentage: 45deg;
                        --primary: #369;
                        --secondary: #adf;
                        --size: 50px;
                        # margin-left: 23
                        width: 175px;
                        height: 50px;
                        aspect-ratio: 2 / 1;
                        border-radius: 50% / 100% 100% 0 0;
                        position: relative;
                        overflow: hidden;
                        animation: light 2s 0.5s forwards ;
                        animation-play-state: running;
                        margin-left: 100px; /* Adjusted margin */
                        margin-top: -60px;
                    }

                    [role="light-bar"]::before {
                        content: '';
                        position: absolute;
                        top: 0;
                        left: 0;
                        width: 100%;
                        height: 100%;
                        background: conic-gradient(from 0.75turn at 50% 100%, var(--primary) calc(var(--percentage) * 1% / 2), var(--secondary) calc(var(--percentage) * 1% / 2 + 0.1%));
                        mask: radial-gradient(at 50% 100%, white 55%, transparent 55.5%);
                        mask-mode: alpha;
                        -webkit-mask: radial-gradient(at 50% 100%, #0000 55%, #000 55.5%);
                        -webkit-mask-mode: alpha;
                    }
                    [role="light-bar"]::after{
                        counter-reset: percentage 13;
                        content: counter(percentage) '%';
                        font-family: Helvetica, Arial, sans-serif;
                        font-size: calc(var(--size) / 5);
                        color: #0000000;
                    }
                    @keyframes light {
                        0% { --percentage: 0; }
                        100% { --percentage: 0; }
                    }
                    @property --percentage {
                        syntax: '<number>';
                        inherits: true;
                        initial-value: 0;
                    }
                    """]
                ):
                    st.markdown(
                        f'''
                        <div>
                        <div role="light-bar"></div>
                        </div>
                        ''',unsafe_allow_html=True
                    )
                    with stylable_container(
                        key="light_container_zac",
                        css_styles=[
                        """
                            .metric-text-light-brightness {
                                font-weight: thin;
                                font-size: 18px; /* Adjust font size for temperature value */
                                color: #545454; /* Adjust text color */
                                margin-top:-50px;
                                margin-left:135px;
                            }
                        """
                        ]
                    ):
                        st.markdown(
                            f'''
                                <div>
                                    <p class="metric-text-light-brightness">0%</p>
                                </div>
                            ''', unsafe_allow_html=True
                        )
                st.markdown(
                    f'''
                    <div>
                        <p class="metric-text-light">Light 1</p>
                        <p class="metric-text-status">Status: OFF</p>
                    </div>
                    ''', unsafe_allow_html=True
                )
                with stylable_container(
                    key="toggleA",
                    css_styles=[
                        """
                        {
                        }
                        """
                    ]
                ):
                    st.toggle("Emergency Light (A)")

        # d_css = """
        # <style>
        # .metric-bg-lightB {
        #     background-color: #dbf7ff; /* Change background color as per your preference */
        #     padding: 50px; /* Increase padding to increase box size */
        #     border-radius: 10px; /* Add border radius for rounded corners */
        #     # display: flex;
        #     # flex-direction: column;
        #     # justify-content: center;
        #     # align-items: center;
        #     height: 300px; /* Set a fixed height for all metric boxes */
        # }

        # .metric-text-label-B {
        #     font-weight: bold; /* Make the text bold */
        #     font-size: 22px; /* Adjust font size */
        #     color: #545454; /* Adjust text color */
        #     margin-top: -30px; /* Adjust margin to move text upwards */
        #     margin-left: -30px; /* Adjust this value as needed */
        #     text-align: left;
        # }
        # .metric-text-lightB {
        #     font-weight: bold; /* Make the text bold */
        #     font-size: 22px; /* Adjust font size */
        #     color: #545454; /* Adjust text color */
        #     margin-top: -30px; /* Adjust margin to move text upwards */
        # }
        # .metric-text-lightB {
        #     font-weight: thin;
        #     font-size: 20px; /* Adjust font size for temperature value */
        #     color: #545454; /* Adjust text color */
        #     margin-top: 20px; /* Adjust margin to move text upwards */
        # }
        # .metric-text-statusB {
        #     font-weight: thin;
        #     font-size: 20px; /* Adjust font size for temperature value */
        #     color: #545454; /* Adjust text color */
        #     margin-top: -20px; /* Adjust margin to move text upwards */
        # }
        # .metric-text-light-brightnessB {
        #     font-weight: thin;
        #     font-size: 20px; /* Adjust font size for temperature value */
        #     color: #545454; /* Adjust text color */
        #     margin-top: -25px; /* Adjust margin to move text upwards */
        #     margin-left: 185px;
        # }
        # [role="light-barB"] {
        #     --percentage: 45deg;
        #     --primary: #369;
        #     --secondary: #adf;
        #     --size: 50px;
        #     # margin-left: 23
        #     width: 175px;
        #     height: 50px;
        #     aspect-ratio: 2 / 1;
        #     border-radius: 50% / 100% 100% 0 0;
        #     position: relative;
        #     overflow: hidden;
        #     animation: lightB 2s 0.5s forwards ;
        #     animation-play-state: running;
        #     margin-left: 150px; /* Adjusted margin */
        # }

        # [role="light-barB"]::before {
        #     content: '';
        #     position: absolute;
        #     top: 0;
        #     left: 0;
        #     width: 100%;
        #     height: 100%;
        #     background: conic-gradient(from 0.75turn at 50% 100%, var(--primary) calc(var(--percentage) * 1% / 2), var(--secondary) calc(var(--percentage) * 1% / 2 + 0.1%));
        #     mask: radial-gradient(at 50% 100%, white 55%, transparent 55.5%);
        #     mask-mode: alpha;
        #     -webkit-mask: radial-gradient(at 50% 100%, #0000 55%, #000 55.5%);
        #     -webkit-mask-mode: alpha;
        # }
        # [role="light-barB"]::after{
        #     counter-reset: percentage 13;
        #     content: counter(percentage) '%';
        #     font-family: Helvetica, Arial, sans-serif;
        #     font-size: calc(var(--size) / 5);
        #     color: #0000000;
        # }
        # @keyframes lightB {
        #     0% { --percentage: 0; }
        #     100% { --percentage: 10; }
        # }
        # @property --percentage {
        #     syntax: '<number>';
        #     inherits: true;
        #     initial-value: 0;
        # }
        # </style>
        # """
        # st.markdown(d_css, unsafe_allow_html=True)

        # d1,d2 = st.columns((6,4))
        # # # d1.markdown(f'''
        # # #             <div class="metric-bg-lightB">
        # # #                 <div role="light-bar" aria-valuenow="33" aria-valuemin="0" aria-valuemax="100" style="--value: 78"></div>
        # # #                 <p class="metric-text-light-brightness">23%</p>
        # # #             </div>
        # # #             ''',  unsafe_allow_html=True)

        # d2.markdown(
        #     f'''
        #     <div class="metric-bg-lightB">
        #         <p class="metric-text-label-B">Zone B</p>
        #         <i class="material-icons">light</i>
        #         <div role="light-barB"></div>
        #         <p class="metric-text-light-brightnessB">10%</p>
        #         <p class="metric-text-lightB">Light 1</p>
        #         <p class="metric-text-statusB">Status: ON</p>
        #     </div>
        #     ''', 
        #         unsafe_allow_html=True
        #     )
        # d2.toggle("Emergency Light Zone B")
        #st.markdown("<style>.button1 { /* Button 1 CSS attributes*/ }</style>", unsafe_allow_html=True)
        # button_css = """
        # <style>
        #     [data-baseweb="toggle"] [data-testid="stWidgetLabel"] p {
        #         /* Styles for the label text for checkbox and toggle */
        #         font-size: 3.5rem;
        #         width: 3000px;
        #         margin-top: 1rem;
        #     }

        #     [data-baseweb="toggle"] div {
        #         /* Styles for the slider container */
        #         height: 3rem;
        #         width: 4rem;
        #     }
        #     [data-baseweb="toggle"] div div {
        #         /* Styles for the slider circle */
        #         height: 2.8rem;
        #         width: 2.8rem;
        #     }
        #     [data-testid="stToggle"] label span {
        #         /* Styles the checkbox */
        #         height: 4rem;
        #         width: 4rem;
        #     }
        #     </style>
        #     """
                
        # css = """
        # <style>
        # [data-baseweb="checkbox"] [data-testid="stWidgetLabel"] p {
        #     /* Styles for the label text for checkbox and toggle */
        #     font-size: 16px ;
        #     width: 300px;
        #     margin-top: 1rem;
        # }

        # [data-baseweb="checkbox"] div {
        #     /* Styles for the slider container */
        #     height: 30px;
        #     width: 40px;
        #     margin-top: 50px;
        # }
        # [data-baseweb="checkbox"] div div {
        #     /* Styles for the slider circle */
        #     height: 20px;
        #     width: 20px;
        # }
        # [data-testid="stCheckbox"] label span {
        #     /* Styles the checkbox */
        #     height: 4rem;
        #     width: 4rem;
        # }
        # </style>
        # """

        # st.markdown(css, unsafe_allow_html=True)

        # d1.markdown(
        #     f'''
        #     <div class="metric-bg-lightB">
        #         <div [data-baseweb="checkbox"]></div>
        #     </div>
        #     ''', 
        #         unsafe_allow_html=True
        #     )
        
        # st.markdown(button_css,unsafe_allow_html=True)
        # with d1:
        # #     st.button("Seconday button")  # st.button default type is secondary
        # #     st.button("Primary button", type="primary")
        #     st.toggle("Toggle One")
        #     st.write(button_css,unsafe_allow_html=True)


        # tog.st_toggle_switch(label="Label", 
        #             key="Key1", 
        #             default_value=False, 
        #             label_after = True, 
        #             inactive_color = '#D3D3D3', 
        #             active_color="#11567f", 
        #             track_color="#29B5E8"
        #             )
        # with st.sidebar:
        #     toggle1 = tog.st_toggle_switch(
        #         label="Option 1",
        #         key="Key5",
        #         default_value=False,
        #         label_after=False,
        #         inactive_color="#D3D3D3",
        #         active_color="#11567f",
        #         track_color="#29B5E8",
        #     )
        #     toggle2 = tog.st_toggle_switch(
        #         label="Option 1",
        #         key="Key2",
        #         default_value=False,
        #         label_after=True,
        #         inactive_color="#D3D3D3",
        #         active_color="#11567f",
        #         track_color="#29B5E8",
        #     )

        #Zone B Light Container
        d1,d2 = st.columns((6,4))
        with d1:
            dataB = {"Time": timeB, "Zone B":data_ZoneB}
            chart_data = pd.DataFrame(dataB)
            st.line_chart(chart_data, x="Time", y="Zone B")

        with d2:
            with stylable_container(
                key="light_containerB",
                css_styles=[
                    """
                    {
                        display: flex;
                        justify-content: space-between;
                        align-items: center;
                        background-color: #dbf7ff;
                        padding: 40px;
                        border-radius: 10px;
                        height:50px;
                    }
                    """,
                    """
                    /* Define a class for the icon */
                    .material-icons {
                        font-family: 'Material Icons';
                        font-weight: normal;
                        font-style: normal;
                        font-size: 24px;  /* Adjust the font size as needed */
                        display: inline-block;
                        line-height: 1;
                        text-transform: none;
                        letter-spacing: normal;
                        word-wrap: normal;
                        white-space: nowrap;
                        direction: ltr;
                        margin-left: 50px;
                        margin-top: 30px;  
                    }
                    .metric-text-label {
                        font-weight: bold; /* Make the text bold */
                        font-size: 22px; /* Adjust font size */
                        color: #545454; /* Adjust text color */
                        margin-top: -30px; /* Adjust margin to move text upwards */
                        margin-left: 30px; /* Adjust this value as needed */
                        text-align: left;
                    }
                    .metric-text-lightA {
                        font-weight: bold; /* Make the text bold */
                        font-size: 22px; /* Adjust font size */
                        color: #545454; /* Adjust text color */
                        margin-top: -30px; /* Adjust margin to move text upwards */
                    }
                    .metric-text-light {
                        font-weight: thin;
                        font-size: 18px; /* Adjust font size for temperature value */
                        color: #545454; /* Adjust text color */
                        margin-top: -40px; /* Adjust margin to move text upwards */
                        margin-left:30px;
                    }
                    .metric-text-status {
                        font-weight: thin;
                        font-size: 18px; /* Adjust font size for temperature value */
                        color: #545454; /* Adjust text color */
                        margin-top: -20px; /* Adjust margin to move text upwards */
                        margin-left:30px;
                    }
                    """
                    
                ]
            ): 
                st.markdown(
                    f'''
                    <div>
                    <p class="metric-text-label">Zone B</p>
                    </div>
                    ''',unsafe_allow_html=True
                )
                with stylable_container(
                    key="light_container_zb",
                    css_styles=[
                    # """
                    # {
                    #     border: 1px hidden;
                    #     padding: 30px;
                    #     width: 20px;
                    #     height:20px;
                    #     margin-left:-140px;
                    # }

                    # """,
                    """
                    .material-icons {
                        margin-left:-100px;
                    }
                    """,
                    ]
                ):
                    # Add the Material Icons CSS to Streamlit
                    st.markdown(
                        f'<link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">',
                        unsafe_allow_html=True
                    )
                    st.markdown(
                        f'''
                        <div>
                        <i class="material-icons">light</i>
                        </div>
                        ''', unsafe_allow_html=True
                    )

                with stylable_container(
                    key="light_container_zbb",
                    css_styles=[
                    """
                    [role="light-bar"] {
                        --percentage: 45deg;
                        --primary: #369;
                        --secondary: #adf;
                        --size: 50px;
                        # margin-left: 23
                        width: 175px;
                        height: 50px;
                        aspect-ratio: 2 / 1;
                        border-radius: 50% / 100% 100% 0 0;
                        position: relative;
                        overflow: hidden;
                        animation: light 2s 0.5s forwards ;
                        animation-play-state: running;
                        margin-left: 100px; /* Adjusted margin */
                        margin-top: -60px;
                    }

                    [role="light-bar"]::before {
                        content: '';
                        position: absolute;
                        top: 0;
                        left: 0;
                        width: 100%;
                        height: 100%;
                        background: conic-gradient(from 0.75turn at 50% 100%, var(--primary) calc(var(--percentage) * 1% / 2), var(--secondary) calc(var(--percentage) * 1% / 2 + 0.1%));
                        mask: radial-gradient(at 50% 100%, white 55%, transparent 55.5%);
                        mask-mode: alpha;
                        -webkit-mask: radial-gradient(at 50% 100%, #0000 55%, #000 55.5%);
                        -webkit-mask-mode: alpha;
                    }
                    [role="light-bar"]::after{
                        counter-reset: percentage 13;
                        content: counter(percentage) '%';
                        font-family: Helvetica, Arial, sans-serif;
                        font-size: calc(var(--size) / 5);
                        color: #0000000;
                    }
                    @keyframes light {
                        0% { --percentage: 0; }
                        100% { --percentage: 0; }
                    }
                    @property --percentage {
                        syntax: '<number>';
                        inherits: true;
                        initial-value: 0;
                    }
                    """]
                ):
                    st.markdown(
                        f'''
                        <div>
                        <div role="light-bar"></div>
                        </div>
                        ''',unsafe_allow_html=True
                    )
                    with stylable_container(
                        key="light_container_zbc",
                        css_styles=[
                        """
                            .metric-text-light-brightness {
                                font-weight: thin;
                                font-size: 18px; /* Adjust font size for temperature value */
                                color: #545454; /* Adjust text color */
                                margin-top:-50px;
                                margin-left:135px;
                            }
                        """
                        ]
                    ):
                        st.markdown(
                            f'''
                                <div>
                                    <p class="metric-text-light-brightness">0%</p>
                                </div>
                            ''', unsafe_allow_html=True
                        )
                st.markdown(
                    f'''
                    <div>
                        <p class="metric-text-light">Light 1</p>
                        <p class="metric-text-status">Status: OFF</p>
                    </div>
                    ''', unsafe_allow_html=True
                )
                with stylable_container(
                    key="toggleB",
                    css_styles=[
                        """
                        {
                            
                        }
                        """
                    ]
                ):
                    st.toggle("Emergency Light (B)")

    else:
        st.warning("Please Login First")
        