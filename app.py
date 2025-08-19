import streamlit as st
import pandas as pd
import pickle

st.set_page_config(page_title="🎬 Movie Recommender", layout="wide")
st.title("🎬 Movie Recommender")

@st.cache_data
def load_movies():
    movies = pd.read_csv('movies.csv')
    return movies

movies = load_movies()

@st.cache_resource
def load_similarities():
    with open("rating_sim.pkl", "rb") as f:
        rating_sim = pickle.load(f)
    with open("genre_sim.pkl", "rb") as f:
        genre_sim_df = pickle.load(f)
    return rating_sim, genre_sim_df

rating_sim, genre_sim_df = load_similarities()

def combined_similarity(movie_id, genre_weight, top_k=50):
    combined = (1 - genre_weight) * rating_sim[movie_id] + genre_weight * genre_sim_df[movie_id]
    combined = combined.drop(movie_id).sort_values(ascending=False).head(top_k)
    return combined

def recommend_movies(movie_title, top_n=5, genre_weight=0.3):
    if movie_title not in movies['title'].values:
        return pd.DataFrame(columns=['title', 'genres', 'score'])
    
    movie_id = movies.loc[movies['title'] == movie_title, 'movieId'].values[0]
    top_scores = combined_similarity(movie_id, genre_weight, top_k=top_n)
    recs = movies[movies['movieId'].isin(top_scores.index)][['movieId','title','genres']]
    recs = recs.merge(top_scores.rename("score"), left_on="movieId", right_index=True)
    recs = recs.sort_values("score", ascending=False)
    return recs

movie_choice = st.selectbox("🎥 Select a movie:", movies['title'].tolist())
num_recs = st.slider("📌 Number of recommendations:", min_value=1, max_value=10, value=5)
genre_weight = st.slider("🎭 Genre influence (0 = ignore, 1 = only genre):", min_value=0.0, max_value=1.0, value=0.3)

if st.button("Get Recommendations"):
    recommendations = recommend_movies(movie_choice, num_recs, genre_weight)
    if recommendations.empty:
        st.info("No recommendations found.")
    else:
        st.subheader(f"Movies similar to **{movie_choice}**:")

        cols = st.columns(min(num_recs, 5)) 
        for i, row in enumerate(recommendations.itertuples()):
            col = cols[i % len(cols)]
            with col:
                with st.container(border=True):
                    st.write(f"**{row.title}**")
                    st.caption(row.genres)
                    st.metric(label="Similarity", value=f"{row.score * 100:.2f}%")

