# setup:
import re
import json
import datetime as dt
media_tag = "<Media omitted>"
with open("assets/en_stopwords.json") as stopwords:
    stopwords_data = json.load(stopwords)
# opening (as read only --> "r") the chat file that we are going to deal with
# every line of the chat will be in a list case
chat_file = open("assets/chat.txt", "r")
chat = chat_file.read().split("\n")
# msg_list is a list that contain msgs
def purify(msgs, stop_words, media_tag):
    arr = []
    for msg in msgs:
        if msg.count(":") <= 1: continue
        if media_tag in msg: 
            arr.append(msg)
            continue
        converser_name = msg[:msg.find(": ")+2]
        msg_words = [word for word in msg[msg.find(": ")+2:].split(" ") if word not in stop_words]
        arr.append(f"{converser_name}{" ".join(msg_words)}")
    return arr
msgs = purify(chat, stopwords_data, media_tag)
msg_list = [line[line.find("-")+1:] for line in msgs]
# name of conversers
conversers = list({msg[:msg.find(":")] for msg in msg_list if msg.count(":") > 1})
# extracting the time and the date from each line of the chat list
# the same for the date but extracting from the time_and_date list
time_and_date = [line[:line.find("-")-1] for line in msgs]
date = [date_i[:date_i.find(",")] for date_i in time_and_date]

# count words sent by converser_k:
print("##################################################")
def words_count(msg_list, conversers):
    conversers_words_count = {}
    for converser in conversers:
        cnt = sum([
            len(msg[msg.find(":")+1:].split(" ")) 
            for msg in msg_list 
            if msg.find(media_tag) == -1 and converser in msg])
        conversers_words_count[converser] = cnt
    return conversers_words_count
converserk_words_count = words_count(msg_list, conversers)
for converser in conversers:
    print(f"words sent by {converser} = {converserk_words_count[converser]}")

# count messages number per converser:
print("##################################################")
def msg_count(msg_list, conversers):
    converser_msg_count = {}
    for converser in conversers:
        cnt = 0
        for msg in msg_list:
            if converser in msg:
                cnt += 1
        converser_msg_count[converser] = cnt
    return converser_msg_count
converserk_msg_count = msg_count(msg_list, conversers)
for converser, value in converserk_msg_count.items():
    print(f"msgs sent by {converser} = {value}")

# count sent media number per converser:
print("##################################################")
def media_count(msg_list, conversers, media_tag):
    converser_msg_count = {}
    for converser in conversers:
        cnt = 0
        for msg in msg_list:
            if converser in msg and media_tag in msg:
                cnt += 1
        converser_msg_count[converser] = cnt
    return converser_msg_count
converserk_media_count = media_count(msg_list, conversers, media_tag)
for converser, value in converserk_media_count.items():
    print(f"number of media sent by {converser} = {value}")

# average words or length:
# a function that return the average length of messages (if the separator is "" )
# or return the average words (if the separator is " ") sent by converser_k
print("##################################################")
def average(msg_list, conversers, msg_count, separator):
    average_words_converser = {}
    for converser in conversers:
        cnt = 0
        for msg in msg_list:
            string = msg[msg.find(":")+2:]
            length = len(string) if separator == "" else len(string.split(separator))
            cnt += length if converser in msg else 0
        average_words_converser[converser] = float("{0:.2f}".format(cnt / msg_count[converser]))
    return average_words_converser
av_len = average(msg_list, conversers, converserk_msg_count, separator = "")
av_words = average(msg_list, conversers, converserk_msg_count, separator = " ")
for converser in conversers:
    print(f"average msg's length for {converser} = {av_len[converser]}")
    print(f"average words per msg sent by {converser} = {av_words[converser]}")

# frequency of used words:
print("##################################################")
def words_frequency(media_tag, msg_list, conversers):
    word_freq_converserk = {} 
    for converser in conversers:
        # filter all msgs: remove msgs that contain media and extract just the msg
        filtered_msgs = [line[line.find(":")+2:] for line in msg_list if line.find(media_tag) == -1 and converser in line]
        # join filtered_msgs and split them to get all msgs words
        words = " ".join(filtered_msgs).split(" ")
        # filter the words: get the unique words
        unique_words = list(set(words))
        # get the frequency of every word in the unique_words list
        word_freq_converserk[converser] = [{"word": word, "count": words.count(word)} for word in unique_words if words.count(word) > 10]
    return word_freq_converserk
converserk_words_freq = words_frequency(media_tag, msg_list, conversers)
for converser in conversers:
    print(f"most used words by {converser}")
    pk_words = converserk_words_freq[converser]
    for word in pk_words:
        print(word)

# chatting time pattern:
# Which hour of the day do you usually chat the most?
print("##################################################")
def most_active_hour(time_and_date, date):
    unique_date = list(set(date))
    freq = []
    for date_i in unique_date:
        date_arr = [date for date in time_and_date if date_i in date]
        active_hours = []
        for date in date_arr:
            active_hour = date[date.find(",")+2:].replace(date[date.find(":"):-2], "")
            active_hours.append(active_hour)
            most_active_h = max(active_hours, key = active_hours.count)
        freq.append({"date": date_i, "most_active_hour": most_active_h)}
    return freq
for hour in most_active_hour(time_and_date, date):
    print(f"in {hour['date']} conversers were active at {hour['most_active_hour']}")

# Which day of the week do you usually chat the most?
print("##################################################")
def get_week(date):
    formatted_date = dt.datetime.strptime(date, "%m/%d/%y")
    week = dt.datetime.date(formatted_date).isocalendar()[1]
    return week
def most_active_day(date):
    # get weeks from date list
    weeks = list({get_week(date_i) for date_i in date})
    m_active_day = []
    for week in weeks:
        # get dates that have the same week
        days = [date_i for date_i in date if get_week(date_i) == week]
        m_active_d = max(days, key = days.count)
        month, day, year = (int(x) for x in m_active_d.split("/"))
        m_active_d = dt.date(year, month, day).strftime("%A")
        m_active_day.append({"week": week, "most_active_day": m_active_d})
    return m_active_day
for week in most_active_day(date):
    print(f"for week number {week['week']} conversers were active on {week['most_active_day']}")

# Which month have you chatted the most?
print("##################################################")
def most_active_month(date):
    # get years from date list
    years = list({dt.datetime.strptime(date_i, "%m/%d/%y").year for date_i in date})
    m_active_month = []
    for year_i in years:
    # get months that have the same year
        months = []
        for date_i in date:
            if dt.datetime.strptime(date_i, "%m/%d/%y").year == year_i:
                month, day, year = (int(x) for x in date_i.split("/"))
                months.append(dt.date(year, month, day).strftime("%B"))
        m_active_m = max(months, key = months.count)
        m_active_month.append({"year": year_i, "most_active_month": m_active_m})
    return m_active_month
for year in most_active_month(date):
    print(f"in {year['year']} conversers were active in {year['most_active_month']}")

# most-shared websites function:
print("##################################################")
def most_shared_websites(msg_list, conversers):
    m_shared_websites = {}
    url_pattern = "http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"
    for converser in conversers:
        converserk_msgs = [msg for msg in msg_list if converser in msg]
        shared_websites = [url for msg in converserk_msgs for url in re.findall(url_pattern, msg)]
        shared_websites = [links for links in shared_websites if links is not []]
        unique_shared_websites = list(set(shared_websites))
        m_shared_websites[converser] = [{web_site: shared_websites.count(web_site)} for web_site in unique_shared_websites]
    return m_shared_websites
shared_websites = most_shared_websites(msg_list, conversers)
for converser in conversers:
    if len(shared_websites[converser]) == 0:
        print("ther's no shared links")
    else:
        print(f"links shared by {converser}")
        for link in shared_websites[converser]:
            print(link)

# get first texts for every converser:
print("##################################################")
def get_first_msg(time_and_date, msgs):
    first_texts = []
    for index in range(0, len(time_and_date) - 1):
        date_format = "%m/%d/%y, %H:%M %p"
        d1 = dt.datetime.strptime(time_and_date[index], date_format)
        d2 = dt.datetime.strptime(time_and_date[index + 1], date_format)
        if (d2 - d1).seconds > 900:
            first_texts.append(msgs[index])
    return first_texts
for msg in get_first_msg(time_and_date, msg_list):
    print(msg)

# get first texts count for every converser:
print("##################################################")
def get_first_text_count(conversers, first_texts):
    converserk_first_msgs_count = []
    for converser in conversers:
        cnt = 0
        for msg in first_texts:
            if converser in msg: cnt +=1
        converserk_first_msgs_count.append({converser: cnt})
    return converserk_first_msgs_count
print(get_first_text_count(conversers, get_first_msg(time_and_date, msg_list)))

# get how long did the chat go:
print("##################################################")
def get_chat_long(time_and_date):
    date_format = "%m/%d/%y, %H:%M %p"
    first_msg_date = dt.datetime.strptime(time_and_date[0], date_format)
    last_msg_date = dt.datetime.strptime(time_and_date[len(time_and_date)-1], date_format)
    return last_msg_date - first_msg_date
