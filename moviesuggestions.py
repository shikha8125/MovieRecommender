import pandas as pd
import numpy as np
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk

root = Tk()
root.title("Movie Recommender")
root.geometry("400x170")
root.configure(background = "#004b81")

dataframe = pd.read_csv("IMDB-Movie-Data.csv")

df = dataframe[['Title', 'Genre', 'Year', 'Rating']]
df.dropna() 
df['Year'] = df['Year'].astype(str)
df['Year'] = '(' + df['Year'] + ')'
df['Movie'] = df[['Title', 'Year']].agg(' '.join, axis=1)
df['Genre'] = df['Genre'].str.lower() 
df['Genre'] = df['Genre'].apply(lambda x: [i.strip() for i in x.split(',')])

#frame = Frame(root)
#frame.pack(pady=10)

title = Label(root, text="Movie Recommender", font=("Verdana", 16, "bold"), background = "#004b81")
title.grid(row = 0, column = 0, padx = 20, pady=20, columnspan = 2)

label = Label(root, text="Enter a Genre:", font=("Arial", 16), background = "#004b81")
label.grid(row = 1, column = 0, padx = 10)

entry = Entry(root, font=("Arial", 12), width=35)
entry.grid(row = 1, column = 1)

def recommend():
    genre = entry.get().strip().lower()
    filtered = []

    if not genre:
        messagebox.showerror("Input Error", "Please enter a genre.")
        return

    filtered = df[df['Genre'].apply(lambda x: genre in x)]
    filtered = filtered.copy()
    filtered['Genre'] = filtered['Genre'].apply(lambda lst: [g.title() for g in lst])
 
    if filtered.empty:
        messagebox.showinfo("No Results", f"No movies found in the genre '{genre}'.")
        return

    top_recs = filtered.sort_values(by='Rating', ascending=False).head(10)
    result = "\n".join(top_recs['Movie'].tolist())
    messagebox.showinfo("Top Recommendations", f"Top {genre} movies:\n\n{result}")

btn = Button(root, text="Get Recommendations", font=("Arial", 12), background="#000000", command = recommend)
btn.grid(row = 2, column = 0, columnspan = 2, pady = 20, padx = 15)

mainloop()




