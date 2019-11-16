import bs4 as bs
import urllib.request
import tkinter as tk
import sqlite3
import urllib.request

HEIGHT = 700
WIDTH = 1300
RELBUTTONHEIGHT = 0.05

def get_link_from_onclick(onclick_text):
    string_split = onclick_text.split("'")
    return string_split[1]

def get_jobs():

    source = urllib.request.urlopen(
        'https://www.hamburg.de/clp/stellensuche-online-clip/clp1/data/YM9QhJaWvZn9DYmz_iframe/rc_YM9QhJaWvZn9DYmz2_iframe.php?link_5=and&custval13=nein&freitextsuche=&custlabel59=Entgeldgruppe+1&custval43=&custlabel60=Entgeldgruppe+2&custval46=&custlabel22=Besoldungsgruppe+1&custval23=&custlabel23=Besoldungsgruppe+2&custval24=&custlabel29=Arbeitszeit&link_1=and&custval29=&custlabel35=Behoerde&link_4=and&custval2%5B%5D=&custlabel31=Bewerbungsschluss&link_2=and&bewerbungsschluss=&custlabel33=Arbeitsbeginn&link_3=and&arbeitsbeginn=&nav=suchen&dienstesuche_start=Anzeigen+suchen').read()
    soup = bs.BeautifulSoup(source, 'lxml')

    linklist =[]

    container_with_jobs = soup.body.main.find(id='clp-form-rahmen')

    for link in container_with_jobs.find_all('a'):
        if link.get_text() == "":
            continue
        linklist.append([get_link_from_onclick(link.get('onclick')), link.get_text()])

# #SQLite settings:
# conn = sqlite3.connect("hamburg_stellensuche.db")
# c = conn.cursor()

# root = tk.Tk()
# root.title("Hamburg Stellensuch by KOshey")

# #setting up the size and bg image:
# canvas = tk.Canvas(root, height = HEIGHT, width = WIDTH)
# canvas.pack()

# bg_image = tk.PhotoImage(file="money.png")
# bg_label= tk.Label(root, image= bg_image)
# bg_label.place(relheight = 1, relwidth = 1)


# root.mainloop()
