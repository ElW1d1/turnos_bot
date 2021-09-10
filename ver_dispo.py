# -*- coding: utf-8 -*-
"""
Turnero ANAC
Created on Mon Aug 23 17:31:27 2021
Hice esto porque me hinchó las pelotas no haya nunca turno disponible.
@author: ElWidi.
"""
import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from win10toast import ToastNotifier

with open('claves.txt','r') as f:
    texto = f.read()
cuil, clave, repetir = [x.split(':')[1] for x in texto.split('\n')[:3]]

repetir = repetir == 'True'

def correr():
    llaves = {'user':{'nombre':'cuil','campo':cuil},
              'pas':{'nombre':'password_confirmacion',
                     'campo':clave}}
    
    trayectos = {            
              'pcia':'appointment.province',
              'sel_pcia':'Capital Federal',
              'loc':'appointment.locality',
              'sel_loc':'San Telmo',
              'para_mi':'',
               'sede':'appointment.healthcenter',
             'boton_login':'login',
             'boton_sacar_turno':'SacarTurno'
             }
    
    link = 'https://mi.argentina.gob.ar/turnos/seleccion-turno/974'
    
    driver = webdriver.Chrome('chromedriver.exe')
    driver.implicitly_wait(20)
    driver.get(link)   
    
    user = driver.find_element_by_id(llaves['user']['nombre'])
    user.send_keys(llaves['user']['campo'])
    pas = driver.find_element_by_id('cuil')
    pas = driver.find_element_by_id(llaves['pas']['nombre'])
    pas.send_keys(llaves['pas']['campo'])
    driver.find_element_by_id(trayectos['boton_login']).click()
    
    
    for ele in driver.find_elements_by_name('forWhomIsIt'):
        if ele.find_element_by_xpath("./..").text == 'Para mi':
            trayectos['para_mi'] = ele.get_attribute('id')
    
    driver.find_element_by_id(trayectos['para_mi']).click()   
    driver.find_element_by_id(trayectos['boton_sacar_turno']).click()
    
    select = Select(driver.find_element_by_name(trayectos['pcia']))
    select.select_by_visible_text(trayectos['sel_pcia'])
    select = Select(driver.find_element_by_name(trayectos['loc']))
    select.select_by_visible_text(trayectos['sel_loc'])
    
    sede = driver.find_element_by_name(trayectos['sede'])
    texto = sede.find_element_by_xpath('//label/p').text
    driver.quit()
    return texto

corridas = 0

def chequear():
    texto = correr()
    global corridas
    corridas +=1
    print('Corrida '+str(corridas)+' ejecutada.\n')
    try:
        if texto != 'No hay turnos disponibles en esta sede':
            notificar = ToastNotifier()
            notificar.show_toast(title='Foliado ANAC', 
                             msg='Ya se puede sacar turno!!!',
                             duration=15)
            with open(os.getenv('userprofile')+'/desktop/ANAC.txt', 'a') as f:
                leyenda="Texto:\n\t"+texto+"\n\t"+"encontrado @ "+time.ctime()+'\n'
                f.write(leyenda)
        else:
            print('Todavía no hay turno, esperando otra hora.\n')
            notificar = ToastNotifier()
            notificar.show_toast(title='Foliado ANAC', 
                             msg='Todavía no hay turnos disponibles.',
                             duration=5)
            with open(os.getenv('userprofile')+'/desktop/ANAC.txt', 'a') as f:
                leyenda="Ejecutado sin novedad @ "+time.ctime()+'\n'
                f.write(leyenda)
            if repetir:
                time.sleep(3600)
                chequear()
    except:
        print('Todavía no hay turno, esperando otra hora.\n')
        notificar = ToastNotifier()
        notificar.show_toast(title='Foliado ANAC', 
                             msg='Todavía no hay turnos disponibles.',
                             duration=5)
        with open(os.getenv('userprofile')+'/desktop/ANAC.txt', 'a') as f:
                    leyenda="Ejecutado sin novedad @ "+time.ctime()+'\n'
                    f.write(leyenda)
        if repetir:
            time.sleep(3600)
            chequear()
        
chequear()
