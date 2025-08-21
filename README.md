# 🎬 Movie Recommendation System  

A personalized **movie recommender system** built using the [MovieLens dataset](https://www.kaggle.com/datasets/shubhammehta21/movie-lens-small-latest-dataset).  
The system recommends movies based on **item-item collaborative filtering** with an optional **genre influence filter**.  

## 🍿 Live Demo
Deployed as an interactive **Streamlit app** where users can select a movie and instantly see recommendations.  
Try the app 👉[here](https://tar-movie-recommendation-system.streamlit.app/)👈


## ✨ Features
- **Item-based collaborative filtering** using cosine similarity.  
- **Optional genre influence** (0 = ignore, 1 = only show same-genre movies).  
- Fast recommendations by **precomputing similarity matrices**.  
- Clean, interactive Streamlit UI.  


## 📂 Dataset
I use the **MovieLens small latest dataset** which contains:
- `movies.csv` – movie titles and genres  
- `ratings.csv` – user ratings  
