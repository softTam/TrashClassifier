from openai import OpenAI

client = OpenAI()

# Once you add your API key below, make sure to not share it with anyone! The API key should remain private.
OPENAI_API_KEY= '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'

# completion = client.chat.completions.create(
#   model="gpt-3.5-turbo",
messages=[
  {"role": "system", "content": "You are a intelligent assistant."}]
#     # {"role": "user", "content": "You are a garbage disposer."}
#   ]
# )
#
# print(completion.choices[0].message)



item_description = "banana peel"
question1 = "Is a " + item_description + " compostable, recyclable, or disposable? (one word answer)"
print(question1)
message = question1
if message:
  messages.append(
    {"role": "user", "content": message},
  )
  completion = client.chat.completions.create(model="gpt-3.5-turbo", messages=messages)
response1 = completion.choices[0].message.content
print(f"{response1}")
edit_response1 = response1.replace(".", "")

question2 = "What to do with " + edit_response1 + "s? (summary)"
print(question2)
message2 = question2
if message2:
  messages.append(
    {"role": "user", "content": message2},
  )
  completion = client.chat.completions.create(model="gpt-3.5-turbo", messages=messages)
response2 = completion.choices[0].message.content
print(f"{response2}")








