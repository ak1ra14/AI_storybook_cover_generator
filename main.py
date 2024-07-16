import streamlit as st
from openai import OpenAI
import requests


def make_prompt(story):
  design_response = client.chat.completions.create(
      model='gpt-3.5-turbo',
      messages=[{
          "role": 'system',
          "content": "Based on the story given, you will design a detailed cover image of the story. The image prompt should include the theme of the story with the relevant color suitable adults. The output should be in 100 words",
      },
              {
                  "role": "user",
                  "content": f'{story}'
              }
      ],
      max_tokens = 100,
      temperature = 0.8
  )
  return design_response.choices[0].message.content

def make_url(design_prompt):
  client_image = client.images.generate(
      model='dall-e-2',
      prompt = f"{design_prompt}",
      size = "256x256",
      quality='standard',
      n = 1
  )
  return client_image.data[0].url

def show_image(image_url):
    url = image_url
    filename = "story.png"
    if url:
        response = requests.get(image_url)
        if response.status_code == 200:
            with open(filename, 'wb') as f:
                f.write(response.content)
            print(f"Image successfully downloaded and saved as {filename}")
            st.write(story)
            st.image(filename)

my＿api_key = st.secrets['OPENAI_SECRET']

client = OpenAI(api_key=my_api_key)
st.header("Story Generator", divider='rainbow')
with st.form("This section is not empty"):
    st.write("This is for the use to enter infomation about the story")
    story = st.text_input(label="Enter your story:")
    submit = st.form_submit_button(label="Submit")
    if submit:
        story_prompt = make_prompt(story)
        image_url = make_url(story_prompt)
        show_image(image_url)
       