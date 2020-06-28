# WhatsApp chat analyser

when chatting with a close friend, have you ever wanted to know: 
the number of messages sent by each of you or the average length 
of your messages or who texts first and the first text in each 
conversation or your chatting time patterns-hourly, daily, 
and monthly or most shared websites link or most common words that 
each of you use? from this came the idea of whatsapp chat analyser.

## version 1!

    words_count(msg_list, conversers)
    msg_count(msg_list, conversers)
    average(msg_list, conversers, msg_count, separator)
    words_frequency(media_id, msg_list, conversers)
    most_active_hour(time_and_date, date)
    most_active_day(date)
    most_active_month(date)
    most_shared_websites(msg_list, conversers)

## version 2!

    get_first_msg(time_and_date, msgs)
    get_first_text_count(conversers, first_texts)
    get_chat_long(time_and_date)

### done with:

* [Python](https://www.python.org) - python programming language
* [JSON](https://json.org/json-en.html) - javascript object notation

### Installation:
1. open the whatsapp conversation you would like to have analysed and tap 
    on the three points in top-right of the conversation.
2. tap the more option.
3. tap on "Export chat".
4. slect one of the two options "include media" or "without media".
5. select via what do you want to share the file.
6. import the chat file in the assets directory of the tool dir.
7. rename it as chat.txt.
8. `pip install virtualenv` to install `virtualenv`.
9. `virtualenv venv` to create a virtualenv.
10. `source venv/bin/activate` to activate the virtualenv.
11. to install this tool requirements type `pip install requirements.txt`.
12. all you have now to do is execute the `chat_stat.py` file.

wtp chat analyser requires [python](https://www.python.org) v3.x+ to run.

### Todos

 - [X] remove stopwords
 - [X] calculate the number of sent media by each converser
 - [X] get first texts for every converser
 - [ ] calculate how long did every chat go
 - [ ] calculate when and how much you were messaging and sending files: timeline
 - [ ] calculate letters count
 - [ ] determinate who did write the most
 - [ ] determinate how many images, videos, voice messages, and locations did conversers share
 - [ ] visualisation of the chat as a poster
 - [ ] a book with the complete conversation including the visualisations
 
### Author:
**created at 🌙 with 💻 and ❤ by the walking dead**
* **Fedi abdouli** - *WhatsApp chat analyser* - [fedi abdouli](https://github.com/cs-fedy)
* my twitter account [FediAbdouli](https://www.twitter.com/FediAbdouli)
* my instagram account [fedyy_the_walking_dead](https://www.instagram.com/fedyy_the_walking_dead)
