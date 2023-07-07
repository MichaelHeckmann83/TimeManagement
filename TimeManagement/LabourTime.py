import os
import csv
import datetime
from prettytable import PrettyTable


class LabourTime:

    def __init__(self):
        self.idnr = ""
        self.name = ""
        self.buffer = list()
        self.work_time = datetime.timedelta()
        self.path = ""

    @classmethod
    def create_employee(cls, idnr: str = " 008 ", name: str = " Michael Heckmann ", data: bool = False):
        instance = cls()
        instance.idnr = idnr.strip()
        instance.name = name.strip()
        instance.path = f"TimeManagement/{instance.idnr}.csv"
        instance.create_file(data)
        instance.calculate_work_time()
        print(instance.get_time_info())
        print(instance.get_table())
        print(instance.get_full_table())
        return instance

    def get_time_info(self):
        work_time = self.calculate_work_time()
        return f"{self.name} ({self.idnr}) hat {work_time} Stunden gearbeitet"

    def __str__(self):
        return self.get_time_info()

    def get_table(self):
        self.fill_buffer_clean()
        table = PrettyTable()
        table.field_names = ["Zeitstempel", "Art"]
        for date_time, change_type in self.buffer:
            in_put = [str(self.try_date(date_time))[:19], change_type]
            table.add_row(in_put)
        return table

    def get_full_table(self):
        self.fill_buffer()
        table = PrettyTable()
        table.field_names = ["Zeitstempel", "Art"]
        for date_time, change_type in self.buffer:
            table.add_row([date_time, change_type])
        return table

    def create_file(self, data: bool = False):
        fieldnames = ["date_time", "change_type"]
        try:
            with open(self.path, "x") as file:
                writer = csv.DictWriter(file, fieldnames)
                writer.writeheader()
        except FileExistsError:
            print("Mitarbeiter existiert bereits")
            return False
        else:
            if data:
                self.fill_file()
            print("Mitarbeiter erstellt")
            return True

    def fill_file(self):
        self.__set_stamp(datetime.datetime.fromisoformat("2023-01-20 10:05:57.283"), " sTaRt")
        self.__set_stamp(datetime.datetime.fromisoformat("2023-01-18 16:37:23.283"), "end")
        self.set_stamp("2023-01-20 14:32:23.283001", True)
        self.__set_stamp("2023-01-20 16:33:23.283", "EnD")
        self.__set_stamp(datetime.datetime.fromisoformat("2023-01-19 10:05:23.283"), "start ")
        self.__set_stamp("2023-01-1913:37:23.283", "enD")
        self.set_stamp(datetime.datetime.fromisoformat("2023-01-19 13:57:23.283001"), False)
        self.__set_stamp(datetime.datetime.fromisoformat("2023-01-19 14:32:23.283"), " START")
        self.__set_stamp("2023-01-21 14:32:23.283", "start")
        self.__set_stamp(datetime.datetime.fromisoformat("2023-01-19 14:32:23.283"), "start")
        self.__set_stamp(datetime.datetime.fromisoformat("2023-01-18 16:37:23.283"), " end")
        self.__set_stamp("2023-01-20 10:05:57.283", "Start")
        self.__set_stamp("2023-01-20 13:37:57.283", "eNd")
        self.__set_stamp("2023-01-20 13:37:23.283", "bumm         ")
        self.__set_stamp("2023-01-20 14:32:23.283", "blub")
        self.__set_stamp("2023-01-20 16:33:23.283", "      END")
        self.__set_stamp(datetime.datetime.fromisoformat("2023-01-19 17:07:23.283"), "end")
        return True

    def __set_stamp(self, date_time: datetime.datetime, change_type: str = "start "):
        date_time = self.try_date(date_time)
        change_type = change_type.lower().strip()
        fieldnames = ["date_time", "change_type"]
        line = {"date_time": date_time, "change_type": change_type}
        try:
            with open(self.path, "a", newline="") as file:
                writer = csv.DictWriter(file, fieldnames)
                writer.writerow(line)
        except FileNotFoundError as error:
            print(f"Mitarbeiter nicht gefunden ({error})")
            return False
        except ValueError as error:
            print(f"Zeitstempel nicht lesbar ({error})")
            return False
        else:
            return True

    def set_stamp(self, date_time: datetime.datetime, change_type: bool = True):
        date_time = self.try_date(date_time)
        if not change_type:
            return_value = self.__set_stamp(date_time, "end")
        else:
            return_value = self.__set_stamp(date_time, "start")
        return return_value

    def set_stamp_now(self, change_type: bool = True):
        return_value = self.set_stamp(datetime.datetime.now(), change_type)
        return return_value

    def __set_stamp_now(self, change_type: str = "start"):
        return_value = self.__set_stamp(datetime.datetime.now(), change_type)
        return return_value

    def stamp(self, date_time: datetime.datetime):
        self.fill_buffer()
        date_time = self.try_date(date_time)
        string = str(date_time)
        self.buffer.append([string, "start"])
        self.buffer.sort()
        index = self.buffer.index([string, "start"])
        start = self.buffer[index - 1][1] == "start"
        if bool(self.buffer) and start:
            self.set_stamp(date_time, False)
            return "end"
        else:
            self.set_stamp(date_time)
            return "start"

    def stamp_now(self):
        return_value = self.stamp(datetime.datetime.now())
        return return_value

    def delete_stamp_from_buffer(self, row):
        self.buffer.pop(row)
        return True

    def save_buffer(self):
        for date_time, change_type in self.buffer:
            self.__set_stamp(date_time, change_type)
        return True

    def delete_file(self):
        if os.path.exists(self.path):
            os.remove(self.path)
            return True
        else:
            return False

    def file_exists(self):
        return os.path.exists(self.path)

    def fill_buffer(self):
        self.buffer = []
        try:
            with open(self.path, "r") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    line = [row["date_time"], row["change_type"]]
                    self.buffer.append(line)
        except FileNotFoundError as error:
            print(f"Mitarbeiter nicht gefunden ({error})")
            return False
        except UnboundLocalError as error:
            print(f"Zeitkonto leer ({error})")
            return "Zeitkonto leer"
        else:
            return self.buffer
        finally:
            self.buffer.sort()

    def fill_buffer_clean(self):
        self.fill_buffer()
        self.clean_buffer()
        return True

    def clean_buffer(self):
        buffer = self.buffer
        self.buffer = []
        repeat = False
        start = []
        end = []
        for date_time, change_type in buffer:
            in_put = [date_time, change_type]
            if type(self.try_date(date_time)) is datetime.datetime:
                if change_type == "start" and not repeat:
                    if bool(end):
                        self.buffer.append(end)
                    start = in_put
                    repeat = True
                elif change_type == "end" and bool(start):
                    if repeat:
                        self.buffer.append(start)
                    end = in_put
                    repeat = False
        if not repeat and bool(end):
            self.buffer.append(end)
        return True

    def calculate_work_time(self):
        self.work_time = datetime.timedelta()
        self.fill_buffer_clean()
        start = datetime.timedelta()
        for date_time, change_type in self.buffer:
            if change_type == "start":
                start = date_time
            if change_type == "end":
                delta = self.try_date(date_time) - self.try_date(start)
                self.work_time = self.work_time + delta
        return self.work_time

    @staticmethod
    def try_date(date_time: datetime.datetime):
        try:
            date_time = datetime.datetime.fromisoformat(str(date_time).strip())
        except ValueError as error:
            print(f"Datum hat das falsche format ({error})")
        except TypeError as error:
            print(f"Kein Datum nicht erkannt ({error})")
        finally:
            return date_time

