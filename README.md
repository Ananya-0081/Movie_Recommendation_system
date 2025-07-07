# 🎬 Movie Recommendation System

This is a netflix theme based **Movie Recommendation System** built using **Machine Learning** and **Streamlit**. The system recommends similar movies based on the selected movie title using precomputed similarity scores.

## 🚀 Features

- ✅ Content-Based Filtering using movie metadata
- ✅ Top 5 movie recommendations
- ✅ Movie poster display using **TMDB API**
- ✅ Interactive user interface built with **Streamlit**

---

## 📂 Project Structure
-app.py            # Streamlit app
-movie.pkl         # Movie titles list
-movie_dict.pkl   # Movie metadata dictionary
-simiilarity.pkl  # Cosine similarity matrix


---

## 🔧 How It Works

1. The app loads precomputed **cosine similarity** between movies from `.pkl` files.
2. Users select a movie title from the dropdown.
3. The system displays the top 5 similar movies along with posters fetched from **TMDB API**.

---

## 📊 Example Output
For the input:

> Harry Potter and the Half-Blood Prince

The system suggests:

-Harry Potter and the Order of the Phoenix
-Harry Potter and the Goblet of Fire
-Harry Potter and the Chamber of Secrets
-Harry Potter and the Philosopher's Stone
-Harry Potter and the Prisoner of Azkaban

## 📸 Preview of the Movie Recommendation 

![Screenshot 2025-07-07 123629](https://github.com/user-attachments/assets/35fbe3d1-91be-4488-9f70-bfa74a1dfb6d)


