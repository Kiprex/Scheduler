from tkinter import *
from tkinter import messagebox, ttk, simpledialog
import sys, os

#---------------------------------------Вспомогательные функции----------------------------------------------

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

#---------------------------------------Функции кнопок---------------------------------------------- 
def btn_click():
    global current_day, current_num, entries, subjects
    number = current_num
    subject = subjects.get()
    output_empty = f'Под номером {number} предмет удален'
    if number == '':
        messagebox.showerror(title='Ошибка', message='Вы не ввели номер предмета!')
    else:    
        if subject == '*удалить предмет*':
            with open(f'data/{current_day}.txt', 'r', encoding='utf-8') as x:
                day = x.read().split('|')
                day[int(number) - 1] = 'пусто'
            with open(f'data/{current_day}.txt', 'w', encoding='utf-8') as x:
                x.truncate(0)
                x.seek(0)
                x.write('|'.join(day))    
            messagebox.showinfo(title='Операция завершена', message=output_empty)
        elif subject == 'Добавить':
            prompt = simpledialog.askstring(title='Введите новый предмет', prompt='Введите новый предмет')
            messagebox.showinfo(title='Операция завершена', message=f'Под номером {number} записан предмет {prompt}')
            with open(f'data/{current_day}.txt', 'r', encoding='utf-8') as x:
                day = x.read().split('|')
                day[int(number) - 1] = prompt
            with open(f'data/{current_day}.txt', 'w', encoding='utf-8') as x:
                x.truncate(0) 
                x.seek(0)
                x.write('|'.join(day))
            with open('data/lessons.txt', 'r', encoding='utf-8') as x:
                les = x.read().split('|')
                les.remove('Добавить')
                les.append(prompt)
                les.append('Добавить')
                subjects['values'] = les
            with open('data/lessons.txt', 'w', encoding='utf-8') as x:
                x.truncate(0)
                x.seek(0)
                x.write('|'.join(les))
        elif subject == '':
            messagebox.showerror(title='Ошибка', message='Вы ничего не ввели!')
        else:
            with open(f'data/{current_day}.txt', 'r', encoding='utf-8') as x:
                day = x.read().split('|')
                day[int(number) - 1] = subject
            with open(f'data/{current_day}.txt', 'w', encoding='utf-8') as x:
                x.truncate(0)
                x.seek(0)
                x.write('|'.join(day))
            messagebox.showinfo(title='Операция завершена', message=f'Под номером {number} записан предмет {subject}')
            
def clear_lessons():
    with open(f'data/lessons.txt', 'w', encoding='utf-8') as x:
        x.truncate(0)
        x.seek(0)
        x.write('*удалить предмет*|Добавить')
    messagebox.showinfo(title='Операция завершена', message='Список предметов очищен')
    with open('data/lessons.txt', 'r', encoding='utf-8') as x:
        subjects['values'] = x.read().split('|')

def clear_schedule():
    for i in range(1, 7):
        with open(f'data/{i}.txt', 'r', encoding='utf-8') as x:
            day = x.read().split('|')
            for j in range(8):
                day[j - 1] = 'пусто'
        with open(f'data/{i}.txt', 'w', encoding='utf-8') as x:
            x.truncate(0)
            x.seek(0)
            x.write('|'.join(day))
    messagebox.showinfo(title='Операция завершена', message='Расписание очищено')
    
def left_n():
    global right_b_n, switch_label_n, left_b_n, current_num
    current_num -= 1
    switch_label_n.configure(text=current_num)
    if current_num == 1:
        left_b_n.configure(state='disable', relief=FLAT)
    else:
        right_b_n.configure(state='active', relief=GROOVE)

def right_n():
    global left_b_n, switch_label_n, right_b_n, current_num
    current_num += 1
    switch_label_n.configure(text=current_num)
    if current_num == 8:
        right_b_n.configure(state='disable', relief=FLAT)
    else:
        left_b_n.configure(state='active', relief=GROOVE)

def left():
    global current_day, switch_label, week, left_b
    current_day -= 1
    switch_label.configure(text=week[current_day])
    if current_day == 1:
        left_b.configure(state='disable', relief=FLAT)
    else:
        right_b.configure(state='active', relief=GROOVE)

def right():
    global current_day, switch_label, week, right_b
    current_day += 1
    switch_label.configure(text=week[current_day])
    if current_day == 6:
        right_b.configure(state='disable', relief=FLAT)
    else:
        left_b.configure(state='active', relief=GROOVE)

#---------------------------------------Конфиг второго окна----------------------------------------------         

def show_schedule():
    Schedule = Toplevel(Main_window)
    Schedule.geometry('1000x900+0+0')
    Schedule.title('Расписание')
    Schedule.resizable(width=False, height=False)
    md = (d1 := open('data/1.txt', 'r', encoding="utf-8")).readline().split('|')
    tue = (d2 := open('data/2.txt', 'r', encoding="utf-8")).readline().split('|')
    wd = (d3 := open('data/3.txt', 'r', encoding="utf-8")).readline().split('|')
    thu = (d4 := open('data/4.txt', 'r', encoding="utf-8")).readline().split('|')
    fri = (d5 := open('data/5.txt', 'r', encoding="utf-8")).readline().split('|')
    st = (d6 := open('data/6.txt', 'r', encoding="utf-8")).readline().split('|')
    
    (MainFrame := LabelFrame(Schedule)).pack(side=TOP)
    
    (TopFrame := LabelFrame(MainFrame)).pack(side=TOP)
    (BottomFrame := LabelFrame(MainFrame)).pack(side=TOP)

    (monday := LabelFrame(TopFrame, bg='gray', text='Понедельник')).pack(ipadx=10, ipady=10, expand=1, fill=BOTH, side=LEFT)
    (tuesday := LabelFrame(TopFrame, bg='gray', text='Вторник')).pack(ipadx=10, ipady=10, expand=1, fill=BOTH, side=LEFT)
    (wednesday := LabelFrame(TopFrame, bg='gray', text='Среда')).pack(ipadx=10, ipady=10, expand=1, fill=BOTH, side=LEFT)
    (thursday := LabelFrame(BottomFrame, bg='gray', text='Четверг')).pack(ipadx=10, ipady=10, expand=1, fill=BOTH, side=LEFT)
    (friday := LabelFrame(BottomFrame, bg='gray', text='Пятница')).pack(ipadx=10, ipady=10, expand=1, fill=BOTH, side=LEFT)
    (saturday := LabelFrame(BottomFrame, bg='gray', text='Суббота')).pack(ipadx=10, ipady=10, expand=1, fill=BOTH, side=LEFT)

    for i in range(8):
        (m := LabelFrame(monday)).pack(side=TOP)
        Label(m, width=2, height=2, bg='cornsilk2', text=f'{i + 1}').pack(side=LEFT)
        Label(m, width=30, height=2, bg='cornsilk2', text=f'{md[i]}').pack(side=LEFT)
    for i in range(8):
        (tu := LabelFrame(tuesday)).pack(side=TOP)
        Label(tu, width=2, height=2, bg='cornsilk2', text=f'{i + 1}').pack(side=LEFT)
        Label(tu, width=30, height=2, bg='cornsilk2', text=f'{tue[i]}').pack(side=LEFT)
    for i in range(8):
        (w := LabelFrame(wednesday)).pack(side=TOP)
        Label(w, width=2, height=2, bg='cornsilk2', text=f'{i + 1}').pack(side=LEFT)
        Label(w, width=30, height=2, bg='cornsilk2', text=f'{wd[i]}').pack(side=LEFT)
    for i in range(8):
        (th := LabelFrame(thursday)).pack(side=TOP)
        Label(th, width=2, height=2, bg='cornsilk2', text=f'{i + 1}').pack(side=LEFT)
        Label(th, width=30, height=2, bg='cornsilk2', text=f'{thu[i]}').pack(side=LEFT)
    for i in range(8):
        (f := LabelFrame(friday)).pack(side=TOP)
        Label(f, width=2, height=2, bg='cornsilk2', text=f'{i + 1}').pack(side=LEFT)
        Label(f, width=30, height=2, bg='cornsilk2', text=f'{fri[i]}').pack(side=LEFT)
    for i in range(8):
        (s := LabelFrame(saturday)).pack(side=TOP)
        Label(s, width=2, height=2, bg='cornsilk2', text=f'{i + 1}').pack(side=LEFT)
        Label(s, width=30, height=2, bg='cornsilk2', text=f'{st[i]}').pack(side=LEFT)
    d1.close()
    d2.close()
    d3.close()
    d4.close()
    d5.close()
    d6.close()
    
#---------------------------------------Списки и переменные---------------------------------------------- 
current_num = 1
current_day = 1
current_switcher = 1
week = {1:'Понедельник', 
        2:'Вторник', 
        3:'Среда', 
        4:'Четверг', 
        5:'Пятница', 
        6:'Суббота'}


#---------------------------------------Конфиг главного окна----------------------------------------------  

Main_window = Tk()
Main_window.iconbitmap('data/icon.ico')
Main_window.geometry('800x600+80+80')
Main_window.title('Составитель расписания')
Main_window.config(bg='azure3')
Main_window.resizable(width=False, height=False)



#Переключатель дня недели
(switcher := Frame(Main_window, bg='azure3')).pack(ipadx=10, ipady=10, expand=1, side=TOP)
Label(switcher, text='Выберите номер урока', bg='azure3').pack(ipadx=10, ipady=10, side=TOP, anchor=CENTER)
(left_b := Button(switcher, text='◀', bg='darkgray', relief=FLAT, bd=8,  command=left, state='disable')).pack(side=LEFT, anchor=CENTER)
(switch_label := Label(switcher, text=week[current_day], bg='darkgray', bd=2, width=10, relief=GROOVE)).pack(ipadx=10, ipady=10, side=LEFT, anchor=CENTER)
(right_b := Button(switcher, text='▶', bg='darkgray', relief=GROOVE, bd=8, command=right)).pack(side=LEFT, anchor=CENTER)

#Переключатель номера урока
(switcher_n := Frame(Main_window, bg='azure3')).pack(ipadx=10, ipady=10, expand=1, side=TOP, anchor=CENTER)
Label(switcher_n, text='Выберите номер урока', bg='azure3').pack(ipadx=10, ipady=10, side=TOP, anchor=CENTER)
(left_b_n := Button(switcher_n, text='◀', bg='darkgray', relief=FLAT, bd=8, command=left_n, state='disable')).pack(side=LEFT, anchor=CENTER)
(switch_label_n := Label(switcher_n, text=current_num, bg='darkgray', bd=2, width=10, relief=GROOVE)).pack(ipadx=10, ipady=10, side=LEFT, anchor=CENTER)
(right_b_n := Button(switcher_n, text='▶', bg='darkgray', relief=GROOVE, bd=8, command=right_n)).pack(side=LEFT, anchor=CENTER)

#Поля ввода
(entries := Frame(Main_window, bg='azure3')).pack(ipadx=10, ipady=10, expand=1, fill=BOTH ,side=TOP, anchor=CENTER)
Label(entries, text='Введите предмет', bg='azure3').pack(ipadx=10, ipady=10, side=TOP)
subjects = ttk.Combobox(entries, textvariable=int)
with open('data/lessons.txt', 'r', encoding='utf-8') as x:
    subjects['values'] = x.read().split('|')
subjects['state'] = 'readonly'
subjects.pack(ipadx=10, ipady=10, side=TOP)
Button(entries, text='Отправить', bg='darkgray', relief=GROOVE, bd=8, command=btn_click).pack(ipadx=10, ipady=10, side=TOP)

#Кнопки
(buttons := Frame(Main_window, bg='azure3')).pack(ipadx=10, ipady=10, expand=1, fill=BOTH, side=TOP)
Button(buttons, text='Показать текущее расписание', bg='darkgray', relief=GROOVE, bd=8, width=28, command=show_schedule).pack(ipadx=10, ipady=10, side=RIGHT, anchor='w')
Button(buttons, text='Очистить список предметов', bg='darkgray', relief=GROOVE, bd=8, width=28, command=clear_lessons).pack(ipadx=10, ipady=10, side=RIGHT, anchor='c')
Button(buttons, text='Очистить текущее расписание', bg='darkgray', relief=GROOVE, bd=8, width=28, command=clear_schedule).pack(ipadx=10, ipady=10, side=RIGHT, anchor='e')

Main_window.mainloop()