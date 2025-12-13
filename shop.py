from tkinter import *
from tkinter import messagebox


"""Структура возвращаемого значения:
{"щит": 0, "часы": 0, "нитро": 0, "удвоитель": 0}"""


class _Pockupka:
    def __init__(self, sum_score):
        self.sum_score = sum_score
        self.purchased = {"щит": 0, "часы": 0, "нитро": 0, "удвоитель": 0}
        
    def block(self, name_tovar = "щита за 80 очков"):
        if messagebox.askokcancel("Потвердите покупку", f"Пожалуйста, потвердите покупку {name_tovar}"):
            if self.sum_score - 80 < 0:
                messagebox.showerror("Слишком мало денег!", f"К сожалению, у вас на счету всего {self.sum_score}, чего недостаточно для покупки.")
                return
            self.sum_score -= 80
            self.purchased["щит"] = 1
            self._welcomeMinus()

    def time(self, name_tovar = "замедлителя времени за 110 очков"):
        if messagebox.askokcancel("Потвердите покупку", f"Пожалуйста, потвердите покупку {name_tovar}"):
            if self.sum_score - 110 < 0:
                messagebox.showerror("Слишком мало денег!", f"К сожалению, у вас на счету всего {self.sum_score} очков, чего недостаточно для покупки.")
                return
            self.sum_score -= 110
            self.purchased["часы"] = 1
            self._welcomeMinus()

    def limit_turbo(self, name_tovar = "увеличения лимита нитро за 130 очков"):
        if messagebox.askokcancel("Потвердите покупку", f"Пожалуйста, потвердите покупку {name_tovar}"):
            if self.sum_score - 130 < 0:
                messagebox.showerror("Слишком мало денег!", f"К сожалению, у вас на счету всего {self.sum_score} очков, чего недостаточно для покупки.")
                return
            self.sum_score -= 130
            self.purchased["нитро"] = 1
            self._welcomeMinus()

    def x2_moneys(self, name_tovar = "удвоения получаемых очков в первые 30 секунд за 200 очков"):
        if messagebox.askokcancel("Потвердите покупку", f"Пожалуйста, потвердите покупку {name_tovar}"):
            if self.sum_score - 200 < 0:
                messagebox.showerror("Слишком мало денег!", f"К сожалению, у вас на счету всего {self.sum_score} очков, чего недостаточно для покупки.")
                return
            
            self.sum_score -= 200
            self.purchased["удвоитель"] = 1
            self._welcomeMinus()
    
    def _welcomeMinus(self):
        global welcome
        
        if self.sum_score >= 10 and self.sum_score <= 20:
            welcome["text"] = f"Добро пожаловать в магазин! Ваш текущий баланс: {self.sum_score} очков"
        elif int(str(self.sum_score)[-1]) == 0 or int(str(self.sum_score)[-1]) >= 5:
            welcome["text"] = f"Добро пожаловать в магазин! Ваш текущий баланс: {self.sum_score} очков"
        elif int(str(self.sum_score)[-1]) == 1:
            welcome["text"] = f"Добро пожаловать в магазин! Ваш текущий баланс: {self.sum_score} очко"
        else:
            welcome["text"] = f"Добро пожаловать в магазин! Ваш текущий баланс: {self.sum_score} очка"

def open_shop(sum_score: int):
    global root, app, welcome

    root = Tk()
    root.title("Магазин")
    root.geometry("360x250")
    app = Frame(root)
    app.grid()

    pockupka = _Pockupka(sum_score)

    if sum_score >= 10 and sum_score <= 20:
        welcome = Label(app, text="Добро пожаловать в магазин! " + 
                                   f"Ваш текущий баланс: {pockupka.sum_score} очков")
    elif int(str(sum_score)[-1]) == 0 or int(str(sum_score)[-1]) >= 5:
        welcome = Label(app, text="Добро пожаловать в магазин! " + 
                                   f"Ваш текущий баланс: {pockupka.sum_score} очков")
    elif int(str(sum_score)[-1]) == 1:
        welcome = Label(app, text="Добро пожаловать в магазин! " + 
                                   f"Ваш текущий баланс: {pockupka.sum_score} очко")
    else:
        welcome = Label(app, text="Добро пожаловать в магазин! " + 
                                   f"Ваш текущий баланс: {pockupka.sum_score} очка")
    
    welcome.grid()

    Label(app, text="\nВыберете, что вы хотите купить:").grid()
    
    Button(app, text="Щит, цена 80 очков", command=pockupka.block).grid()
    Button(app, text="Замедление времени, цена 110 очков", command=pockupka.time).grid()
    Button(app, text="Лимит нитро + 20, цена 130 очков", command=pockupka.limit_turbo).grid()
    Button(app, text="Удвоитель очков, цена 200 очков", command=pockupka.x2_moneys).grid()


    Label(app, text="\nОбратите внимание, что каждый товар можно купить \n" + 
                    "сколько угодно раз, но если вы так купите щит, то \n" + 
                    "деньги за 2-ой и т.д. разы просто пропадут даром!").grid()

    root.mainloop()
    return pockupka.purchased