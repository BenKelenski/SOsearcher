import sys
import requests
import webbrowser
from bs4 import BeautifulSoup


def main():
    #questionStr = input("What's your error? ")
    questionStr = "semicolon not found"
    questionStr = questionStr.replace(" ","+")
    response = requests.get("https://stackoverflow.com/search?q="+questionStr)
    soup = BeautifulSoup(response.text, 'html.parser')

    # div.answered-accepted
    # div.votes
    questions = soup.find_all(class_="question-summary")
    questCnt = 1
    for question in questions[0:5]:
        title = question.find(class_="question-hyperlink").get_text().replace('\n','')
        votes = question.find(class_="votes").get_text().replace('\n','')
        
        print("{} and {}".format(questCnt, title))
        questCnt+=1

    """ webbrowser.open("https://stackoverflow.com/search?q="+questionStr, new=2) """

if __name__ == "__main__":
    main()