# Explain Like I'm 10

Imagine you have a giant basket of mail. Some letters are real and important. Some are junk trying to trick you. This project is like a smart helper that looks at each letter and says, "Keep this" or "Throw this away."

## Who Uses It?
People who want to quickly sort email.
This matters because it saves time and helps you focus on the messages that count.

## What Does It Do?
It reads email text and guesses whether it is spam or ham.
Think of it like a librarian that learns which books belong in the story shelf and which belong in the trash pile.
This matters because the helper turns messy text into a simple answer.

## When Do People Use It?
They use it when they have one email to check or a whole box of messages to sort.
A single email is like checking one apple. A batch of emails is like sorting a whole fruit basket.
This matters because the project works for both quick checks and bigger cleanups.

## Where Does It Run?
It runs on your computer in a browser window using Streamlit.
That is like opening a control panel in a web page instead of installing a big separate machine.
This matters because it makes the tool easy to try.

## Why Was It Built?
Because reading junk mail by hand is boring and slow.
The project trains on examples first, then uses what it learned to make new guesses.
This matters because learning from examples is how the helper gets smart.

## The Main Pieces
- The dataset is the pile of old mail examples.
- TF-IDF is the word sorter that gives important words more weight.
- The model is the brain that learns the difference between spam and ham.
- The saved files are the memory that lets the app work later without retraining.

## The Story
First, the project opens a big box of old emails.
Next, it cleans the words so they are easier to understand.
Then it teaches several different model "brains" and picks the best one.
After that, the app uses the best brain to check new emails.
This matters because the whole system is just a careful learning-and-guessing loop.
