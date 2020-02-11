from tkinter import *


class Gui:

    def __init__(self, root):


        #colors
        bg = "#ddd"
        fg = "#444"
        ofr = "#009999"
        white = "#eee"

        #font
        fnt = {'Helvetica',24, 'bold'}
        fnt_alt = {'Helvetica', 10}


        self.main_container = Frame(root, bg=white)
        self.main_container.pack()


        self.entries = {}



        '''
        desired layout:

        INPUT Fields
        _________________________________
        |_____________TITLE_____________|
        |   Radiator    | Width |Height |
        |_______________|_______|_______|
        | Separation    |               |
        |_______________|_______________|
        |     Type      |    |     |    |
        |_______________|____|_____|____|
        |     Title     |               |
        |_______________|_______________|
        '''

        self.containers = [0] * 5


        for i in range(0,len(self.containers)):
            self.containers[i] = Frame(self.main_container)
            self.containers[i].pack(side=TOP, fill=BOTH, expand=YES)

        self.app_title = Label(self.containers[0], text="BR187 External Fire Spread Tool", bg=ofr, fg=white, font=fnt, justify=CENTER)
        self.app_title.pack(side=TOP, fill=BOTH, expand=YES)

        self.radiator_label = Label(self.containers[1], text="Radiator Geometry")
        self.radiator_label.pack(side=LEFT)

        self.radiatior_geometry_frame = Frame(self.containers[1])
        self.radiatior_geometry_frame.pack(side=LEFT)
        self.radiatior_geometry_width_frame = Frame(self.radiatior_geometry_frame)
        self.radiatior_geometry_width_frame.pack(side=LEFT)

        self.radiatior_geometry_height_frame = Frame(self.radiatior_geometry_frame)
        self.radiatior_geometry_height_frame.pack(side=LEFT)


        self.radiator_width_label = Label(self.radiatior_geometry_width_frame, text="Width")
        self.radiator_width_label.pack(side=TOP)
        self.radiator_width_entry = Entry(self.radiatior_geometry_width_frame)
        self.radiator_width_entry.pack(side=TOP)
        self.entries['width'] = self.radiator_width_entry


        self.radiator_height_label = Label(self.radiatior_geometry_height_frame, text="Height")
        self.radiator_height_label.pack(side=TOP)
        self.radiator_height_entry = Entry(self.radiatior_geometry_height_frame)
        self.radiator_height_entry.pack(side=TOP)
        self.entries['height'] = self.radiator_height_entry



        self.separation_label = Label(self.containers[2], text="Separation")
        self.separation_label.pack(side=LEFT)

        self.separation_entry = Entry(self.containers[2])
        self.separation_entry.pack(side=RIGHT)
        self.entries['separation'] = self.separation_entry

        self.type_label = Label(self.containers[3], text="Type")
        self.type_label.pack(side=LEFT)

        self.type_entry = Entry(self.containers[3])
        self.type_entry.pack(side=RIGHT)
        self.entries['type'] = self.type_entry


        self.title_label = Label(self.containers[4], text="Title")
        self.title_label.pack(side=LEFT)

        self.title_entry = Entry(self.containers[4])
        self.title_entry.pack(side=RIGHT)
        self.entries['title'] = self.title_entry

        update_button = Button(self.main_container, text="Update", command=self.update)
        update_button.pack()

    def update(self):
        for description, entry in self.entries.items():
            print(description + ": " +str(entry.get()))



root = Tk()
gui = Gui(root)
root.mainloop()
