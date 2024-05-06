import streamlit as st
import firebase_admin 
from dataclasses import dataclass
from datetime import datetime
import json
import pytz
import time

from firebase_admin import credentials
from firebase_admin import auth

cred = credentials.Certificate('mtj-parklightcam-5c721af4886f.json')
firebase_admin.initialize_app(cred) #only need to run this once



def app():

    st.title('Welcome to :violet[MTJ Park Management]')#🌳

    
    def f():
        try: 
            user = auth.get_user_by_email(email)
            #print(user.uid)
            # st.write('Login Success')


            st.session_state.username = user.uid
            st.session_state.useremail = user.email
            st.session_state.job_title = user.display_name
            st.session_state.phone = user.phone_number
            
            st.session_state.signedout = True
            st.session_state.signout = True

        except:
            st.warning('Login Failed')

    def t():
        st.session_state.signout = False
        st.session_state.signedout = False   
        st.session_state.username = ''

    if "signedout"  not in st.session_state:
        st.session_state["signedout"] = False
    if 'signout' not in st.session_state:
        st.session_state['signout'] = False


    if not st.session_state['signedout']:
        choice = st.selectbox('Login/Signup',['Login','Sign Up'])

        if choice == 'Login':
            email = st.text_input('Email Address')
            password = st.text_input('Password', type='password')

            st.button('Login', on_click=f) #when button clicked call f function

        else:
            email = st.text_input('Email Address') #anthony.p@mtjpark.com
            password = st.text_input('Password', type='password') ##anthony
            username = st.text_input('Enter your unique username') #@anthony.p
            jobtitle = st.text_input('Enter your job title') #Park management staff
            phone = st.text_input('Enter your phone number') #0912122222

            if st.button('Create my account'):
                user = auth.create_user(email=email, password=password, uid=username, display_name=jobtitle, phone_number=phone)

                st.success('Account created successfully!')
                st.markdown('Please Login using your email and password')
                st.balloons()

    if st.session_state.signout:
        # col1, col2 = st.columns(2)
        col1, col2, col3 = st.columns(3)
        with col2:
            st.image("https://raw.githubusercontent.com/MartinHeinz/MartinHeinz/master/wave.gif",width=60)
            
        with col1:
            st.header('Hello '+st.session_state.username)
            st.text_input('Username',st.session_state.username,disabled=True)
            st.text_input('Email', st.session_state.useremail, disabled=True)
            st.text_input('Position', st.session_state.job_title, disabled=True)
            st.text_input('Phone number', st.session_state.phone, disabled=True)
            # st.text('Hello👋 '+st.session_state.username)
            # st.text('Email id: '+st.session_state.useremail)
            st.button('Sign out', on_click=t)

        with col3:            
            st.write("               ")

            timezone = pytz.timezone('Asia/Bangkok')
            bkk_time = datetime.now(timezone)
            time_text = st.empty()  # Placeholder for displaying time

            # st.text(bkk_time.strftime("Date: %A, %B %d, %Y"))
            # st.text(bkk_time.strftime("Time: %H:%M:%S"))

            # @st.cache(suppress_st_warning=True)
            bkk_time = datetime.now(timezone)
            time_text.text(bkk_time.strftime("%A, %B %d, %Y\nTime: %H:%M:%S"))
            time.sleep(1)  # Update time every second

            @dataclass
            class Message:
                actor: str
                payload: str

                # def __init_subclass__(cls):
                #     st.session_state[MESSAGES] = []


                
            USER = "user"
            MESSAGES = "messages"
            
            if MESSAGES not in st.session_state:
                # st.session_state[MESSAGES] = [Message(actor=ASSISTANT, payload="Hi!How can I help you?")]
                st.session_state[MESSAGES] = [Message(actor="Anthony", payload="Pls check light in Zone A")]
                st.session_state[MESSAGES].append(Message(actor="Michelle", payload="Pls check camera in Zone B"))
                st.session_state[MESSAGES].append(Message(actor="Cole", payload="Fireworks tonight, pls adjust light to 30%"))

            emoji = ['🌳','👩‍🦱','🧔']
            i = 0
            msg: Message
            for msg in st.session_state[MESSAGES]:
                if i == 3:
                    i = 0
                if msg.actor == USER:
                    st.chat_message(msg.actor).write(msg.payload)
                else:
                    st.chat_message(msg.actor,avatar=emoji[i]).write(msg.payload)
                i+=1

            prompt: str = st.chat_input("Enter a prompt here")

            if prompt:
                st.session_state[MESSAGES].append(Message(actor=USER, payload=prompt))
                st.chat_message(USER).write(prompt)
            #     response: str = f"You wrote {prompt}"
            #     st.session_state[MESSAGES].append(Message(actor=ASSISTANT, payload=response))
            #     st.chat_message(ASSISTANT).write(response) 
            

        
