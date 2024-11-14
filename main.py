from openai import OpenAI
from bs4 import BeautifulSoup

# Read API key value
with open("key.txt", "r", encoding="utf-8") as file:
    api_key = file.readline()

client = OpenAI(api_key=api_key)

file_input = open("Zadanie dla JJunior AI Developera - tresc artykulu.txt", "r")

# Using API to send prompt
completion = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {
            "role": "system", 
            "content": [
                {
                    "type": "text",
                    "text": "You will be provided with an article and your task is to structurize it with HTML tags, however use them only as if they are inside the body tag. Moreover you should propose where is it worth to insert images and also write prompts for generating these images in the alt attribute and image caption."
                }
            ]
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": file_input.read()
                }
            ]
        }
    ]
)

# Generating images based on prompts received
article_soup = BeautifulSoup(completion.choices[0].message.content, "html.parser")

for img in article_soup.find_all("img"):
    alt_text = img.get("alt")
    response = client.images.generate(
        prompt=alt_text,
        size="256x256"
    )
    new_src_value = response.data[0].url
    img["src"] = new_src_value

with open("artykul.html", "w", encoding="utf-8") as file:
    file.write(article_soup.prettify())

# Template and body merging
with open("szablon.html", "r", encoding="utf-8") as file:
    template_soup = BeautifulSoup(file.read(), "html.parser")

template_soup.body.replace_with(article_soup)

with open("podglad.html", "w", encoding="utf-8") as file:
    file.write(template_soup.prettify())

client.close()
file_input.close()