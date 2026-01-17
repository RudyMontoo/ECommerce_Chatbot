from jsonschema._keywords import pattern
from groq import Groq
import os
import re
import sqlite3
import pandas as pd
from pathlib import Path
from dotenv import load_dotenv
from pandas import DataFrame

load_dotenv()
GROQ_MODEL=os.getenv("GROQ_MODEL")
db_path=Path(__file__).parent.parent / "db.sqlite"

client_sql=Groq()

sql_prompt = """You are an expert in understanding the database schema and generating SQL queries for a natural language question asked
pertaining to the data you have. The schema is provided in the schema tags. 
<schema> 
table: product 

fields: 
product_link - string (hyperlink to product)	
title - string (name of the product)	
brand - string (brand of the product)	
price - integer (price of the product in Indian Rupees)	
discount - float (discount on the product. 10 percent discount is represented as 0.1, 20 percent as 0.2, and such.)	
avg_rating - float (average rating of the product. Range 0-5, 5 is the highest.)	
total_ratings - integer (total number of ratings for the product)

</schema>
Make sure whenever you try to search for the brand name, the name can be in any case. 
So, make sure to use %LIKE% to find the brand in condition. Never use "ILIKE". 
Create a single SQL query for the question provided. 
The query should have all the fields in SELECT clause (i.e. SELECT *)

Just the SQL query is needed, nothing more. Always provide the SQL in between the <SQL></SQL> tags."""


comprehension_prompt = """You are an expert in understanding the context of the question and replying based on the data pertaining to the question provided.
You will be provided with Question: and Data:. The data will be in the form of an array or a dataframe or dict. Reply based on only the data provided as Data for answering the question asked as Question. Do not write anything like 'Based on the data' or any other technical words. Just a plain simple natural language response.
The Data would always be in context to the question asked. For example is the question is “What is the average rating?” and data is “4.3”, then answer should be “The average rating for the product is 4.3”. So make sure the response is curated with the question and data. Make sure to note the column names to have some context, if needed, for your response.
There can also be cases where you are given an entire dataframe in the Data: field. Always remember that the data field contains the answer of the question asked. 
All you need to do is to always reply in the following format when asked about a product: 
Strictly use this HTML template for each product. Do not output Markdown.
<div style="background-color: #1e1e1e; padding: 15px; border-radius: 10px; margin-bottom: 10px; border: 1px solid #444; box-shadow: 0 4px 6px rgba(0,0,0,0.3);">
  <h3 style="color: #4da6ff; margin: 0 0 5px 0; font-size: 18px;">Product Title</h3>
  <p style="color: #ccc; margin: 0 0 10px 0; font-size: 14px;">Price: <b>Rs. X (Y% off)</b> | Rating: <b>Z ⭐</b></p>
  <a href="product_link" target="_blank" style="display: inline-block; background-color: #007bff; color: white; padding: 8px 12px; text-decoration: none; border-radius: 5px; font-weight: bold; font-size: 12px;">View on Flipkart ↗</a>
</div>

For example:
<div style="...">
  <h3 ...>Campus Women Running Shoes</h3>
  <p ...>Price: <b>Rs. 1104 (35% off)</b> | Rating: <b>4.4 ⭐</b></p>
  <a href="https://..." target="_blank" ...>View on Flipkart ↗</a>
</div>

"""
def generate_sql_query(question):
   
    chat_completion = client_sql.chat.completions.create(
    model=os.environ['GROQ_MODEL'],
    messages=[
        {
            "role": "system",
            "content": sql_prompt
        },
        {
            "role": "user",
            "content": question
        }
    ],
    temperature=0.2,
    max_tokens=1024
    )
    return chat_completion.choices[0].message.content

def run_query(query):
    if query.strip().upper().startswith("SELECT"):
        with sqlite3.connect(db_path) as conn:
            df=pd.read_sql_query(query, conn)
            return df
    else:
        raise ValueError("Query must be a SELECT statement")

def data_comprehension(question, context):
    chat_completion = client_sql.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": comprehension_prompt,
            },
            {
                "role": "user",
                "content": f"QUESTION: {question}. DATA: {context}",
            }
        ],
        model=os.environ['GROQ_MODEL'],
        temperature=0.2,
        # max_tokens=1024
    )

    return chat_completion.choices[0].message.content

def sql_chain(question):
    sql_query = generate_sql_query(question)
    pattern = "<SQL>(.*?)</SQL>"
    matches = re.findall(pattern, sql_query, re.DOTALL)

    if len(matches) == 0:
        return "Sorry, LLM is not able to generate a query for your question"

    print(matches[0].strip())

    response = run_query(matches[0].strip())
    if response is None:
        return "Sorry, there was a problem executing SQL query"

    context = response.to_dict(orient='records')

    answer = data_comprehension(question, context)
    return answer


if __name__ == "__main__":
    # question = "All shoes with rating higher than 4.5 and total number of reviews greater than 500"
    # sql_query = generate_sql_query(question)
    # print(sql_query)
    question = "Show top 3 shoes in descending order of rating"
    # question = "Show me 3 running shoes for woman"
    # question = "sfsdfsddsfsf"
    answer = sql_chain(question)
    print(answer)
