import os
from datetime import datetime

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from plyer import storagepath


class MyStorageManager:
    def append(self, model, date, code):
        fileName = f"{model}-{date}.csv"
        path = os.path.join(str(storagepath.get_home_dir()), "ScannerApp")

        # Check if the "ScannerApp" directory exists, and create it if it doesn't
        if not os.path.exists(path):
            os.makedirs(path)

        # Create the CSV file if it doesn't exist
        csv_file_path = os.path.join(path, fileName)
        if not os.path.exists(csv_file_path):
            with open(csv_file_path, 'w') as file:
                print(code + ';', file=file)
        else:
            # If the file already exists, you can choose to handle it in some way, e.g., append data.
            with open(csv_file_path, 'a') as file:
                print(code + ';', file=file)
        print(csv_file_path)



class MyScreenManager(ScreenManager):
    # the models of items
    models = ["ОБН-35",
              "ОБН-75",
              "ОБН-150",
              "ОБП-300",
              "ОБПе-300",
              "ОБПе-450",
              "ОБРН-1х15",
              "ОБРН-2х15",
              "ОБРН-2х30",
              "ОБРПе-2х30",
              "ОБРПе-2х15"]

    SM = MyStorageManager()

    current_model = None

    def updateCurrentModel(self, modelNum):
        # Access the Label with id 'current_choice' and change its text
        self.current_model = self.models[modelNum]
        self.ids.current_choice.text = "Current model is " + self.current_model

    def submitCode(self):
        qr_input = str(self.ids.qr_input.text).strip()
        barcode_input = str(self.ids.barcode_input.text).strip()

        if len(qr_input) < 39 or len(qr_input) > 86:
            self.ids.current_choice.text = "QR code is wrong"
            self.ids.qr_input.text = ""
            self.ids.barcode_input.text = ""
            return

        if len(barcode_input) != 11:
            self.ids.current_choice.text = "Barcode is wrong"
            self.ids.qr_input.text = ""
            self.ids.barcode_input.text = ""
            return


        GS = chr(29)  # separator symbol

        QR_parts = []

        QR_parts.append(qr_input[:qr_input.find("91")])  # part 1

        QR_parts.append(qr_input[qr_input.find("91"):
                                 qr_input[qr_input.find("91"):].find("92") + qr_input.find("91")])  # part 2
        QR_parts.append(qr_input[qr_input[qr_input.find("91"):].find("92") + qr_input.find("91"):])  # part 3

        new_code = GS + GS.join(QR_parts) + GS + "97" + barcode_input


        current_date = str(datetime.now().strftime('%y%m%d'))
        self.SM.append(self.current_model, current_date, new_code)

        self.ids.qr_input.text = ""
        self.ids.barcode_input.text = ""


class TestApp(App):

    def build(self):
        return MyScreenManager()


if __name__ == '__main__':
    TestApp().run()
