from Close.Close_wiki import Close_wiki


def ask(input):
    # check if the input is a number may be it's type is string buy it's value is a number

    if not len(input) == 1:
        # print('input is 1: ' + str(len(input)))
        # save the question in a file hidden in the res folder .question.txt
        f = open('res/.question.txt', 'w')
        f.write(input)
        f.close()
    # read the question from the file
    f = open('res/.question.txt', 'r')
    question = f.read()
    f.close()
    # print('input is 2: ' + str(len(input)))

    close = Close_wiki(question)

    if not len(input) == 1:
        # print('input is 3: ' + str(len(input)))

        title_dict = close.get_titles()
        # global titles
        titles = ''
        for i in range(len(title_dict)):
            titles += str(i) + ' ' + title_dict[i] + '\n'
        return str(titles)
    else:
        # print('input is 4: ' + str(len(input)))
        # as for the title index
        title_index = close.set_title_index(int(input))
        print('title index is: ' + str(title_index))
        # get the text
        title = close.return_title(title_index)
        print('title is: ' + str(title))

        close.get_text()
        # get the answer
        answer = close.get_answer()
        print('answer is: ' + str(answer['answer']))
        return str(answer['answer'])


