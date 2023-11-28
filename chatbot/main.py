import re
import datetime
import long_responses as long


def message_probability(user_message, recognised_words, single_response=False, required_words=[]):
    message_certainty = 0
    has_required_words = True

    # Counts how many words are present in each predefined message
    for word in user_message:
        if word in recognised_words:
            message_certainty += 1

    # Calculates the percent of recognised words in a user message
    percentage = float(message_certainty) / float(len(recognised_words))

    # Checks that the required words are in the string
    for word in required_words:
        if word not in user_message:
            has_required_words = False
            break

    # Must either have the required words, or be a single response
    if has_required_words or single_response:
        return int(percentage * 100)
    else:
        return 0


def check_all_messages(message):
    highest_prob_list = {}

    # Simplifies response creation / adds it to the dict
    def response(bot_response, list_of_words, single_response=False, required_words=[]):
        nonlocal highest_prob_list
        highest_prob_list[bot_response] = message_probability(message, list_of_words, single_response, required_words)

    # Responses -------------------------------------------------------------------------------------------------------
    response('Hello!', ['hello', 'hi', 'hey', 'sup', 'heyo'], single_response=True)
    response('See you!', ['bye', 'goodbye'], single_response=True)
    response('I\'m doing fine, and you?', ['how', 'are', 'you', 'doing'], required_words=['how'])
    response('You\'re welcome!', ['thank', 'thanks'], single_response=True)
    response('Why did the programmer quit his job? Because he didn\'t get arrays! 😄', ['tell', 'joke'],
             required_words=['tell', 'joke'])
    response(
        'Did you know that honey never spoils? Archaeologists have found pots of honey in ancient Egyptian tombs that are over 3,000 years old and still perfectly edible!',
        ['trivia', 'interesting', 'fact'], single_response=True)
    response('I recommend watching "The Shawshank Redemption." It\'s a classic!', ['recommend', 'movie'],
             required_words=['recommend', 'movie'])
    response('I recommend reading "To Kill a Mockingbird." It\'s a great book!', ['recommend', 'book'],
             required_words=['recommend', 'book'])
    # New response for time
    if 'time' in message and 'what' in message:
        current_time = datetime.datetime.now().strftime('%H:%M:%S')
        response(f"The current time is {current_time}.", ['time', 'what'])

    # New response for date
    if 'date' in message and ('today' in message or 'what' in message):
        current_date = datetime.date.today().strftime('%Y-%m-%d')
        response(f"Today's date is {current_date}.", ['date', 'today', 'what'])
    # Longer responses
    response(long.R_ADVICE, ['give', 'advice'], required_words=['advice'])
    response(long.R_EATING, ['what', 'you', 'eat'], required_words=['you', 'eat'])

    best_match = max(highest_prob_list, key=highest_prob_list.get)
    # print(highest_prob_list)
    # print(f'Best match = {best_match} | Score: {highest_prob_list[best_match]}')

    return long.unknown() if highest_prob_list[best_match] < 1 else best_match


# Used to get the response
def get_response(user_input):
    split_message = re.split(r'\s+|[,;?!.-]\s*', user_input.lower())
    response = check_all_messages(split_message)
    return response


# Testing the response system
while True:
    print('Bot: ' + get_response(input('You: ')))