import bs4 as bs
import urllib.request
import tkinter as tk
import sqlite3
import urllib.request
from functools import partial
import webbrowser
from datetime import datetime

HEIGHT = 700
WIDTH = 1300
dateofposting = f"{datetime.now():%d-%m-%Y}"

def myfunction(event):
    scroll_canvas.configure(scrollregion = scroll_canvas.bbox("all"))

def get_url_from_onclick(onclick_text):
    string_split = onclick_text.split("'")
    return string_split[1]

def get_id_from_link(alink):
    alink_splitted_by_qual = alink.split("=")
    job_id = alink_splitted_by_qual[1].split("&")[0]
    return job_id

def sort_jobs(joblist):
    
    c.execute('SELECT * FROM NEW')
    newjobs = c.fetchall()
    
    for job in newjobs:

        c.execute('INSERT OR IGNORE INTO OLD SELECT * FROM NEW WHERE ID = "{jobid}"'.format(jobid = job[0]))
        c.execute('DELETE FROM NEW WHERE ID = "{jobid}"'.format(jobid = job[0]))
    
    conn.commit()

    c.execute('SELECT * FROM OLD')
    oldjobs = c.fetchall()
    id_oldjobs = [job[0] for job in oldjobs]

    for job in joblist:
        if job[0] in id_oldjobs:
            continue
        params = (job[0], job[1], job[2], job[3])
        c.execute('INSERT INTO NEW VALUES (?, ?, ?, ?)', params)
    conn.commit()


def get_jobs_from_web():

    source = urllib.request.urlopen(
        'https://www.hamburg.de/clp/stellensuche-online-clip/clp1/data/YM9QhJaWvZn9DYmz_iframe/rc_YM9QhJaWvZn9DYmz2_iframe.php?link_5=and&custval13=nein&freitextsuche=&custlabel59=Entgeldgruppe+1&custval43=&custlabel60=Entgeldgruppe+2&custval46=&custlabel22=Besoldungsgruppe+1&custval23=&custlabel23=Besoldungsgruppe+2&custval24=&custlabel29=Arbeitszeit&link_1=and&custval29=&custlabel35=Behoerde&link_4=and&custval2%5B%5D=&custlabel31=Bewerbungsschluss&link_2=and&bewerbungsschluss=&custlabel33=Arbeitsbeginn&link_3=and&arbeitsbeginn=&nav=suchen&dienstesuche_start=Anzeigen+suchen').read()
    soup = bs.BeautifulSoup(source, 'lxml')

    joblist =[]

    container_with_jobs = soup.body.main.find(id='clp-form-rahmen')

    for link in container_with_jobs.find_all('a'):
        if link.get_text() == "":
            continue
        url = get_url_from_onclick(link.get('onclick'))
        joblist.append([get_id_from_link(url), link.get_text() , url, dateofposting])

    return joblist

def get_jobs_from_db(table):
    c.execute('SELECT * FROM {table}'.format(table = table))
    newjobs = c.fetchall()
    return newjobs

def open_url(url):
    webbrowser.open(url)

def display_jobs(listofjobs, table):
    
    if table == "OLD":
        listofjobs.reverse()

    frames = []
    for n in range(len(listofjobs)):
        frame = tk.Frame(scroll_frame, bg = "white")
        frame.pack(side='top', anchor='w', fill = "x")
        # Store the current frame reference in "frames"
        frames.append(frame)

    for i, frame in enumerate(frames):
        if table == "NEW":
            new_label = tk.Label(frame, text="NEW: ", bg = "white", fg="red")
            new_label.pack(side='left', padx=10)
        label = tk.Label(frame, text=listofjobs[i][1], bg = "white")
        label.pack(side='left', fill="x", pady=10, padx = 10)
        datelabel = tk.Label(frame, text= "|     Online seit: " + listofjobs[i][3] + "     |", bg = "white", fg="grey")
        datelabel.pack(side='left', fill="x")
        openurlinbrowser = partial(open_url, listofjobs[i][2])
        url_button = tk.Button(frame, text = "Im Browser öffnen", command = openurlinbrowser)
        url_button.pack(side='left', padx = 10)

def update_infoframe():
    
    text_job_count = "Jobs verfügbar: " + str(len(get_jobs_from_db("NEW")) + len(get_jobs_from_db("OLD")))
    label_job_count = tk.Label(infoframe, text = text_job_count, bg = "bisque")
    label_job_count.pack(side = 'left', padx = 20)

    text_new_job_count = "Neue Jobs: " + str(len(get_jobs_from_db("NEW")))
    label_new_job = tk.Label(infoframe, text = text_new_job_count, bg = "bisque")
    label_new_job.pack(side = 'left', padx = 20)
    
    text_old_job_count = "Alte Jobs: " + str(len(get_jobs_from_db("OLD")))
    label_old_job = tk.Label(infoframe, text = text_old_job_count, bg = "bisque")
    label_old_job.pack(side = 'left', padx = 20)

#SQLite settings:
conn = sqlite3.connect("hamburg_stellensuche.db")
c = conn.cursor()

c.execute('CREATE TABLE IF NOT EXISTS "NEW" ("ID" TEXT NOT NULL,"Name" TEXT NOT NULL, "Link" TEXT NOT NULL, "Date" TEXT NOT NULL, PRIMARY KEY ("ID"))')
c.execute('CREATE TABLE IF NOT EXISTS "OLD" ("ID" TEXT NOT NULL,"Name" TEXT NOT NULL, "Link" TEXT NOT NULL, "Date" TEXT NOT NULL, PRIMARY KEY ("ID"))')
conn.commit()

root = tk.Tk()
root.title("Hamburg Stellensuche by KOshey")

#setting up the size and bg image:
canvas = tk.Canvas(root, height = HEIGHT, width = WIDTH)
canvas.pack()

bg_image = tk.PhotoImage(file="hamburg-als-arbeitgeber.png")
bg_label= tk.Label(root, image= bg_image)
bg_label.place(relheight = 1, relwidth = 1)

textframe = tk.Frame(root, bg = "white")
textframe.place(relx = 0.05, rely = 0.05, relwidth = 0.90, relheight = 0.90)

infoframe = tk.Frame(textframe, bg = "bisque")
infoframe.place(relheight = 0.07, relwidth=1)

scroll_canvas = tk.Canvas(textframe, bg = "white")
scroll_frame = tk.Frame(scroll_canvas)
scrollbar = tk.Scrollbar(textframe, orient = "vertical", command = scroll_canvas.yview)
scrollbar.place(relx = 0.99, rely = 0.07, relwidth=0.01, relheight=0.93)
scroll_canvas.config(yscrollcommand = scrollbar.set)
scroll_canvas.place(rely = 0.07, relwidth=1, relheight=0.93)
scroll_canvas.create_window((0,0), window = scroll_frame, anchor = 'nw')
scroll_frame.bind("<Configure>", myfunction)


#fetching, sorting and displaying the jobs
sort_jobs(get_jobs_from_web())
update_infoframe()
display_jobs(get_jobs_from_db("NEW"), "NEW")
display_jobs(get_jobs_from_db("OLD"), "OLD")
        
root.mainloop()
