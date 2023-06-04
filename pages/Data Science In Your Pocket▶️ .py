import pandas as pd
import streamlit as st
import os

st.header('Youtube Playlists')
path = os.getcwd()+'/pdfs/youtube.csv'
df = pd.read_csv(path)
df = df.sample(frac = 1).reset_index()
x=0
html = '''<iframe id="ytplayer" type="text/html" width="75%" height="300"
src="https://www.youtube.com/embed/?listType=playlist&list={}"
frameborder="0" allowfullscreen>'''

while x<len(df):
        url = "https://www.youtube.com/playlist?list="+df.at[x,'playlist']
        st.subheader("[{}]({})".format(df.at[x,'name'],url))
        st.components.v1.html(html.format(df.at[x,'playlist']), width=800, height=300, scrolling=False)
        x+=1