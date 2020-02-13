from tkinter import *
from tkinter import filedialog
from tkinter.ttk import *

class Gui:

    def __init__(self, root):


        #colors
        bg = "#ddd"
        fg = "#444"
        ofr = "#009999"
        white = "#eee"

        #font
        fnt_title = 'Helvetica 18 bold'
        fnt_h1 = 'Helvetica 16 bold underline'
        fnt_h2 = 'Helvetica 14 bold'
        fnt_alt = 'Helvetica 12'
        fnt = 'Helvetica 10'


        style = Style()
        style.configure("TFrame", foreground=fg, background=bg, font=fnt_alt)
        style.configure("TLabel", foreground=fg, background=bg, font=fnt, justify=LEFT)
        style.configure("title.TLabel", foreground=white, background=ofr, font=fnt_title)
        style.configure("heading.TLabel", foreground=fg, background=bg, font=fnt_h1)
        style.configure("heading2.TLabel", foreground=fg, background=bg, font=fnt_h2)
        style.configure("TRadiobutton", foreground=fg, background=bg)

        self.closed = False #this is a bad sign already isn't it...
        self.selected_type = StringVar()

        #event stuff YES I KNOW THIS IS JANKY
        self.calculateThisLoop = False
        self.save = False


        #GUI layout
        self.root = root


        self.main_container = Frame(root)
        self.main_container.pack()

        self.title_container = Frame(self.main_container, style="title.TLabel")
        self.title_container.pack(side=TOP, expand=YES, fill=BOTH)
        self.app_title = Label(self.title_container, text="BR187 External Fire Spread Tool", style="title.TLabel", justify=CENTER)
        self.app_title.pack()


        self.io_container = Frame(self.main_container, padding=10)
        self.io_container.pack(side=TOP)

        self.input_container = Frame(self.io_container, padding=10)
        self.input_container.pack(side=LEFT)

        self.output_container = Frame(self.io_container, padding=10)
        self.output_container.pack(side=RIGHT, fill=BOTH, expand=YES)

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

        #input side

        self.containers = [0] * 4


        for i in range(0,len(self.containers)):
            self.containers[i] = Frame(self.input_container, padding=10)
            self.containers[i].pack(side=TOP, fill=BOTH, expand=YES)

        #Analysis title selection
        self.title_label = Label(self.containers[0], text="Title")
        self.title_label.pack(side=LEFT)

        self.title_entry = Entry(self.containers[0])
        self.title_entry.pack(side=RIGHT)
        self.entries['title'] = self.title_entry

        # Type Selection
        self.type_label = Label(self.containers[1], text="Type")
        self.type_label.pack(side=LEFT)

        self.type_entry = Frame(self.containers[1])
        self.type_entry.pack(side=RIGHT)
        self.type_rad_p = Radiobutton(self.type_entry, text="Parallel", value='p', variable=self.selected_type, style="TRadiobutton").pack(side=LEFT)
        self.type_rad_p = Radiobutton(self.type_entry, text="Perpendicular", value='o', variable=self.selected_type, style="TRadiobutton").pack(side=LEFT)
        self.type_rad_p = Radiobutton(self.type_entry, text="Corner", value='c', variable=self.selected_type, style="TRadiobutton").pack(side=LEFT)
        self.entries['type'] = self.selected_type


        self.radiator_label = Label(self.containers[2], text="Radiator Geometry")
        self.radiator_label.pack(side=LEFT)

        self.radiatior_geometry_frame = Frame(self.containers[2])
        self.radiatior_geometry_frame.pack(side=LEFT, expand=YES, fill=BOTH)

        self.radiatior_geometry_height_frame = Frame(self.radiatior_geometry_frame)
        self.radiatior_geometry_height_frame.pack(side=RIGHT)

        self.radiatior_geometry_width_frame = Frame(self.radiatior_geometry_frame, padding=10)
        self.radiatior_geometry_width_frame.pack(side=RIGHT)



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


        self.separation_label = Label(self.containers[3], text="Separation (TWICE THE BOUNDARY DISTANCE)")
        self.separation_label.pack(side=LEFT)

        self.separation_entry = Entry(self.containers[3])
        self.separation_entry.pack(side=RIGHT)
        self.entries['separation'] = self.separation_entry




        calculate_button = Button(self.input_container, text="Calculate", command=self.calculate)
        calculate_button.pack()


        #output container

        #frames
        self.results_title = Label(self.output_container, text="Results", style="heading.TLabel").pack(side=TOP, expand=YES, fill=BOTH)

        self.standard_load_results = Frame(self.output_container, padding=20)
        self.standard_load_results.pack(side=TOP, expand=YES, fill=BOTH)
        self.standard_label = Label(self.standard_load_results, text="Standard Fire Load (168 kW/sqm)", style="heading2.TLabel").pack()
        self.reduced_load_results = Frame(self.output_container, padding=20)
        self.reduced_load_results.pack(side=TOP, expand=YES, fill=BOTH)
        self.reduced_label = Label(self.reduced_load_results, text="Reduced Fire Load (84 kW/sqm)", style="heading2.TLabel").pack()

        self.save_button = Button(self.output_container, text="Save Results", command=self.save_results)
        self.save_button.pack(side=TOP)


        self.reduced_distance_frame = Frame(self.reduced_load_results)
        self.reduced_distance_frame.pack(side=TOP, expand=YES, fill=BOTH)
        self.reduced_sprinklered = Frame(self.reduced_load_results)
        self.reduced_sprinklered.pack(side=TOP, expand=YES, fill=BOTH)
        self.reduced_unsprinklered = Frame(self.reduced_load_results)
        self.reduced_unsprinklered.pack(side=TOP, expand=YES, fill=BOTH)


        self.reduced_distance_label = Label(self.reduced_distance_frame, text="Minimum Safe Distance").pack(side=LEFT)
        self.reduced_unsprinklered_label = Label(self.reduced_unsprinklered, text="Maximum Nonsprinklered Unprotected Area").pack(side=LEFT)
        self.reduced_sprinklered_label = Label(self.reduced_sprinklered, text="Maximum Sprinklered Unprotected Area").pack(side=LEFT)

        self.reduced_distance_result = Label(self.reduced_distance_frame, text="0")
        self.reduced_distance_result.pack(side=RIGHT)
        self.reduced_sprinklered_result = Label(self.reduced_sprinklered, text="0")
        self.reduced_sprinklered_result.pack(side=RIGHT)
        self.reduced_unsprinklered_result = Label(self.reduced_unsprinklered, text="0")
        self.reduced_unsprinklered_result.pack(side=RIGHT)

        self.standard_distance_frame = Frame(self.standard_load_results)
        self.standard_distance_frame.pack(side=TOP, expand=YES, fill=BOTH)
        self.standard_sprinklered = Frame(self.standard_load_results)
        self.standard_sprinklered.pack(side=TOP, expand=YES, fill=BOTH)
        self.standard_unsprinklered = Frame(self.standard_load_results)
        self.standard_unsprinklered.pack(side=TOP, expand=YES, fill=BOTH)

        self.standard_distance_label = Label(self.standard_distance_frame, text="Minimum Safe Distance").pack(side=LEFT)
        self.standard_unsprinklered_label = Label(self.standard_unsprinklered, text="Maximum Nonsprinklered Unprotected Area").pack(side=LEFT)
        self.standard_sprinklered_label = Label(self.standard_sprinklered, text="Maximum Sprinklered Unprotected Area").pack(side=LEFT)

        self.standard_distance_result = Label(self.standard_distance_frame, text="0")
        self.standard_distance_result.pack(side=RIGHT)
        self.standard_sprinklered_result = Label(self.standard_sprinklered, text="0")
        self.standard_sprinklered_result.pack(side=RIGHT)
        self.standard_unsprinklered_result = Label(self.standard_unsprinklered, text="0")
        self.standard_unsprinklered_result.pack(side=RIGHT)

    def calculate(self):
        self.calculateThisLoop = True

    def save_results(self):
        self.save_file = filedialog.asksaveasfile(mode="w")
        self.save = True

    def populate_results(self, results):
        #distances
        self.standard_distance_result.configure(text=str(results['Standard Fire Load']['Safe Distance']) + "m")
        self.reduced_distance_result.configure(text=str(results['Reduced Fire Load']['Safe Distance']) + "m")

        #protected areas
        self.standard_sprinklered_result.configure(text=str(results['Standard Fire Load']['Unprotected Area']['sprinklered']) + "%")
        self.standard_unsprinklered_result.configure(text=str(results['Standard Fire Load']['Unprotected Area']['unsprinklered']) + "%")

        self.reduced_sprinklered_result.configure(text=str(results['Reduced Fire Load']['Unprotected Area']['sprinklered']) + "%")
        self.reduced_unsprinklered_result.configure(text=str(results['Reduced Fire Load']['Unprotected Area']['unsprinklered']) + "%")

    def update(self):
        try:
            self.root.update()
            return True
        except (TclError):
            self.closed = True
            return False
            # do nothing, the app is closed


def init(title, icon):
    root = Tk()
    root.wm_title(title)
    root.iconbitmap(icon)
    gui = Gui(root)
    return gui
