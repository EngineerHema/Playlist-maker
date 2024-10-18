from bs4 import BeautifulSoup
import requests
import tkinter.messagebox
from time import sleep

scraper=BeautifulSoup()

def scrap(selected_year):
    global scraper
    
    date=str(selected_year)

    try:
        response = requests.get("https://www.officialcharts.com/charts/singles-chart/"+date)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        tkinter.messagebox.showerror("Error", f"Something went wrong! {e}\nCheck your input and try again later.")
        sleep(3)
        exit(0)
        
    scraper = BeautifulSoup(response.text, 'html.parser')

def get_songs():
    global scraper
    '''returns a list containing all songs name and artists, each in a tuple'''
    songs_info = scraper.find_all(name= "div" , class_="description block")
    return [(info.select("a span")[1].get_text(), info.select("a span")[2].get_text()) for info in songs_info]
    
    
