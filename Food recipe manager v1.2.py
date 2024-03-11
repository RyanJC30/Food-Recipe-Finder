import tkinter as tk
from tkinter import messagebox
import os
import sys

def show_ingredient_menu():
    # Create a Toplevel window for ingredient selection
    ingredient_window = tk.Toplevel(root)
    ingredient_window.title("Select Ingredient")

    # Create a Listbox for ingredient selection
    ingredient_listbox = tk.Listbox(ingredient_window, selectmode=tk.MULTIPLE)
    ingredient_listbox.pack(padx=10, pady=10)

    # Insert ingredients into the Listbox in alphabetical order
    for ingredient in sorted(all_ingredients, key=str.lower):
        ingredient_listbox.insert(tk.END, ingredient)

    # Button to confirm ingredient selection
    confirm_button = tk.Button(ingredient_window, text="Confirm", command=lambda: on_ingredient_confirm(ingredient_listbox))
    confirm_button.pack(pady=10)

def on_ingredient_confirm(listbox):
    selected_ingredients = listbox.curselection()

    if not selected_ingredients:
        messagebox.showinfo("Error", "Please select at least one ingredient.")
        return

    # Get the selected ingredients and update the entry widget
    selected_ingredients_list = [listbox.get(idx) for idx in selected_ingredients]
    ingredient_entry.delete(0, tk.END)
    ingredient_entry.insert(0, ', '.join(selected_ingredients_list))

    # Close the ingredient selection window
    listbox.master.destroy()

def show_recipes():
    # Clear any previous results
    recipe_display.delete(1.0, tk.END)

    # Call the appropriate function based on the user's initial selection
    selection = menu_var.get()
    if selection == 1:
        find_recipes_by_ingredient()
    elif selection == 2:
        find_recipes_by_all_ingredients()

def find_recipes_by_ingredient():
    user_ingredient = ingredient_entry.get().lower()  # Convert to lowercase
    ingredient_found = False

    recipes_file_path = os.path.join(os.path.dirname(sys.argv[0]), 'recipes.txt')

    with open(recipes_file_path, 'r') as recipe_file:
        for line in recipe_file:
            line = line.strip()
            recipe_name, *recipe_ingredients = map(str.strip, line.split(","))

            # Convert recipe ingredients to lowercase for case-insensitive comparison
            recipe_ingredients_lower = [ingredient.lower() for ingredient in recipe_ingredients]

            if user_ingredient in recipe_ingredients_lower:
                if not ingredient_found:
                    recipe_display.insert(tk.END, f"Recipes with the ingredient {user_ingredient}:\n\n")
                    ingredient_found = True
                recipe_display.insert(tk.END, f"{recipe_name}: {', '.join(recipe_ingredients)}\n")

    if not ingredient_found:
        recipe_display.insert(tk.END, "Ingredient not found in recipes")

def find_recipes_by_all_ingredients():
    user_ingredient_list = ingredient_entry.get().lower().split(',')
    user_ingredient_list = [ingredient.strip() for ingredient in user_ingredient_list if ingredient.strip()]

    recipes_file_path = os.path.join(os.path.dirname(sys.argv[0]), 'recipes.txt')

    with open(recipes_file_path, 'r') as recipe_file:
        for line in recipe_file:
            line = line.strip()
            recipe_name, *recipe_ingredients = map(str.strip, line.split(","))
            
            # Convert recipe ingredients to lowercase for case-insensitive comparison
            recipe_ingredients_lower = [ingredient.lower() for ingredient in recipe_ingredients]

            user_ingredient_count = sum(1 for item in user_ingredient_list if item in recipe_ingredients_lower)
            recipe_ingredient_count = len(recipe_ingredients_lower)

            if user_ingredient_count == recipe_ingredient_count:
                recipe_display.insert(tk.END, f"{recipe_name}: {', '.join(recipe_ingredients)}\n")

# Determine the path of the 'recipes.txt' file
recipes_file_path = os.path.join(os.path.dirname(sys.argv[0]), 'recipes.txt')

# Read ingredients from 'recipes.txt' file and convert to lowercase
with open(recipes_file_path, 'r') as recipe_file:
    all_ingredients = set(ingredient.strip() for line in recipe_file for ingredient in line.split(',')[1:])

# Create the main window
root = tk.Tk()
root.title("Food Recipe Manager")

# Create and set up the widgets
menu_var = tk.IntVar()
menu_var.set(0)

menu_label = tk.Label(root, text="Please choose an option from the menu:")
menu_label.pack()

menu_options = [("Find recipes with 1 main ingredient", 1),
                ("Find recipes using all ingredients you have", 2),
                ("Exit", 3)]

for text, value in menu_options:
    tk.Radiobutton(root, text=text, variable=menu_var, value=value).pack()

ingredient_label = tk.Label(root, text="Select ingredient/s:")
ingredient_entry = tk.Entry(root)

select_ingredient_button = tk.Button(root, text="Select", command=show_ingredient_menu)
submit_button = tk.Button(root, text="Submit", command=show_recipes)

recipe_display = tk.Text(root, height=10, width=50)

# Packing the widgets
ingredient_label.pack()
ingredient_entry.pack()
select_ingredient_button.pack()
submit_button.pack()
recipe_display.pack()

# Run the main loop
root.mainloop()