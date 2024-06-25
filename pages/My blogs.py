import pandas as pd
import streamlit as st
import os
import streamlit.components.v1 as components

st.error('My debut book on Generative AI is out', icon="📕")
name="LangChain in your Pocket: Beginner's Guide to Building Generative AI Applications using LLMs"
url="https://medium.com/data-science-in-your-pocket/my-first-book-langchain-in-your-pocket-is-out-9a1f156c0f7b"
st.markdown("""<a href={}><b><u>{}</b></u></a>""".format(url,name),unsafe_allow_html=True)

st.error('My AI Podcast, AIQ is out now', icon="🎤")
name = "AIQ : Artificial Intelligence Quotient"
url = "https://www.youtube.com/watch?v=Qj_hlIRZiJg&list=PLnH2pfPCPZsIH5TUPuyu2fVbJDYjK1RVw"
components.html(f"""<a href="{url}" target="_blank"><b><u>{name}</u></b></a>""", height=30)

st.header('My Blogs')
path = os.getcwd()+'/pdfs/my_blogs.csv'
df = pd.read_csv(path)
df['category1'] = df.apply(lambda x:x['category1'].split('|'),axis=1)
df = df.explode('category1')
grouped = df.groupby(['category1']).agg(list)
grouped['total'] = grouped['url'].transform(len)
grouped.at['Other technical','total'] = 0
grouped.at['Other non technical','total'] = 0
grouped = grouped.sort_values(by='total',ascending=False)
for x,y in grouped.iterrows():
    with st.expander(x.upper()):
        blog = {a:b for a,b in zip(y['title'],y['url'])}
        for a,b in blog.items():
            st.markdown("""<a href={}><b><u>{}</b></u></a>""".format(b,a),unsafe_allow_html=True)
