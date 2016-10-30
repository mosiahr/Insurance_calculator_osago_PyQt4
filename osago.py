#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from roundUp import roundUp
from PyQt4 import QtGui, QtCore

class Data(object):
    """ pass """

    base_pay = 180
    # ------------------- for auto type ( k1) ----------------------
    auto_list = [u'(В1) Легковий автомобіль до 1600 куб. см.',
                      u'(В2) Легковий автомобіль до 1601-2000 куб. см.',
                      u'(В3) Легковий автомобіль до 2001-3000 куб. см.',
                      u'(В4) Легковий автомобіль більше 3000 куб. см.',
                      u'(F) Причепи до легкових автомобілів',
                      u'(D1) Автобуси з кількістю місць для сидіння до 20 осіб (включно)',
                      u'(D2) Автобуси з кількістю місць для сидіння більше 20 осіб',
                      u'(С1) Вантажні автомобілі вантажопідйомністю до 2 тонн (включно)',
                      u'(С2) Вантажні автомобілі вантажопідйомністю більше 2 тонни',
                      u'(E) Причепи до вантажних автомобілів',
                      u'(A1) Мотоцикли та моторолери до 300 куб. см. (включно)',
                      u'(A2) Мотоцикли та моторолери більше 300 куб. см.']
    auto_k = [1, 1.14, 1.18, 1.82, 0.34, 2.55, 3, 2, 2.18, 0.5, 0.34, 0.68]

    # ---------------------  for separator of auto  --------------------------------
    separator_auto = [4, 6, 9, 12, 14]

    # ---------------------  for vehicle use area (k2) ----------------------------------
    zone_list = [u'1.Київ',
                      u'2.Бориспіль, Боярка, Бровари, Ірпінь, Васильків, Вишневе, Вишгород',
                      u'3.Одеса, Харків',
                      u'4.Дніпропетровськ, Донецьк, Запоріжжя, Кривий Ріг, Львів',
                      u'5.Міста з населенням 500 – 100 тисяч чоловік',
                      u'6.Населені пункти, які не зазначені в інших рядках',
                      u'7.Для ТЗ, які зареєстровані в інших країнах (за межами України)']
    zone_k = [4.8, 2.5, 3.4, 2.8, 2.2, 1.5, 3.0]

    # ------------------  for period ( k5) ----------------------
    period_list = [u'{} міс.'.format(p) for p in range(6, 13)]
    period_k = [0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 1]

    # ------------------  for validity (k7) ---------------------
    validity_list = [u'15 днів', u'1 місяць', u'2 місяці', u'3 місяці',
                            u'4 місяці',] + [u'{} місяців'.format(v) for v in range(5, 13)]
    validity_k = [0.15, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 1]

    # ------------------ for bonus (bm) -------------------------
    bm_k = [2.45, 2.3, 1.55, 1.4, 1, 0.95, 0.9, 0.85, 0.8]
    bm_list = [u'Клас M ({})'.format(bm_k[0])] + \
                   [u'Клас {} ({})'.format(i, bm_k[1:][i]) for i in range(len(bm_k)-1)]

    # ------------------  for a park vehicle ----------------
    park_list = [u'до 4 (0%)', u'від 5 до 9 (-5%)', u'від 10 до 19 (-10%)',
                      u'від 20 до 99 (-15%)', u'від 100 до 499 (-20%)',
                      u'від 500 до 1999 (-25%)', u'від 2000 і більше (-30%)']
    park_k = [1, 0.95, 0.9, 0.85, 0.8, 0.85, 0.75, 0.7]

    # ------------------ for vehicle features ---------------
    vf_list = [u'ТЗ не зареєстрований (нові ТЗ тощо)',
                u'ТЗ тимчасово зареєстрований (тимчасові, транзитні номери)',
                u'ТЗ зареєстрований на території іноземної держави', u'Інше']
    vf_k = ['not_registered', 'temporarily', 'foreign', 'other']

    def __init__(self):
        self.create_all_dict()

    def create_all_dict(self):
        self.auto_dict = self.creature_dict(self.auto_list, self.auto_k)
        self.zone_dict = self.creature_dict(self.zone_list, self.zone_k)
        self.period_dict = self.creature_dict(self.period_list, self.period_k)
        self.validity_dict = self.creature_dict(self.validity_list, self.validity_k)
        self.bm_dict = self.creature_dict(self.bm_list, self.bm_k)
        self.park_dict = self.creature_dict(self.park_list, self.park_k)
        self.vf_dict = self.creature_dict(self.vf_list, self.vf_k)

    def creature_dict(self, list_key, list_value ):
        """ creature a dictionary of the two lists """
        return {list_key[i]: list_value[i] for i in range(len(list_key)) }


class Rezult(Data):
    """ pass """
    kod_featires = []
    kod_type = []  # B1, B2,  Зона 6 і т.д.
    koef = {}
    koef_bool = {}

    def koef_3(self, kod, vehicle_type):
        if kod is not None:
            if (self.koef_bool['taxi'] == False
                and kod in [vehicle_type[a] for a in range(4)]
                or kod in vehicle_type[10] or kod in vehicle_type[11]): # ['B1', 'B2', 'B3', 'B4', 'A1', 'A2']:
                if self.koef_bool['ind'] == True:
                    self.koef['k3'] = 1
                elif self.koef_bool['ind'] == False:
                    self.koef['k3'] = 1.3
            if self.koef_bool['taxi'] == False and kod in [vehicle_type[a] for a in range(4, 10)]: #['C1', 'C2', 'D1', 'D2', 'E', 'F']:
                self.koef['k3'] = 1
            if (self.koef_bool['taxi'] == True and self.koef_bool['ind'] == True
            and kod in [vehicle_type[a] for a in range(4)] or kod in vehicle_type[5]):  # ['B1', 'B2', 'B3', 'B4', 'D1'] , self.auto_t[5]
                self.koef['k3'] = 1.4
            if (self.koef_bool['taxi'] == True and self.koef_bool['ind'] == False
            and kod in [vehicle_type[a] for a in range(4)] or kod in vehicle_type[5]):  # ['B1', 'B2', 'B3', 'B4', 'D1'] , self.auto_t[5]
                self.koef['k3'] = 1.5
            return self.koef['k3']

    def koef_4(self):
        if self.koef_bool['ind'] == True:
            self.koef['k4'] = 1.5
        else: self.koef['k4'] = 1.2
        return self.koef['k4']

    def koef_6(self):
        if self.koef_bool['fraud'] == True:
            self.koef['k6'] = 2
        else: self.koef['k6'] = 1
        return self.koef['k6']

    def koef_pension(self):
        if self.koef_bool['pension']  == False:
            self.koef['pension'] = 1
        else: self.koef['pension'] = 0.5

    def rez(self):
        self.koef['bp'] = self.base_pay
        self.koef_3(self.kod_type[0], self.auto_list)
        self.koef_4()
        self.koef_6()
        self.koef_pension()
        self.rezult = reduce(lambda res, x: res*x, self.koef.values(), 1)  # (((bp*k1)*k2)*k3)*...
        return self.rezult

    def rez_label(self, label):
        label.setText(u"Результат: <i>{:.2f} грн.</i>".format(roundUp(self.rez(), 2)))


class Main(QtGui.QWidget, Rezult, Data):
    """ UI Main window """

    title = u"Калькулятор ОЦВ"

    def __init__(self):
        super(Main, self).__init__()
        Data.__init__(self)
        self.initUI()

    def initUI(self):
        """ Initialization UI Main window """
        self.center()
        self.resize(700, 630)  # the new size of the window
        self.setWindowTitle(' '.join(self.title))
        self.setWindowIcon(QtGui.QIcon('./icons/car.png'))
        #  ---------------  Labels  ----------------------------------------
        self.label = QtGui.QLabel(u'Розрахунок ОЦВ')
        self.label.setAlignment(QtCore.Qt.AlignCenter)

        # ----------------  List  ----------------------------
        self.list_auto = ListBox('k1', self.auto_list,
                                 u'Тип ТЗ:', self.auto_dict,
                                 set_cur_ind=0, separator=self.separator_auto)
        self.list_zone = ListBox('k2', self.zone_list,
                                 u'Місце реєстрації ТЗ:',
                                 self.zone_dict, set_cur_ind=5)
        self.list_validity = ListBox('k7', self.validity_list,
                                      u'Строк дії договору', self.validity_dict,
                                     set_cur_ind=12)
        self.list_bonus = ListBox('bm', self.bm_list, u'Бонус-малус', self.bm_dict, set_cur_ind=4)
        self.list_park = ListBox('park', self.park_list, u'Парк ТЗ', self.park_dict)

        # ----------------  Radio button  ----------------------
        self.experience = RadioBut('experience', u'Водійський стаж меньше 3-х років ? ', activate=True)
        self.pension = RadioBut('pension', u'ТЗ використовує пільговик ?', activate=False)
        self.taxi = RadioBut('taxi', u'ТЗ використовується як таксi ?', activate=False)
        self.otk = RadioBut('otk', u'ТЗ підлягає ОТК ?', activate=False)
        self.ind = RadioBut('ind', u'Фізична чи юридична особа ?', activate=True, radio_first=u'Фізична', radio_second=u'Юридична')
        self.fraud = RadioBut('fraud', u'Чи були спроби шахрайства ?', activate=False)

        self.kod_type.append(self.list_auto.get_kod_type())
        self.koef_3(self.kod_type[0], self.auto_list)

        # ----------------  Label rezult  -------------------------
        self.label_rezult = QtGui.QLabel(u"Результат: <i>{:.2f} грн.</i>".format(roundUp(self.rez())))
        self.label_rezult.setAlignment(QtCore.Qt.AlignCenter)

        #  ---------------  Button  ----------------------------
        self.pay_btn = Button(u'Розрахувати')
        self.pay_btn.button_rezult(self.label_rezult)

        self.quit = Button(u'Вихід')
        self.quit.button_quit()

        self.hbox_button = QtGui.QHBoxLayout()
        self.hbox_button.addWidget(self.pay_btn)
        self.hbox_button.addWidget(self.quit)

        # ----------------  Grid main  -----------------------------------
        self.grid = QtGui.QGridLayout()
        self.grid.addWidget(self.label, 0, 0, 1, 4)
        self.grid.addWidget(self.list_auto, 1, 0, 1, 2)
        self.grid.addWidget(self.list_zone, 2, 0, 1, 2)
        self.grid.addWidget(self.list_validity, 3, 0, 1, 2)
        self.grid.addWidget(self.list_bonus, 4, 0, 1, 2)
        self.grid.addWidget(self.list_park, 5, 0, 1, 2)
        self.grid.addWidget(self.experience, 1, 2, 1, 2)
        self.grid.addWidget(self.pension, 2, 2, 1, 2)
        self.grid.addWidget(self.taxi, 3, 2, 1, 2)
        self.grid.addWidget(self.ind, 4, 2, 1, 2)
        self.grid.addWidget(self.fraud, 5, 2, 1, 2)
        self.grid.addWidget(self.label_rezult, 6, 0, 1, 4)
        self.grid.addWidget(self.pay_btn, 7, 1, 1, 1)
        self.grid.addWidget(self.quit, 7, 2, 1, 1)
        self.setLayout(self.grid)

    def center(self):
        """  Alignment window  """
        window = QtGui.QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((window.width() - size.width()) / 2, (window.height() - size.height()) / 2)

class RadioBut(QtGui.QWidget, Rezult):
    """ UI radio buttons """

    def __init__(self, name, description, activate, radio_first=u"ТАК", radio_second=u"НІ"):
        super(RadioBut, self).__init__()
        Rezult.__init__(self)
        self.name = name
        self.description = description
        self.activate = activate
        self.radio_first = radio_first
        self.radio_second = radio_second
        self.radioUI()

    def radioUI(self):
        self.label = QtGui.QLabel(u"{}".format(self.description))
        self.radio_group = QtGui.QGroupBox(self.description, self)

        self.hbox = QtGui.QHBoxLayout(self.radio_group)  # контейнер горизонт
        self.radio1 = QtGui.QRadioButton(self.radio_first, self.radio_group)
        self.radio2 = QtGui.QRadioButton(self.radio_second, self.radio_group)
        self.activ(self.radio1, self.radio2, self.activate)

        self.hbox.addWidget(self.radio1)
        self.hbox.addWidget(self.radio2)
        self.radio_group.setLayout(self.hbox)

        self.mainbox = QtGui.QVBoxLayout(self)
        self.mainbox.addWidget(self.radio_group)
        self.setLayout(self.mainbox)

        self.add_switch_current(self.radio1)
        self.connect(self.radio1, QtCore.SIGNAL("toggled(bool)"), self.add_switch)

    def activ(self, radio1, radio2, bool):
        """ Set on the switch """
        if bool:
            radio1.setChecked(True)
        else:
            radio2.setChecked(True)

    def add_switch_current(self, rbutton):
        """ Add current element in dict koef """
        self.koef_bool[self.name] = rbutton.isChecked()
        return rbutton.isChecked()

    def add_switch(self, bool):
        """ Add element in dict koef """
        self.koef_bool[self.name] = bool
        self.rez()
        return bool

class ListBox(QtGui.QWidget, Rezult):
    """  UI List Box  """
    def __init__(self, name, category, description, dict, set_cur_ind=None, separator=None):
        super(ListBox, self).__init__()
        Rezult.__init__(self)
        self.name = name
        self.category = category
        self.description = description
        self.dict = dict
        self.set_cur_ind = set_cur_ind
        self.separator = separator
        self.listUI()

    def listUI(self):
        self.mainbox = QtGui.QVBoxLayout(self)
        self.frame = QtGui.QFrame(self)
        self.frame.setFrameShape(QtGui.QFrame.Box)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setMidLineWidth(1)

        self.label = QtGui.QLabel(u"{}".format(self.description))
        self.combo = QtGui.QComboBox()
        self.combo.setSizeAdjustPolicy(QtGui.QComboBox.AdjustToMinimumContentsLengthWithIcon)

        # ----------------  Add combo, separator  -------------
        self.add_combo_separ(self.combo, self.category)

        # ----------------  Combo index activation  --------------
        self.combo.activated['QString'].connect(self.handleActivated)

        # ----------------  Setter current index  ----------------
        self.set_current_index()
        self.currentIndex = self.combo.currentIndex()
        self.comboCurrent = self.combo.itemText(self.currentIndex)
        self.handCurrent(self.comboCurrent)

        self.hbox_type = QtGui.QHBoxLayout(self.frame)
        self.hbox_type.addWidget(self.label)
        self.hbox_type.addWidget(self.combo)

        self.mainbox.addWidget(self.frame)
        self.setLayout(self.mainbox)
        self.kod_type = self.get_kod_type()

    def set_current_index(self):
        if self.set_cur_ind is not None:
            self.combo.setCurrentIndex(int(self.set_cur_ind))
        else:
            self.combo.setCurrentIndex(0)

    def add_combo_separ(self, combo, category):
        if category:
            combo.addItems(category)
        if self.separator:
            for sep in self.separator:
                combo.insertSeparator(sep)

    def handCurrent(self, combo_current):
        value = self.dict.get(u'{}'.format(combo_current))
        self.koef[self.name] = value

    def handleActivated(self, text):
        value = self.dict.get(u'{}'.format(text))
        self.koef[self.name] = value

    def get_kod_type(self):
        return u'{}'.format(self.combo.currentText()) # B1, B2 і т.д.


class Button(QtGui.QWidget, Rezult):
    """ pass """
    def __init__(self, description):
        super(Button, self).__init__()
        Rezult.__init__(self)
        self.description = description
        self.buttonUI()

    def buttonUI(self):
        self.mainbox = QtGui.QVBoxLayout()
        self.btn = QtGui.QPushButton(self.description)
        self.mainbox.addWidget(self.btn)
        self.setLayout(self.mainbox)

    def button_rezult(self, label):
        self.connect(self.btn, QtCore.SIGNAL("clicked()"), lambda : self.rez_label(label))

    def button_quit(self):
        self.connect(self.btn, QtCore.SIGNAL("clicked()"), QtGui.qApp.quit)

def main():
    app = QtGui.QApplication(sys.argv)
    app.setStyleSheet(open("./style.css", "r").read())
    window = Main()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
