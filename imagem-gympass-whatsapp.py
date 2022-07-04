import requests as req
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import urllib
import time

def request_clients(take, skip):
    response = req.get(f'https://evo-integracao.w12app.com.br/api/v1/members?take={take}&skip={skip}',
        headers={
            "username":"PRIMAXFITNESS",
            "password":"0E2C8476-A2B2-44E2-B260-F35F24BC81CD",
            "Authorization":"Basic UFJJTUFYRklUTkVTUzowRTJDODQ3Ni1BMkIyLTQ0RTItQjI2MC1GMzVGMjRCQzgxQ0Q=",
            "Content-Type": "application/json"
            }
    )

    return response.json()

#Request total number of clients
def request_number_all_clients():
    response = req.get(f'https://evo-integracao.w12app.com.br/api/v1/members',
        headers={
            "username":"PRIMAXFITNESS",
            "password":"0E2C8476-A2B2-44E2-B260-F35F24BC81CD",
            "Authorization":"Basic UFJJTUFYRklUTkVTUzowRTJDODQ3Ni1BMkIyLTQ0RTItQjI2MC1GMzVGMjRCQzgxQ0Q=",
            "Content-Type": "application/json"
            }
    )

    return response.headers['total']

# Request one client by id
def request_client_by_id(number):
    response = req.get(f'https://evo-integracao.w12app.com.br/api/v1/members/{number}',
           headers={
            "username":"PRIMAXFITNESS",
            "password":"0E2C8476-A2B2-44E2-B260-F35F24BC81CD",
            "Authorization":"Basic UFJJTUFYRklUTkVTUzowRTJDODQ3Ni1BMkIyLTQ0RTItQjI2MC1GMzVGMjRCQzgxQ0Q=",
            "Content-Type": "application/json"
            }
    )
    return response.json()

#Format evo date to compare datetime
def format_evo_date(lastAccessDate):
    data_evo = lastAccessDate.split('-')
    data_evo_hour = data_evo[2].split('T')
    new_evo_hour = '/'.join(data_evo_hour)
    data_evo[2]= new_evo_hour
    formatted_hour = '/'.join(data_evo)
    another = formatted_hour.split('/')
    another.pop()
    formatted_another = '/'.join(another)
    data_evo_new = datetime.strptime(formatted_another, '%Y/%m/%d').date()
    return data_evo_new

def enviar_midia(midia):
    driver.find_element_by_css_selector("span[data-icon='clip']").click()
    attach = driver.find_element_by_css_selector("input[type='file']")
    attach.send_keys(midia)
    time.sleep(3)
    send = driver.find_element_by_css_selector("span[data-icon='send']")
    send.click()  

primax_clients = []

i = 0
n = 0

all_ids = int(request_number_all_clients()) + 1000

while i <= all_ids:

    response = request_clients(50, i)

# lembrar amanha quando dou getAll aparece gympassId , mas quando dou getbyid nao aparece

    print(i)
    try:
        for j in response:
            lastAcessDate = j['lastAccessDate']
            if lastAcessDate != None:
                lastAccessDate = format_evo_date(j['lastAccessDate'])
                if j['tokenGympass'] != None:
                        client = request_client_by_id(j['idMember'])
                        primax_client = []
                        for k in client['contacts']:
                            if k['contactType'] == 'Cellphone':
                                print('================================================================')
                                print(client['idMember'],client['firstName'], client['lastName'])
                                print(k['contactType'],k['description'])
                                print('================================================================')
                                primax_client.append(client['firstName'])
                                primax_client.append(client['lastName'])
                                primax_client.append(k['description'])
                            else:
                                print("contato inválido:" ,k['description'])
                        
                        primax_clients.append(primax_client)
                        n+=1
                        print("total de gympass na academia hoje:" , n)
            
        i+= 50
    except:
        print('internet caiu')    
