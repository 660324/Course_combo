import pandas as pd
import streamlit as st
import requests
import io
pd.set_option('display.max_columns', None)
from PIL import Image

# original_df = pd.read_excel('C:/Users/yuhao1/Desktop/Course combo/from power bi.xlsx')
# original_df.to_pickle("C:/Users/yuhao1/Desktop/Course combo/powerbi.pkl")
#df=pd.read_pickle("C:/Users/yuhao1/Desktop/Course combo/python.pkl")
# df=pd.read_pickle("C:/Users/yuhao1/Desktop/Course combo/powerbi.pkl")
# print (df)
#streamlit run "C:\Users\yuhao1\Desktop\Course combo\best_comb_new.py"

# @st.cache
# def get_course():
#     return pd.read_excel('C:/Users/yuhao1/Desktop/Course combo/python.pkl')
# df = get_course()


st.header('Course Recommendation Tool')

text_input_container = st.empty()
password = text_input_container.text_input("Enter Password")
if password!='12345':
    st.write('Wrong Password')
else:
    text_input_container.empty()
    st.info('Welcome Memeber '+password)

    response = requests.get('https://github.com/660324/Course_combo/blob/main/logo.png?raw=true')
    logo = io.BytesIO(response.content)
    #logo = Image.open('C:/Users/yuhao1/Desktop/Course combo/logo.png')
    st.sidebar.image(logo)
    st.sidebar.text("")
    st.sidebar.text('Select Student Features (Optional)')
    Gender=st.sidebar.multiselect('Gender', ['F', 'M'], default=None)
    Race=st.sidebar.multiselect('Race', ['AMERIND','ASIAN','BLACK','HAWPACI','HISPANIC','MULTIRAC','NOTSPEC','WHITE'], default=None)
    Residency=st.sidebar.multiselect('Residency', ['IS', 'OS'], default=None)
    Fulltime=st.sidebar.multiselect('Full-time Status', ['FT', 'PT'], default=None)
    Firsttime=st.sidebar.multiselect('First-time Freshman', ['Yes', 'No'], default=None)
    Firsttrans=st.sidebar.multiselect('First-time Transfer', ['Yes', 'No'], default=None)
    Firstgen=st.sidebar.multiselect('First Generation', ['Y', 'N'], default=None)
    International=st.sidebar.multiselect('International', ['International', 'Non_International'], default=None)
    College=st.sidebar.multiselect('College', ['AG','AR','AS','BA', 'ED', 'EN', 'HE','TC', 'UG'], default=None)
    AcadLevel=st.sidebar.multiselect('Academic Level', ['Freshman','Sophomore','Junior','Senior', 'Special Undergraduate', 'Non Degree Undergraduate',
                                                'High School','Unknown'], default=None)

       #st.write(Gender)


    @st.cache(allow_output_mutation=True)
    def get_course():
        url = 'https://github.com/660324/Course_combo/blob/main/powerbi1.pkl?raw=true'
        df = pd.read_pickle(url)
        #df=pd.read_pickle("C:/Users/yuhao1/Desktop/Course combo/powerbi.pkl")
        df['Course'] = df['Subject'] + df['CatalogNumber'].astype(str)
        return df

    course_grade=get_course()
    course = course_grade['Course'].sort_values(ascending=True).drop_duplicates()


    make_choice = st.multiselect('Select your course:', course, default=None, help='Select as many courses as you need')

    select_term = st.select_slider('Based on terms between:', options=['spring2017','fall2017','spring2018','fall2018'
        ,'spring2019','fall2019','spring2020','fall2020','spring2021','fall2021'],value=('spring2017', 'fall2021'))



    if not make_choice: #need to add if condition because it's very slow if no course is selected
        st.write("Please select at least one course")


    if len(make_choice)>0:

        st.text('')
        st.text('Table1: Most frequent course combinations that include the course(s) you selected')
        st.caption('*Click headers to sort table')

        st.text('')
        st.text('')
        st.text('Table2: Most frequent single courses that are taken together with the course(s) you selected')

        st.text('')
        st.text('')
        st.text('Table3: Students performance in the course(s) you selected')

        st.text('')
        st.text('')
        st.text('Table 4: Most frequent two courses that are taken together with the course(s) you selected')
        st.caption('*Click headers to sort table')
