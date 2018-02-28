# Lambda Functions
This directory contains two lambda functions and the test cases for each.

## HowCanIHelpAPI.py
This lambda function houses all of the logic needed for the web application
to interact with the same storage layer as the Alexa Skill.

## HowCanIHelp.py
This lambda function contains all of the logic needed for the Alexa skill
to interact with the same storage layer as the web application. This function
is more complex than the lambda function for the web application because the
Alexa Skills Kit (ASK) has more requirements than simple HTTPS requests.
