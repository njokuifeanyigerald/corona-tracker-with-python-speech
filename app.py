import requests
import json
import pyttsx3
import speech_recognition as sr 
import re
import threading
import time


APIKEY= 't_Hc1GB4FOkj'
PROJECTTOKEN = 'tN9U7jFUG2JB'
RUNTOKEN = 'tPFHv-guQC-5'


class Data:
    def __init__(self, api_key, project_token):
        self.api_key = api_key
        self.project_token = project_token
        self.params = {
            'api_key': api_key
        }
        self.data = self.get_data()

    def get_data(self):
        response = requests.get(f'https://www.parsehub.com/api/v2/projects/{self.project_token}/last_ready_run/data', params=self.params)
        data = json.loads(response.text)
        return data

    def get_total_cases(self):
        data = self.data['total']
        for content in data:
            if content['name'] == 'Coronavirus Cases:':
                return content['value']
        return 'network breakdown'
    def get_total_deaths(self):
        data = self.data['total']
        for content in data:
            if content['name'] == 'Deaths:':
                return content['value']
        return 'network breakdown'
    def get_total_recovered(self):
        data = self.data['total']
        for content in data:
            if content['name'] == 'Recovered:':
                return content['value']
        return 'network breakdown'
    
    def get_country_data(self, country):
        data =  self.data['country']
        
        for content in data:
            if content['name'].lower() == country.lower():
                return content
        return 'network breakdown'

    def get_country_list(self):
        countries = []
        for country in self.data['country']:
            countries.append(country['name'])
        
        return countries

    def update_data(self):
        response = requests.post(f'https://www.parsehub.com/api/v2/projects/{self.project_token}/run', params=self.params)
        def poll():
            time.sleep(0.1)
            oldData = self.data
            while True:
                new_data = self.get_data()
                if new_data != oldData:
                    self.data = new_data
                    print('updating data...')
                    break
                time.sleep(5)


        t = threading.Thread(target=poll)
        t.start()

data = Data(APIKEY,PROJECTTOKEN)
# print(data.update_data())
print(data.get_total_cases())
print(data.get_total_deaths())
print(data.get_total_recovered())
print(data.get_country_data('nigeria')['total_cases'])
def speak(self,text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def get_audio(self):
    r= sr.Recognizer()
    with sr.Microphone() as  source:
        audio = r.listen(source)
        said = ""
        try:
            said = r.recognize_google(audio)
        except Exception as e:
            print('exception', str(e))

    return said.lower()
def main(self):
    print('start program')
    end_word = 'end'
    exist_word = 'exit'
    stop_word = 'stop'
    country_list = data.get_country_list()

    Patterns = {
        re.compile('[\w\s] + total [\w\s] + cases'):data.get_total_cases,
        re.compile('[\w\s] + total cases'):data.get_total_cases,
        re.compile('[\w\s] + total [\w\s] + deaths'):data.get_total_cases,
        re.compile('[\w\s] + total deaths'):data.get_total_cases

    }
    countryPatterns = {
        re.compile('[\w\s] + cases [\w\s]+'):data.get_country_data['total_cases'],
        re.compile('[\w\s] + death [\w\s]+'):data.get_country_data['total_deaths']
    }
    updateCommand = 'update'

    while True:
        print('i de hear you!!!...')
        text = get_audio()
        result = None
        for pattern, func in countryPatterns.items():
            if pattern.match(text):
                words = set(text.split(' '))
                for country in country_list:
                    if country in words:
                        result = func(country)
                        break

                break
        for pattern, func in Patterns.items():
            if pattern.match(text):
                result = func()
                break
        if text == updateCommand:
            result = 'data is been updated'
            data.update_data()
        if result:
            speak(result)

        if text.find(end_word or exist_word or stop_word) != -1:
            print("exit")
            break
