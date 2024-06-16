from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")

# Prompt Template
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a professional chef/nutritionist. Your job is to provide the best possible recipe for the ingredients available with the user (separated by a comma). You need to adjust the recipe according to the cuisine preference given by the user. You also need to make sure that if the user has given any nutritional preference, then the recipe needs to adhered to it. If the nutritional preference is not given, you can assume that the user is okay to eat however calorie intensive or extensive the recipe is. You can assume that the user has spices available. Make sure you mention the nutritional value of the recipe with how many people it would serve. You don't have to use all the available ingredients. It's not mandatory, but if needed, go for it."),
        ("user", "List of Ingredients: {question}. Nutritional value preference: {nutri_value}. Cuisine: {cuisine}")
    ]
)

# StreamLit Framework

st.title('FoodieAI')
ingredients = st.text_input("Please enter the list of ingredients separated by a comma", key="ingredients")
nutri_value = st.text_input("Please enter any specific type of nutritional value you would prefer in your recipe (such as, protein-rich, less-sugar, etc.)", key="nutri_value")
cuisine = st.text_input("Do you have any cuisine preference?", key="cuisine")

# LLM
llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro-latest")
output_parser = StrOutputParser()
chain = prompt | llm | output_parser

# Button to trigger the AI
if st.button("Get Recipe"):
    # Add a divider
    st.markdown("<hr>", unsafe_allow_html=True)
    if ingredients:
        query = {
            'question': ingredients,
            'nutri_value': nutri_value if nutri_value else "No preference",
            'cuisine': cuisine if cuisine else "No preference"
        }
        response = chain.invoke(query)
        st.write(response)
    else:
        st.write("Please enter the list of ingredients to get a recipe.")


