# Tactic 2: Instruct the model to work out its own solution before rushing to a conclusion


from openai import OpenAI
from dotenv import load_dotenv
import os
from IPython.display import display, HTML


load_dotenv()

client = OpenAI()

def get_completion(prompt):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content

# fact_sheet_chair = """
# OVERVIEW
# - Part of a beautiful family of mid-century inspired office furniture, 
# including filing cabinets, desks, bookcases, meeting tables, and more.
# - Several options of shell color and base finishes.
# - Available with plastic back and front upholstery (SWC-100) 
# or full upholstery (SWC-110) in 10 fabric and 6 leather options.
# - Base finish options are: stainless steel, matte black, 
# gloss white, or chrome.
# - Chair is available with or without armrests.
# - Suitable for home or business settings.
# - Qualified for contract use.

# CONSTRUCTION
# - 5-wheel plastic coated aluminum base.
# - Pneumatic chair adjust for easy raise/lower action.

# DIMENSIONS
# - WIDTH 53 CM | 20.87”
# - DEPTH 51 CM | 20.08”
# - HEIGHT 80 CM | 31.50”
# - SEAT HEIGHT 44 CM | 17.32”
# - SEAT DEPTH 41 CM | 16.14”

# OPTIONS
# - Soft or hard-floor caster options.
# - Two choices of seat foam densities: 
#  medium (1.8 lb/ft3) or high (2.8 lb/ft3)
# - Armless or 8 position PU armrests 

# MATERIALS
# SHELL BASE GLIDER
# - Cast Aluminum with modified nylon PA6/PA66 coating.
# - Shell thickness: 10 mm.
# SEAT
# - HD36 foam

# COUNTRY OF ORIGIN
# - Italy
# """

# prompt = f"""
# Your task is to help a marketing team create a 
# description for a retail website of a product based 
# on a technical fact sheet.

# Write a product description based on the information 
# provided in the technical specifications delimited by 
# triple backticks.

# Use at most 50 words.

# Technical specifications: ```{fact_sheet_chair}```
# """

# prompt = f"""
# Your task is to help a marketing team create a 
# description for a retail website of a product based 
# on a technical fact sheet.

# Write a product description based on the information 
# provided in the technical specifications delimited by 
# triple backticks.

# The description is intended for furniture retailers, 
# so should be technical in nature and focus on the 
# materials the product is constructed from.

# At the end of the description, include every 7-character 
# Product ID in the technical specification.

# After the description, include a table that gives the 
# product's dimensions. The table should have two columns.
# In the first column include the name of the dimension. 
# In the second column include the measurements in inches only.

# Give the table the title 'Product Dimensions'.

# Format everything as HTML that can be used in a website. 
# Place the description in a <div> element.

# Technical specifications: ```{fact_sheet_chair}```
# """


text = f"""
are you shope keeper

shop sell some product like : all fruit, vegitable, grocery

some costomer come to shop and ask about product and he want to buy \
and shope keeper give him some information about product and cost and other \
information about product and then costomer buy product and leave shop

example:
1. here use name of customer : give me apple and orange
2. shop keeper : yes we have apple and orange, apple cost is 100 rs per
so one etc

rule: 
1. don't ignore costomer question and product information
2. give correct information about product and cost
3. if costomer ask about product and you don't have that product then you can say that
4. if any product not abailable then you can say that (sorry we don't have that product)
5. if customer say about non seeling product then you can say that (sorry we don't sell that product)

Note: vagitable is today not available
"""

prompt = f"""
your work is give clear answer to all user according shop stokes and product, \
product information and cost.

1. ivan : give me apple and orange
2. parth : give me furniture
3. ramesh : give me some vegitable
4. rahul : give me details about rice and oil or wheat
5. rasad : give me electronic product information and cost

```{text}```
"""


response = get_completion(prompt)
print(response)
print(len(response.split()))
# display(HTML(f"<p style='color:blue;font-size:20px;'>{response}</p>"))