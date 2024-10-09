
import os
import streamlit as st
from langchain_ollama import OllamaLLM
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

load_dotenv()
os.environ["LANGCHAIN_PROJECT"] = os.getenv("LANGCHAIN_PROJECT")
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")
print(os.getenv("LANGCHAIN_API_KEY"))

# Initialize the Ollama LLM
llm = OllamaLLM(model="llama3")

# Function to generate recipe names based on ingredients
def generate_recipe_names(selected_items):
    """
    Generate a list of recipe names using a list of selected ingredients.

    Args:
        selected_items (list): A list of ingredients selected by the user.

    Returns:
        dict: A dictionary containing generated recipe names.
    """
    
    prompt1 = ChatPromptTemplate.from_template(
        "Generate a list of meal names that can be prepared using the provided ingredients. "
        "Ingredients are {ingredients}. "
        "It's not necessary to use all of the ingredients, "
        "and the list can include both simple and complex meal names. "
        "Please consider the ingredients provided and suggest meal names accordingly."
    )

    chain1 = prompt1 | llm | StrOutputParser()

    response = chain1.invoke({"ingredients": selected_items})
    
    return response

# Function to generate a comprehensive recipe
def generate_recipe(recipe_name):
    """
    Generate a detailed recipe using the recipe name as input.

    Args:
        recipe_name (str): The name of the recipe.

    Returns:
        dict: A recipe including ingredients and instructions.
    """
    
    prompt2 = ChatPromptTemplate.from_template(
        "Generate a recipe for {recipe_name}. Please include a list of ingredients and "
        "step-by-step instructions for preparing {recipe_name}. "
        "Please include the cooking time and any special instructions."
    )

    chain2 = prompt2 | llm | StrOutputParser()

    response = chain2.invoke({"recipe_name": recipe_name})

    return response


# Streamlit UI
st.title("AI Recipe Generator")
st.write("Enter your ingredients to generate recipe ideas and get full recipes!")

# User input for ingredients
ingredients = st.text_area("Enter ingredients (comma-separated):", placeholder="e.g., chicken, broccoli, rice")

if ingredients:
    # Generate recipe names
    st.write("### Suggested Recipes:")
    selected_items = ingredients.split(",")
    recipe_names = generate_recipe_names(selected_items)
    st.write(recipe_names)

    # Allow user to select a recipe name
    selected_recipe = st.selectbox("Select a recipe to get the full instructions:", recipe_names.split('\n'))

    if selected_recipe:
        # Generate full recipe
        recipe = generate_recipe(selected_recipe)
        st.write(f"### Recipe for {selected_recipe}:")
        st.write(recipe)

