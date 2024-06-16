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
        ("system", "You are a professional chef/nutritionist. Your job is to provide the best possible recipe for the ingredients available with the user (separated by a comma). You need to adjust the recipe according to the nutrition preference given by the user. If not given, you can assume that the user is okay to eat however calorie intensive or extensive the recipe is. You can assume that the user has spices available. Make sure you mention the nutritional value of the recipe with how many people it would serve."
                   "that the user might have"),
        ("user", "List of Ingredients: {question}. Nutritional value preference: {nutri-value}")
    ]
)

# filled_prompt = prompt.format(question="What is the weather going to be if it rained yesterday, but has been sunny since morning, in the summer season?")
# print(filled_prompt)

# StreamLit Framework

st.title('FoodieAI')
ingredients = st.text_input("Please enter the list of ingredients separated by a comma")
nutri_value = st.text_input("Please enter any specific type of nutritional value you would prefer in your recipe (such as, protein-rich, less-sugar, etc.)")


# Ollama LLM
llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro-latest")
output_parser = StrOutputParser()
chain = prompt | llm | output_parser

if ingredients and nutri_value:
    st.write(chain.invoke({'question' : ingredients, 'nutri-value': nutri_value}))
elif ingredients:
    st.write(chain.invoke({'question' : ingredients}))