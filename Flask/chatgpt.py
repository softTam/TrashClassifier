from openai import OpenAI
from flask import jsonify
client = OpenAI()

# Once you add your API key below, make sure to not share it with anyone! The API key should remain private.

# completion = client.chat.completions.create(
#   model="gpt-3.5-turbo",
messages=[
  {"role": "system", "content": "You are an expert at trash classification."}]
#     # {"role": "user", "content": "You are a garbage disposer."}
#   ]
# )
#
# print(completion.choices[0].message)

def solution(item_description):
  # item_description = "banana peel"
  question1 = "How do you trash-classify " + item_description[0] + " as compostable, recyclable, or disposable? (One word only)" 
  # print(question1)
  message = question1
  if message:
    messages.append(
      {"role": "user", "content": message},
    )
    completion = client.chat.completions.create(model="gpt-3.5-turbo", messages=messages)
  response1 = completion.choices[0].message.content
  # print(f"{response1}")
  edit_response1 = response1.replace(".", "")   # trash classification
  question2 = "Now, Give me 4 options I can do with " + item_description[0] + " as " + "trash?"
  # print(question2)
  message2 = question2
  if message2:
    messages.append(
      {"role": "user", "content": message2},
    )
    completion = client.chat.completions.create(model="gpt-3.5-turbo", messages=messages)
  response2 = completion.choices[0].message.content   # handling instruction
  return {"Object": item_description, "Category" : edit_response1, "Msg" : response2}









