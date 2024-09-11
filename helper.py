def medal_tally(df) :
    medal_tally = df.drop_duplicates(subset = ['Team', 'NOC', 'Games', 'Year', 'Season', 'City', 'Sport', 'Event', 'Medal'])
    medal_tally = medal_tally.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold', ascending = False).reset_index()
    medal_tally['Total'] = medal_tally['Gold'] + medal_tally['Silver'] + medal_tally['Bronze']

    return medal_tally

def fetch_medal_tally(df, year, country):
    medal_df = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    flag = 0
    if year == 'Overall' and country == 'Overall':

        temp_df = medal_df
    if year == 'Overall' and country != 'Overall':
        flag = 1
        temp_df = medal_df[medal_df['region'] == country]
    if year != 'Overall' and country == 'Overall':
        temp_df = medal_df[medal_df['Year'] == int(year)]
    if year != 'Overall' and country != 'Overall':
        temp_df = medal_df[(medal_df['Year'] == year) & (medal_df['region'] == country)]

    if flag == 1:
        x = temp_df.groupby('Year').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Year', ascending=True).reset_index()
    else:
        x = temp_df.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold',ascending=False).reset_index()

    return x



def country_year_list(df) :
    years = df['Year'].unique().tolist()
    years.sort()
    years.insert(0 , 'Overall')

    country = df['region'].dropna().unique().tolist()
    country.sort()
    country.insert(0, 'Overall')
    return years, country

def data_over_time(df,col):

    nations_over_time = df.drop_duplicates(['Year', col])['Year'].value_counts().reset_index().sort_values('Year')

    return nations_over_time

def events_over_time(df,col):

    events_over_time = df.drop_duplicates(['Year', col])['Year'].value_counts().reset_index().sort_values('Year')

    return events_over_time

def athlete_over_time(df,col):

    athlete_over_time = df.drop_duplicates(['Year', col])['Year'].value_counts().reset_index().sort_values('Year')

    return athlete_over_time

def most_successful(df, sport):
    # Drop rows where 'Medal' is NaN
    temp_df = df.dropna(subset=['Medal'])

    # Filter by sport if it's not 'Overall'
    if sport != 'Overall':
        temp_df = temp_df[temp_df['Sport'] == sport]

    # Count the number of medals each athlete has won
    x = temp_df['Name'].value_counts().reset_index()
    x.columns = ['Name', 'Medal_Count']  # Rename columns for clarity

    # Merge to get additional info like 'Sport' and 'region'
    x = x.merge(df[['Name', 'Sport', 'region']], on='Name', how='left').drop_duplicates('Name')

    return x.head(15)  # Return top 15 athletes

def yearwise_medal_tally(df, country) :
    temp_df = df.dropna(subset="Medal")
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'Season', 'City', 'Sport', 'Event', 'Medal'],
                            inplace=True)
    new_df = temp_df[temp_df['region'] == country]
    Medals_per_year = new_df.groupby('Year').count()['Medal'].reset_index()

    return Medals_per_year;

def country_event_heatmap(df,country) :
    temp_df = df.dropna(subset="Medal")
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'Season', 'City', 'Sport', 'Event', 'Medal'],
                            inplace=True)
    new_df = temp_df[temp_df['region'] == country]
    pt = new_df.pivot_table(index='Sport', columns='Year', values='Medal', aggfunc='count').fillna(0)
    return pt;


def most_successful_countrywise(df, country):
    # Drop rows where 'Medal' is NaN
    temp_df = df.dropna(subset=['Medal'])

    temp_df = temp_df[temp_df['region'] == country]

    # Count the number of medals each athlete has won
    x = temp_df['Name'].value_counts().reset_index()
    x.columns = ['Name', 'Medal_Count']  # Rename columns for clarity

    # Merge to get additional info like 'Sport' and 'region'
    x = x.merge(df[['Name', 'Sport']], on='Name', how='left').drop_duplicates('Name')

    return x.head(15)









