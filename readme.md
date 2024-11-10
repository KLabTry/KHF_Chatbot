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

### 4. Run Rasa Actions
In a separate terminal, start the Rasa actions server at port 5056:

```bash
cd rasa
rasa run actions --port 5056
```

Make sure to have both terminals running to ensure the chatbot and its actions work correctly.
