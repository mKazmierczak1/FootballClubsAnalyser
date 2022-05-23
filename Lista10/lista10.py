from operator import itemgetter
from datetime import datetime
from tkinter.scrolledtext import ScrolledText
from tkinter import *
from tkcalendar import *
import covid

# vars
config_path = ".\\config.txt"
totals = ["On", "Off"]
sort_methods = ["Date", "Number"]
orders = ["Ascending", "Descending"]
types_of_data = ["cases", "deaths"]
territories = []
territories.extend(covid.get_countries())
territories.extend(covid.get_continents())

# main window
main_window = Tk()
main_window.title("Lista 10")
main_window.geometry("390x260")

# vars bind with gui
total_value = BooleanVar()
sort_method_value = StringVar()
order_value = StringVar()
types_of_data_value = StringVar()
territories_value = StringVar()
start_date_value = StringVar()
end_date_value = StringVar()

def set_values_from_file():
    config_file = open(config_path, 'r')
    line = config_file.read()
    config_values = line.split(" ")

    total_value.set(config_values[0])
    sort_method_value.set(config_values[1])
    order_value.set(config_values[2])
    types_of_data_value.set(config_values[3])
    territories_value.set(config_values[4])
    start_date_value.set(config_values[5])
    end_date_value.set(config_values[6])

    config_file.close()

set_values_from_file()

# menu and tool bars
menubar = Menu(master=main_window)

total_menu = Menu(menubar, tearoff=0)
total_menu.add_checkbutton(label="On", variable=total_value)
menubar.add_cascade(label="Total", menu=total_menu)

sort_menu = Menu(menubar, tearoff=0)
sort_menu.add_radiobutton(label="Date", variable=sort_method_value, value="Date")
sort_menu.add_radiobutton(label="Number", variable=sort_method_value, value="Number")
menubar.add_cascade(label="Sort", menu=sort_menu)

order_menu = Menu(menubar, tearoff=0)
order_menu.add_radiobutton(label="Ascending", variable=order_value, value="Ascending")
order_menu.add_radiobutton(label="Descending", variable=order_value, value="Descending")
menubar.add_cascade(label="Order", menu=order_menu)

def do_nothing():
    nothing_window = Toplevel(main_window)
    nothing_window.title("Nothing to see here")

    text = Label(nothing_window, text="What a suprise, there is nothing to see here!", font = ("Times New Roman",25), foreground="purple", background="grey")
    text.pack()
    nothing_window.resizable(False, False)

def write_values_to_file():
    config_file = open(config_path, 'w')
    config_file.write(
        str(total_value.get()) + " " +
        str(sort_method_value.get()) + " " +
        str(order_value.get()) + " " +
        str(types_of_data_value.get()) + " " +
        str(territories_value.get()) + " " +
        str(start_date_value.get()) + " " +
        str(end_date_value.get())
    )

    config_file.close()

toolbar = Frame(main_window, borderwidth=2, relief="groove")
toolbar_label = Label(toolbar, text="Complitly useless toolbar", background='#ff1245', font = ("Times New Roman",10))
toolbar_label.grid(row=0, column=0, padx=25)
do_nothing_button = Button(toolbar,background="green", command=do_nothing, text="Nothing", font = ("Times New Roman",10))
do_nothing_button.grid(row=0, column=1, padx=25)
save_button = Button(toolbar,background="blue", command=write_values_to_file, text="Save", font = ("Times New Roman",10))
save_button.grid(row=0, column=2, padx=25)
toolbar.pack(side=TOP, fill=X)

# main frame
main_frame = Frame(main_window)
main_frame.grid_columnconfigure(1, weight=1)

# show formated data from covid file
def sort_by_date(data:list, descending):
    return sorted(data, key=itemgetter(0), reverse=descending)

def sort_by_number(data:list, descending):
    return sorted(data, key=itemgetter(2), reverse=descending)

def sort(data:list):
    global sort_method_value, order_value

    if sort_method_value.get() == "Date":
        return sort_by_date(data, order_value.get() == "Descending")
    else:
        return sort_by_number(data, order_value.get() == "Descending")

def format_record(record: tuple):
    global types_of_data_value
    return str(record[0]) + " " + record[1] + " " + str(record[2]) + " " + types_of_data_value.get()
        

def format_records(records: list):
    result = ""

    try:
        for record in records:
            result += format_record(record) + '\n'
    except:
        return "Wrong dates!"

    return result

def create_dropdown_menu(value: StringVar, menu_options: list, text: str, column, row):
    label = Label( main_frame , text = text)
    label.grid(column=column - 1, row=row, padx=10, pady=5)

    drop = OptionMenu(main_frame , value , *menu_options)
    drop.grid(column=column, row=row, padx=10, pady=5)

def show():
    global main_window, total_value, types_of_data_value
    d1 = start_date_value.get().split(".")
    d2 = end_date_value.get().split(".")
    result = ""

    if total_value.get() == False:
        result = format_records(sort(covid.show_records_from_period(datetime(int(d1[2]), int(d1[1]), int(d1[0])), 
    datetime(int(d2[2]), int(d2[1]), int(d2[0])), territories_value.get(), types_of_data_value.get())))
    else:
        result = str(covid.show_total_from_period(datetime(int(d1[2]), int(d1[1]), int(d1[0])), 
    datetime(int(d2[2]), int(d2[1]), int(d2[0])), territories_value.get(), types_of_data_value.get())) + " " + types_of_data_value.get()

    result_window = Toplevel(main_window)
    result_window.title("Result")

    text_area = ScrolledText(result_window, wrap = WORD, width = 50, height = 25, font = ("Times New Roman",15))
    text_area.insert(INSERT, result)
    text_area.configure(state ='disabled')
    text_area.pack()
    result_window.resizable(False, False)

# creating content of main frame
create_dropdown_menu(types_of_data_value, types_of_data, "Type of data", 1, 1)
create_dropdown_menu(territories_value, territories, "Territory", 1, 2)

d1 = start_date_value.get().split(".")
d2 = end_date_value.get().split(".")

start_date_label = Label( main_frame , text = "Start date")
end_date_label = Label( main_frame , text = "End date")
start_date = DateEntry(main_frame, selectmode='day', year=int(d1[2]), day=int(d1[0]), month=int(d1[1]), textvariable=start_date_value)
end_date = DateEntry(main_frame, selectmode='day', year=int(d2[2]), day=int(d2[0]), month=int(d2[1]), textvariable=end_date_value)

start_date_label.grid(column=0, row=3)
start_date.grid(column=1, row=3, padx=10, pady=5)
end_date_label.grid(column=0, row=4)
end_date.grid(column=1, row=4, padx=10, pady=5)
  
button = Button(main_frame , text = "Show" , command = show).grid(column=1, row=5, padx=10, pady=10)

# status bar
statusbar = Label(main_window, text="Status bar...", bd=1, relief=SUNKEN, anchor=W)
statusbar.pack(side=BOTTOM, fill=X)

main_frame.pack()
main_window.resizable(False, False)
main_window.config(menu=menubar)
main_window.mainloop()