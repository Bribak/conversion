## Conversion
Functions in this repo start from a text file with cocktail recipes (one recipe per line) in the form:
Name - XX ml ingredient - XX ml ingredient - .... - stir/shake

# featurize_recipes(filename)

Takes the recipe text file and extracts the ingredients and their amounts into a dataframe which it returns

# get_recipe_tsne(filename,sourcefile)

Takes the dataframe from featurize_recipes as filename and the original text recipe database sourcefile.
Performs t-SNE on ingredient features and plots t-SNE components of cocktails with Plotly as a scatterplot.
Colors cocktails according to their main spirit.
Cursor hovering over points shows cocktail recipe.
