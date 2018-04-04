from microbit import *
import os
import speech

id = 1
custom_inf, custom_sup = 20, 30
memory = "empty"

def temperature_status(temp, borne_max, borne_min):
  if temp <= borne_max and temp >= borne_min:
    display.scroll(str(temp))
  elif temp > borne_max:
    display.scroll(str(temp) + " - HIGH")
    speech.say("Temperature is too high")
  elif temp < borne_min:
    display.scroll(str(temp) + " - LOW")
    speech.say("Temperature is too low")

def set_borne(custom_val):
    custom_val -= 0.5*button_a.get_presses()
    custom_val += 0.5*button_b.get_presses()
    display.scroll(str(custom_val))
    return custom_val

def set_bornes(custom_inf, custom_sup):
    display.scroll("Choose min")
    while not (button_a.is_pressed() and button_b.is_pressed()):
        custom_inf = set_borne(custom_inf)
    display.scroll("Choose max")
    while not (button_a.is_pressed() and button_b.is_pressed()):
        custom_sup = set_borne(custom_sup)
    return custom_inf, custom_sup

def create_file():
    with open('data.csv', 'w') as my_file:
        my_file.write("Identifiant, Temperature, Date et heure d'enregistrement")

def register_data(n, data, time_spent):
    with open('data.csv') as file:
        output = file.read()
    memory = output
    with open('data.csv', 'w') as my_File:
        my_File.write(memory + "\n" + str(n) + ", " + str(data) + ", " + str(time_spent))

    # with open('data.csv') as file:
    #     verif = file.readline()
    # display.scroll(verif)
    sleep(5000)

create_file()
while True:
  # enregistrement de la température toutes les 5000 secondes
  time = running_time()
  temp = temperature() - 4
  register_data(id, temp, time)
  id += 1

  # afficher le statut de la température
  temperature_status(temp, custom_sup, custom_inf)

  # choisir les bornes de la température min et max
  if button_a.is_pressed() and button_b.is_pressed():
    custom_inf, custom_sup = set_bornes(custom_inf, custom_sup)












