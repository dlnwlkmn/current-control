import requests
from bs4 import BeautifulSoup as Bs
import smtplib
import time
from datetime import datetime

class Currency:
    currentData = None
    fileData = None

    def get_currData(self):
        return self.currentData

    def get_fileData(self):
        f = open('data.txt', 'r')
        temp = f.readlines()[-1]
        f.close()
        return temp.split()

    def __init__(self, justInCase):
        self.justInCase = justInCase

    def get_currency(self):
        currency_url = '''https://www.стопкоронавирус.рф'''

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) \
            Chrome/80.0.3987.149 Safari/537.36'
        }

        full_page = requests.get(currency_url, headers=headers)
        soup = Bs(full_page.content, 'html.parser')
        currentData = soup.find_all('div', {'class': 'cv-countdown__item-value'}, 'span')

        return currentData

    def send_mail(self, text):
        """Send mail alert about extremely change currency"""

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.ehlo()

        server.login('lesh77906@gmail.com', 'pcfatrhicdocqken')
        subject = 'Coronavirus Currency Alert'
        body = text
        message = f'Subject: {subject}\n\n{body}'

        server.sendmail(
            'admin@itproger.com',
            'dln.wlkmn@gmail.com',
            message
        )

        # server.sendmail(
        #     'admin@itproger.com',
        #     'enjoy4u@bk.ru',
        #     message
        # )

        print("\nthe email has been sent")

        server.quit()

    def check_data(self):

        fileData = self.get_fileData()

        self.currentData = self.get_currency()

        if (float(fileData[0]) < float(remove_gaps(self.currentData[1].text)) and
                float(fileData[2]) <= float(remove_gaps(self.currentData[3].text)) and
                float(fileData[3]) <= float(remove_gaps(self.currentData[4].text))):
            f = open('data.txt','a')
            f.write("\n")
            tempCount = 0
            for i in self.currentData:
                if tempCount != 0:
                    f.write(remove_gaps(str(i.text)) + " ")
                tempCount += 1
            f.write(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            f.close()
            print("data has been updated...\n")
            time.sleep(3)
        else:
            self.currentData = None
            print("we all gonna die...\n")
            time.sleep(2)
            print("kidding, nothing new\n")
            time.sleep(2)

def remove_gaps(str):
    return str.replace(' ', '')

def menu():
    print("Menu\n"
          "1) Make checking request\n"
          "2) Show last results\n"
          "3) Send mail\n"
          "4) Exit")
    choice = input(">>> ")
    return choice

situation = Currency(1)

while True:
    choice = float(menu())
    if choice == 1:
       situation.check_data()
    elif choice == 2:
        fileData = situation.get_fileData()
        print(f'Cases: {fileData[0]} (+{fileData[1]}), Death: {fileData[3]}, Recovered: {fileData[2]} [actual on {fileData[4]} {fileData[5]}]' )
        input("press Enter...\n")
    elif choice == 3:
        if situation.currentData != None:
            situation.send_mail(f'The situation with coronavirus in Russia has changed!\n'
                           f'Here is the most up-to-date (on {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}) data:\n'
                           f'Cases: {remove_gaps(situation.currentData[1].text)} (+{remove_gaps(situation.currentData[2].text)})\n'
                           f'Death: {remove_gaps(situation.currentData[4].text)}\n'
                           f'Recovered: {remove_gaps(situation.currentData[3].text)}\n---\n(spamm)')
            input("press Enter...\n")
        else:
            print("there is nothing new to send!...")
            input("press Enter...\n")
    elif choice == 4:
        print("bye bye\n")
        break
    else:
        print("choise right menu option...\n")

input("press Enter to close app...")
