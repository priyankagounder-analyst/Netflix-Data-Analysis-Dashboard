# Netflix Data Analysis & Visualization using Python and Streamlit

# Open command and run streamlit run "C:\Users\Priyanka\OneDrive\Pictures\Downloads\Projects\Python\Netflix project\app.py"


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# page config 

st.set_page_config(
    page_title= "Netflix Dashboard",
    layout="wide"
)

st.title("🎬 Netflix Data Analysis Dashboard")

# load data 

df = pd.read_csv("C:/Users/Priyanka/OneDrive/Pictures/Downloads/Projects/Python/Netflix project/archive/netflix_titles.csv")

# data cleaning 
df.drop_duplicates(inplace=True)

df['country'] = df['country'].fillna('Unknown')
df['date_added']= pd.to_datetime(
    df['date_added'],
    errors = 'coerce'
)

df['year_added'] = df['date_added'].dt.year

#sidebar filters 

st.sidebar.header("Filters")

selected_type = st.sidebar.multiselect(
    "Select Content Type",
    options=df['type'].unique(),
    default = df['type'].unique()
)


selected_year = st.sidebar.multiselect(
    "Select Year",
    options=sorted(df['year_added'].dropna().unique()),
    default=sorted(df['year_added'].dropna().unique())
)


filtered_df = df[
    (df['type'].isin(selected_type)) &
    (df['year_added'].isin(selected_year))
]



search_title = st.sidebar.text_input("Search Title")

if search_title:
    filtered_df = filtered_df[
        filtered_df['title']
        .str.contains(search_title, case=False, na=False)
    ]


# data preview

st.subheader("Dataset Preview")

st.dataframe(filtered_df.head())  

#KPI section 
movies_count = len(filtered_df[filtered_df['type']== 'Movie'])

tv_count = len(filtered_df[filtered_df['type'] == 'TV Show'])

total_titles = len(filtered_df)

col1,col2,col3 = st.columns(3)

col1.metric("Total Titles", total_titles)
col2.metric("Movies", movies_count)
col3. metric("TV Show", tv_count)


#MOVIES VS TV SHOWS 

st.subheader("Movies VS TV Show")

fig1, ax1 = plt.subplots()

sns.countplot(
    x = 'type',
    data = filtered_df,
    ax = ax1
)

st.pyplot(fig1)

# content added over years 

st.subheader("Content Added Over Years")

year_data = (
    filtered_df['year_added']
    .value_counts()
    .sort_index ()
)

fig2, ax2 = plt.subplots(figsize = (10,5))

year_data.plot (
    kind = 'line',
    marker ='o',
    ax= ax2
)

ax2.set_xlabel("Year")
ax2.set_ylabel("Number of Titles")
st.pyplot(fig2)

# top countries

st.subheader("Top 10 Countries")

top_countries =(
    filtered_df['country']
    .value_counts()
    .head(10)
)

fig3, ax3 = plt.subplots(figsize = (10,5))
top_countries.plot(
    kind = 'bar',
    ax = ax3
)

ax3.set_label("Count")

st.pyplot(fig3)
# genre popularity trend 

st.subheader("Top 15 Genres on Netflix")

genres = (
    filtered_df['listed_in']
    .str.split(',', expand=True)
    .stack()
)

genres = genres.str.strip()

top_genres = genres.value_counts().head(15)

fig4,ax4 = plt.subplots(figsize = (12,6))

sns.barplot(
    x = top_genres.values,
    y = top_genres.index,
    ax = ax4
)

ax4.set_xlabel("Count")
ax4.set_ylabel("Genre")

st.pyplot(fig4)

# rating distribution 

st.subheader("Rating Distribution")

fig5,ax5 = plt.subplots(figsize =(10,6))

sns.countplot(
    y = 'rating',
    data = filtered_df,
    order = filtered_df['rating']
    .value_counts()
    .index,
    ax= ax5
)

st.pyplot(fig5)

# insights section 

st.subheader("Key Insights")

st.markdown("""
- Movies dominate Netflix content compared to TV Shows.
- Netflix content additions increased rapidly after 2015.
- The United States contributes the highest amount of content.
- Drama and International genres are among the most popular.
- TV-MA is one of the most common content ratings.
""")

