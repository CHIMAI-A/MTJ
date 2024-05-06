import streamlit as st

from streamlit_option_menu import option_menu

import account, dashboard

st.set_page_config(layout='centered',
    page_title="MTJ Park Management🌳",
)

class MultiApp:

    def __init__(self):
        self.apps = []
    
    def add_app(self, title, function):
        self.apps.append({
            'title': title,
            'function': function
        })

    def run():
        with st.sidebar:
            app = option_menu( 
                menu_title='MTJ Park',
                options=['Account','Dashboard'],
                icons=['person-circle','clipboard-data'],
                menu_icon='tree-fill',
                default_index=1,
                styles={
                    "container":{"padding": "5!important","background-color":'white'},
                    "icon":{"color":"black","font-size":"23px"},
                    "nav-link":{"color":"black","font-size":"20px","text-align":"left","margin":"0px","--hover-color":"#b8f5b3"},
                    "nav-link-selected":{"background-color":"#29eb17"},
                }
            )

        if app=="Account":
            account.app()
        if app=="Dashboard":
            dashboard.app()
    
    run()

            