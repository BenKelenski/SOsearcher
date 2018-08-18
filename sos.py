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
        questionCnt = 1
        for question in questions[0:5]:
            # Get title of question
            title = question.find(class_="question-hyperlink").get_text().replace('\n','')
            
            # Find votes div
            votes = question.find(class_="votes")
            try:
                # Get vote text. If no text 'No' is assigned
                votes = votes.find('strong').get_text()
            except AttributeError:
                votes = "No"

            # Find answer divs        
            answers = question.find(class_="answered-accepted")
            try:
                # Gets answer text. If no text 'No' is assigned
                answers = answers.find('strong').get_text()
            except AttributeError:
                answers = "No"

            # lstrip() strips away any leading whitespace
            print(title.lstrip())
            print("Q{}: {} vote(s) & {} answer(s) \n".format(questionCnt, votes, answers))

            questionCnt+=1
        questionSelect = input("Select a answer(1-5) or 'r' to redo your search: ")
        if questionSelect.isdigit():
            if 1 <= int(questionSelect) < 6:
                flag = False
        elif questionSelect=='r':
            continue

    return questionSelect

def main():
    #questionStr = input("What's your error? ")
    questionStr = "semicolon not found"
    questionStr = questionStr.replace(" ","+")
    selectedQuestion = getQuestions(questionStr)

    # div.answered-accepted
    # div.votes
    print(selectedQuestion)



    """ webbrowser.open("https://stackoverflow.com/search?q="+questionStr, new=2) """

if __name__ == "__main__":
    main()