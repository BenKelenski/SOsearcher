#!/usr/bin/env python

import sys
import requests
import webbrowser
from bs4 import BeautifulSoup


def getQuestions(questionStr):
    flag = True
    while(flag):
        response = requests.get("https://stackoverflow.com/search?q="+questionStr)
        soup = BeautifulSoup(response.text, 'html.parser')
        questions = soup.find_all(class_="question-summary")
        if len(questions) == 0:
            print()
            print('************************************************')
            print("No results found!")
            print('************************************************')
            print()
            questionStr = input("Enter a new question: ")
        else:
            questionCnt = 1
            print('************************************************')
            for question in questions[0:5]:
                # Get title of question
                try:
                    title = question.find(class_="question-hyperlink").get_text().strip()
                except AttributeError:
                    title = "No title found"
                
                try:
                    # Find votes div
                    votes = question.find(class_="votes")
                    # Get vote text. If no text 'No' is assigned
                    votes = votes.find('strong').get_text()
                except AttributeError:
                    votes = "No"

                try:
                    # Find answer divs        
                    answers = question.find(class_="answered-accepted")
                    # Gets answer text. If no text 'No' is assigned
                    answers = answers.find('strong').get_text()
                except AttributeError:
                    answers = "No"
                
                try:
                    date = question.find(class_="started").get_text()
                    date.strip()
                except AttributeError:
                    date = "No date given"
                
                # lstrip() strips away any leading whitespace
                print(title.lstrip())
                print("Q{}: {} vote(s) & {} answer(s) {}\n".format(questionCnt, votes, answers, date))

                questionCnt+=1
            print('************************************************')
            while(True):
                questionSelect = input("Select answer(1-5) or (r)eask or (q)uit: ")
                if questionSelect.isdigit():
                    if 1 <= int(questionSelect) < 6:
                        flag = False
                        link = questions[int(questionSelect)-1]
                        link = link.find(class_="question-hyperlink")
                        link = link['href']

                        break
                elif questionSelect.lower()=='r':
                    questionStr = input("Ask new question: ")
                    questionStr.replace(" ","+")
                    break
                elif questionSelect.lower()=='q':
                    exit()
                else:
                    print('Not an option!')
    
    return link


def openAnswerPage(link):
    webbrowser.open("https://stackoverflow.com/"+link, new=2)


def main():
    if len(sys.argv)>1:
        questionStr = "+".join(sys.argv[1:])
        link = getQuestions(questionStr)
    else:
        questionStr = input("What's your error? ")
        questionStr = questionStr.replace(" ","+")
        link = getQuestions(questionStr)
    openAnswerPage(link)


if __name__ == "__main__":
    main()