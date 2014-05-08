num = [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]

with open('C', 'a') as tar:
    for i in num:
        f = open('corpus_' + str(i), 'r')
        for line in f:
            tar.write(line)

with open('T', 'a') as tar:
    for i in num:
        f = open('tweets_' + str(i), 'r')
        for line in f:
            tar.write(line)
