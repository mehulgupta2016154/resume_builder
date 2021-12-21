import pandas as pd
import graphviz as graphviz

edu = [['B.Tech','CSE','2020','IIIT Jabalpur','8.1 CGPA'],['12th','Science','2016','Bhavan\'s KDKVM', '94.2%'],['10th','-','2012','Bhavan\'s KDKVM','10 CGPA']]

info = {'name':'Mehul Gupta', 'Brief':'Data Scientist eager to learning new things. Right Now: Streamlit !!','photo':{'path':'abc.jpg','width':150}, 'Mobile':'8103795345','Email':'mehulgupta2016154@gmail.com','Medium':'https://medium.com/@mehulgupta_7991/about','City':'Nagda, Madhya Pradesh','Stackoverflow_flair':'''<a href="https://stackoverflow.com/users/8422170/mehul-gupta"><img src="https://stackoverflow.com/users/flair/8422170.png?theme=clean" width="250" height="70"  alt="profile for Mehul Gupta at Stack Overflow, Q&amp;A for professional and enthusiast programmers" title="profile for Mehul Gupta at Stack Overflow, Q&amp;A for professional and enthusiast programmers"></a>''','edu':pd.DataFrame(edu,columns=['Qualification','Stream','Year','Institute','Score']),'skills':['Data Science','RDBMS','Cassandra','AWS Athena','Snowflake','Comet-ML','Python','Java','C++','Airflow','AWS S3','Tableau','Metabase'],'achievements':['Top AI writer @ Medium','1.3k+ reputation points on Stackoverflow','TCS humAIn Finalist,2019','25 Kaggle medals','Shikshan Bharati Kulapati K.M. Munshi Award in Mathematics,2014','Bharatiya Vidya Bhavan Shri C. Subramaniam Award for excellence in character, 2009 & 2012','Certificate of Merit(Proficiency in Co-curricular activities) for Declamation and Extempore'],'publication_url':'https://medium.com/data-science-in-your-pocket/tagged/beginner'}

paper_info = {'name':['Attended RPA of prescriptions','Algorithms for rapid digitalization of prescriptions'],'year':['2021','2021'],'role':['Co-Author','Author'],'Summary':['Around prescription digitization pipeline currently deployed at Tata 1mg for easing out on human verification of prescriptions that include a suite of Data Science models','About a couple of algorithms devised to extract medicine names from handwritten & printed prescription images'],'file':['attented_rpa_of_prescriptions.pdf','algorithms_for_rapid_digitzation_of_prescriptions.pdf'],'images':{'0':[{'path':'rpa1.png','caption':'Digitization pipeline','width':600}],'1':[[{'path':'pr1.png','caption':'Capture seed words'},{'path':'pr2.png','caption':'cluster words using seed words'},{'path':'pr3.png','caption':'clean junk words'}],[{'path':'hw1.png','caption':'Filter 1'},{'path':'hw2.png','caption':'Filter 2'},{'path':'hw3.png','caption':'Filter 3'}]]}}

models = ('Random array to image creation','Cycle GAN for season change')
cycle_models = ('Winter to Summer','Summer to Winter')
cycle_model_url = {cycle_models[0]:['https://wallpaperaccess.com/full/903536.jpg','https://i.ytimg.com/vi/jOf3cip4vZU/maxresdefault.jpg','https://images.unsplash.com/photo-1486140525285-12e658d9ac0f?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxzZWFyY2h8MXx8d2ludGVyJTIwc2NlbmV8ZW58MHx8MHx8&w=1000&q=80','https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTukGoWlxM_lgs47YrjorsMnXzKPrybzqhaRw&usqp=CAU'],cycle_models[1]:['https://wallpaperaccess.com/full/2559948.jpg','https://image.shutterstock.com/image-photo/summer-field-landscape-yellow-flower-260nw-623155247.jpg','https://thumbs.dreamstime.com/b/summer-scenery-5822122.jpg','https://c4.wallpaperflare.com/wallpaper/690/223/700/dream-of-summer-scenery-wallpaper-preview.jpg']}

rpa_metrics = pd.DataFrame([['Overall',66.4, 72.5],['printed rx',54.6, 64.6],['handwritten',67.3,73.3]], columns=['category','ds','non-ds'])
rapid_metrics = pd.DataFrame([['printed',91.6,70,79.4],['handwritten',21.1,34.7,26.2],['Brute-Force_Printed',29.9,82.7,41.8],['Brute-Force_Handwritten',0.2,62,0.3]],columns=['category','precision','recall','f1_score'])
rapid_metrics = rapid_metrics.set_index(['category'])

skill_col_size = 5
embed_component= {'linkedin':"""<script src="https://platform.linkedin.com/badges/js/profile.js" async defer type="text/javascript"></script>
        <div class="badge-base LI-profile-badge" data-locale="en_US" data-size="medium" data-theme="light" data-type="VERTICAL" data-vanity="mehulgupta7991" data-version="v1"><a class="badge-base__link LI-simple-link" href="https://in.linkedin.com/in/mehulgupta7991?trk=profile-badge"></a></div>""", 'medium':"""<div id="medium-widget"></div>
            <script src="https://medium-widget.pixelpoint.io/widget.js"></script>
            <script>MediumWidget.Init({renderTo: '#medium-widget', params: {"resource":"https://medium.com/data-science-in-your-pocket","postsPerLine":3,"limit":9,"picture":"big","fields":["description","claps","likes","publishAt"],"ratio":"landscape"}})</script>"""}



