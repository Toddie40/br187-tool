from tkinter import *


class Gui:

    def __init__(self, root):


        #colors
        bg = "#ddd"
        fg = "#444"
        ofr = "#009999"
        white = "#eee"

        #font
        fnt_title = 'Helvetica 18 bold'
        fnt_alt = 'Helvetica 12'
        fnt = 'Helvetica 10'

        self.closed = False #this is a bad sign already isn't it...
        self.selected_type = StringVar()

        #event stuff YES I KNOW THIS IS JANKY
        self.calculateThisLoop = False


        #GUI layout
        self.root = root



        self.main_container = Frame(root, bg=white)
        self.main_container.pack()

        self.title_container = Frame(self.main_container)
        self.title_container.pack(side=TOP, expand=YES, fill=BOTH)
        self.app_title = Label(self.title_container, text="BR187 External Fire Spread Tool", bg=ofr, fg=white, font=fnt_title, justify=CENTER)
        self.app_title.pack(side=TOP, fill=BOTH, expand=YES)


        self.io_container = Frame(self.main_container)
        self.io_container.pack(side=TOP)

        self.input_container = Frame(self.io_container)
        self.input_container.pack(side=LEFT)

        self.output_container = Frame(self.io_container, bg=bg)
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
            self.containers[i] = Frame(self.input_container)
            self.containers[i].pack(side=TOP, fill=BOTH, expand=YES)


        self.radiator_label = Label(self.containers[0], text="Radiator Geometry")
        self.radiator_label.pack(side=LEFT)

        self.radiatior_geometry_frame = Frame(self.containers[0])
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


        self.separation_label = Label(self.containers[1], text="Separation")
        self.separation_label.pack(side=LEFT)

        self.separation_entry = Entry(self.containers[1])
        self.separation_entry.pack(side=RIGHT)
        self.entries['separation'] = self.separation_entry


        # Type Selection
        self.type_label = Label(self.containers[2], text="Type")
        self.type_label.pack(side=LEFT)

        self.type_entry = Frame(self.containers[2])
        self.type_entry.pack(side=RIGHT)
        self.type_rad_p = Radiobutton(self.type_entry, text="Parallel", value='p', variable=self.selected_type).pack(side=LEFT)
        self.type_rad_p = Radiobutton(self.type_entry, text="Perpendicular", value='o', variable=self.selected_type).pack(side=LEFT)
        self.type_rad_p = Radiobutton(self.type_entry, text="Corner", value='c', variable=self.selected_type).pack(side=LEFT)
        self.entries['type'] = self.selected_type

        #Analysis title selection
        self.title_label = Label(self.containers[3], text="Title")
        self.title_label.pack(side=LEFT)

        self.title_entry = Entry(self.containers[3])
        self.title_entry.pack(side=RIGHT)
        self.entries['title'] = self.title_entry

        calculate_button = Button(self.input_container, text="Calculate", command=self.calculate)
        calculate_button.pack()


        #output container

        #frames
        self.results_title = Label(self.output_container, text="Results", font=fnt_alt, bg=bg).pack(side=TOP, expand=YES, fill=BOTH)

        self.standard_load_results = Frame(self.output_container)
        self.standard_load_results.pack(side=TOP)
        self.standard_label = Label(self.standard_load_results, text="Standard Fire Load (168 kW/sqm)", fg=fg, bg=bg, font=fnt_alt).pack()
        self.reduced_load_results = Frame(self.output_container)
        self.reduced_load_results.pack(side=TOP)
        self.reduced_label = Label(self.reduced_load_results, text="Reduced Fire Load (84 kW/sqm)", fg=fg, bg=bg, font=fnt_alt).pack()


        self.reduced_safe_distance_frame = Frame(self.reduced_load_results)
        self.reduced_safe_distance_frame.pack(side=TOP)

        self.reduced_protected_area_frame = Frame(self.reduced_load_results)
        self.reduced_protected_area_frame.pack(side=TOP)

        self.standard_safe_distance_frame = Frame(self.standard_load_results)
        self.standard_safe_distance_frame.pack(side=TOP)

        self.standard_protected_area_frame = Frame(self.standard_load_results)
        self.standard_protected_area_frame.pack(side=TOP)

        #widgets

        self.outputs = {}

        self.reduced_safe_distance_label = Label(self.reduced_safe_distance_frame, text="Minimum Safe Distance: ").pack(side=LEFT)
        self.outputs['reduced_safe_distance'] = self.reduced_safe_distance_label

        self.reduced_protected_area_label = Label(self.reduced_protected_area_frame, text="Minimum Unprotected Area:").pack(side=LEFT)
        self.reduced_protected_area_result_frame = Frame(self.reduced_protected_area_frame)
        self.reduced_protected_area_result_frame.pack(side=RIGHT, expand=YES, fill=BOTH)
        self.reduced_protected_area_frame


        self.standard_safe_distance_label = Label(self.standard_safe_distance_frame, text="Minimum Safe Distance: ").pack(side=LEFT)
        self.standard_protected_area_label = Label(self.standard_protected_area_frame, text="Minimum Unprotected Area:").pack(side=LEFT)
        self.standard_protected_area_result_frame = Frame(self.standard_protected_area_frame)
        self.standard_protected_area_result_frame.pack(side=RIGHT, expand=YES, fill=BOTH)
        self.standard_protected_area_nonsprinklered = Label(self.standard_protected_area_result_frame, text="Non-Sprinklered:").pack(side=TOP)
        self.standard_protected_area_sprinklered = Label(self.standard_protected_area_result_frame, text="Sprinklered:").pack(side=TOP)



    def calculate(self):
        self.calculateThisLoop = True


    def set_output_field(self, field, new_value):
        self.outputs[field]['text'] = new_value

    def update(self):
        try:
            self.root.update()
            return True
        except (TclError):
            self.closed = True
            return False
            # do nothing, the app is closed


def init():
    root = Tk()
    gui = Gui(root)
    return gui
