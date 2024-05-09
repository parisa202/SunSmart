from .models import *
import pandas as pd


def clean_data():
    # Query data from Django models
    recipes = RECIPES.objects.all()
    ingredients = INGREDIENT.objects.all()
    recipe_ingredients = RECIPE_INGREDIENT.objects.all()

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

    # Create DataFrames
    recipes_df = pd.DataFrame.from_dict(recipes_dict, orient='index')
    ingredients_df = pd.DataFrame.from_dict(ingredients_dict, orient='index')
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

    # Optionally, you can drop unnecessary columns
    # merged_df.drop(['recipe_id', 'ingredient_id'], axis=1, inplace=True)

    # Display the merged DataFrame
    print(merged_df)
    
    # Transform data
    
    
def k-means(data=data_frame):
    
    pass