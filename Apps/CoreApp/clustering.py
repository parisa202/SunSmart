from .models import *
import pandas as pd
from django.db import connection
import re
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import cosine_similarity

def get_intermediary_table_data_as_dataframe():
    with connection.cursor() as cursor:
        cursor.execute('SELECT * FROM public."CoreApp_recipes_health_tag";')
        intermediary_data = cursor.fetchall()
    
    # Define column names based on your intermediary table structure
    column_names = ['id', 'recipe_id', 'health_id']
    
    # Convert the fetched data into a Pandas DataFrame
    df = pd.DataFrame(intermediary_data, columns=column_names)
    return df


def clean_data():
    # Query data from Django models
    recipes = RECIPES.objects.all()
    ingredients = INGREDIENT.objects.all()
    recipe_ingredients = RECIPE_INGREDIENT.objects.all()
    health_tags = HEALTH_TAG.objects.all()
    recipe_healthTags = get_intermediary_table_data_as_dataframe() # Returns a Dataframe

    # Convert querysets to dictionaries
    recipes_dict = {recipe.id: {
        'recipe_name': recipe.name,
        'description': recipe.description,
        'url': recipe.url,
        'total_time': recipe.total_time,
        'serving': recipe.serving,
        # Add other fields you need
    } for recipe in recipes}

    ingredients_dict = {ingredient.id: {
        'name': ingredient.name,
        'food_category': ingredient.food_category,
        # Add other fields you need
    } for ingredient in ingredients}

    recipe_ingredients_list = [{
        'recipe_id': ri.recipe_id,
        'ingredient_id': ri.ingredient_id,
        'ingredient_text': ri.ingredient_text
    } for ri in recipe_ingredients]

    health_tag_dict = {health.id: {
        'tag': health.tag
    } for health in health_tags}
    
    
    # Create DataFrames
    recipes_df = pd.DataFrame.from_dict(recipes_dict, orient='index')
    ingredients_df = pd.DataFrame.from_dict(ingredients_dict, orient='index')
    health_df = pd.DataFrame.from_dict(health_tag_dict, orient='index')
    recipe_ingredients_df = pd.DataFrame(recipe_ingredients_list)

    # Merge DataFrames based on relationships
    merged_df = pd.merge(recipe_ingredients_df,
                        recipes_df,
                        left_on='recipe_id',
                        right_index=True,
                        how='left')

    merged_df = pd.merge(merged_df,
                        ingredients_df,
                        left_on='ingredient_id',
                        right_index=True,
                        how='left')
    
    merged_df = pd.merge(merged_df,
                    recipe_healthTags,
                    left_on='recipe_id',
                    right_on='recipe_id',
                    how='left')
    
    merged_df = pd.merge(merged_df,
                health_df,
                left_on='health_id',
                right_index=True,
                how='left')

    # Optionally, you can drop unnecessary columns
    # merged_df.drop(['recipe_id', 'ingredient_id'], axis=1, inplace=True)

    # Display the merged DataFrame
    
    #merged_df.to_csv('GGGG.csv', index=False)
    
    # Transform data
    # Drop specified columns
    columns_to_drop = ['ingredient_text', 'description', 'url', 'total_time', 'serving', 'id', 'health_id','ingredient_id']
    df = merged_df.drop(columns=columns_to_drop)

    # Convert all strings to lowercase
    df = df.applymap(lambda x: x.lower() if isinstance(x, str) else x)
    
    
    # Define mappings of words to their standardized forms using regular expressions
    word_mappings = {
        r'\b(beef|filet)\b': 'beef',
        r'\b(egg|eggs)\b': 'egg',
        r'\b(olive oil)\b': 'olive oil',
        r'\b(bread)\b': 'bread',
        r'\b(pepper)\b':'pepper',
        r'\b(lemon|lemons)\b':'lemon',
        r'\b(almond|almonds)\b':'almond',
        r'\b(sugar)\b':'sugar',
        r'\b(pork|bacon)\b':'pork',
        r'\b(garlic)\b':'Garlic',
        r'\b(cucumbers|cucumber)\b':'Cucumber',
        r'\b(beans)\b':'beans',
        r'\b(potatoes|potato)\b':'Potato',
        r'\b(salt)\b':'Salt',
        r'\b(yogurt)\b':'Yogurt',
        r'\b(tomatoes|tomato)\b':'Tomato',
        r'\b(cacao)\b':'Cacao',
        r'\b(broccoli)\b':'Broccoli',
        r'\b(mustard)\b':'Mustard',
        r'\b(onion|onions)\b':'Onion',
        r'\b(spaghetti|pasta|fettuccine|penne )\b':'pasta',
        r'\b(chicken thighs)\b':'Chicken thigh',
        r'\b(chicken broth)\b':'Chicken broth',
        r'\b(cauliflower)\b':'Cauliflower',
        r'\b(carrots|carrot)\b':'Carrot',
        r'\b(chickpeas)\b':'Chickpea',
        r'\b(zucchini)\b':'Zucchini',
        r'\b(lettuce)\b':'Lettuce',
        r'\b(milk)\b':'milk',
        r'\b(Nut)\b':'Nut',
        r'\b(avocado)\b':'avocado',
        r'\b(ginger)\b':'ginger',
        r'\b(cabbage)\b':'cabbage',
        r'\b(flour)\b':'flour',
        r'\b(rice)\b':'rice',
        r'\b(soy)\b':'soy',
        r'\b(strawberry|strawberries)\b':'strawberry',
        r'\b(lentils|lentil)\b':'lentil',
        r'\b(grapes|grape)\b':'grapes',
        r'\b(watermelon|honeydew melon|clementine|cantaloupe|papaya|fruit)\b':'fruit',
        r'\b(curry)\b':'curry',
        r'\b(cream)\b':'cream',
        r'\b(orange|oranges)\b':'orange',
        r'\b(walnut|walnuts)\b':'walnut',
        r'\b(banana|bananas)\b':'banana',
        r'\b(tomato|tomatos)\b':'tomato',
        r'\b(green olives|kalamata olives|manzanilla olives|spanish queen olives|'
        r'nicoise olives|picholine olives|ligurian olives|gaeta olives|cerignola olives|olives)\b':'olives',
        r'\b(sesame oil)\b':'sesame oil',
        r'\b(tofu)\b':'tofu',
        r'\b(vinegar)\b':'vinegar',
        r'\b(kiwi|kiwis)\b':'kiwi',
        r'\b(rice)\b':'rice',
        r'\b(Soybean Oil|Canola Oil|Sunflower Oil|Corn Oil|vegetable oil|'
        r'Olive Oil|Palm Oil|Coconut Oil|Peanut Oil|Sesame Oil)\b': 'vegetable oil'
    }

    # Compile regular expressions with the IGNORECASE flag
    compiled_mappings = {re.compile(pattern, flags=re.IGNORECASE): standard_form for pattern, standard_form in word_mappings.items()}

    # Function to apply the mappings to ingredient names using regular expressions
    def clean_ingredient(name):
        for pattern, standard_form in compiled_mappings.items():
            if pattern.search(name):
                return standard_form.lower()
        return name.lower()

    # Apply the mappings to the 'name' column and create a new column for cleaned ingredients
    df['cleaned_ingredient'] = df['name'].apply(clean_ingredient)
    df_filtered = df[df['food_category'] != 'condiments and sauces']
    
    # Print the unique cleaned ingredient names to verify
    # print(df_filtered.head(2))
    return df_filtered


def feature_engineering(df):
    
    # Create dummy variables for cleaned ingredients
    ingredient_dummies = pd.get_dummies(df['cleaned_ingredient'])

    # Create dummy variables for tags
    tag_dummies = pd.get_dummies(df['tag'])

    # Assign weights to tags (0.1 for tags)
    tag_dummies_weighted = tag_dummies * 0.01

    # Create dummy variables for food category
    food_category_dummies = pd.get_dummies(df['food_category'])

    food_category_dummies_weighted = food_category_dummies * 100

    # Concatenate the dummy variables with the original DataFrame
    df_transformed = pd.concat([df['recipe_id'], ingredient_dummies,food_category_dummies, tag_dummies_weighted], axis=1)

    # Group by 'id' and sum the binary values across the rows
    df_transformed = df_transformed.groupby('recipe_id').sum()
    
    # Apply a transformation: if sum > 0 then 1, else 0
    df_transformed_ingredient = df_transformed.applymap(lambda x: 0.1 if x > 100 else (2 if x > 1 else (0.3 if 0 < x < 1 else 0)))
    df_transformed_tags = df_transformed.applymap(lambda x: 1 if x > 1 else (2 if 0 < x < 1 else 0))

    # Reset the index to make 'id' a column again
    df_transformed.reset_index(inplace=True)
    # print(df_transformed_ingredient)
    
    return(df_transformed_ingredient)


def analysis(df):
    pass

def k_means_cluster(X):
    # Perform K-means clustering with the optimal number of clusters
    kmeans = KMeans(n_clusters=2, init='k-means++', random_state=2024)
    kmeans.fit(X)
    clusters = kmeans.predict(X)

    # Add the cluster labels to the DataFrame
    X['cluster'] = clusters
        # Reset index and rename columns
    X.reset_index(inplace=True)
    X.rename(columns={'index': 'recipe_id'}, inplace=True)
    
    # print(X.loc[X['recipe_id']==50,'cluster'] )
    return X

def get_similar_recipes(df_clustered,recipe_id, top_n=3):
    
    # Get the cluster of the given recipe
    recipe_cluster = df_clustered.loc[df_clustered['recipe_id'] == recipe_id, 'cluster'].values[0]
    
    # Filter recipes belonging to the same cluster
    cluster_recipes = df_clustered[df_clustered['cluster'] == recipe_cluster]
    
    # Compute cosine similarity matrix within the cluster
    cosine_sim_cluster = cosine_similarity(cluster_recipes.iloc[:, 1:], cluster_recipes.iloc[:, 1:])
    
    # Get the index of the recipe within the cluster
    idx = cluster_recipes.index[cluster_recipes['recipe_id'] == recipe_id].tolist()[0]
    
    # Get pairwise similarity scores with other recipes within the cluster
    sim_scores = list(enumerate(cosine_sim_cluster[idx]))
    
    # Sort the recipes based on similarity scores
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    
    # Exclude the input recipe itself from the recommendations
    sim_scores = [x for x in sim_scores if x[0] != idx]
    
    # Get the indices of the top N similar recipes
    similar_recipes_indices = [i[0] for i in sim_scores[:top_n]]
    
    # Return the ids of the top N similar recipes
    return cluster_recipes['recipe_id'].iloc[similar_recipes_indices].tolist()


def recommended_recipes(recipe_id):
    cleaned_data = clean_data()
    features = feature_engineering(cleaned_data)
    #clustered_data = k_means_cluster(features)
    clustered_data = features
    clustered_data.reset_index(inplace=True)
    clustered_data.rename(columns={'index': 'recipe_id'}, inplace=True)
    clustered_data['cluster'] = 0
    similar_recipes = get_similar_recipes(clustered_data,recipe_id, top_n=4)
    
    return similar_recipes


def feature_engineering_custom_recipe(df, custome_recipe_columns):
    
    
    
    # Create dummy variables for cleaned ingredients
    ingredient_dummies = pd.get_dummies(df['cleaned_ingredient'])

    # Create dummy variables for food category
    food_category_dummies = pd.get_dummies(df['food_category'])

    # Concatenate the dummy variables with the original DataFrame
    df_transformed = pd.concat([df['recipe_id'], ingredient_dummies,food_category_dummies], axis=1)

    # Group by 'id' and sum the binary values across the rows
    df_transformed = df_transformed.groupby('recipe_id').sum()
    
    # Apply a transformation: if sum > 0 then 1, else 0
    df_transformed = df_transformed.map(lambda x: 1 if x > 0 else 0)
    
    # Reset the index to make 'id' a column again
    df_transformed.reset_index(inplace=True)
    
    # Create a new row with 0s
    new_row = pd.DataFrame(0, index=range(1), columns=df_transformed.columns)

    # Set values to 1 for the columns specified in columns_to_set_to_1
    for col in custome_recipe_columns:
        if col in new_row.columns:
            new_row[col] = 1

    # Append the new row to the DataFrame
    df_transformed = pd.concat([df_transformed, new_row], ignore_index=True)
    #df_transformed = df_transformed.append(new_row, ignore_index=True)
    
    return(df_transformed)


def recommended_custom_recipes(ingredient_list):
    cleaned_data = clean_data()
    #clustered_data = k_means_cluster(features)
    clustered_data = feature_engineering_custom_recipe(cleaned_data, ingredient_list)
    #clustered_data.reset_index(inplace=True)
    #clustered_data.rename(columns={'index': 'recipe_id'}, inplace=True)
    clustered_data['cluster'] = 0
    # print(clustered_data)
    similar_recipes = get_similar_recipes(clustered_data,0, top_n=3)
    # print(similar_recipes)
    return similar_recipes