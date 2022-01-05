from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QLabel, QSlider
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QThread, pyqtSignal
import edge_ui
import sys
import subprocess
import os
import time
import traceback
import queue
import thread
import serial


# class pcba_ate(pcba_ui.Ui_Form):
#    def __init__(self,Form):
#        super().setupUi(Form)
def find_touch_id():
    touch_index = -1
    cmd = "sudo cat /proc/bus/input/devices"
    res = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    mi = res.stdout.readlines()
    for n in range(0, len(mi)):
        if "fts_ts" in mi[n] or "goodix-ts" in mi[n]:
            try:
                while True:
                    n = n + 1
                    if "Handlers=" in mi[n]:
                        temp = mi[n].split(" ")
                        for p in range(0, len(temp)):
                            if "event" in temp[p]:
                                touch_index = temp[p].replace("event", "")
                                break
                        break
            except:
                pass
        # print(touch_index)
        if touch_index != -1:
            break
    return touch_index


class camera_thread(QtCore.QThread):
    my_signal_camera = pyqtSignal(str)

    def __init__(self):
        super(camera_thread, self).__init__()

    def __del__(self):
        self.wait()

    def run(self):
        subprocess.call("evtest /dev/input/event%s > test.log &" % find_touch_id(), shell=True)
        while True:
            output = os.popen("cat test.log")
            data = output.read()
            if "(ABS_MT_TRACKING_ID), value" in data:
                subprocess.call("killall evtest;killall gst-launch-1.0;", shell=True)
                self.my_signal_camera.emit("pass")
                break
            else:
                time.sleep(1)


class mbox(QtWidgets.QWidget, edge_ui.Ui_Form):
    def __init__(self, parent=None):
        super(mbox, self).__init__(parent)
        self.setupUi(self)

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.operate)
        self.timer.start(2000)

        self.funcvalue.setText(str(volume))
        self.frame_list = [self.funclte_frame,
                           self.funccamera_frame,
                           self.funcsiren_frame,
                           self.funcbat_frame,
                           self.funcspk_frame,
                           self.funcvoicecall_frame,
                           self.funcwireless_frame,
                           self.funcio_frame,
                           self.rfwifi_frame,
                           self.rfbt_frame,
                           self.rf900_frame,
                           self.rfzwave_frame,
                           self.rflte_frame,
                           self.welcome_frame]

        self.mode_list = [self.funclte,
                          self.funccamera,
                          self.funcsiren,
                          self.funcbat,
                          self.funcspk,
                          self.funcvoicecall,
                          self.funcwireless,
                          self.funcio,
                          self.funcwireless,
                          self.rfbt,
                          self.rfwifi,
                          self.rfzwave,
                          self.rf900,
                          self.rflte]

        self.funcwireless_list = [self.funcwireless_wifion,
                                  self.funcwireless_wifioff,
                                  self.funcwireless_enablebt,
                                  self.funcwireless_btscanon,
                                  self.funcwireless_btscanoff,
                                  self.funcwireless_btpair,
                                  self.funcwireless_btoff,
                                  self.funcwireless_900on,
                                  self.funcwireless_900off,
                                  self.funcwireless_345on]

        self.rfwifi_list = [self.rfwifi_modulationsend_cmd,
                            self.rfwifi_modulationsend,
                            self.rfwifi_modulationstop,
                            self.rfwifi_tonesend_cmd,
                            self.rfwifi_tonesend,
                            self.rfwifi_rxsend_cmd,
                            self.rfwifi_rxsend,
                            self.rfwifi_rxstop]

        self.funcmode.clicked.connect(self.funcmode_switch)
        self.rfmode.clicked.connect(self.rfmode_switch)
        self.funclte.clicked.connect(self.funclte_switch)
        self.funccamera.clicked.connect(self.funccamera_switch)
        self.funcsiren.clicked.connect(self.funcsiren_switch)
        self.funcbat.clicked.connect(self.funcbat_switch)
        self.funcspk.clicked.connect(self.funcspk_switch)
        self.funcvoicecall.clicked.connect(self.funcvoicecall_switch)

        self.readapn_btn.clicked.connect(self.readapn_btn_clicked)
        self.readip_btn.clicked.connect(self.readip_btn_clicked)
        self.readlte_btn.clicked.connect(self.readlte_btn_clicked)
        self.ping_btn.clicked.connect(self.ping_btn_clicked)
        self.stopping_btn.clicked.connect(self.stopping_btn_clicked)
        self.setautoapn_btn.clicked.connect(self.setautoapn_btn_clicked)
        self.setapn_btn.clicked.connect(self.setapn_btn_clicked)
        self.sendat_btn.clicked.connect(self.sendat_btn_clicked)
        self.speedtest_btn.clicked.connect(self.speedtest_btn_clicked)

        self.funcwireless.clicked.connect(self.funcwireless_switch)
        self.funcio.clicked.connect(self.funcio_switch)
        self.rfwifi.clicked.connect(self.rfwifi_switch)
        self.rfbt.clicked.connect(self.rfbt_switch)
        self.rf900.clicked.connect(self.rf900_switch)
        self.rfzwave.clicked.connect(self.rfzwave_switch)
        self.rflte.clicked.connect(self.rflte_switch)

        self.funcmode.setEnabled(True)
        self.rfmode.setEnabled(True)
        self.funclte.setEnabled(False)
        self.funccamera.setEnabled(False)
        self.funcsiren.setEnabled(False)
        self.funcbat.setEnabled(False)
        self.funcspk.setEnabled(False)
        self.funcvoicecall.setEnabled(False)
        self.funcwireless.setEnabled(False)
        self.funcio.setEnabled(False)
        self.rfwifi.setEnabled(False)
        self.rfbt.setEnabled(False)
        self.rf900.setEnabled(False)
        self.rfzwave.setEnabled(False)
        self.rflte.setEnabled(False)

        self.funclte_on.clicked.connect(self.funclte_on_clicked)
        self.funclte_mainset.clicked.connect(self.funclte_mainset_clicked)
        self.funclte_mainset_2.clicked.connect(self.funclte_mainset_2_clicked)
        self.funclte_off.clicked.connect(self.funclte_off_clicked)
        self.funccamera_on.clicked.connect(self.funccamera_on_clicked)
        self.funccamera_off.clicked.connect(self.funccamera_off_clicked)
        self.funcsiren_on.clicked.connect(self.funcsiren_on_clicked)
        self.funcsiren_off.clicked.connect(self.funcsiren_off_clicked)
        self.funccut.clicked.connect(self.funccut_clicked)
        self.funcadd.clicked.connect(self.funcadd_clicked)
        self.exittest_btn.clicked.connect(self.exittest_clicked)

        self.funcusb_detect.clicked.connect(self.usb_detect)
        self.funcbat_on.clicked.connect(self.funcbat_on_clicked)
        self.funcspk_on.clicked.connect(self.funcspk_on_clicked)
        self.funcspk_off.clicked.connect(self.funcspk_off_clicked)

        self.funcwireless_wifion.clicked.connect(self.funcwireless_wifion_clicked)
        self.funcwireless_wifioff.clicked.connect(self.funcwireless_wifioff_clicked)
        self.funcwireless_enablebt.clicked.connect(self.funcwireless_enablebt_clicked)

        self.funcwireless_btscanon.clicked.connect(self.funcwireless_btscanon_clicked)
        self.funcwireless_btscanoff.clicked.connect(self.funcwireless_btscanoff_clicked)
        self.funcwireless_btpair.clicked.connect(self.funcwireless_btpair_clicked)
        self.funcwireless_btoff.clicked.connect(self.funcwireless_btoff_clicked)
        self.funcwireless_900on.clicked.connect(self.funcwireless_900on_clicked)
        self.funcwireless_900off.clicked.connect(self.funcwireless_900off_clicked)
        self.funcwireless_345on.clicked.connect(self.funcwireless_345on_clicked)
        self.funcio_tx.clicked.connect(self.funcio_tx_clicked)
        self.funcio_rx.clicked.connect(self.funcio_rx_clicked)

        self.funcvoicecall_call.clicked.connect(self.funcvoicecall_call_clicked)
        self.funcvoicecall_receive.clicked.connect(self.funcvoicecall_receive_clicked)
        self.funcvoicecall_hangup.clicked.connect(self.funcvoicecall_hangup_clicked)

        self.sendcmd_btn.clicked.connect(self.sendcmd_btn_clicked)
        self.stop_btn.clicked.connect(self.stop_btn_clicked)

        self.rfwifi_modulationsend.clicked.connect(self.rfwifi_modulationsend_clicked)
        self.rfwifi_modulationstop.clicked.connect(self.rfwifi_modulationstop_clicked)

        self.rfwifi_modulationsend_cmd.clicked.connect(self.rfwifi_modulationsend_cmd_clicked)

        self.rfwifi_tonesend_cmd.clicked.connect(self.rfwifi_tonesend_cmd_clicked)
        self.rfwifi_tonesend.clicked.connect(self.rfwifi_tonesend_clicked)

        self.rfwifi_rxsend.clicked.connect(self.rfwifi_rxsend_clicked)
        self.rfwifi_rxsend.clicked.connect(self.rfwifi_rxstop_clicked)
        self.rfwifi_rxsend_cmd.clicked.connect(self.rfwifi_rxsend_cmd_clicked)

        self.rfbt_enable.clicked.connect(self.rfbt_enable_clicked)
        self.rfbt_disable.clicked.connect(self.rfbt_disable_clicked)
        self.rfbt_txcmd.clicked.connect(self.rfbt_txcmd_clicked)
        self.rfbt_txsend.clicked.connect(self.rfbt_txsend_clicked)
        self.rfbt_rxcmd.clicked.connect(self.rfbt_rxcmd_clicked)
        self.rfbt_rxsend.clicked.connect(self.rfbt_rxsend_clicked)

        self.rf900_txsend.clicked.connect(self.rf900_txsend_clicked)
        self.rf900_txtone.clicked.connect(self.rf900_txtone_clicked)
        self.rf900_txstop.clicked.connect(self.rf900_txstop_clicked)
        self.rf900_rxsend.clicked.connect(self.rf900_rxsend_clicked)
        self.rf900_rxcounter.clicked.connect(self.rf900_rxcounter_clicked)

        self.rfzwave_txsend.clicked.connect(self.rfzwave_txsend_clicked)
        self.rfzwave_txtone.clicked.connect(self.rfzwave_txtone_clicked)
        self.rfzwave_txstop.clicked.connect(self.rfzwave_txstop_clicked)
        self.rfzwave_rxsend.clicked.connect(self.rfzwave_rxsend_clicked)
        self.rfzwave_rxcounter.clicked.connect(self.rfzwave_rxcounter_clicked)

        self.rflte_txsend.clicked.connect(self.rflte_txsend_clicked)
        self.rflte_txstop.clicked.connect(self.rflte_txstop_clicked)
        self.rflte_rxsend.clicked.connect(self.rflte_rxsend_clicked)
        self.rflte_rxstop.clicked.connect(self.rflte_rxstop_clicked)

        self.my_camera_thread = camera_thread()
        self.my_camera_thread.my_signal_camera.connect(self.set_camera_func)

    def operate(self):
        try:
            pingout = ping_process.stdout.readlines()
            if len(pingout) != 0:
                self.cmdoutput.setText(str(pingout))
        except Exception as e:
            pass

        if not resq.empty():
            getresq = resq.get()
            if getresq[0] == "funcmode":
                if getresq[1] == True:
                    self.funcmode.setEnabled(True)
                    self.rfmode.setEnabled(True)
                    self.funclte.setEnabled(True)
                    self.funccamera.setEnabled(True)
                    self.funcsiren.setEnabled(True)
                    self.funcbat.setEnabled(True)
                    self.funcspk.setEnabled(True)
                    self.funcvoicecall.setEnabled(True)
                    self.funcwireless.setEnabled(True)
                    self.funcio.setEnabled(True)
                    self.rfwifi.setEnabled(False)
                    self.rfbt.setEnabled(False)
                    self.rf900.setEnabled(False)
                    self.rfzwave.setEnabled(False)
                    self.rflte.setEnabled(False)
                else:
                    self.funcmode.setEnabled(True)
                    self.rfmode.setEnabled(True)
                    self.cmdoutput.setText(str(getresq[1]))

            elif getresq[0] == "rfmode":
                if getresq[1] == True:
                    self.funcmode.setEnabled(True)
                    self.rfmode.setEnabled(True)
                    self.funclte.setEnabled(False)
                    self.funccamera.setEnabled(False)
                    self.funcsiren.setEnabled(False)
                    self.funcbat.setEnabled(False)
                    self.funcspk.setEnabled(False)
                    self.funcvoicecall.setEnabled(False)
                    self.funcwireless.setEnabled(False)
                    self.funcio.setEnabled(False)
                    self.rfwifi.setEnabled(True)
                    self.rfbt.setEnabled(True)
                    self.rf900.setEnabled(True)
                    self.rfzwave.setEnabled(True)
                    self.rflte.setEnabled(True)
                else:
                    self.funcmode.setEnabled(True)
                    self.rfmode.setEnabled(True)
                    self.cmdoutput.setText(str(getresq[1]))

            elif getresq[0] == "functurnonlte":
                if getresq[1] == True:
                    self.funcmode.setEnabled(True)
                    self.rfmode.setEnabled(True)
                    self.funclte_off.setEnabled(True)
                    self.funclte_mainset.setEnabled(True)
                    # self.funclte_mainset_2.setEnabled(True)
                else:
                    self.funcmode.setEnabled(True)
                    self.rfmode.setEnabled(True)
                    self.funclte_off.setEnabled(True)
                    self.funclte_mainset.setEnabled(True)
                    self.funclte_mainset_2.setEnabled(True)
                    self.cmdoutput.setText(str(getresq[1]))

            elif getresq[0] == "functurnofflte":
                if getresq[1] == True:
                    self.funcmode.setEnabled(True)
                    self.rfmode.setEnabled(True)
                    self.funclte_on.setEnabled(True)
                    self.funclte_off.setEnabled(True)
                else:
                    self.funcmode.setEnabled(True)
                    self.rfmode.setEnabled(True)
                    self.funclte_on.setEnabled(True)
                    self.funclte_off.setEnabled(True)
                    self.cmdoutput.setText(str(getresq[1]))

            elif getresq[0] == "funcmainset":
                if getresq[1] == True:
                    self.funcmode.setEnabled(True)
                    self.rfmode.setEnabled(True)
                    self.funclte_off.setEnabled(True)
                    self.funclte_mainset_2.setEnabled(True)
                else:
                    self.funcmode.setEnabled(True)
                    self.rfmode.setEnabled(True)
                    self.funclte_off.setEnabled(True)
                    self.funclte_mainset_2.setEnabled(True)
                    self.cmdoutput.setText(str(getresq[1]))

            elif getresq[0] == "funcmainseton":
                if getresq[1] == True:
                    self.funcmode.setEnabled(True)
                    self.rfmode.setEnabled(True)
                    self.funclte_off.setEnabled(True)
                    self.funclte_mainset.setEnabled(True)
                else:
                    self.funcmode.setEnabled(True)
                    self.rfmode.setEnabled(True)
                    self.funclte_off.setEnabled(True)
                    self.funclte_mainset.setEnabled(True)
                    self.cmdoutput.setText(str(getresq[1]))

            elif getresq[0] == "speedtest":
                self.cmdoutput.setText(str(getresq[1]))
                self.speedtest_btn.setEnabled(True)

            elif getresq[0] == "voicecallping":
                global ping_output
                if getresq[1] == True:
                    self.cmdoutput.setText(ping_output)
                    self.ping_btn.setEnabled(True)
                    self.funcmode.setEnabled(True)
                    self.rfmode.setEnabled(True)
                    self.showwindow(self.funcvoicecall_frame)
                else:
                    self.ping_btn.setEnabled(True)
                    self.funcmode.setEnabled(True)
                    self.rfmode.setEnabled(True)
                    self.cmdoutput.setText(str(getresq[1]))

            elif getresq[0] == "wifion":
                if getresq[1] == True:
                    self.funcmode.setEnabled(True)
                    self.rfmode.setEnabled(True)
                    self.enable_funcwireless_btn()
                    self.cmdoutput.setText(str(getresq[2]))
                else:
                    self.cmdoutput.setText(str(getresq[1]))

            elif getresq[0] == "rfwifion":
                if getresq[1] == True:
                    self.funcmode.setEnabled(True)
                    self.rfmode.setEnabled(True)
                    self.enable_rfwifi_btn()
                else:
                    self.funcmode.setEnabled(True)
                    self.rfmode.setEnabled(True)
                    self.enable_rfwifi_btn()

            elif getresq[0] == "rfturnonlte":
                if getresq[1] == True:
                    self.funcmode.setEnabled(True)
                    self.rfmode.setEnabled(True)
                    self.showwindow(self.rflte_frame)
                else:
                    self.funcmode.setEnabled(True)
                    self.rfmode.setEnabled(True)
                    self.cmdoutput.setText(str(getresq[1]))

            elif getresq[0] == "voicecallon":
                if getresq[1] == True:
                    self.funcmode.setEnabled(True)
                    self.rfmode.setEnabled(True)
                    self.showwindow(self.funcvoicecall_frame)
                else:
                    self.funcmode.setEnabled(True)
                    self.rfmode.setEnabled(True)
                    self.cmdoutput.setText(str(getresq[1]))

    def showMsg(self, message_type, title, issue):
        if message_type == "question":
            a = QtWidgets.QMessageBox.question(self, title, issue, QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
            return a == QtWidgets.QMessageBox.Yes
        if message_type == "warning":
            a = QtWidgets.QMessageBox.warning(self, title, issue, QtWidgets.QMessageBox.Ok)
        if message_type == "infomation":
            a = QtWidgets.QMessageBox.warning(self, title, issue, QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
            return a == QtWidgets.QMessageBox.Yes

    def disablemenu_btn(self):
        for n in range(0, len(self.mode_list)):
            self.mode_list[n].setEnabled(False)

    def disable_funcwireless_btn(self):
        for n in range(0, len(self.funcwireless_list)):
            self.funcwireless_list[n].setEnabled(False)

    def enable_funcwireless_btn(self):
        for n in range(0, len(self.funcwireless_list)):
            self.funcwireless_list[n].setEnabled(True)

    def disable_rfwifi_btn(self):
        for n in range(0, len(self.rfwifi_list)):
            print(n)
            self.rfwifi_list[n].setEnabled(False)

    def enable_rfwifi_btn(self):
        for n in range(0, len(self.rfwifi_list)):
            self.rfwifi_list[n].setEnabled(True)

    def showwindow(self, targetwindow):
        for n in range(0, len(self.frame_list)):
            if self.frame_list[n] != targetwindow:
                self.frame_list[n].close()
        targetwindow.show()

    def funcmode_switch(self):
        try:
            self.welcome_frame.show()
            self.disablemenu_btn()
            self.funcmode.setEnabled(False)
            self.rfmode.setEnabled(False)
            thread.start_new_thread(funcmode_switch_thread, (resq,))
        except Exception as e:
            self.cmdoutput.setText(str(e))

    def rfmode_switch(self):
        try:
            self.welcome_frame.show()
            self.disablemenu_btn()
            self.funcmode.setEnabled(False)
            self.rfmode.setEnabled(False)
            thread.start_new_thread(rfmode_switch_thread, (resq,))
        except Exception as e:
            self.cmdoutput.setText(str(e))

    def exittest_clicked(self):
        try:
            os.system("fw_setenv rootfs 2")
            os.system("tar -xjvf /run/media/mmcblk2p1/genesis-uboot.tar.bz2 -C /run/media/mmcblk2p1 --no-same-owner")
            os.system("reboot")
        except Exception as e:
            self.cmdoutput.setText(str(e))

    # LTE_PAGE
    def funclte_switch(self):
        try:
            self.disablemenu_btn()
            self.showwindow(self.funclte_frame)

        except Exception as e:
            self.cmdoutput.setText(str(e))

    def funclte_on_clicked(self):
        try:
            self.disablemenu_btn()
            self.funcmode.setEnabled(False)
            self.rfmode.setEnabled(False)
            self.funclte_off.setEnabled(False)
            self.funclte_on.setEnabled(False)
            self.funclte_mainset.setEnabled(False)
            self.funclte_mainset_2.setEnabled(False)
            thread.start_new_thread(functurnonlte_thread, (resq,))
        except Exception as e:
            self.cmdoutput.setText(str(e))

    def funclte_off_clicked(self):
        try:
            self.disablemenu_btn()
            self.funcmode.setEnabled(False)
            self.rfmode.setEnabled(False)
            self.funclte_off.setEnabled(False)
            self.funclte_on.setEnabled(False)
            thread.start_new_thread(functurnofflte_thread, (resq,))
        except Exception as e:
            self.cmdoutput.setText(str(e))

    def funclte_mainset_clicked(self):
        try:
            print("debug1")
            self.disablemenu_btn()
            self.funcmode.setEnabled(False)
            self.rfmode.setEnabled(False)
            self.funclte_off.setEnabled(False)
            self.funclte_on.setEnabled(False)
            self.funclte_mainset.setEnabled(False)
            thread.start_new_thread(funcmainset_thread, (resq,))
        except Exception as e:
            print("debug2")
            self.cmdoutput.setText(str(e))

    def funclte_mainset_2_clicked(self):
        try:
            self.disablemenu_btn()
            self.funcmode.setEnabled(False)
            self.rfmode.setEnabled(False)
            self.funclte_off.setEnabled(False)
            self.funclte_on.setEnabled(False)
            self.funclte_mainset_2.setEnabled(False)
            thread.start_new_thread(funcmainseton_thread, (resq,))
        except Exception as e:
            self.cmdoutput.setText(str(e))

    # CAMERA_PAGE
    def funccamera_switch(self):
        subprocess.call("killall backlightctl", shell=True)
        try:
            self.disablemenu_btn()
            self.showwindow(self.funccamera_frame)
        except Exception as e:
            self.cmdoutput.setText(str(e))

    def set_camera_func(self, num):
        if num == "pass":
            subprocess.call("killall gst-launch-1.0", shell=True)
            subprocess.call("killall evtest", shell=True)
            subprocess.call("rm test.log", shell=True)

    def funccamera_on_clicked(self):
        try:
            turnon_camera()
        except Exception as e:
            self.cmdoutput.setText(str(e))

    def funccamera_off_clicked(self):
        try:
            subprocess.call(
                "gst-launch-1.0 v4l2src device=/dev/video0 ! 'video/x-raw,width=640,height=480,framerate=(fraction)30/1' ! autovideosink &",
                shell=True)
            self.my_camera_thread.start()
        except Exception as e:
            self.cmdoutput.setText(str(e))

    # Siren_PAGE
    def funcsiren_switch(self):
        try:
            self.disablemenu_btn()
            self.showwindow(self.funcsiren_frame)
        except Exception as e:
            self.cmdoutput.setText(str(e))

    def funcsiren_on_clicked(self):
        try:
            turnon_piezo()
        except Exception as e:
            self.cmdoutput.setText(str(e))

    def funcsiren_off_clicked(self):
        try:
            turnoff_piezo()
        except Exception as e:
            self.cmdoutput.setText(str(e))

    def usb_detect(self):
        try:
            output = os.popen("ls /run/media/sd*\n")
            # print(output.read())
            self.cmdoutput.setText(output.read())
        except Exception as e:
            self.cmdoutput.setText(str(e))

    # BATTERY_PAGE
    def funcbat_switch(self):
        try:
            self.disablemenu_btn()
            self.showwindow(self.funcbat_frame)
        except Exception as e:
            self.cmdoutput.setText(str(e))

    def funcbat_on_clicked(self):
        try:
            enter_battery_mode()
        except Exception as e:
            self.cmdoutput.setText(str(e))

    # PLAYBACK_PAGE
    def funcspk_switch(self):
        try:
            turnon_amp()
            self.disablemenu_btn()
            self.showwindow(self.funcspk_frame)
        except Exception as e:
            self.cmdoutput.setText(str(e))

    def funccut_clicked(self):
        value = int(self.funcvalue.text())
        if 0 < value <= 15:
            value -= 1
        else:
            pass
        subprocess.call("amixer -Dhw:0 cset numid=3 %s" % value, shell=True)
        subprocess.call("amixer -Dhw:0 cset numid=4 %s" % value, shell=True)
        self.funcvalue.setText(str(value))

    def funcadd_clicked(self):
        value = int(self.funcvalue.text())
        if 0 <= value < 15:
            value += 1
        else:
            pass
        subprocess.call("amixer -Dhw:0 cset numid=3 %s" % value, shell=True)
        subprocess.call("amixer -Dhw:0 cset numid=4 %s" % value, shell=True)
        self.funcvalue.setText(str(value))

    def funcspk_on_clicked(self):
        try:
            self.funcspk_on.setEnabled(False)
            playback_on()
        except Exception as e:
            self.cmdoutput.setText(str(e))

    def funcspk_off_clicked(self):
        try:
            self.funcspk_on.setEnabled(True)
            playback_off()
        except Exception as e:
            self.cmdoutput.setText(str(e))

    # VOICECALL_PAGE
    def funcvoicecall_switch(self):
        try:
            self.showwindow(self.funcvoicecall_frame)
            turnon_amp()
            self.funcmode.setEnabled(False)
            self.rfmode.setEnabled(False)
            self.disablemenu_btn()
            thread.start_new_thread(voicecallon_thread, (resq,))
        except Exception as e:
            self.cmdoutput.setText(str(e))

    def funcvoicecall_call_clicked(self):
        try:
            self.funcvoicecall_receive.setEnabled(False)
            self.funcvoicecall_call.setEnabled(False)
            pnum = self.funcvoicecall_num.text()
            subprocess.call("echo '' > /dev/ec21_3", shell=True)
            subprocess.call("""echo "ATD%s;" > /dev/ec21_3""" % pnum, shell=True)
            time.sleep(15)
            subprocess.call("/nsc_tests/voice_over_usb/ec21_pcm_voice_call -m pcm2pcm &", shell=True)
        except Exception as e:
            self.cmdoutput.setText(str(e))

    def funcvoicecall_receive_clicked(self):
        try:
            self.funcvoicecall_receive.setEnabled(False)
            self.funcvoicecall_call.setEnabled(False)
            pnum = self.funcvoicecall_num.text()
            if pnum != "":
                subprocess.call("echo '' > /dev/ec21_3", shell=True)
                subprocess.call("echo ATA > /dev/ec21_3", shell=True)
                time.sleep(3)
                subprocess.call("/nsc_tests/voice_over_usb/ec21_pcm_voice_call -m pcm2pcm &", shell=True)
            else:
                pass
        except Exception as e:
            self.cmdoutput.setText(str(e))

    def funcvoicecall_hangup_clicked(self):
        try:
            pnum = self.funcvoicecall_num.text()
            self.funcvoicecall_receive.setEnabled(True)
            self.funcvoicecall_call.setEnabled(True)
            subprocess.call("echo '' > /dev/ec21_3", shell=True)
            subprocess.call("echo AT+CHUP > /dev/ec21_3", shell=True)
        except Exception as e:
            self.cmdoutput.setText(str(e))

    def readapn_btn_clicked(self):
        try:
            ser = serial.Serial("/dev/ec21_2", 115200, timeout=0.5)
            ser.write("AT\r\n")
            time.sleep(0.5)
            ser.write("AT+CGDCONT?\r\n")
            out = ser.readall().strip()
            self.cmdoutput.setText(out)
            ser.close()
        except Exception as e:
            self.cmdoutput.setText(str(e))

    def readip_btn_clicked(self):
        try:
            ser = serial.Serial("/dev/ec21_2", 115200, timeout=0.5)
            ser.write("AT\r\n")
            time.sleep(0.5)
            ser.write("AT+CGPADDR\r\n")
            out = ser.readall().strip()
            self.cmdoutput.setText(out)
            ser.close()
        except Exception as e:
            self.cmdoutput.setText(str(e))

    def readlte_btn_clicked(self):
        try:
            ser = serial.Serial("/dev/ec21_2", 115200, timeout=0.5)
            ser.write("AT\r\n")
            time.sleep(0.5)
            ser.write("AT+QNWINFO\r\n")
            out = ser.readall().strip()
            self.cmdoutput.setText(out)
            ser.close()
        except Exception as e:
            self.cmdoutput.setText(str(e))

    def speedtest_btn_clicked(self):
        try:
            self.cmdoutput.setText("please wait 20 seconds for result output")
            self.speedtest_btn.setEnabled(False)
            thread.start_new_thread(pspeedtest, (resq,))
        except Exception as e:
            self.cmdoutput.setText(str(e))

    def ping_thread_func():
        out = os.popen("ping www.alarm.com -c 5")

    def ping_btn_clicked(self):
        global web, flag, ping_count
        try:
            flag = 1
            self.ping_btn.setEnabled(False)
            ping_count = self.pinginter_edit.text().strip()
            web = self.web_edit.text().strip()
            thread.start_new_thread(funcvoicecall_start_thread, (resq,))
            web = self.web_edit.text().strip()
        except Exception as e:
            self.cmdoutput.setText(str(e))

    def sendat_btn_clicked(self):
        try:
            pnum = self.cmdinput.toPlainText()
            ser = serial.Serial("/dev/ec21_2", 115200, timeout=0.5)
            ser.write(b"%s\r\n" % pnum.encode())
            out = ser.readall().strip()
            self.cmdoutput.setText(out)
            ser.close()
        except Exception as e:
            self.cmdoutput.setText(str(e))

    def stopping_btn_clicked(self):
        global web, flag
        try:
            flag = 0
            self.ping_btn.setEnabled(True)
        except Exception as e:
            self.cmdoutput.setText(str(e))

    def setautoapn_btn_clicked(self):
        try:
            ser = serial.Serial("/dev/ec21_2", 115200, timeout=0.5)
            ser.write("AT+CGDCONT=1\r\n")
            out = ser.readall().strip()
            ser.write("AT+CGDCONT=2\r\n")
            out = ser.readall().strip()
            ser.write("AT+CGDCONT=3\r\n")
            out = ser.readall().strip()
            ser.write("AT+CGDCONT=4\r\n")
            out = ser.readall().strip()
            ser.write("AT+CGDCONT=5\r\n")
            out = ser.readall().strip()
            ser.write("AT+CGDCONT=6\r\n")
            out = ser.readall().strip()
            self.cmdoutput.setText(out)
            ser.close()
        except Exception as e:
            self.cmdoutput.setText(str(e))

    def setapn_btn_clicked(self):
        try:
            manual_apn = """%s""" % ((self.setapn_edit.text()).strip())
            print("""AT+CGDCONT=%s\r\n""" % manual_apn)
            ser = serial.Serial("/dev/ec21_2", 115200, timeout=0.5)
            ser.write(b"""AT+CGDCONT=%s\r\n""" % (manual_apn.encode()))
            out = ser.readall().strip()
            self.cmdoutput.setText(out)
            ser.close()
        except Exception as e:
            self.cmdoutput.setText(str(e))

    # WIRELESS_PAGE
    def funcwireless_switch(self):
        turnon_zwave()
        try:
            self.disablemenu_btn()
            self.showwindow(self.funcwireless_frame)
        except Exception as e:
            self.cmdoutput.setText(str(e))

    def funcwireless_wifion_clicked(self):
        global ssid, psd
        try:
            ssid = self.funcwireless_wifissid.text()
            psd = self.funcwireless_wifipsd.text()
            self.disable_funcwireless_btn()
            self.funcmode.setEnabled(False)
            self.rfmode.setEnabled(False)
            thread.start_new_thread(funcwireless_wifion_thread, (resq,))
        except Exception as e:
            self.cmdoutput.setText(str(e))

    def funcwireless_wifioff_clicked(self):
        try:
            subprocess.call("ifconfig wlan0 down;ifconfig wlan0 up;killall wpa_supplicant", shell=True)
        except Exception as e:
            self.cmdoutput.setText(str(e))

    def funcwireless_enablebt_clicked(self):
        try:
            subprocess.call("modprobe bcm43455 && hciattach /dev/ttymxc0 bcm43xx 3000000 flow -b -t 120;", shell=True)
            subprocess.call("systemctl restart bluetooth", shell=True)
            subprocess.call("hciconfig hci0 down", shell=True)
            subprocess.call("hciconfig hci0 up", shell=True)
            subprocess.call("hciconfig hci0 name 'edge_panel'", shell=True)
            subprocess.call("hciconfig hci0 down", shell=True)
            subprocess.call("hciconfig hci0 up", shell=True)
            self.funcwireless_enablebt.setEnabled(False)
        except Exception as e:
            self.cmdoutput.setText(str(e))

    def funcwireless_btscanon_clicked(self):
        try:
            subprocess.call("bluetoothctl scan on &", shell=True)
        except Exception as e:
            self.cmdoutput.setText(str(e))

    def funcwireless_btscanoff_clicked(self):
        try:
            # self.program_btn.setText("Programming...")
            # subprocess.call("killall bluetoothctl",shell=True)
            output = os.popen("bluetoothctl devices")
            self.cmdoutput.setText(output.read())
        except Exception as e:
            self.cmdoutput.setText(str(e))

    def funcwireless_btpair_clicked(self):
        try:
            btmac = self.funcwireless_btmac.text()
            if btmac != "":
                subprocess.call("bluetoothctl trust %s" % btmac, shell=True)
                subprocess.call("bluetoothctl discoverable on", shell=True)
                subprocess.call("bluetoothctl pairable on", shell=True)
            else:
                pass
        except Exception as e:
            self.cmdoutput.setText(str(e))

    def funcwireless_btoff_clicked(self):
        try:
            subprocess.call("hciconfig hci0 down", shell=True)
        except Exception as e:
            self.cmdoutput.setText(str(e))

    def funcwireless_900on_clicked(self):
        try:
            output = os.popen("ls /dev/")
            if "ttymxc2" in output.read():
                pass
            else:
                os.system("reboot")
            subprocess.call("stty -F /dev/ttymxc2 115200 time 5 -parenb -parodd  cs8 \
                            -hupcl -cstopb cread clocal -crtscts ignbrk -brkint -ignpar \
                            -parmrk -inpck -istrip -inlcr -igncr -icrnl -ixon -ixoff -iuclc \
                            -ixany -imaxbel -iutf8 -opost -olcuc -ocrnl -onlcr -onocr -onlret \
                            -ofill -ofdel nl0 cr0 tab0 bs0 vt0 ff0 -isig -icanon -iexten -echo \
                            -echoe -echok -echonl -noflsh -xcase -tostop -echoprt -echoctl -echoke", shell=True)
            os.system(
                "echo -en '\\x7e\\x12\\x00\\x03\\x00\\x11\\x22\\x33\\x44\\x55\\x66\\x77\\x88\\x99\\xaa\\xbb\\xcc\\xdd\\xee\\xff\\x00\\x8c\\x8c' > /dev/ttymxc2")

        except Exception as e:
            self.cmdoutput.setText(str(e))

    def funcwireless_900off_clicked(self):
        try:
            subprocess.call("stty -F /dev/ttymxc2 115200 time 5 -parenb -parodd  cs8 \
                            -hupcl -cstopb cread clocal -crtscts ignbrk -brkint -ignpar \
                            -parmrk -inpck -istrip -inlcr -igncr -icrnl -ixon -ixoff -iuclc \
                            -ixany -imaxbel -iutf8 -opost -olcuc -ocrnl -onlcr -onocr -onlret \
                            -ofill -ofdel nl0 cr0 tab0 bs0 vt0 ff0 -isig -icanon -iexten -echo \
                            -echoe -echok -echonl -noflsh -xcase -tostop -echoprt -echoctl -echoke", shell=True)

            output = os.popen("cat /dev/ttymxc2 & sleep 10;killall cat;")
            self.cmdoutput.setText(output.read())
        except Exception as e:
            self.cmdoutput.setText(str(e))

    def funcwireless_345on_clicked(self):
        try:
            subprocess.call("stty -F /dev/ttymxc2 115200 time 5 -parenb -parodd  cs8 \
                    -hupcl -cstopb cread clocal -crtscts ignbrk -brkint -ignpar \
                    -parmrk -inpck -istrip -inlcr -igncr -icrnl -ixon -ixoff -iuclc \
                    -ixany -imaxbel -iutf8 -opost -olcuc -ocrnl -onlcr -onocr -onlret \
                    -ofill -ofdel nl0 cr0 tab0 bs0 vt0 ff0 -isig -icanon -iexten -echo \
                    -echoe -echok -echonl -noflsh -xcase -tostop -echoprt -echoctl -echoke", shell=True)
            output = os.popen("cat /dev/ttymxc2 & sleep 10;killall cat;")
            self.cmdoutput.setText(output.read())
        except Exception as e:
            self.cmdoutput.setText(str(e))

    # Funcion IO PAGE
    def funcio_switch(self):
        try:
            self.disablemenu_btn()
            self.showwindow(self.funcio_frame)
        except Exception as e:
            self.cmdoutput.setText(str(e))

    def funcio_tx_clicked(self):
        try:
            subprocess.call("stty -F /dev/ttyUSB0 115200 time 5 -parenb -parodd  cs8 \
                            -hupcl -cstopb cread clocal -crtscts ignbrk -brkint -ignpar \
                            -parmrk -inpck -istrip -inlcr -igncr -icrnl -ixon -ixoff -iuclc \
                            -ixany -imaxbel -iutf8 -opost -olcuc -ocrnl -onlcr -onocr -onlret \
                            -ofill -ofdel nl0 cr0 tab0 bs0 vt0 ff0 -isig -icanon -iexten -echo \
                            -echoe -echok -echonl -noflsh -xcase -tostop -echoprt -echoctl -echoke", shell=True)
            subprocess.call("cat /dev/ttyUSB0 >> log &", shell=True)
            tx_text = self.funcio_txedit.text()
            subprocess.call("echo '%s' >> /dev/ttyUSB0 >> log" % tx_text, shell=True)
        except Exception as e:
            self.cmdoutput.setText(str(e))

    def funcio_rx_clicked(self):
        try:
            output = os.popen("cat log")
            self.funcio_rxedit.setText(output.read())
            subprocess.call("rm log", shell=True)
        except Exception as e:
            self.cmdoutput.setText(str(e))

    # RF WIFI PAGE
    def rfwifi_switch(self):
        try:
            self.disablemenu_btn()
            self.showwindow(self.rfwifi_frame)
        except Exception as e:
            self.cmdoutput.setText(str(e))

    def rfwifi_modulationsend_cmd_clicked(self):
        try:
            txmregion = self.rfwifi_region.text()
            txmband = self.rfwifi_band.text()
            txmtxbw = self.rfwifi_txbw.text()
            txmmode = self.rfwifi_mode.text()
            txmchn = self.rfwifi_channel.text()
        except:
            txmregion = "ALL"
            txmband = "b"
            txmtxbw = "-1"
            txmmode = "2g_rate -r 12 -b 20"
            txmchn = "channel 1"
        _cmd = "\
wl pkteng_stop tx \n\
wl down \n\
wl mpc 0\n\
wl country %s\n\
wl band %s\n\
wl up\n\
wl %s\n\
wl %s\n\
wl phy_watchdog 0\n\
wl scansuppress 1\n\
wl phy_forcecal 1\n\
wl phy_txpwrctrl 1\n\
wl txpwr1 -1\n\
wl pkteng_start 00:90:4c:14:43:19 tx 100 1000 0\n" % (txmregion, txmband, txmmode, txmchn)
        self.cmdinput.setText(_cmd)

    def rfwifi_modulationsend_clicked(self):
        try:
            txmregion = self.rfwifi_region.text()
            txmband = self.rfwifi_band.text()
            txmtxbw = self.rfwifi_txbw.text()
            txmmode = self.rfwifi_mode.text()
            txmchn = self.rfwifi_channel.text()
        except:
            txmregion = "ALL"
            txmband = "b"
            txmtxbw = "-1"
            txmmode = "2g_rate -r 12 -b 20"
            txmchn = "channel 1"
        self.disable_rfwifi_btn()
        self.funcmode.setEnabled(False)
        self.rfmode.setEnabled(False)
        thread.start_new_thread(rfwifi_modulationsend_thread, (txmregion, txmband, txmtxbw, txmmode, txmchn, resq,))

    def rfwifi_modulationstop_clicked(self):
        try:
            subprocess.call("""wl down""", shell=True)
            subprocess.call("""ifconfig wlan0 down""", shell=True)
            subprocess.call("""ifconfig wlan0 up""", shell=True)
        except Exception as e:
            self.cmdoutput.setText(str(e))

    def rfwifi_tonesend_clicked(self):
        subprocess.call("ifconfig wlan0 down", shell=True)
        subprocess.call("ifconfig wlan0 up", shell=True)
        try:
            txtoneband = self.rfwifi_tonefrequency.text()
            txtonechn = self.rfwifi_tonechannel.text()
        except:
            txtoneband = "b"
            txtonechn = "1"
        cmd_ = "\
wl pkteng_stop tx \n\
wl down\n\
wl up\n\
wl band %s\n\
wl rsdb_mode 0\n\
wl phy_txpwrctrl 0\n\
wl phy_txpwrindex 0 0\n\
wl mpc 0\n\
wl txchain 1\n\
wl out\n\
wl fqacurcy %s\n" % (txtoneband, txtonechn)
        try:
            subprocess.call(cmd_, shell=True)
        except Exception as e:
            self.cmdoutput.setText(str(e))

    def rfwifi_tonesend_cmd_clicked(self):
        subprocess.call("ifconfig wlan0 down", shell=True)
        subprocess.call("ifconfig wlan0 up", shell=True)
        try:
            txtoneband = self.rfwifi_tonefrequency.text()
            txtonechn = self.rfwifi_tonechannel.text()
        except:
            txtoneband = "b"
            txtonechn = "1"
        cmd_ = "\
wl pkteng_stop tx \n\
wl down\n\
wl up\n\
wl band %s\n\
wl rsdb_mode 0\n\
wl phy_txpwrctrl 0\n\
wl phy_txpwrindex 0 0\n\
wl mpc 0\n\
wl txchain 1\n\
wl out\n\
wl fqacurcy %s\n" % (txtoneband, txtonechn)
        try:
            self.cmdinput.setText(cmd_)
        except Exception as e:
            self.cmdoutput.setText(str(e))

    def rfwifi_rxsend_clicked(self):
        try:
            rxchn = self.rfwifi_rxchannel.text()
        except:
            rxchn = "chanspec 36/40"
        '''
        cmd_=""""wl down; wl band auto; wl rsdb_mode 0;wl mpc 0;wl country ALL;wl mimo_bw_cap 1;wl mimo_txbw -1;wl %s;wl txchain 1;wl rxchain 1;wl bi 65535;wl up;wl phy_watchdog 0;wl scansuppress 1;wl phy_forcecal 1;wl reset_cnts\n"""%rxchn
        '''
        try:
            subprocess.call("sudo bash /nsc_tests/gc4_fcc_app/data.sh %s" % rxchn, shell=True)
            time.sleep(10)
            # subprocess.call("wl counters",shell=True)
        except Exception as e:
            print(e)
        self.cmdinput.setText("wl counters")

    def rfwifi_rxstop_clicked(self):
        subprocess.call("wl down\n", shell=True)

    def rfwifi_rxsend_cmd_clicked(self):
        try:
            rxchn = self.rfwifi_rxchannel.text()
        except:
            rxchn = "chanspec 36/40"
        cmd_ = "\
wl pkteng_stop tx \n\
wl down\n\
wl band auto\n\
wl rsdb_mode 0\n\
wl mpc 0\n\
wl country ALL\n\
wl mimo_bw_cap 1\n\
wl mimo_txbw -1\n\
wl %s\n\
wl txchain 1\n\
wl rxchain 1\n\
wl bi 65535\n\
wl up\n\
wl phy_watchdog 0\n\
wl scansuppress 1\n\
wl phy_forcecal 1\n\
wl reset_cnts\n" % rxchn
        try:
            self.cmdinput.setText(cmd_)
        except Exception as e:
            self.cmdoutput.setText(str(e))

    # RF BT PAGE
    def rfbt_switch(self):
        try:
            self.disablemenu_btn()
            self.showwindow(self.rfbt_frame)
        except Exception as e:
            self.cmdoutput.setText(str(e))

    def rfbt_enable_clicked(self):
        try:
            subprocess.call("modprobe bcm43455", shell=True)
            subprocess.call("hciattach /dev/ttymxc0 bcm43xx 3000000 flow -b -t 120", shell=True)
            subprocess.call("hciconfig hci0 up", shell=True)
            self.rfbt_enable.setEnabled(False)
        except Exception as e:
            self.cmdoutput.setText(str(e))

    def rfbt_disable_clicked(self):
        try:
            subprocess.call("hciconfig hci0 down", shell=True)
        except Exception as e:
            self.cmdoutput.setText(str(e))

    def rfbt_txcmd_clicked(self):
        try:
            txchn = self.rfbt_txchannel.text()
        except:
            txchn = "13"
        txchn = str(hex(int(txchn))[2:])
        try:
            subprocess.call("hciconfig hci0 up", shell=True)
            self.cmdinput.setText(
                "hcitool cmd 0x03 0x0003\nhcitool cmd 0x3f 0x0051 55 44 33 22 11 00 01 %s 04 00 04 10 27 09 00 00\n" % txchn)
        except Exception as e:
            self.cmdoutput.setText(str(e))

    def rfbt_txsend_clicked(self):
        try:
            txchn = self.rfbt_txchannel.text()
        except:
            txchn = "13"
        txchn = str(hex(int(txchn))[2:])
        try:
            subprocess.call("hciconfig hci0 up", shell=True)
            subprocess.call("hcitool cmd 0x03 0x0003", shell=True)
            subprocess.call("hcitool cmd 0x3f 0x0051 55 44 33 22 11 00 01 %s 04 00 04 10 27 09 00 00\n" % txchn,
                            shell=True)
        except Exception as e:
            self.cmdoutput.setText(str(e))

    def rfbt_rxcmd_clicked(self):
        try:
            rxchn = self.rfbt_rxchannel.text()
        except:
            rxchn = "13"
        rxchn = str(hex(int(rxchn))[2:])
        try:
            self.cmdinput.setText(
                "hcitool cmd 0x03 0x0003\nhcitool cmd 0x3f 0x0052 EE FF C0 88 00 00 E8 03 %s 04 00 04 FF FF\nhcidump -x\n" % rxchn)
        except Exception as e:
            self.cmdoutput.setText(str(e))

    def rfbt_rxsend_clicked(self):
        try:
            rxchn = self.rfbt_rxchannel.text()
        except:
            rxchn = "1"
        rxchn = str(hex(int(rxchn))[2:])
        try:
            subprocess.call("hcitool cmd 0x03 0x0003", shell=True)
            subprocess.call("hcitool cmd 0x3f 0x0052 EE FF C0 88 00 00 E8 03 %s 04 00 04 FF FF" % rxchn, shell=True)
            self.cmdinput.setText("hcidump -x")
        except Exception as e:
            self.cmdoutput.setText(str(e))

    # RF 900MHZ PAGE
    def rf900_switch(self):
        try:
            self.disablemenu_btn()
            setrunm4(0)
            subprocess.call("stty -F /dev/ttymxc2 115200 time 5 -parenb -parodd  cs8 \
                    -hupcl -cstopb cread clocal -crtscts ignbrk -brkint -ignpar \
                    -parmrk -inpck -istrip -inlcr -igncr -icrnl -ixon -ixoff -iuclc \
                    -ixany -imaxbel -iutf8 -opost -olcuc -ocrnl -onlcr -onocr -onlret \
                    -ofill -ofdel nl0 cr0 tab0 bs0 vt0 ff0 -isig -icanon -iexten -echo \
                    -echoe -echok -echonl -noflsh -xcase -tostop -echoprt -echoctl -echoke", shell=True)
            self.showwindow(self.rf900_frame)
        except Exception as e:
            self.cmdoutput.setText(str(e))

    def rf900_txsend_clicked(self):
        try:
            txchn = self.rf900_txchannel.text()
        except:
            txchn = "1"
        try:
            # subprocess.call("stty -F /dev/ttymxc2 115200 cs8 -cstopb -parenb -ixon -crtscts",shell=True)
            subprocess.call("echo reset > /dev/ttymxc2", shell=True)
            time.sleep(0.1)
            subprocess.call("", shell=True)
            subprocess.call("""echo "rx 0" > /dev/ttymxc2""", shell=True)
            time.sleep(0.1)
            subprocess.call("", shell=True)
            subprocess.call("""echo "setchannel %s" > /dev/ttymxc2""" % txchn, shell=True)
            time.sleep(0.1)
            subprocess.call("", shell=True)
            subprocess.call("""echo "tx 0" > /dev/ttymxc2""", shell=True)
        except Exception as e:
            self.cmdoutput.setText(str(e))

    def rf900_txtone_clicked(self):
        try:
            txchn = self.rf900_txchannel.text()
            # print(txchn)
        except:
            txchn = "1"
        try:
            # subprocess.call("stty -F /dev/ttymxc2 115200 cs8 -cstopb -parenb -ixon -crtscts",shell=True)
            subprocess.call("", shell=True)
            subprocess.call("echo reset > /dev/ttymxc2", shell=True)
            time.sleep(0.5)
            subprocess.call("", shell=True)
            subprocess.call("""echo "rx 0" > /dev/ttymxc2""", shell=True)
            time.sleep(0.5)
            subprocess.call("", shell=True)
            subprocess.call("""echo "setchannel %s" > /dev/ttymxc2""" % txchn, shell=True)
            time.sleep(0.5)
            subprocess.call("", shell=True)
            subprocess.call("""echo "setTxTone 1" > /dev/ttymxc2""", shell=True)
        except Exception as e:
            self.cmdoutput.setText(str(e))

    def rf900_txstop_clicked(self):
        try:
            subprocess.call("""echo "reset" > /dev/ttymxc2""", shell=True)
            subprocess.call("killall cat", shell=True)
        except Exception as e:
            self.cmdoutput.setText(str(e))

    def rf900_rxsend_clicked(self):
        try:
            rxchn = self.rfbt_rxchannel.text()
        except:
            rxchn = "1"
        try:
            subprocess.call("cat /dev/ttymxc2 > log900 &", shell=True)
            subprocess.call("echo reset > /dev/ttymxc2", shell=True)
            subprocess.call("""echo "rx 0" > /dev/ttymxc2""", shell=True)
            subprocess.call("""echo "setchannel %s" > /dev/ttymxc2""" % rxchn, shell=True)
            subprocess.call("""echo "resetCounters" > /dev/ttymxc2""", shell=True)
            subprocess.call("""echo "rx 1" > /dev/ttymxc2""", shell=True)
        except Exception as e:
            self.cmdoutput.setText(str(e))

    def rf900_rxcounter_clicked(self):
        try:
            subprocess.call("""echo "status" > /dev/ttymxc2""", shell=True)
            time.sleep(1)
            output = os.popen("cat log900")
            out = output.read()
            subprocess.call("killall cat", shell=True)
            self.cmdinput.setText(out)
        except Exception as e:
            self.cmdoutput.setText(str(e))

    # RF ZWAVE PAGE
    def rfzwave_switch(self):
        try:
            turnon_zwave()
            self.disablemenu_btn()
            subprocess.call("stty -F /dev/ttyZwave 115200 time 5 -parenb -parodd  cs8 \
                    -hupcl -cstopb cread clocal -crtscts ignbrk -brkint -ignpar \
                    -parmrk -inpck -istrip -inlcr -igncr -icrnl -ixon -ixoff -iuclc \
                    -ixany -imaxbel -iutf8 -opost -olcuc -ocrnl -onlcr -onocr -onlret \
                    -ofill -ofdel nl0 cr0 tab0 bs0 vt0 ff0 -isig -icanon -iexten -echo \
                    -echoe -echok -echonl -noflsh -xcase -tostop -echoprt -echoctl -echoke", shell=True)
            self.showwindow(self.rfzwave_frame)
        except Exception as e:
            self.cmdoutput.setText(str(e))

    def rfzwave_txtone_clicked(self):
        try:
            txchn = self.rfzwave_txchannel.text()
            txpower = self.rfzwave_txpower.text()
            print(txchn, txpower)
        except:
            txchn = "1"
        try:
            os.system("""echo "" > /dev/ttyZwave""")
            os.system("""echo "reset" > /dev/ttyZwave""")
            time.sleep(0.5)
            os.system("""echo "" > /dev/ttyZwave""")
            os.system("""echo "rx 0">/dev/ttyZwave""")
            time.sleep(0.1)
            os.system("""echo "" > /dev/ttyZwave""")
            os.system("""echo "SetZwaveMode 1 3">/dev/ttyZwave""")
            time.sleep(0.1)
            os.system("""echo "" > /dev/ttyZwave""")
            os.system("""echo "setzwaveregion 1">/dev/ttyZwave""")
            time.sleep(0.1)
            os.system("""echo "" > /dev/ttyZwave""")
            os.system("""echo "setGPIOoutPin B 14 0">/dev/ttyZwave""")
            time.sleep(0.1)
            os.system("""echo "" > /dev/ttyZwave""")
            os.system("""echo "setGPIOoutPin B 15 1">/dev/ttyZwave""")
            time.sleep(0.1)
            os.system("""echo "" > /dev/ttyZwave""")
            os.system("""echo "setchannel %s" > /dev/ttyZwave""" % txchn)
            print("""echo "setchannel %s"> /dev/ttyZwave""" % txchn)
            time.sleep(0.1)
            os.system("""echo "" > /dev/ttyZwave""")
            os.system("""echo "setpower %s" > /dev/ttyZwave""" % txpower)
            print("""echo "setpower %s" >/dev/ttyZwave""" % txpower)
            time.sleep(0.1)
            os.system("""echo "" > /dev/ttyZwave""")
            os.system("""echo "setctune 0x123">/dev/ttyZwave""")
            time.sleep(0.5)
            os.system("""echo "" > /dev/ttyZwave""")
            os.system("""echo "setTxTone 1">/dev/ttyZwave""")
        except Exception as e:
            print(e)
            self.cmdoutput.setText(str(e))

    def rfzwave_txsend_clicked(self):
        try:
            txchn = self.rfzwave_txchannel.text()
            txpower = self.rfzwave_txpower.text()
            print(txchn, txpower)
        except:
            txchn = "1"
        try:
            os.system("""echo "" > /dev/ttyZwave""")
            os.system("""echo "reset" > /dev/ttyZwave""")
            time.sleep(0.5)
            os.system("""echo "" > /dev/ttyZwave""")
            os.system("""echo "rx 0">/dev/ttyZwave""")
            time.sleep(0.1)
            os.system("""echo "" > /dev/ttyZwave""")
            os.system("""echo "SetZwaveMode 1 3">/dev/ttyZwave""")
            time.sleep(0.1)
            os.system("""echo "" > /dev/ttyZwave""")
            os.system("""echo "setzwaveregion 1">/dev/ttyZwave""")
            time.sleep(0.1)
            os.system("""echo "" > /dev/ttyZwave""")
            os.system("""echo "setGPIOoutPin B 14 0">/dev/ttyZwave""")
            time.sleep(0.1)
            os.system("""echo "" > /dev/ttyZwave""")
            os.system("""echo "setGPIOoutPin B 15 1">/dev/ttyZwave""")
            time.sleep(0.1)
            os.system("""echo "" > /dev/ttyZwave""")
            os.system("""echo "setchannel %s">/dev/ttyZwave""" % txchn)
            time.sleep(0.1)
            os.system("""echo "" > /dev/ttyZwave""")
            os.system("""echo "setpower %s">/dev/ttyZwave""" % txpower)
            time.sleep(0.1)
            os.system("""echo "" > /dev/ttyZwave""")
            os.system("""echo "settxpayload 7 20">/dev/ttyZwave""")
            time.sleep(0.1)
            os.system("""echo "" > /dev/ttyZwave""")
            os.system("""echo "settxlength 20">/dev/ttyZwave""")
            time.sleep(0.1)
            os.system("""echo "" > /dev/ttyZwave""")
            os.system("""echo "setctune 0x123">/dev/ttyZwave""")
            time.sleep(0.5)
            os.system("""echo "" > /dev/ttyZwave""")
            os.system("""echo "tx 0">/dev/ttyZwave""")
        except Exception as e:
            self.cmdoutput.setText(str(e))

    def rfzwave_txstop_clicked(self):
        try:
            subprocess.call("""echo "reset" > /dev/ttyZwave""", shell=True)
            subprocess.call("killall cat", shell=True)
        except Exception as e:
            self.cmdoutput.setText(str(e))

    def rfzwave_rxsend_clicked(self):
        try:
            rxchn = self.rfzwave_rxchannel.text()
        except:
            rxchn = "1"
        subprocess.call("cat /dev/ttymxc2 > logzwave &", shell=True)
        subprocess.call("echo reset > /dev/ttyZwave", shell=True)

        try:
            subprocess.call("""echo "rx 0" > /dev/ttyZwave\r\n""", shell=True)
            subprocess.call("""echo "SetZwaveMode 1 3" > /dev/ttyZwave\r\n""", shell=True)
            subprocess.call("""echo "SetTxLength 20" > /dev/ttyZwave\r\n""", shell=True)
            subprocess.call("""echo "SetTxPayload 7 20" > /dev/ttyZwave\r\n""", shell=True)
            subprocess.call("""echo "setzwaveregion 1" > /dev/ttyZwave\r\n""", shell=True)
            subprocess.call("""echo "setGPIOoutPin B 14 0" > /dev/ttyZwave\r\n""", shell=True)
            subprocess.call("""echo "setGPIOoutPin B 15 1" > /dev/ttyZwave\r\n""", shell=True)
            subprocess.call("""echo "configRXChannelHopping 0 3 270 0 1 3 450 0 2 3 560 0" > /dev/ttyZwave\r\n""",
                            shell=True)
            subprocess.call("""echo "enableRxChannelHopping 1" > /dev/ttyZwave\r\n""", shell=True)
            subprocess.call("""echo "setpower 25 raw " > /dev/ttyZwave\r\n""", shell=True)
            subprocess.call("""echo "setchannel %s" > /dev/ttyZwave\r\n""" % rxchn, shell=True)
            subprocess.call("""echo "resetCounters" > /dev/ttyZwave\r\n""", shell=True)
            subprocess.call("""echo "tx 10" > /dev/ttyZwave\r\n""", shell=True)
            subprocess.call("""echo "rx 1" > /dev/ttyZwave\r\n""", shell=True)
        except Exception as e:
            self.cmdoutput.setText(str(e))

    def rfzwave_rxcounter_clicked(self):
        try:
            subprocess.call("""echo "status" > /dev/ttyZwave""", shell=True)
            time.sleep(1)
            output = os.popen("cat logzwave")
            out = output.read()
            subprocess.call("killall cat", shell=True)
            self.cmdinput.setText(out)
        except Exception as e:
            self.cmdoutput.setText(str(e))

    # RFLTE PAGE
    def rflte_switch(self):
        try:
            self.disablemenu_btn()
            self.funcmode.setEnabled(False)
            self.rfmode.setEnabled(False)
            thread.start_new_thread(rfturnonlte_thread, (resq,))

        except Exception as e:
            self.cmdoutput.setText(str(e))

    def rflte_txsend_clicked(self):
        try:
            txband = self.rflte_txband.text()
            txchn = self.rflte_txchannel.text()
            txenable = self.rflte_txenable.text()
            txgain = self.rflte_txgain.text()
        except:
            txband = "LTE BAND4"
            txchn = "20000"
            txenable = "ON"
            txgain = "50"
        try:
            subprocess.call("""echo "" > /dev/ec21_3""", shell=True)
            time.sleep(1)
            subprocess.call("""echo "AT+QRFTESTMODE=1" > /dev/ec21_3""", shell=True)
            time.sleep(1)
            subprocess.call("""echo 'AT+QRFTEST="%s",%s,"%s",%s,1' > /dev/ec21_3""" % (txband, txchn, txenable, txgain),
                            shell=True)
            print("""echo 'AT+QRFTEST="%s",%s,"%s",%s,1' > /dev/ec21_3""" % (txband, txchn, txenable, txgain))
        except Exception as e:
            self.cmdoutput.setText(str(e))

    def rflte_txstop_clicked(self):
        try:
            subprocess.call("""echo "" > /dev/ec21_3""", shell=True)
            time.sleep(1)
            subprocess.call("""echo "AT+QRFTESTMODE=0" > /dev/ec21_3""", shell=True)
        except Exception as e:
            self.cmdoutput.setText(str(e))

    def rflte_rxsend_clicked(self):
        try:
            rxband = self.rflte_rxband.text()
            rxpath = self.rflte_rxpath.text()
            rxbw = self.rflte_bw.text()
            rxchn = self.rflte_rxchn.text()
            rxlna = self.rflte_rxlna.text()
        except:
            rxband = "2"
            rxpath = "0"
            rxbw = "3"
            rxchn = "600"
            rxlna = "0"
        try:
            subprocess.call("""echo "" > /dev/ec21_3""", shell=True)
            time.sleep(1)
            subprocess.call("""echo "AT+QRFTESTMODE=1" > /dev/ec21_3""", shell=True)
            time.sleep(1)
            subprocess.call(
                """echo 'AT+QRXFTM=1,%s,%s,%s,%s,%s' > /dev/ec21_3""" % (rxband, rxchn, rxpath, rxlna, rxbw),
                shell=True)
        except Exception as e:
            self.cmdoutput.setText(str(e))

    def rflte_rxstop_clicked(self):
        try:
            subprocess.call("""echo "" > /dev/ec21_3""", shell=True)
            time.sleep(1)
            subprocess.call("""echo "AT+QRFTESTMODE=0" > /dev/ec21_3""", shell=True)
        except Exception as e:
            self.cmdoutput.setText(str(e))

    def rfwifi_modulationstop_clicked(self):
        try:
            subprocess.call("""wl down""", shell=True)
            subprocess.call("""ifconfig wlan0 down""", shell=True)
            subprocess.call("""ifconfig wlan0 up""", shell=True)
        except Exception as e:
            self.cmdoutput.setText(str(e))

    def sendcmd_btn_clicked(self):
        try:
            pnum = self.cmdinput.toPlainText()
            print(pnum)
            output = os.popen(pnum)
            self.cmdoutput.setText(output.read())
        except Exception as e:
            self.cmdoutput.setText(str(e))

    def stop_btn_clicked(self):
        try:
            self.cmdoutput.setText("")
            self.cmdinput.setText("")
        except Exception as e:
            self.cmdoutput.setText(str(e))

        #############################################################################################


def shutdown_amp():
    subprocess.call("echo 0 > /sys/devices/platform/30a30000.i2c/i2c-1/1-0018/PA_PowerEnable", shell=True)
    subprocess.call('echo -n  "$(date +%Y-%m-%d\ %H:%M:%S) " >> /nsc_tests/gc4_fcc_app/app.log', shell=True)
    subprocess.call(
        'echo   " echo 0 > /sys/devices/platform/30a30000.i2c/i2c-1/1-0018/PA_PowerEnable" >>/nsc_tests/gc4_fcc_app/app.log',
        shell=True)
    subprocess.call('echo -n  "$(date +%Y-%m-%d\ %H:%M:%S) " >> /nsc_tests/gc4_fcc_app/app.log', shell=True)
    subprocess.call('cat /sys/kernel/debug/gpio | grep "pa-pwren" >> /nsc_tests/gc4_fcc_app/app.log', shell=True)


def turnon_amp():
    subprocess.call("echo 1 > /sys/devices/platform/30a30000.i2c/i2c-1/1-0018/PA_PowerEnable", shell=True)
    subprocess.call('echo -n    "$(date +%Y-%m-%d\ %H:%M:%S) " >> /nsc_tests/gc4_fcc_app/app.log', shell=True)
    subprocess.call(
        'echo  -n " echo 1 > /sys/devices/platform/30a30000.i2c/i2c-1/1-0018/PA_PowerEnable" >>/nsc_tests/gc4_fcc_app/app.log',
        shell=True)
    subprocess.call('echo -n  "$(date +%Y-%m-%d\ %H:%M:%S) " >> /nsc_tests/gc4_fcc_app/app.log', shell=True)
    subprocess.call('cat /sys/kernel/debug/gpio | grep "pa mute" >> /nsc_tests/gc4_fcc_app/app.log', shell=True)


def shutdown_CX20921():
    output = os.popen("echo 0 > /sys/devices/platform/30a30000.i2c/i2c-1/1-0018/cx20921PowerEnableAudio")
    output = os.popen("cat /sys/kernel/debug/gpio | grep cx20921")
    version = output.read()
    if "lo" in version:
        pass
    else:
        output = os.popen("echo 0 > /sys/devices/platform/30a30000.i2c/i2c-1/1-0018/cx20921PowerEnableAudio")
    subprocess.call('echo -n  "$(date +%Y-%m-%d\ %H:%M:%S) " >> /nsc_tests/gc4_fcc_app/app.log', shell=True)
    subprocess.call(
        'echo  " echo 0 > /sys/devices/platform/30a30000.i2c/i2c-1/1-0018/cx20921PowerEnableAudio ">>/nsc_tests/gc4_fcc_app/app.log',
        shell=True)
    subprocess.call('echo -n  "$(date +%Y-%m-%d\ %H:%M:%S) " >> /nsc_tests/gc4_fcc_app/app.log', shell=True)
    subprocess.call('cat /sys/kernel/debug/gpio | grep cx20921>> /nsc_tests/gc4_fcc_app/app.log', shell=True)


def turnon_cx20921():
    output = os.popen("echo 1 > /sys/devices/platform/30a30000.i2c/i2c-1/1-0018/cx20921PowerEnableAudio")
    output = os.popen("cat /sys/kernel/debug/gpio | grep cx20921")
    version = output.read()
    if "hi" in version:
        pass
    else:
        output = os.popen("echo 1 > /sys/devices/platform/30a30000.i2c/i2c-1/1-0018/cx20921PowerEnableAudio")
    subprocess.call('echo -n  "$(date +%Y-%m-%d\ %H:%M:%S) " >> /nsc_tests/gc4_fcc_app/app.log', shell=True)
    subprocess.call(
        'echo  " echo 1 > /sys/devices/platform/30a30000.i2c/i2c-1/1-0018/cx20921PowerEnableAudio ">>/nsc_tests/gc4_fcc_app/app.log',
        shell=True)
    subprocess.call('echo -n  "$(date +%Y-%m-%d\ %H:%M:%S) " >> /nsc_tests/gc4_fcc_app/app.log', shell=True)
    subprocess.call('cat /sys/kernel/debug/gpio | grep cx20921>> /nsc_tests/gc4_fcc_app/app.log', shell=True)


def turnon_lte():
    output = os.popen("ls /dev/")
    out = output.read()
    if "ec21_2" in out:
        pass
    else:
        subprocess.call("/nsc_tests/ec21Lowpower -D /dev/ec21_2 -r;", shell=True)
        subprocess.call("DISPLAY=:0 /nsc_tests/gc4_fcc_app/backlightctl &", shell=True)
    subprocess.call('echo -n  "$(date +%Y-%m-%d\ %H:%M:%S) " >> /nsc_tests/gc4_fcc_app/app.log', shell=True)
    subprocess.call(
        """echo -n "at+qnvfw=\\"/nv/item_files/modem/lte/ML1/rx_tuning_chan\\",00" > /dev/ec21_2   &&  echo -en '\x0d' > /dev/ec21_2""",
        shell=True)
    # subprocess.call('echo -n " Turn ON LTE  ">>/nsc_tests/gc4_fcc_app/app.log',shell=True)
    subprocess.call('echo  " /nsc_tests/ec21Lowpower -D /dev/ec21_2 -r;">>/nsc_tests/gc4_fcc_app/app.log', shell=True)
    subprocess.call('echo -n  "$(date +%Y-%m-%d\ %H:%M:%S) " >> /nsc_tests/gc4_fcc_app/app.log', shell=True)
    subprocess.call('echo " DISPLAY=:0 /nsc_tests/gc4_fcc_app/backlightctl &">>/nsc_tests/gc4_fcc_app/app.log',
                    shell=True)
    subprocess.call('echo   "$(date +%Y-%m-%d\ %H:%M:%S) " >> /nsc_tests/gc4_fcc_app/app.log', shell=True)
    subprocess.call(
        """echo  "echo -n "at+qnvfw=\"/nv/item_files/modem/lte/ML1/rx_tuning_chan\",00" > /dev/ec21_2 ">>/nsc_tests/gc4_fcc_app/app.log""",
        shell=True)


def turnoff_mainset():
    try:
        subprocess.call("""cat /dev/ec21_3 log &""", shell=True)
        subprocess.call("""echo "" > /dev/ec21_2""", shell=True)
        time.sleep(1)
        subprocess.call(
            """echo -n "at+qnvfw=\\"/nv/item_files/modem/lte/ML1/rx_tuning_chan\\",05" > /dev/ec21_2   &&  echo -en '\x0d' > /dev/ec21_2""",
            shell=True)
        subprocess.call(
            """echo  "at+qnvfr=\\"/nv/item_files/modem/lte/ML1/rx_tuning_chan\\" " > /dev/ec21_2   &&  echo -en '\x0d' > /dev/ec21_2""",
            shell=True)
        subprocess.call("""killall cat """, shell=True)
        # subprocess.call('echo -n  "$(date +%Y-%m-%d\ %H:%M:%S) " >> /nsc_tests/gc4_fcc_app/app.log',shell=True)
        # subprocess.call("""cat /home/root/log >>/nsc_tests/gc4_fcc_app/app.log""",shell=True)
        subprocess.call('echo   "$(date +%Y-%m-%d\ %H:%M:%S) " >> /nsc_tests/gc4_fcc_app/app.log', shell=True)
        subprocess.call(
            """echo  "echo -n "at+qnvfw=\"/nv/item_files/modem/lte/ML1/rx_tuning_chan\",05" > /dev/ec21_2 ">>/nsc_tests/gc4_fcc_app/app.log""",
            shell=True)
        subprocess.call('echo   "$(date +%Y-%m-%d\ %H:%M:%S) " >> /nsc_tests/gc4_fcc_app/app.log', shell=True)
        subprocess.call(
            """echo  "echo  "at+qnvfr=\"/nv/item_files/modem/lte/ML1/rx_tuning_chan\" " > /dev/ec21_2 ">>/nsc_tests/gc4_fcc_app/app.log""",
            shell=True)
        subprocess.call('echo -n  "$(date +%Y-%m-%d\ %H:%M:%S) " >> /nsc_tests/gc4_fcc_app/app.log', shell=True)
        subprocess.call("""echo  "killall cat ">>/nsc_tests/gc4_fcc_app/app.log""", shell=True)

    except Exception as e:
        print(e)


def turnon_mainset():
    try:
        subprocess.call("""cat /dev/ec21_3 log &""", shell=True)
        subprocess.call("""echo "" > /dev/ec21_2""", shell=True)
        time.sleep(1)
        subprocess.call(
            """echo -n "at+qnvfw=\\"/nv/item_files/modem/lte/ML1/rx_tuning_chan\\",00" > /dev/ec21_2   &&  echo -en '\x0d' > /dev/ec21_2""",
            shell=True)
        subprocess.call(
            """echo  "at+qnvfr=\\"/nv/item_files/modem/lte/ML1/rx_tuning_chan\\" " > /dev/ec21_2   &&  echo -en '\x0d' > /dev/ec21_2""",
            shell=True)
        subprocess.call("""killall cat """, shell=True)
        # subprocess.call('echo -n  "$(date +%Y-%m-%d\ %H:%M:%S) " >> /nsc_tests/gc4_fcc_app/app.log',shell=True)
        # subprocess.call("""cat /home/root/log  >>/nsc_tests/gc4_fcc_app/app.log""",shell=True)
        subprocess.call('echo   "$(date +%Y-%m-%d\ %H:%M:%S) " >> /nsc_tests/gc4_fcc_app/app.log', shell=True)
        subprocess.call(
            """echo  "echo -n "at+qnvfw=\"/nv/item_files/modem/lte/ML1/rx_tuning_chan\",00" > /dev/ec21_2">>/nsc_tests/gc4_fcc_app/app.log""",
            shell=True)
        subprocess.call('echo   "$(date +%Y-%m-%d\ %H:%M:%S) " >> /nsc_tests/gc4_fcc_app/app.log', shell=True)
        subprocess.call(
            """echo  "echo  "at+qnvfr=\"/nv/item_files/modem/lte/ML1/rx_tuning_chan\" " > /dev/ec21_2">>/nsc_tests/gc4_fcc_app/app.log""",
            shell=True)
        subprocess.call('echo -n  "$(date +%Y-%m-%d\ %H:%M:%S) " >> /nsc_tests/gc4_fcc_app/app.log', shell=True)
        subprocess.call("""echo  "killall cat ">>/nsc_tests/gc4_fcc_app/app.log""", shell=True)
    except Exception as e:
        print(e)


def turnoff_lte():
    output = os.popen("ls /dev/")
    out = output.read()
    if "ec21_2" in out:
        subprocess.call("/nsc_tests/ec21Lowpower -D /dev/ec21_2 ", shell=True)
        subprocess.call("killall backlightctl", shell=True)
    else:
        pass
    subprocess.call('echo -n  "$(date +%Y-%m-%d\ %H:%M:%S) " >> /nsc_tests/gc4_fcc_app/app.log', shell=True)
    # subprocess.call('echo -n " Turn OFF LTE  ">>/nsc_tests/gc4_fcc_app/app.log',shell=True)
    subprocess.call('echo   " /nsc_tests/ec21Lowpower -D /dev/ec21_2">>/nsc_tests/gc4_fcc_app/app.log', shell=True)
    subprocess.call('echo -n  "$(date +%Y-%m-%d\ %H:%M:%S) " >> /nsc_tests/gc4_fcc_app/app.log', shell=True)
    subprocess.call('echo " killall backlightctl">>/nsc_tests/gc4_fcc_app/app.log', shell=True)


def turnon_camera():
    subprocess.call(
        "gst-launch-1.0 v4l2src device=/dev/video0 ! 'video/x-raw,width=640,height=480,framerate=(fraction)30/1' ! autovideosink & sleep 10;killall gst-launch-1.0;",
        shell=True)


def turnon_piezo():
    subprocess.call("echo 1 > /sys/class/gpio/gpio23/value  && echo 1 > /sys/class/pwm/pwmchip1/pwm0/enable",
                    shell=True)
    subprocess.call('echo -n  "$(date +%Y-%m-%d\ %H:%M:%S) " >> /nsc_tests/gc4_fcc_app/app.log', shell=True)
    subprocess.call(
        'echo  " echo 1 > /sys/class/gpio/gpio23/value  && echo 1 > /sys/class/pwm/pwmchip1/pwm0/enable  ">>/nsc_tests/gc4_fcc_app/app.log',
        shell=True)
    subprocess.call('echo -n  "$(date +%Y-%m-%d\ %H:%M:%S) " >> /nsc_tests/gc4_fcc_app/app.log', shell=True)
    subprocess.call('cat /sys/kernel/debug/gpio | grep gpio-23>>/nsc_tests/gc4_fcc_app/app.log', shell=True)
    subprocess.call('echo -n  "$(date +%Y-%m-%d\ %H:%M:%S) " >> /nsc_tests/gc4_fcc_app/app.log', shell=True)
    subprocess.call('echo  -n " PWM:  ">>/nsc_tests/gc4_fcc_app/app.log', shell=True)
    subprocess.call('cat /sys/class/pwm/pwmchip1/pwm0/enable>>/nsc_tests/gc4_fcc_app/app.log', shell=True)


def turnoff_piezo():
    subprocess.call("echo 0 > /sys/class/gpio/gpio23/value  && echo 0 > /sys/class/pwm/pwmchip1/pwm0/enable ",
                    shell=True)
    subprocess.call('echo -n  "$(date +%Y-%m-%d\ %H:%M:%S) " >> /nsc_tests/gc4_fcc_app/app.log', shell=True)
    subprocess.call(
        'echo  " echo 0 > /sys/class/gpio/gpio23/value  && echo 0 > /sys/class/pwm/pwmchip1/pwm0/enable  ">>/nsc_tests/gc4_fcc_app/app.log',
        shell=True)
    subprocess.call('echo -n  "$(date +%Y-%m-%d\ %H:%M:%S) " >> /nsc_tests/gc4_fcc_app/app.log', shell=True)
    subprocess.call('cat /sys/kernel/debug/gpio | grep gpio-23>>/nsc_tests/gc4_fcc_app/app.log', shell=True)
    subprocess.call('echo -n  "$(date +%Y-%m-%d\ %H:%M:%S) " >> /nsc_tests/gc4_fcc_app/app.log', shell=True)
    subprocess.call('echo -n " PWM:  ">>/nsc_tests/gc4_fcc_app/app.log', shell=True)
    subprocess.call('cat /sys/class/pwm/pwmchip1/pwm0/enable>>/nsc_tests/gc4_fcc_app/app.log', shell=True)


def enter_battery_mode():
    setrunm4(1)
    subprocess.call("echo mem > /sys/power/state", shell=True)


def playback_on():
    subprocess.call("speaker-test -c 2 -t wav &", shell=True)


def playback_off():
    subprocess.call("killall speaker-test", shell=True)


def turnoff_zwave():
    subprocess.call("echo -n off > /sys/kernel/ec21_kobj/powerZwave", shell=True)
    subprocess.call('echo -n  "$(date +%Y-%m-%d\ %H:%M:%S) " >> /nsc_tests/gc4_fcc_app/app.log', shell=True)
    subprocess.call('echo  " echo -n off > /sys/kernel/ec21_kobj/powerZwave ">>/nsc_tests/gc4_fcc_app/app.log',
                    shell=True)
    subprocess.call('echo -n  "$(date +%Y-%m-%d\ %H:%M:%S)  " >> /nsc_tests/gc4_fcc_app/app.log', shell=True)
    subprocess.call('cat  /sys/kernel/ec21_kobj/powerZwave>> /nsc_tests/gc4_fcc_app/app.log', shell=True)
    subprocess.call('echo -n  "$(date +%Y-%m-%d\ %H:%M:%S) " >> /nsc_tests/gc4_fcc_app/app.log', shell=True)
    subprocess.call('cat /sys/kernel/debug/gpio | grep gpio-22>> /nsc_tests/gc4_fcc_app/app.log', shell=True)


def turnon_zwave():
    subprocess.call("echo -n on > /sys/kernel/ec21_kobj/powerZwave", shell=True)
    subprocess.call('echo -n  "$(date +%Y-%m-%d\ %H:%M:%S) " >> /nsc_tests/gc4_fcc_app/app.log', shell=True)
    subprocess.call('echo  " echo -n on > /sys/kernel/ec21_kobj/powerZwave ">>/nsc_tests/gc4_fcc_app/app.log',
                    shell=True)
    subprocess.call('echo -n  "$(date +%Y-%m-%d\ %H:%M:%S) " >> /nsc_tests/gc4_fcc_app/app.log', shell=True)
    subprocess.call('cat  /sys/kernel/ec21_kobj/powerZwave>> /nsc_tests/gc4_fcc_app/app.log', shell=True)
    subprocess.call('echo -n  "$(date +%Y-%m-%d\ %H:%M:%S) " >> /nsc_tests/gc4_fcc_app/app.log', shell=True)
    subprocess.call('cat /sys/kernel/debug/gpio | grep gpio-22>> /nsc_tests/gc4_fcc_app/app.log', shell=True)


def enable_charging():
    subprocess.call("stty -F /dev/ttymxc2 ispeed 115200 ospeed 115200 -ixon", shell=True)
    subprocess.call("echo -en '\x42\x41\x54\x20\x63\x68\x61\x72\x67\x65\x20\x30\x0d' > /dev/ttymxc2", shell=True)
    subprocess.call('echo -n  "$(date +%Y-%m-%d\ %H:%M:%S) " >> /nsc_tests/gc4_fcc_app/app.log', shell=True)
    # subprocess.call('echo -n " Enable Charging ">>/nsc_tests/gc4_fcc_app/app.log',shell=True)
    subprocess.call('echo  " echo -en BAT charge 1>/dev/ttymxc2 ">>/nsc_tests/gc4_fcc_app/app.log', shell=True)


def disable_charging():
    subprocess.call("stty -F /dev/ttymxc2 ispeed 115200 ospeed 115200 -ixon", shell=True)
    subprocess.call("echo -en '\x42\x41\x54\x20\x63\x68\x61\x72\x67\x65\x20\x31\x0d' > /dev/ttymxc2", shell=True)
    subprocess.call('echo -n  "$(date +%Y-%m-%d\ %H:%M:%S) " >> /nsc_tests/gc4_fcc_app/app.log', shell=True)
    # subprocess.call('echo -n " Disable Charging ">>/nsc_tests/gc4_fcc_app/app.log',shell=True)
    subprocess.call("echo   ' echo -en BAT charge 1>/dev/ttymxc2  '>>/nsc_tests/gc4_fcc_app/app.log", shell=True)


def disable_dc12():
    subprocess.call("echo 1 > /sys/devices/platform/acDetect/DC12_OnOff", shell=True)
    subprocess.call('echo -n  "$(date +%Y-%m-%d\ %H:%M:%S) " >> /nsc_tests/gc4_fcc_app/app.log', shell=True)
    subprocess.call("echo   ' echo 1 > /sys/devices/platform/acDetect/DC12_OnOff  '>>/nsc_tests/gc4_fcc_app/app.log",
                    shell=True)


def setrunm4(target):
    output = os.popen("fw_printenv runm4")
    print("runm4=0" in output.read())
    if "runm4=0" in output.read() and target == 1:
        subprocess.call("fw_setenv runm4 1", shell=True)
        os.system("reboot")
        return "runm4=1, please reboot your system"
    elif "runm4=1" in output.read() and target == 0:
        subprocess.call("fw_setenv runm4 0", shell=True)
        os.system("reboot")
        return "runm4=0, please reboot your system"
    else:
        return "env error, please reboot your system"


def disable_all(resq):
    try:
        turnoff_lte()
        turnoff_piezo()
        playback_off()
        shutdown_CX20921()
        shutdown_amp()
        turnoff_zwave()
        disable_charging()
        disable_dc12()
        subprocess.call("killall evtest", shell=True)
        subprocess.call("rm test.log", shell=True)
        subprocess.call("killall backlightctl", shell=True)
        subprocess.call("killall gst-launch-1.0;", shell=True)
        subprocess.call("killall speaker-test", shell=True)
        resq.put(["disableall", True])

    except Exception as e:
        resq.put(["disableall", str(e)])


###############Page Switch
def funcmode_switch_thread(resq):
    try:
        disable_all(resq)
        os.system(
            """sed -i "s/fw_bcm43455c0_ag_mfg.bin/fw_bcm43455c0_ag_apsta.bin/g" /etc/modprobe.d/GcNext-ap6255-wifi.conf""")
        resq.put(["funcmode", True])
    except Exception as e:
        resq.put(["funcmode", str(e)])


def rfmode_switch_thread(resq):
    try:
        disable_all(resq)
        os.system(
            """sed -i "s/fw_bcm43455c0_ag_apsta.bin/fw_bcm43455c0_ag_mfg.bin/g" /etc/modprobe.d/GcNext-ap6255-wifi.conf""")
        resq.put(["rfmode", True])
    except Exception as e:
        resq.put(["rfmode", str(e)])


def functurnonlte_thread(resq):
    try:
        turnon_lte()
        resq.put(["functurnonlte", True])
    except Exception as e:
        resq.put(["functurnonlte", str(e)])


def rfturnonlte_thread(resq):
    try:
        turnon_lte()
        resq.put(["rfturnonlte", True])
    except Exception as e:
        resq.put(["rfturnonlte", str(e)])


def functurnofflte_thread(resq):
    try:
        turnoff_lte()
        resq.put(["functurnofflte", True])
    except Exception as e:
        resq.put(["functurnofflte", str(e)])


def funcmainset_thread(resq):
    try:
        turnoff_mainset()
        resq.put(["funcmainset", True])
    except Exception as e:
        resq.put(["funcmainset", str(e)])


def funcmainseton_thread(resq):
    try:
        turnon_mainset()
        resq.put(["funcmainseton", True])
    except Exception as e:
        resq.put(["funcmainseton", str(e)])


def voicecallon_thread(resq):
    try:
        setrunm4(1)
        turnon_cx20921()
        turnon_lte()
        output = os.popen("ls /nsc_tests/")
        if "quectel-CM" in output.read():
            pass
        else:
            subprocess.call("cd /nsc_tests/ && unzip test.zip", shell=True)
            time.sleep(2)

        subprocess.call("/nsc_tests/swmode/./swmode.sh 2", shell=True)
        subprocess.call("ifconfig eth0 down && ifconfig eth0 up", shell=True)
        subprocess.call("/nsc_tests/quectel-CM &", shell=True)
        subprocess.call("echo '' > /dev/ec21_3", shell=True)
        subprocess.call("echo '' > /dev/ec21_3", shell=True)
        subprocess.call("echo '' > /dev/ec21_3", shell=True)
        subprocess.call("echo AT+COPS? > /dev/ec21_3", shell=True)
        resq.put(["voicecallon", True])
    except Exception as e:
        resq.put(["voicecallon", str(e)])


def funcwireless_wifion_thread(resq):
    out = "wiif connect error"
    try:
        subprocess.call(
            "ifconfig wlan0 down;ifconfig wlan0 up;killall wpa_supplicant;wpa_passphrase %s %s > wpa.conf;wpa_supplicant -B -i wlan0 -c wpa.conf;udhcpc -i wlan0;" % (
            ssid, psd), shell=True)
        output = os.popen("ifconfig wlan0")
        out = output.read()
        resq.put(["wifion", True, str(out)])
        # self.cmdoutput.setText(out)
    except Exception as e:
        print(e)
        resq.put(["wifion", False, str(out)])
        # self.cmdoutput.setText(str(e))


def rfwifi_modulationsend_thread(txmregion, txmband, txmtxbw, txmmode, txmchn, resq):
    try:
        subprocess.call("ifconfig wlan0 down", shell=True)
        subprocess.call("ifconfig wlan0 up", shell=True)
        subprocess.call("wl pkteng_stop tx", shell=True)
        time.sleep(0.3)
        subprocess.call("wl down", shell=True)
        time.sleep(0.3)
        subprocess.call("wl mpc 0", shell=True)
        time.sleep(0.3)
        subprocess.call("wl country %s" % txmregion, shell=True)
        time.sleep(0.3)
        subprocess.call("wl band %s" % txmband, shell=True)
        time.sleep(0.3)
        subprocess.call("wl up", shell=True)
        time.sleep(0.3)
        subprocess.call("wl %s" % txmmode, shell=True)
        time.sleep(0.3)
        subprocess.call("wl %s" % txmchn, shell=True)
        time.sleep(0.3)
        subprocess.call("wl phy_watchdog 0", shell=True)
        time.sleep(0.3)
        subprocess.call("wl scansuppress 1", shell=True)
        time.sleep(0.3)
        subprocess.call("wl phy_forcecal 1", shell=True)
        time.sleep(0.3)
        subprocess.call("wl phy_txpwrctrl 1", shell=True)
        time.sleep(0.3)
        subprocess.call("wl txpwr1 -1", shell=True)
        time.sleep(0.3)
        subprocess.call("wl pkteng_start 00:90:4c:14:43:19 tx 100 1000 0", shell=True)
        resq.put(["rfwifion", True])
    except Exception as e:
        resq.put(["rfwifion", str(e)])


def funcvoicecall_start_thread(resq):
    global ping_output, flag
    try:
        while True:
            if flag == 1:
                ping_out = os.popen("ping -c 6 %s" % (web))
                time.sleep(10)
                ping_output = ping_out.read()
                print(ping_output)
                if "packets transmitted" in ping_output:
                    resq.put(["voicecallping", True])
                else:
                    resq.put(["voicecallping", False])
                time.sleep(3600 / int(ping_count))
            else:
                break
    except Exception as e:
        resq.put(["voicecallstart", str(e)])


def pspeedtest(resq):
    out = os.popen("./speedtest-cli")
    out = out.read()
    resq.put(["speedtest", out])


if __name__ == '__main__':
    flag = 0
    volume = os.popen("amixer -Dhw:0 cget numid=3")
    volume = (volume.read().split()[7].split("values=")[1])
    # volume=15
    os.system(
        "echo 23 > /sys/class/gpio/export && echo out > /sys/class/gpio/gpio23/direction && echo 0 > /sys/class/pwm/pwmchip1/export&& echo 200000 > /sys/class/pwm/pwmchip1/pwm0/period && echo 110000 > /sys/class/pwm/pwmchip1/pwm0/duty_cycle ")
    os.system("rm -rf /nsc_tests/gc4_fcc_app/app.log")
    shutdown_amp()
    shutdown_CX20921()
    resq = queue.Queue()
    app = QtWidgets.QApplication(sys.argv)
    myWin = mbox()
    myWin.show()
    sys.exit(app.exec_())





