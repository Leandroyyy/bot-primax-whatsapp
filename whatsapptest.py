import requests as req
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import urllib
import os

dir_path = os.getcwd()

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

primax_clients = [['Leandro', 'Cavallari', '(11)973139189']]

browser = webdriver.Chrome(executable_path="bot-primax-whatsapp\chromedriver.exe")

print(primax_clients)

def enviar_midia(midia):
    driver.find_element_by_css_selector("span[data-icon='clip']").click()
    attach = driver.find_element_by_css_selector("input[type='file']")
    attach.send_keys(midia)
    time.sleep(3)
    send = driver.find_element_by_css_selector("span[data-icon='send']")
    send.click()  

def format_clients_primax_cellphone(primax_list):
    for i in primax_list:
        
        if i != []:
            print(i)

            first_support  = i[2].replace('(','')
            second_support  = first_support.replace(')', '')

            i[2] = '55'+second_support

    return primax_list


midia = dir_path + '/bot-primax-whatsapp/imagem/imagem.jpeg'

print(midia)

new_primax_list = format_clients_primax_cellphone(primax_clients)

n=0
for i in new_primax_list:

    firstName = i[0].title()
    cellphone = i[2]

    print(len(cellphone))

    message = urllib.parse.quote(f'''Boa noite {firstName}!! Tudo bem? Estamos sentindo sua falta aqui na Primax Academia. Observamos que você não está frequentando a academia faz 5 dias hoje, gostaríamos de saber como você está? E mais, que você volte com a sua rotina de treino para que conquiste seus objetivos e melhore cada dia mais sua qualidade de vida.\nVenha treinar!!! Esperamos por você!!!''')

    link = f'https://web.whatsapp.com/send?phone={cellphone}'

    browser.get(link)

    while len(browser.find_elements_by_id('side')) < 1:
        time.sleep(20)

    try:
        if(browser.find_element_by_xpath('//*[@id="app"]/div/span[2]/div/span/div/div/div/div/div/div[2]/div/div') != None):
            print(i)
            print('número de celular está inválido')
            time.sleep(40)
    except:
        try:
            print('caiu aqui')
            print(i)
            browser.find_element_by_css_selector("span[data-icon='clip']").click()
            time.sleep(5)
            attach = browser.find_element_by_css_selector("input[type='file']")
            
            attach.send_keys(midia)
            time.sleep(3)

            send = browser.find_element_by_xpath("/html/body/div[1]/div/div/div[2]/div[2]/span/div/span/div/div/div[2]/div/div[2]/div[2]/div/div/span")
            send.click()
            #browser.find_element_by_xpath('/html/body/div[1]/div/div/div[4]/div/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[2]').send_keys(Keys.ENTER)
            time.sleep(40)
        except Exception as e:
            print("Erro ao enviar media", e)

