# WORK IN PROGRESS AT THE MOMENT

# CognitiveChatbot

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
<br><br>
<img src="/static/images/chatbot1.gif" title="chatbot1">
