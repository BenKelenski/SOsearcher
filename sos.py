#!/usr/bin/env python

import sys
import requests
import webbrowser
from bs4 import BeautifulSoup


def setSearchFlags(searchFlag):
    flagsDict = {
        '-r':'&tab=relevance',
        '-n':'&tab=newest',
        '-a':'&tab=active',
        '-v':'&tab=votes'
    }
    return flagsDict.get(searchFlag,'')


def getQuestions(questionStr, searchFlag=''):
    flag = True
    while(flag):
        response = requests.get("https://stackoverflow.com/search?q="+questionStr+searchFlag)
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
                    searchFlag = input("Set flags: ")
                    if searchFlag:
                        searchFlag = setSearchFlags(searchFlag)
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
        if len(sys.argv)>2:
            # get question from back of the list
            questionStr = sys.argv[-1].replace(' ','+')
            # get flag in 1st position of lit
            searchFlag = setSearchFlags(sys.argv[1])
            # get link
            link = getQuestions(questionStr,searchFlag)
        else:
            # get question from back of list
            questionStr = sys.argv[-1].replace(' ','+')
            # get link
            link = getQuestions(questionStr)
    else:
        # ask for question
        questionStr = input("What's your error? ")
        questionStr = questionStr.replace(" ","+")
        # Ask for flag
        searchFlag = input("Set a search flag '-r','-n','-v','-a': ")
        if not searchFlag:
            link = getQuestions(questionStr, searchFlag)
        # get flag link
        searchFlag = setSearchFlags(searchFlag)
        # get link
        link = getQuestions(questionStr, searchFlag)
    # open question in new tab or browser
    openAnswerPage(link)


if __name__ == "__main__":
    main()