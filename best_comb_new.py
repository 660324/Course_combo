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

    #handle no selection situtation as default above is none
    if not Gender:
        Gender=['F', 'M']
    if not Race:
        Race=['AMERIND','ASIAN','BLACK','HAWPACI','HISPANIC','MULTIRAC','NOTSPEC','WHITE']
    if not Residency:
        Residency=['IS', 'OS']
    if not Fulltime:
        Fulltime=['FT', 'PT']
    if not Firstgen:
        Firstgen=['Y', 'N']
    if not College:
        College=['AG','AR','AS','BA', 'ED', 'EN','HE','TC', 'UG']
    if not Firsttime:
        Firsttime=['Yes', 'No']
    if not Firsttrans:
        Firsttrans=['Yes', 'No']
    if not International:
        International=['International', 'Non_International']
    if not AcadLevel:
        AcadLevel= ['Freshman','Sophomore','Junior','Senior', 'Special Undergraduate', 'Non Degree Undergraduate', 'High School','Unknown']
    #st.write(Gender)


    @st.cache(allow_output_mutation=True)
    def get_course():
        url = 'https://github.com/660324/Course_combo/blob/main/powerbi.pkl?raw=true'
        df = pd.read_pickle(url)
        #df=pd.read_pickle("C:/Users/yuhao1/Desktop/Course combo/powerbi.pkl")
        df['Course'] = df['Subject'] + df['CatalogNumber'].astype(str)
        return df

    course_grade=get_course()
    course = course_grade['Course'].sort_values(ascending=True).drop_duplicates()


    make_choice = st.multiselect('Select your course:', course, default=None, help='Select as many courses as you need')

    select_term = st.select_slider('Based on terms between:', options=['spring2017','fall2017','spring2018','fall2018'
        ,'spring2019','fall2019','spring2020','fall2020','spring2021','fall2021'],value=('spring2017', 'fall2021'))
    select_term = list(select_term)
    for i in (0,1):
        if select_term[i]=='spring2017':
            select_term[i]=2172
        if select_term[i]=='fall2017':
            select_term[i]=2175
        if select_term[i]=='spring2018':
            select_term[i]=2182
        if select_term[i]=='fall2018':
            select_term[i]=2185
        if select_term[i]=='spring2019':
            select_term[i]=2192
        if select_term[i]=='fall2019':
            select_term[i]=2195
        if select_term[i]=='spring2020':
            select_term[i]=2202
        if select_term[i]=='fall2020':
            select_term[i]=2205
        if select_term[i]=='spring2021':
            select_term[i]=2212
        if select_term[i]=='fall2021':
            select_term[i]=2215

    @st.cache()
    def get_data():
        url = 'https://github.com/660324/Course_combo/blob/main/python.pkl?raw=true'
        result = pd.read_pickle(url)
        #result=pd.read_pickle("C:/Users/yuhao1/Desktop/Course combo/python.pkl")
        if not make_choice:  # need to add if condition because it's very slow if no course is selected
            result=pd.DataFrame()
        else:
            result = result[(result['Gender'].isin(Gender)) & (result['Ethnicity'].isin(Race)) & (result['Residency'].isin(Residency))
                            & (result['FullPartTime'].isin(Fulltime)) & (result['First-time Freshman'].isin(Firsttime))
                            & (result['FirstGen'].isin(Firstgen)) & (result['First-time Transfer'].isin(Firsttrans))
                            & (result['AcadLevelDescription'].isin(AcadLevel)) & (result['international'].isin(International))
                            & (result['College'].isin(College)) & (result['Term']>=select_term[0]) & (result['Term']<=select_term[1])]
            result = result[result['Course'].apply(lambda x: all(word in x for word in make_choice))]
        return result
    result=get_data()




    if not make_choice: #need to add if condition because it's very slow if no course is selected
        st.write("Please select at least one course")

    if len(make_choice)>0 and result.empty:
        st.write("No student meeting this criteria took this course(s) in the past")

    if len(make_choice)>0 and not result.empty:
        output1 = result.groupby('Course', as_index=False).agg(
            Takings=('Course', 'count'),
            Mean_GPA_in_semester=('GPA_1', 'mean'),
            Counts=('Number', 'max'))

        output1=output1.sort_values(by=['Takings','Mean_GPA_in_semester'], ascending=[False, False])

        st.text('')
        st.text('Most frequent course combinations that include the course(s) you selected')
        st.caption('*Click headers to sort table')
        st._legacy_dataframe(output1)


        course_comb=[]
        for row in result['Course']:
            row_li=row.split (' ')
            row_li=[e for e in row_li if e not in make_choice]
            course_comb.append(row_li)



        import itertools
        import collections

        counts = collections.defaultdict(int)
        for collab in course_comb:
            collab.sort()
            for pair in itertools.combinations(collab, 1):
                counts[pair] = counts[pair]+1

        data1 = []

        for pair, freq in counts.items():
            course=' '.join (pair)
            count=freq
            mean_GPA_in_semester=result.loc[result['Course'].apply(lambda x: all(word in x for word in pair)),'GPA_1'].mean()
            data1.append([course, count, mean_GPA_in_semester])

        additional1 = pd.DataFrame(data1, columns=['Course','Count','Mean_GPA_in_semester'])
        additional1=additional1.sort_values(by=['Count','Mean_GPA_in_semester'], ascending=[False, False])

        course_grade = course_grade[(course_grade['Gender'].isin(Gender)) & (course_grade['Ethnicity'].isin(Race)) & (course_grade['Residency'].isin(Residency))
            & (course_grade['FullPartTime'].isin(Fulltime)) & (course_grade['First-time Freshman'].isin(Firsttime))
            & (course_grade['FirstGen'].isin(Firstgen)) & (course_grade['First-time Transfer'].isin(Firsttrans))
            & (course_grade['AcadLevelDescription'].isin(AcadLevel)) & (course_grade['international'].isin(International))
            & (course_grade['College'].isin(College)) & (course_grade['Term']<=select_term[1]) & (course_grade['Term']>=select_term[0])]

        course_grade['DFW'] = 0
        course_grade.loc[course_grade['Grade'].isin (['D', 'F', 'W']), 'DFW'] = 1
        course_grade = course_grade[['Course', 'GradePoints', 'DFW']].groupby('Course', as_index=False).agg\
            (Mean_grade_of_this_course=('GradePoints', 'mean'),DFW=('DFW', 'mean'))
        course_grade['DFW'] = course_grade['DFW'].astype(float).map("{:.2%}".format)

        additional1 = pd.merge(additional1, course_grade, how='left', left_on=['Course'], right_on=['Course'])

        st.text('')
        st.text('')
        st.text('Most frequent single courses that are taken together with the course(s) you selected')
        st.caption('*Click headers to sort table')
        st._legacy_dataframe(additional1)

        st.text('Students performance in the course(s) you selected')
        course_grade_selected = course_grade[course_grade['Course'].isin(make_choice)]
        st._legacy_dataframe(course_grade_selected)



        counts = collections.defaultdict(int)
        for collab in course_comb:
            collab.sort()
            for pair in itertools.combinations(collab, 2):
                #         print (pair)
                counts[pair] = counts[pair] + 1
        # print (counts[pair])

        data2 = []

        for pair, freq in counts.items():
            course = ' '.join(pair)
            count = freq
            mean_GPA_in_semester = result.loc[result['Course'].apply(lambda x: all(word in x for word in pair)), 'GPA_1'].mean()
            data2.append([course, count, mean_GPA_in_semester])

        additional2 = pd.DataFrame(data2, columns=['Course', 'Count', 'Mean_GPA_in_semester'])
        additional2 = additional2.sort_values(by=['Count', 'Mean_GPA_in_semester'], ascending=[False, False])

        st.text('')
        st.text('')
        st.text('Most frequent two courses that are taken together with the course(s) you selected')
        st.caption('*Click headers to sort table')
        st._legacy_dataframe(additional2)

