# cdbot
A selenium "API" for OpenAI's chatGPT

# How it works
You have two text files, c-input, and c-output, c-output will serve as a communication point with chatGPT and your application, any text that is dumped into c-output will be given to chatGPT, each time the keys are sent, the c-output is cleared, c-input will act like a log of the conversation, it will get all the messages from the chat and record them, it will sort them, each user message will be given a User: prefix, and each chatGPT message will be given an AI: prefix, to ensure that the extraction doesn't happen to early, it only extracts when the "stop generating" thingy disappears, c-input is cleared each time the script initializes.

# You can use this in any application, just remember to credit me :)

## NOTE
I wouldn't recommend to use this in anything except for personal applications and/or testing due to legal reasons
