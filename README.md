# Cognitive Chatbot

Customizable multi-platform chatbot written in Python and RiveScript

## Description

This project is part of my thesis work while attending Federico II University of Naples. The work consists in a complete design and development of a multi-platform virtual assistant. The aim of the project is to develop a chatbot capable of help people in daily tasks: despite this was implemented to help customer service operators, it can be customized to perform a lot of actions.
<br>The chatbot has three key functions:
- speech customization
- admin profile support
- REST services integration
<br>

## Architecture
The architecture of the chatbot can be divided in two modules:
- **pattern recognition module**, written in RiveScript, supports all languages
- **machine learning module**, written in Python using TensorFlow and tflearn: the module uses custom Italian libraries and 
therefore Italian only is supported. However, these libraries can be easily swapped with other libraries.
<br>
This example uses pattern recognition module:
<br><br>
<img src="https://raw.githubusercontent.com/lucamadd/CognitiveChatbot/master/static/images/chatbot1.gif" title="chatbot1" height="400">

Machine Learning module is based on a deep neural network, as shown in the picture.
<br><br>
<img src="/static/images/Neural Network.png" title="dnn" height="300">

Nested topics are supported. You can restrict user's questions on a specific topic. More info on <a href="https://www.rivescript.com/">RiveScript site</a><br>
Multiple answers are supported in every language.
<br><br>
<img src="https://raw.githubusercontent.com/lucamadd/CognitiveChatbot/master/static/images/chatbot2.gif" title="chatbot2" height="400">

## Customization

New questions and answers can be added via simple workflows as an admin. The chatbot can send HTTP requests with parameters, however program logic to fetch the request/send a response must be implemented server-side.

## Usage

- Make sure your Python version is 3.6.5
- Run ```pip install -r requirements.txt```
- Run the file ```serverflask.py```, optionally defining a port to listen on. (default 8080)
- Open your browser and go to http://localhost:8080 (or the port you've defined)
- Done!

## Notes

This is a demo. You may add new interactions with the chatbot by accessing settings page. You can't remove old interactions at the moment, unless you edit configuration files directly. Most dialogues are in Italian in this version, and keep in mind that machine learning module won't work in other languages. Pattern recognition module works in every language instead, as well as multiple answers.
