import bs4 as bs
import urllib.request
import tkinter as tk
import sqlite3
import urllib.request

HEIGHT = 700
WIDTH = 1300
RELBUTTONHEIGHT = 0.05

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
        params = (job[0], job[1], job[2])
        c.execute('INSERT INTO NEW VALUES (?, ?, ?)', params)
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
        joblist.append([get_id_from_link(url), link.get_text() , url])

    return joblist

def get_jobs_from_db(table):
    c.execute('SELECT * FROM {table}'.format(table = table))
    newjobs = c.fetchall()
    return newjobs

def display_jobs(listofjobs, table):
    if table == "NEW":
        textbox.delete(0.0, tk.END)
    for job in listofjobs:
        if table == "NEW":
            textbox.insert(tk.INSERT, "NEW: ")
        textbox.insert(tk.INSERT, job[2])
        textbox.insert(tk.INSERT, "\n")


#SQLite settings:
conn = sqlite3.connect("hamburg_stellensuche.db")
c = conn.cursor()

c.execute('CREATE TABLE IF NOT EXISTS "NEW" ("ID" TEXT NOT NULL,"Name" TEXT NOT NULL, "Link" TEXT NOT NULL, PRIMARY KEY ("ID"))')
c.execute('CREATE TABLE IF NOT EXISTS "OLD" ("ID" TEXT NOT NULL,"Name" TEXT NOT NULL, "Link" TEXT NOT NULL, PRIMARY KEY ("ID"))')
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

textbox = tk.Text(textframe, bg = "white",  relief = "groove", spacing1 = 10)
textbox.place(rely = 0.07, relwidth=1, relheight=0.93)

sort_jobs(get_jobs_from_web())
display_jobs(get_jobs_from_db("NEW"), "NEW")
display_jobs(get_jobs_from_db("OLD"), "OLD")
        
root.mainloop()
