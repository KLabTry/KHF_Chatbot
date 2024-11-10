# KFH Chatbot

This repository contains a Chatbot that helps users search for jobs and find out the currency exchange rate.
 
## How to Use

### 1. Install Requirements
To install the necessary requirements, run the following command in your terminal:

```bash
pip install -r requirements.txt
```

### 2. Train the Model
To train the Rasa model, run the following command in your terminal:
```bash
cd rasa
rasa train
```

### 3. Run the Rasa Shell
To interact with the chatbot, run the Rasa shell while inside the `rasa` directory:

```bash
rasa shell
```

Note: to stop the conversation at any time use `/stop` command in the chat


### 4. Run Rasa Actions
In a separate terminal, start the Rasa actions server at port 5056:

```bash
cd rasa
rasa run actions --port 5056
```

Make sure to have both terminals running to ensure the chatbot and its actions work correctly.


## Overview of Rasa's components:

- **nlu.yml**: Contains training data for the Natural Language Understanding (NLU) component, including examples of user inputs and their corresponding intents and entities. This enables the chatbot to comprehend user messages effectively.

- **rules.yml**: Defines specific rules that dictate the chatbot's responses to certain user inputs or situations. Rules are used for straightforward, predictable interactions where the chatbot's behavior should follow a fixed pattern.

- **stories.yml**: Outlines example conversations, known as stories, that demonstrate how the chatbot should handle various dialogue scenarios. Stories are not implemented as an essential components for for this particular chatbot.

- **config.yml**: Specifies the components (pipeline) used to train the Chatbot. It contains both the NLU training components and and dialogue management policies. It allows customization of how the chatbot processes and responds to user inputs.

- **domain.yml**: Defines the chatbot's domain, including intents, entities, slots, responses, and actions. It serves as a blueprint for the chatbot's design.

- **endpoints.yml**: Configures the external endpoints that the chatbot interacts with, mainly the action server.

- **actions/actions.py**: Defines the actions that the chatbot is able to take, such as calling the job search or currency exchange APIs. The actions are also responsible for generating the response message that will be displayed to the user.

