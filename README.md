# Cognitive Chatbot

Customizable multi-platform chatbot written in Python and RiveScript

## Description

This project is part of my thesis work at the Federico II University of Naples. The work consists in a complete design and development of a multi-platform virtual assistant. The aim of the project is to develop a chatbot capable of help people in daily tasks: despite this was implemented to help customer service operators, it can be customized to perform a lot of actions.
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
<br>
<img src="https://raw.githubusercontent.com/lucamadd/CognitiveChatbot/master/static/images/chatbot1.gif" title="chatbot1" height="400">

Machine Learning module is based on a deep neural network, as shown in the picture.
<br><br>
<img src="/static/images/Neural Network.png" title="dnn" height="300">

Multiple answers are supported in every language.
<br>
<img src="https://raw.githubusercontent.com/lucamadd/CognitiveChatbot/master/static/images/chatbot2.gif" title="chatbot2" height="400">

## Customization

New questions and answers can be added via simple workflows by an admin. The chatbot can send HTTP requests with parameters, however program logic to fetch the request/send a response must be implemented server-side.
