from pywinauto import application
from pywinauto import findwindows
from pywinauto.keyboard import send_keys
import time


class CCentralGUIControl:
    def __init__(self):
        self.APP_PATH = r"C:\Program Files (x86)\Choretronics\C-Central\Client\Base\FarmLine.GUI.FCentral.exe"
        self.app = application.Application(backend='uia')
        self.pid = None

    def getAllProcesses(self):
        procs = findwindows.find_elements()
        for proc in procs:
            if 'Control Units, Operation - C-Central' in proc.name:
                print(f"Found PID: {proc.process_id} for window '{proc.name}'")
                self.pid = proc.process_id


    def programeStart(self):
        self.app.start(self.APP_PATH)
        time.sleep(20)  # 프로그램이 열릴 때까지 대기
        self.pid = self.app.process

    def login(self):
        if self.app is None:
            raise Exception("Application not started.")

        window = self.app.window(title_re="Log on")



        # Password 필드에 텍스트 입력
        password_field = window.child_window(auto_id="tbPassword", control_type="Edit")
        password_field.type_keys("12345", with_spaces=True)
        ok_button = window.child_window(title="OK", auto_id="btnOk", control_type="Button")
        ok_button.click_input()

    def selectMainWindow(self):
        self.app.connect(process=self.pid)
        self.dlg = self.app['Control Units, Operation - C-Central']
        #


    def clickOverview(self):
        overviews_button = self.dlg.child_window(title="Overviews", control_type="Button")
        overviews_button.click_input()  # Simulates a click


    def clickCustomOverview(self):
        myfarm_tree_item = self.dlg.child_window(title="MyFarm", control_type="TreeItem")
        myfarm_tree_item.click_input()  # Simulates a click

        test_list_item = self.dlg.child_window(title="test", control_type="ListItem")
        test_list_item.click_input()


    def clickSetTemperPannelOnOverview(self, setTemperature):
        temperature_text = self.dlg.child_window(
            auto_id="392f7925-fe00-48ea-a701-ce016ec7382c",
            control_type="Text"
        )
        temperature_text.click_input()
        send_keys(f"{setTemperature}")

    def clickFarmOprtation(self):
        operation_button = self.dlg.child_window(title="Operation", control_type="Button")
        operation_button.click_input()  # Simulates a click

        choiyul2_tree_item = self.dlg.child_window(title="choiyul 1", control_type="TreeItem")
        choiyul2_tree_item.click_input()

    def clickCurrentCondition(self):
        #CC 버튼
        btn_current_condition_pane = self.dlg.child_window(auto_id="btnCurrentCondition", control_type="Pane")
        btn_current_condition_pane.click_input()

    def clickSetTemperature(self):
        set_temp_pane = self.dlg.child_window(
            auto_id="currentConditionsSetTemperaturesButton",
            control_type="Pane"
        )
        set_temp_pane.click_input()  # Simulates a click

    def selectSetTemperaturePannel(self, temperature):

        # self.dlg.click_input(coords=(600, 720))  # Adjust the coordinates as necessary
        set_temperature_pane = self.dlg.child_window(
            auto_id="edtSetTemperature",
            control_type="Pane"
        ) #(L2727, T753, R2817, B795)

        self.dlg.print_control_identifiers()

        set_temperature_pane.click_input()
        self.controlNumberPad(temperature)



    def clickMainManu(self):
        main_menu_pane = self.dlg.child_window(auto_id="btnMainMenu", control_type="Pane")
        main_menu_pane.click_input()

    def clickVentilationSettingsPane(self):
        ventilation_settings_pane = self.dlg.child_window(
            title="환기설정",
            auto_id="bitmapButton2",
            control_type="Pane"
        )
        ventilation_settings_pane.click_input()

    def clickMinimumVentilationTimePane(self):
        # Locate the Pane element using the title and auto_id
        minimum_ventilation_time_pane = self.dlg.child_window(
            title="최소환기 시간",
            auto_id="bitmapButton2",
            control_type="Pane"
        )
        minimum_ventilation_time_pane.click_input()

    def setOnOffValues(self, on_value, off_value):
        # 최소 환기텍스트 lblMinVentilation   (L2409, T953, R2658, B988)
        on_text_element = self.dlg.child_window(
            auto_id="edtMinVentilationOn",
            control_type="Pane"
        )
        on_text_element.click_input()
        self.controlNumberPad(on_value)

        off_text_element = self.dlg.child_window(
            auto_id="edtMinVentilationOff",
            control_type="Pane"
        )
        off_text_element.click_input()
        self.controlNumberPad(off_value)


    def controlNumberPad(self,temperature):
        temperature_str = str(temperature)

        # Map each character to the corresponding button's auto_id
        button_map = {
            '0': "button0",
            '1': "button1",
            '2': "button2",
            '3': "button3",
            '4': "button4",
            '5': "button5",
            '6': "button6",
            '7': "button7",
            '8': "button8",
            '9': "button9",
            '.': "buttonPeriod"
        }

        # Iterate over each character in the temperature string
        for char in temperature_str:
            if char in button_map:
                # Locate the button using the auto_id and click it
                button = self.dlg.child_window(auto_id=button_map[char], control_type="Button")
                button.click_input()  #

        # Click the "OK" button
        ok_button = self.dlg.child_window(auto_id="buttonOk", control_type="Button")
        ok_button.click_input()  # Simulate clicking the "OK" button



    def operateSequence(self):
        # self.programeStart()
        # self.login()

        self.selectMainWindow()
        self.clickFarmOprtation()
        # def setTemperature( tamperature):
        #     self.clickCurrentCondition()
        #     self.clickSetTemperature()
        #     self.selectSetTemperaturePannel()
        #     self.controlNumberPad(tamperature)

        def setMinVent(onTime, offTime):
            self.clickCurrentCondition()
            self.clickMainManu()
            self.clickVentilationSettingsPane()
            self.clickMinimumVentilationTimePane()
            self.selectSetTemperaturePannel(13.9)
            self.setOnOffValues(onTime, offTime)

        # setTemperature(16)
        setMinVent(61,301)
        # self.clickOverview()
        # self.clickCustomOverview()
        # self.clickSetTemperPannelOnOverview(26.8)


    # def printStructure(self):
    #     self.app.print_control_identifiers()


if __name__ == "__main__":
    ccc = CCentralGUIControl()
    ccc.getAllProcesses()
    ccc.operateSequence()
