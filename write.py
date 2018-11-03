from nltk.sentiment.vader import SentimentIntensityAnalyzer

sid = SentimentIntensityAnalyzer()

with open('sentences.txt', 'a') as f:
    command = None
    while True:
        sentence = input('Next sentence: ')
        polarity = sid.polarity_scores(sentence)['compound']
        print(polarity)
        command = input('[w]rite, [n]ext or [e]xit? ')
        if command == 'w':
            f.write(sentence + '\n')
        elif command == 'n':
            continue
        elif command == 'e':
            exit(0)
        else:
            exit(1)
