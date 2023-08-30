import pickle,os
import streamlit as st
import requests
import pandas as pd
from PIL import Image

# st.set_page_config(layout="wide")
# import streamlit as st
# st.write('<style>div.block-container{padding-top:0rem;}</style>', unsafe_allow_html=True)

css='''
<style>
    section.main > div {max-width:70rem}
    div.block-container{padding-top:2rem;}
</style>
'''
st.markdown(css, unsafe_allow_html=True)

# recomendation
def fetchPoster(movie_id):
    path = "posters/"+str(movie_id)+".jpg"
    directory_path='posters/'
    file_name = str(movie_id)+".jpg"
    if os.path.exists(os.path.join(directory_path, file_name)):
        file_path = os.path.join(directory_path, file_name)
        image = Image.open(path)
        return image
    else:
        return Image.open('posters/default-movie-poster.jpg')

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        # fetch the movie poster
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetchPoster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)
    return recommended_movie_names,recommended_movie_posters

similarity = pickle.load(open('similarity.pkl','rb'))    
    
movies = pd.read_csv('movie_list.csv')
movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)


# based on user's history
user_data = pd.read_csv("user_data.csv")
def userWatchHistory(movie, cols):
    recommended_movie_user = []
    recommended_movie_user_posters = []
    for col,mov in zip(cols, movie):
        index = user_data[user_data[col] == mov].index[0]
        distances = sorted(list(enumerate(user_history_similarity[index])),reverse=True,key = lambda x: x[1])
        for i in distances[1:6]:
            recommended_movie_user.append(movies.iloc[i[0]].title)
            # recommended_movie_user_posters.append(fetch_poster(movies.iloc[i[0]].movie_id))
            recommended_movie_user_posters.append(fetchPoster(movies.iloc[i[0]].movie_id))
#             print(user_data.iloc[i[0]].watch_history1,user_data.iloc[i[0]].watch_history2,user_data.iloc[i[0]].watch_history3)
    return recommended_movie_user,recommended_movie_user_posters

user_history_similarity = pickle.load(open('user_history_similarity.pkl','rb'))
user_list = user_data['user_id'].values
select_user = st.selectbox(
    "select user's ID",
    user_list
)
user_data1 = user_data.set_index('user_id')
mov1 = user_data1.loc[select_user,'watch_history1']
mov2 = user_data1.loc[select_user,'watch_history2']
mov3 = user_data1.loc[select_user,'watch_history3']
recommended_movie_user,recommended_movie_user_posters = userWatchHistory([mov1, mov2,mov3],['watch_history1','watch_history2','watch_history3'])

# top genres
top_gnr = pd.read_csv("top_genres.csv").head(5)
top_gnr.drop("Unnamed: 0", inplace=True, axis=1)
top_gnr_poster_list = []
top_gnr_title_list = []
for i in range(len(top_gnr)):
    top_gnr_poster_list.append(fetchPoster(top_gnr.iloc[i]['movie_id']))
    top_gnr_title_list.append(top_gnr.iloc[i]['title'])

# top trending movies
top_mov = pd.read_csv("top_trend_mov.csv")
top_mov_poster_list = []
top_mov_title_list = []
for i in range(5):
    top_mov_poster_list.append(fetchPoster(top_mov.iloc[i]['movie_id']))
    top_mov_title_list.append(top_mov.iloc[i]['title'])



# webpage 
if st.button('Show Recommendation'):
    recommended_movie_names,recommended_movie_posters = recommend(selected_movie)
    searched_movie_id = movies[movies['title'] == selected_movie]['movie_id'].values[0]
    searched_movie_poster = fetchPoster(searched_movie_id)
    st.subheader(
    "Results based on search"
    )
       
    st.image(searched_movie_poster, caption=selected_movie,width=220)
    st.subheader(
    "Recomendation similar to {}".format(selected_movie)
    )
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        # image = Image.open('posters/10733.jpg')
        # st.image(image, caption='Sunrise by the mountains')
        st.image(recommended_movie_posters[0],caption=recommended_movie_names[0])
    with col2:
        st.image(recommended_movie_posters[1],caption=recommended_movie_names[1])
    with col3:
        st.image(recommended_movie_posters[2],caption=recommended_movie_names[2])
    with col4:
        st.image(recommended_movie_posters[3],caption=recommended_movie_names[3])
    with col5:
        st.image(recommended_movie_posters[4],caption=recommended_movie_names[4])

    st.subheader(
        "For you:"
    )

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        # image = Image.open('posters/10733.jpg')
        # st.image(image, caption='Sunrise by the mountains')
        st.image(recommended_movie_user_posters[0],caption=recommended_movie_user[0])
    with col2:
        st.image(recommended_movie_user_posters[1],caption=recommended_movie_user[1])

    with col3:
        st.image(recommended_movie_user_posters[2],caption=recommended_movie_user[2])
    with col4:
        st.image(recommended_movie_user_posters[3],caption=recommended_movie_user[3])
    with col5:
        st.image(recommended_movie_user_posters[4],caption=recommended_movie_user[4])


    st.subheader(
        "Recomendation based on Top Genres!"
    )

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.image(top_gnr_poster_list[0],caption=top_gnr_title_list[0])
    with col2:
        st.image(top_gnr_poster_list[1],caption=top_gnr_title_list[1])
    with col3:
        st.image(top_gnr_poster_list[2],caption=top_gnr_title_list[2])
    with col4:
        st.image(top_gnr_poster_list[3],caption=top_gnr_title_list[3])
    with col5:
        st.image(top_gnr_poster_list[4],caption=top_gnr_title_list[4])

    st.subheader(
        "Top Trending:"
    )

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.image(top_mov_poster_list[0],caption=top_mov_title_list[0])
    with col2:
        st.image(top_mov_poster_list[1],caption=top_mov_title_list[1])
    with col3:
        st.image(top_mov_poster_list[2],caption=top_mov_title_list[2])
    with col4:
        st.image(top_mov_poster_list[3],caption=top_mov_title_list[3])
    with col5:
        st.image(top_mov_poster_list[4],caption=top_mov_title_list[4])