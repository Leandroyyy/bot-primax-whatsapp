import requests as req
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

# I just can request 50 clients per request
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

#Here you can get the day you want before today
def less_days_than_today(number):
    today = datetime.date(datetime.now())

    old_day = today - timedelta(number) 

    return old_day

n = 0
i = 0

primax_clients = []

all_ids = int(request_number_all_clients()) + 1000

while i <= all_ids:

    response = request_clients(50, i)

    seven_days_before = less_days_than_today(7)

    print(i)

    try:
        for j in response:
            lastAcessDate = j['lastAccessDate']
            if lastAcessDate != None:
                lastAccessDate = format_evo_date(j['lastAccessDate'])
                if j['tokenGympass'] != None:
                        if seven_days_before == lastAccessDate:
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

def format_clients_primax_cellphone(primax_list):
    for i in primax_list:
        
        if i != []:
            first_support  = i[2].replace('(','')
            second_support  = first_support.replace(')', '')

            i[2] = '55'+second_support

    return primax_list

browser = webdriver.Chrome()

new_primax_list = format_clients_primax_cellphone(primax_clients)

for i in new_primax_list:

    firstName = i[0].title()
    lastName = i[1].title()
    cellphone = i[2]
 
    link = f'https://web.whatsapp.com/send?phone={cellphone}'

    browser.get(link)

    while len(browser.find_elements_by_id('side')) < 1:
        time.sleep(20)

    try:
        if(browser.find_element_by_xpath('//*[@id="app"]/div/span[2]/div/span/div/div/div/div/div/div[2]/div/div') != None):
            print(f'número de celular {cellphone} está inválido, nome da pessoa: {firstName} {lastName}')
            time.sleep(40)
    except:
        try:
            print(i)
            browser.find_element_by_css_selector("span[data-icon='clip']").click()
            time.sleep(5)
            attach = browser.find_element_by_css_selector("input[type='file']")
            
            attach.send_keys(midia)
            time.sleep(3)

            send = browser.find_element_by_xpath("/html/body/div[1]/div/div/div[2]/div[2]/span/div/span/div/div/div[2]/div/div[2]/div[2]/div/div/span")
            send.click()

            time.sleep(40)
        except Exception as e:
            print("Erro ao enviar media", e)


print('=======================================================')
print('finalizado')
print('=======================================================')