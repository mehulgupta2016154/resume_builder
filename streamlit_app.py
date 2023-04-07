import streamlit as st 
from constant import *
import numpy as np 
import pandas as pd
from PIL import Image
from streamlit_timeline import timeline
import plotly.express as px
import plotly.figure_factory as ff
import requests
import re
import plotly.graph_objects as go
import io
import matplotlib.pyplot as plt
import streamlit.components.v1 as components
from graph_builder import *
import tensorflow as tf
from cycle import *
from vanilla_gan import return_decoder
from streamlit_player import st_player

st.set_page_config(page_title='mehul gupta\'s portfolio' ,layout="wide",page_icon='👨‍🔬')


st.sidebar.markdown(info['Stackoverflow_flair'],unsafe_allow_html=True)
st.subheader('Summary')
st.write(info['Brief'])


st.subheader('Career snapshot')


    
with st.spinner(text="Building line"):
    with open('timeline.json', "r") as f:
        data = f.read()
        timeline(data, height=500)


st.subheader('Skills & Tools ⚒️')
def skill_tab():
    rows,cols = len(info['skills'])//skill_col_size,skill_col_size
    skills = iter(info['skills'])
    if len(info['skills'])%skill_col_size!=0:
        rows+=1
    for x in range(rows):
        columns = st.columns(skill_col_size)
        for index_ in range(skill_col_size):
            try:
                columns[index_].button(next(skills))
            except:
                break
with st.spinner(text="Loading section..."):
    skill_tab()


st.subheader('Education 📖')

fig = go.Figure(data=[go.Table(
    header=dict(values=list(info['edu'].columns),
                fill_color='paleturquoise',
                align='left',height=65,font_size=20),
    cells=dict(values=info['edu'].transpose().values.tolist(),
               fill_color='lavender',
               align='left',height=40,font_size=15))])

fig.update_layout(width=750, height=400)
st.plotly_chart(fig)
st.subheader('Research Papers 📝')

def plot_bar():
    
    st.info('Comparing Brute Force approach with the algorithms')
    temp1 = rapid_metrics.loc[['Brute-Force_Printed','printed'],:].reset_index().melt(id_vars=['category'],value_vars=['precision','recall','f1_score'],var_name='metrics',value_name='%').reset_index()
    
    temp2 = rapid_metrics.loc[['Brute-Force_Handwritten','handwritten'],:].reset_index().melt(id_vars=['category'],value_vars=['precision','recall','f1_score'],var_name='metrics',value_name='%').reset_index()
    
    cols = st.columns(2)
    
    fig = px.bar(temp1, x="metrics", y="%", 
             color="category", barmode = 'group')
     
    cols[0].plotly_chart(fig,use_container_width=True)
    
    fig = px.bar(temp2, x="metrics", y="%", 
             color="category", barmode = 'group')
    cols[1].plotly_chart(fig,use_container_width=True)
    
    

def image_and_status_loader(image_list,index=0):
    if index==0:
        img = Image.open(image_list[0]['path'])
        st.image(img,caption=image_list[0]['caption'],width=image_list[0]['width'])
       
    else:
        st.success('C-Cube algorithm for printed prescriptions')
        rapid_metrics.loc[['Brute-Force_Printed','printed'],:].plot(kind='bar')
        cols = st.columns(3)
        for index_,items in enumerate(image_list[0]):
            cols[index_].image(items['path'],caption=items['caption'],use_column_width=True)
     
        
        st.success('3 step filtering algorithm for handwritten algorithms')
        cols = st.columns(3)
        for index_,items in enumerate(image_list[1]):
            cols[index_].image(items['path'],caption=items['caption'],use_column_width=True)
        
        plot_bar()
        
        

def paper_summary(index):
    st.markdown('<h5><u>'+paper_info['name'][index]+'</h5>',unsafe_allow_html=True)
    st.caption(paper_info['role'][index])
    st.caption(paper_info['journal'][index]+' , '+paper_info['publication'][index]+' , '+paper_info['year'][index])
    with st.expander('detailed description'):
        with st.spinner(text="Loading details..."):
                st.write(paper_info['Summary'][index])
                pdfFileObj = open('pdfs/{}'.format(paper_info['file'][index]), 'rb')
                image_and_status_loader(paper_info['images'][str(index)], index)
                if index==0:
                    rpa_metrics['time_improvement'] = rpa_metrics['non-ds']-rpa_metrics['ds']
                    st.markdown('**Time taken per order involving Rx in seconds** (green indicates improvements from baseline)')
                    cols = st.columns(3)
                    for index_, row in rpa_metrics.iterrows():
                        cols[index_].metric(row['category'],str(row['ds'])+'s',delta=str(round(row['time_improvement'],1))+'s' )
                st.download_button('download paper',pdfFileObj,file_name=paper_info['file'][index],mime='pdf')
    


paper_summary(0)
paper_summary(1)

st.subheader('Achievements 🥇')
achievement_list = ''.join(['<li>'+item+'</li>' for item in info['achievements']])
st.markdown('<ul>'+achievement_list+'</ul>',unsafe_allow_html=True)


st.subheader('Medium Profile ✍️')
st.markdown("""<a href={}> access full profile here</a>""".format(info['Medium']),unsafe_allow_html=True)
page1,page2 = requests.get(info['Medium']), requests.get(info['publication_url'])

followers = re.findall('(\d+\.\d+[kK]?) Followers',page1.text)[0]
following = re.findall('(\d+) Following',page1.text)[0]
pub_followers = re.findall('Followers (?:\w+\s+){4}(\d+)',re.sub('\W+',' ', page2.text ))[0]

st_player("https://www.youtube.com/watch?v=UUlWmAbA2q0")
cols = st.columns(3)
cols[0].metric('Followers',followers)
cols[1].metric('Following',following)
cols[2].metric('Publication followers',pub_followers)

with st.expander('read my latest blogs below'):
    components.html(embed_component['medium'],height=500)
        
st.subheader('Daily routine as Data Scientist')
st.graphviz_chart(graph)

st.subheader('Time for some ML')
st.caption('As training GANs is a computationally heavy task, the below 2 models have been trained just to produce acceptable results for the sake of demonstration')
        
selection = st.radio('Choose one of the two models',models)
if selection == models[0]:
    input_ = st.slider('How many random samples you wish to generate?',0,15)
    if input_:
        with st.spinner('loading random samples generated...'):
                noise = tf.random.normal((input_,4),mean=0,stddev=1)
                st.caption('random noise array generated')
                st.write(noise.numpy())
                decoder_v = return_decoder()
                images = iter(decoder_v(noise,training=False))
                row, cols = input_//4,input_%4
                if cols:
                    row+=1
                for x in range(row):
                    if (x-1)<row:
                        columns = st.columns(4)
                    else:
                        columns = st.columns(cols)
                    for index_ in range(len(columns)):
                        try:
                            img = next(images)
                        except:
                            break
                        fig,ax = plt.subplots()
                        ax.imshow(img)
                        columns[index_].pyplot(fig)
                    
elif selection==models[1]:
    selected_model = st.selectbox('select one transition',cycle_models) 
    if selected_model:
        with st.spinner('loading default sample ...'):
                    data_ = []
                    for images in cycle_model_url[selected_model]:
                            
          
                            img = Image.open(images)
                            image = img.resize((128,128))
                            data_.append(np.array(image))
                            
                    st.image(data_,caption=[x for x in range(len(data_))],width=250,clamp=True)
                    selected_images = st.multiselect('Choose images for transition',[x+1 for x in range(len(data_))])
                    if selected_images:
                        data_=[data_[int(x)-1] for x in selected_images]
                        dataset = tf.data.Dataset.from_tensor_slices({'image':data_})
                        dataset = dataset.map(preprocess).batch(n_batch).__iter__()
                        samples,_ = generate_real(next(dataset),n_batch,0)
                        if selected_model==cycle_models[0]:
                                        images,_ = generate_fake(samples, generator_B_A,n_batch,0)
                        elif selected_model==cycle_models[1]:
                                        images,_ = generate_fake(samples, generator_A_B,n_batch,0)
                        images = images.numpy()
                        st.image(images,clamp=True,width=250)

st.sidebar.caption('Wish to connect?')
st.sidebar.write('📧: mehulgupta2016154@gmail.com')
pdfFileObj = open('pdfs/mehul_gupta_resume.pdf', 'rb')
st.sidebar.download_button('download resume',pdfFileObj,file_name='mehul_gupta_resume.pdf',mime='pdf')



        

        
        
    
    
