# Project-Prisma---VTuver---English---version XTTS

## Description
Project-Prisma is an interactive application that simulates a VTuber named Ely. Ely is an energetic and friendly virtual assistant designed to interact with users through live YouTube chats, answering questions and generating responses dynamically and entertainingly.

## Features
- **Real-time interaction**: Ely can respond to questions in real-time during live YouTube streams.
- **Defined personality**: Ely has a well-defined personality, with characteristics such as her name, visual style, voice tone, skills, and more.
- **Personalized responses**: Ely uses predefined rules to answer common questions and generate responses consistent with her personality.
- **Voice synthesis**: Ely can convert text to speech using PowerShell for a more immersive experience.
- **Integration with language models**: Ely uses the Ollama language model to generate more complex and natural responses.

## Project Structure
The project is organized as follows:
- `main.py`: Main file that handles real-time interaction with YouTube chat, generates responses using the Ollama language model, and synthesizes Ely's voice.
- `data/ely_personality.json`: JSON file containing Ely's defined personality.
- `data/ely_rules.json`: JSON file containing predefined rules for answering common questions.
- `experimental/`: Directory with experimental scripts and tests.

## How `main.py` Works
The `main.py` file performs the following tasks:
1. Loads Ely's personality and rules from JSON files.
2. Connects to the live YouTube chat using `ChatDownloader`.
3. Processes each chat message, looking for matches with predefined rules.
4. Generates a response using the Ollama language model.
5. Filters the generated text to remove internal analysis.
6. Converts the response to speech using `pyttsx3`.