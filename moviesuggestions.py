import pandas as pd
from tkinter import *
from tkinter import messagebox

# =================== ROOT WINDOW =================== #
root = Tk()
root.title("Movie Recommender")
root.geometry("400x170")
root.configure(background="#004b81")

# =================== LOAD DATA =================== #
dataframe = pd.read_csv("IMDB-Movie-Data.csv")

# Select relevant columns and drop missing values
df = dataframe[['Title', 'Genre', 'Year', 'Rating']].dropna().copy()

# Format Year and Movie columns
df['Year'] = df['Year'].astype(str)
df['Year'] = '(' + df['Year'] + ')'
df['Movie'] = df[['Title', 'Year']].agg(' '.join, axis=1)

# Clean Genre column
df['Genre'] = df['Genre'].str.lower()
df['Genre'] = df['Genre'].apply(lambda x: [i.strip() for i in x.split(',')])

# =================== GUI ELEMENTS =================== #
title = Label(root, text="Movie Recommender", font=("Verdana", 16, "bold"), background="#004b81", fg="white")
title.grid(row=0, column=0, padx=20, pady=20, columnspan=2)

label = Label(root, text="Enter a Genre:", font=("Arial", 16), background="#004b81", fg="white")
label.grid(row=1, column=0, padx=10)

entry = Entry(root, font=("Arial", 12), width=35)
entry.grid(row=1, column=1)

# =================== RECOMMENDATION FUNCTION =================== #
def recommend():
    genre = entry.get().strip().lower()

    if not genre:
        messagebox.showerror("Input Error", "Please enter a genre.")
        return

    # Filter movies by genre
    filtered = df[df['Genre'].apply(lambda x: genre in x)].copy()
    
    if filtered.empty:
        messagebox.showinfo("No Results", f"No movies found in the genre '{genre}'.")
        return

    # Capitalize genre names for display
    filtered['Genre'] = filtered['Genre'].apply(lambda lst: [g.title() for g in lst])

    # Get top 10 movies by rating
    top_recs = filtered.sort_values(by='Rating', ascending=False).head(10)
    result = "\n".join(top_recs['Movie'].tolist())

    messagebox.showinfo("Top Recommendations", f"Top {genre.title()} movies:\n\n{result}")

# =================== BUTTON =================== #
btn = Button(root, text="Get Recommendations", font=("Arial", 12), background="#000000", fg="white", command=recommend)
btn.grid(row=2, column=0, columnspan=2, pady=20, padx=15)

# =================== MAIN LOOP =================== #
root.mainloop()









