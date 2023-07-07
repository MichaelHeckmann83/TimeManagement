import tkinter
from tkinter import ttk
import TimeManagement
import datetime


class Visualizer:
    def __init__(self):
        self.time_measurement = None

    @classmethod
    def build_visualizer(cls, time_measurement: TimeManagement.LabourTime.LabourTime):
        instance = cls()
        instance.time_measurement = time_measurement
        return instance

    @classmethod
    def get_visualizer(cls, idnr: str, name: str):
        time_measurement = TimeManagement.LabourTime.LabourTime.create_employee(idnr, name)
        instance = cls.build_visualizer(time_measurement)
        return instance

    @staticmethod
    def show_info(string: str, courier: bool = False, title: str = "Info"):
        if courier:
            Visualizer.show_info_font(string, "Courier 10", title)
        else:
            Visualizer.show_info_font(string, "Calibri 10", title)
        return True

    @staticmethod
    def show_info_font(string: str, font: str = "Calibri 10", title: str = "Info"):
        tki = tkinter.Tk()
        tki.title(title)
        frm = ttk.Frame(tki, padding=5)
        frm.grid()
        ttk.Label(frm, font=font, text=string).grid(padx=15, pady=5)
        ttk.Button(frm, text="Schließen", command=tki.destroy).grid(padx=10, pady=5, row=1)
        Visualizer.center(tki)
        tki.mainloop()
        return True

    def show_time_info(self):
        self.show_info(self.time_measurement.get_time_info(), False, "Zeitinfo")
        return True

    def show_table(self):
        self.show_info(self.time_measurement.get_table(), True, "Register")
        return True

    def show_full_table(self):
        self.show_info(self.time_measurement.get_full_table(), True, "Rohdaten")
        return True

    @staticmethod
    def center(tki):
        tki.update_idletasks()
        width = tki.winfo_width()
        frm_width = tki.winfo_rootx() - tki.winfo_x()
        win_width = width + 2 * frm_width
        height = tki.winfo_height()
        titlebar_height = tki.winfo_rooty() - tki.winfo_y()
        win_height = height + titlebar_height + frm_width
        x = tki.winfo_screenwidth() // 2 - win_width // 2
        y = tki.winfo_screenheight() // 2 - win_height // 2
        tki.geometry(f"{width}x{height}+{x}+{y}")
        tki.deiconify()

    def stamper(self):
        tki = tkinter.Tk()
        tki.title("Zeitstempel setzen")
        date_time = datetime.datetime.now()
        frm = ttk.Frame(tki, padding=5)
        frm.grid()
        ttk.Label(frm, font="Calibri 10", text=f"Zeitstempel setzen? {date_time}").grid(padx=10, pady=5, row=0)

        def go():
            change_typ = self.time_measurement.stamp(date_time)
            tki.destroy()
            print(date_time)
            self.show_info(f"Zeitstempel gesetzt: {date_time} {str(change_typ).capitalize()}", title="Ausgeführt")

        ttk.Button(frm, text="Ausführen", command=go).grid(padx=50, pady=5, row=1, sticky=tkinter.W)
        ttk.Button(frm, text="Abbrechen", command=tki.destroy).grid(padx=50, pady=5, row=1, sticky=tkinter.E)
        self.center(tki)
        tki.mainloop()
        return True

    def ask(self, string: str, font: str = "Calibri 10", title: str = "Info"):
        change_type = False

        def go():
            tki.destroy()
            nonlocal change_type
            change_type = True

        tki = tkinter.Tk()
        tki.title(title)
        frm = ttk.Frame(tki, padding=5)
        frm.grid()
        ttk.Label(frm, font=font, text=string).grid(padx=10, pady=5, row=0)
        ttk.Button(frm, text="Löschen", command=go).grid(padx=50, pady=5, row=1, sticky=tkinter.W)
        ttk.Button(frm, text="Abbrechen", command=tki.destroy).grid(padx=50, pady=5, row=1, sticky=tkinter.E)
        self.center(tki)
        tki.mainloop()
        return change_type

    def show_table_pretty(self, full: bool = False):
        tki = tkinter.Tk()

        def delete(row_in):
            tki.destroy()
            text = f"{self.time_measurement.buffer[row_in - 1][0]} " \
                   f"{str(self.time_measurement.buffer[row_in - 1][1]).capitalize()}"
            check = self.ask("Zeitstempel löschen? " + text, title="Löschen?")
            if check:
                self.show_info("Zeitstempel wurde gelöscht: " + text, title="Ausgeführt")
                self.time_measurement.delete_stamp_from_buffer(row_in - 1)
                self.time_measurement.delete_file()
                self.time_measurement.create_file()
                self.time_measurement.save_buffer()
                print(self.time_measurement.get_full_table)
            self.show_table_pretty(True)

        def switch():
            tki.destroy()
            if full:
                self.show_table_pretty()
            else:
                self.show_table_pretty(True)

        def add():
            tki.destroy()
            if full:
                self.stamper_admin()
                self.show_table_pretty(True)
            else:
                self.stamper()
                self.show_table_pretty()

        self.time_measurement.calculate_work_time()
        buffer = []
        if full:
            tki.title("Rohdaten")
            self.time_measurement.fill_buffer_clean()
            buffer = self.time_measurement.buffer
            self.time_measurement.fill_buffer()
        else:
            tki.title("Register")
        frm = ttk.Frame(tki, padding=10)
        frm.grid(row=0)
        row = 0
        ttk.Label(frm, font="Calibri 11 bold", text="Zeitstempel").grid(column=0, padx=10, pady=5, row=row)
        ttk.Label(frm, font="Calibri 11 bold", text="Art").grid(column=1, padx=5, pady=5, row=row, sticky=tkinter.W)
        row += 1
        repeat = False
        for date_time, change_type in self.time_measurement.buffer:
            string = [date_time, change_type]
            if not full:
                date_time = str(date_time)[:19]
                change_type = str(change_type).capitalize()
            else:
                if buffer and string in buffer:
                    if change_type == "start" and not repeat:
                        change_type = "Start v"
                        repeat = True
                    elif change_type == "end" and repeat:
                        change_type = "End ^"
                        repeat = False
            label = ttk.Label(frm, background="white", text=date_time)
            label.grid(column=0, padx=10, pady=1, row=row, sticky=tkinter.W)
            label = ttk.Label(frm, background="white", text=change_type)
            label.grid(column=1, padx=5, pady=1, row=row, sticky=tkinter.W)
            if full:
                button = ttk.Button(frm, command=lambda r=row: delete(r), text="Löschen")
                button.grid(column=2, padx=5, pady=0, row=row, sticky=tkinter.W)
            row += 1
        if full:
            string = "Hinzufügen"
        else:
            string = "Stempeln"
        ttk.Button(frm, text=string, command=add).grid(column=0, padx=10, pady=5, row=row, sticky=tkinter.E)
        frm1 = ttk.Frame(tki)
        frm1.grid(row=1)
        string = f"Name:\nIDNr:\nArbeitszeit:"
        ttk.Label(frm1, font="Calibri 10", text=string).grid(column=0, padx=5, pady=0, row=0)
        string = f"{self.time_measurement.name}\n{self.time_measurement.idnr}\n{self.time_measurement.work_time}"
        ttk.Label(frm1, font="Calibri 10", text=string).grid(column=1, padx=5, pady=0, row=0)
        frm2 = ttk.Frame(tki)
        frm2.grid(row=10)
        if full:
            string = "Register"
        else:
            string = "Rohdaten"
        ttk.Button(frm2, text=string, command=switch).grid(column=0, padx=10, pady=10, row=0)
        ttk.Button(frm2, text="Schließen", command=tki.destroy).grid(column=1, padx=10, pady=10, row=0)
        self.center(tki)
        tki.mainloop()
        return True

    def stamper_input(self):
        change_type = "start"

        def get_entry():
            in_put.clear()
            nonlocal change_type
            for entry_in in entries:
                if entry_in.get():
                    in_put.append(entry_in.get())
                else:
                    in_put.append("")
            in_put.append(change_type)
            tki.destroy()

        def start():
            nonlocal change_type
            change_type_start.set(1)
            change_type_end.set(0)
            change_type = "start"

        def end():
            nonlocal change_type
            change_type_end.set(1)
            change_type_start.set(0)
            change_type = "end"

        def destroy():
            tki.destroy()
            in_put.append("destroy")

        tki = tkinter.Tk()
        tki.title("Zeiteingabe")
        row = 0
        frm = ttk.Frame(tki, padding=10)
        frm.grid(row=0)
        strings = ("Jahr:", "Monat:", "Tag:", "Stunden:", "Minuten:", "Sekunden:", "Millisekunden:")
        entries = []
        in_put = []
        ttk.Label(frm, text="Name:").grid(column=0, pady=1, padx=5, row=row, sticky=tkinter.E)
        name = self.time_measurement.name
        ttk.Label(frm, text=name).grid(column=1, pady=1, padx=5, row=row, sticky=tkinter.W)
        row += 1
        ttk.Label(frm, text="IDNr:").grid(column=0, pady=1, padx=5, row=row, sticky=tkinter.E)
        name = self.time_measurement.idnr
        ttk.Label(frm, text=name).grid(column=1, pady=1, padx=5, row=row, sticky=tkinter.W)
        row += 1
        ttk.Label(frm, text="Arbeitszeit:").grid(column=0, pady=1, padx=5, row=row, sticky=tkinter.E)
        name = self.time_measurement.work_time
        ttk.Label(frm, text=name).grid(column=1, pady=1, padx=5, row=row, sticky=tkinter.W)
        row += 1
        for string in strings:
            ttk.Label(frm, text=string).grid(column=0, pady=1, padx=5, row=row, sticky=tkinter.E)
            entry = ttk.Entry(frm)
            entry.grid(column=1, padx=5, pady=1, row=row, sticky=tkinter.W)
            entries.append(entry)
            row += 1
        frm1 = ttk.Frame(tki, padding=0)
        frm1.grid(row=1)
        ttk.Label(frm1, text="Start:").grid(column=0, row=row)
        change_type_start = tkinter.IntVar()
        change_type_end = tkinter.IntVar()
        start()
        ttk.Radiobutton(frm1, command=start, variable=change_type_start).grid(column=1, row=row)
        ttk.Label(frm1, text="Stop:").grid(column=2, row=row)
        ttk.Radiobutton(frm1, command=end, variable=change_type_end).grid(column=3, row=row)
        row += 1
        frm2 = ttk.Frame(tki, padding=10)
        frm2.grid(row=2)
        ttk.Button(frm2, text="Hinzufügen", command=get_entry).grid(padx=10, column=0, row=row)
        ttk.Button(frm2, text="Abbrechen", command=destroy).grid(padx=10, column=1, row=row)
        self.center(tki)
        tki.mainloop()
        return in_put

    def stamper_admin(self):
        in_put = []
        while not self.try_datetime(in_put):
            in_put = self.stamper_input()
            if in_put and in_put[-1] == "destroy":
                break
            if self.check_input(in_put):
                in_put = self.default_input(in_put)
        date_time = self.try_datetime(in_put)
        if date_time:
            if in_put[-1] == "start":
                self.time_measurement.set_stamp(date_time)
                self.show_info(f"Zeitstempel wurde gesetzt: {date_time} Start", title="Ausgeführt")
            elif in_put[-1] == "end":
                self.time_measurement.set_stamp(date_time, False)
                self.show_info(f"Zeitstempel wurde gesetzt: {date_time} End", title="Ausgeführt")
        return date_time

    @staticmethod
    def try_datetime(in_put):
        try:
            date_time = datetime.datetime(int(in_put[0]), int(in_put[1]), int(in_put[2]), int(in_put[3]),
                                 int(in_put[4]), int(in_put[5]), int(in_put[6]))
        except ValueError as error:
            if not in_put[-1] == "destroy" and Visualizer.check_input(in_put):
                Visualizer.show_info(str(error).capitalize().strip())
                print(f"Daten fehlerhaft ({error})")
            return False
        except IndexError as error:
            print("Keine Daten vorhanden", error)
            return False
        else:
            return date_time

    @staticmethod
    def default_input(in_put):
        place = 0
        today = datetime.datetime.today()
        for entry in in_put:
            if not entry:
                if place == 0:
                    in_put[place] = today.year
                elif place == 1:
                    in_put[place] = today.month
                elif place == 2:
                    in_put[place] = today.day
                elif place == 7:
                    in_put[place] = "start"
                else:
                    in_put[place] = 0
            place += 1
        return in_put

    @staticmethod
    def check_input(in_put):
        check = False
        for entry in in_put[:7]:
            if entry:
                check = True
        if check:
            return True
        else:
            return False
