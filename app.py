import streamlit as st
import pandas as pd

import helper
import preprocessor

import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

import plotly.figure_factory as ff

df = pd.read_csv('/home/amulya/Downloads/athlete_events.csv.zip')
region_df = pd.read_csv('/home/amulya/Downloads/noc_regions.csv')


df = preprocessor.preprocess( df , region_df)
st.sidebar.header("Olympic Analysis")
user_menu = st.sidebar.radio(
    'select an option',
    ('Medal Tally','Overall Analysis','Country-wise Analysis' )
)

if user_menu == 'Medal Tally' :
    st.sidebar.header("Medal Tally")
    years,country = helper.country_year_list(df)

    selected_year =st.sidebar.selectbox("Select Year" , years)
    selected_country = st.sidebar.selectbox("Select country", country)
    medal_tally = helper.fetch_medal_tally(df ,selected_year ,selected_country)

    if selected_country == 'Overall' and selected_year == 'Overall' :
       st.title("Overall Tally")
    elif selected_country == 'Overall' and selected_year != 'Overall':
       st.title("Medal Tally in " + str(selected_year) + " Olympics")
    elif selected_country != 'Overall' and selected_year == 'Overall':
       st.title(selected_country + " overall performance")
    elif selected_country != 'Overall' and selected_year != 'Overall' :
       st.title("Medal Tally of " + selected_country , " in " + str(selected_year))

    st.table(medal_tally)

if user_menu == 'Overall Analysis' :

        editions = df['Year'].unique().shape[0] - 1
        cities = df['City'].unique().shape[0]
        sports = df['Sport'].unique().shape[0]
        events = df['Event'].unique().shape[0]
        athletes = df['Name'].unique().shape[0]
        nations = df['region'].unique().shape[0]

        st.title("Top Statistics")
        col1,col2,col3 = st.columns(3)
        with col1 :
             st.header("Editions")
             st.title(editions)
        with col2 :
             st.header("Hosts")
             st.title(cities)
        with col3 :
             st.header("Sports")
             st.title(sports)

        col1,col2,col3 = st.columns(3)
        with col1 :
             st.header("Events")
             st.title(events)
        with col2 :
             st.header("athletes")
             st.title(athletes)
        with col3 :
             st.header("Nations")
             st.title(nations)

        nations_over_time = helper.data_over_time(df, 'region')
        fig = px.line(nations_over_time, x="Year", y="count")
        st.title("Participating Nations over the years")
        st.plotly_chart(fig)

        events_over_time = helper.events_over_time(df, 'Event')
        fig = px.line(events_over_time, x="Year", y="count")
        st.title("No. of events over the years")
        st.plotly_chart(fig)

        athlete_over_time = helper.athlete_over_time(df, 'Name')
        fig = px.line(athlete_over_time, x="Year", y="count")
        st.title("Athletes over the years")
        st.plotly_chart(fig)

        st.title("No. of events over_time(Every sport")
        fig,ax = plt.subplots(figsize = (20 ,20))
        x = df.drop_duplicates(['Year' ,'Sport','Event'])
        ax = sns.heatmap(
            x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype('int'),
            annot=True)
        st.pyplot(fig)

        st.title("Most successful Athletes")
        sport_list = df['Sport'].unique().tolist()
        sport_list.sort()
        sport_list.insert(0, 'Overall')

        selected_sport = st.selectbox('Select a Sport', sport_list)
        x = helper.most_successful(df, selected_sport)
        st.table(x)

if user_menu == 'Country-wise Analysis' :
        st.title("Country-wise Analysis")
        country_list = df['region'].dropna().unique().tolist()
        country_list.sort()

        selected_country = st.sidebar.selectbox('Select a country' , country_list)
        Medals_per_year = helper.yearwise_medal_tally(df , selected_country)
        fig = px.line(Medals_per_year, y='Medal', x='Year')
        st.title(selected_country + " Medal Tally over the years")
        st.plotly_chart(fig)

        st.title(selected_country + " excels in the following sports")

        pt = helper.country_event_heatmap(df , selected_country)
        fig ,ax =plt.subplots(figsize =(60 ,60))
        ax = sns.heatmap(pt,annot = True,annot_kws={"size": 50})
        ax.tick_params(axis='x', labelsize=50)  # Set font size for x-axis labels
        ax.tick_params(axis='y', labelsize=50)
        st.pyplot(fig)

        top10_df = helper.most_successful_countrywise(df , selected_country)
        st.title("Top 10 athletes of " + selected_country)









































































