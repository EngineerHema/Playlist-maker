from tkinter import *
import datetime
import controller


if __name__ =="__main__":
    BG = "light green"

    years = [year for year in range(1960, datetime.datetime.now().year + 1)]
    canvas = Tk()
    canvas.config(background=BG)
    canvas.minsize(width=200, height=300)
    canvas.title("Spotify")

    header = Label(canvas, text="SPOTIFY TOP SONGS", fg="blue", bg=BG)
    header.pack(pady=10)

    playlist_name = StringVar(value="PLAYLIST NAME")
    playlist_name_entry = Entry(canvas, textvariable=playlist_name)
    playlist_name_entry.pack()

    frame = Frame(canvas)
    frame.pack(expand=True)

    listbox = Listbox(frame)
    listbox.pack(side=LEFT, fill=BOTH, expand=True)

    scrollbar = Scrollbar(frame, orient=VERTICAL, command=listbox.yview)
    scrollbar.pack(side=RIGHT, fill=Y)

    listbox.config(yscrollcommand=scrollbar.set)

    for year in years:
        listbox.insert(END, year)

    error_label = Label(canvas, text="", bg=BG)
    error_label.pack(pady=10)

    def chosenYear():
        try:
            selected_year = listbox.get(listbox.curselection())
            error_label.config(text="")
            return selected_year
        except TclError:
            error_label.config(text="Please select a year.")
            return None

    def chosenPlayListName():
        selected_name = playlist_name.get()
        if selected_name == "" or selected_name == "PLAYLIST NAME":
            error_label.config(text="Please enter a playlist name.")
            return None
        error_label.config(text="")
        return selected_name

    def on_submit():
        selected_year = chosenYear()
        selected_name = chosenPlayListName()
        
        if selected_year and selected_name:
            controller.Controller(selected_name, selected_year)



    submit = Button(frame, text="SUBMIT", command=on_submit)
    submit.pack()
    canvas.mainloop()
