import numpy as np
import openai
import jellyfish


openai.api_key = "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"

question = "How should I spend my 20s?"
speakers = []
convo = []


def getting_replies(actual_number):
  global recent_prompt
  names = [
    'Elon Musk', 'Naval Ravikant', 'Steve Jobs', 'Andrej Karpathy', 'George Hotz'
  ]
  for i in range(actual_number-1):
    response = people_convo(names)    
    if jellyfish.jaro_distance(recent_prompt, response) < 0.7:
      convo.append(response)
      recent_prompt = response
    else:
      break



def people_convo(names):
  global recent_prompt 
  name = names[np.random.choice(len(names))]
  max_messages = 3
  if speakers[-1 * max_messages:].count(name) == max_messages:
    someone_other = name
    while name != someone_other:
      name = names[np.random.choice(len(names))]
  s = ", "
  names_string = s.join(names)
  j = " "
  convo_string = j.join(convo)

  summary_prompt = """Summarize this text conversation between business       leaders that are helping me: %s""" % (convo_string)
  convo_summary = openai.Completion.create(model="text-davinci-002",
                                           prompt=summary_prompt,
                                           temperature=0,
                                           max_tokens=64,
                                           top_p=1.0,
                                           frequency_penalty=0.0,
                                           presence_penalty=0.0)
  
  
  #creating a prompt for openAI to genrate a response
  prompt = """
  The startup founders %s are having a long text conversation to exclusively answer my questions. This is the summary of the conversation %s. This is the last text %s. %s had a response, and they said:
  """ % (names_string
         , convo_summary, recent_prompt, name)


  #generating a response using openAI API
  response = openai.Completion.create(engine="text-davinci-002",
                                      prompt=prompt,
                                      temperature=0.9,
                                      max_tokens=256,
                                      top_p=1,
                                      frequency_penalty=0,
                                      presence_penalty=0)


  text = response['choices'][0]['text']
  recent_response = text.replace('"', '')

  print("""%s said %s""" % (name, recent_response))

  return recent_response


  