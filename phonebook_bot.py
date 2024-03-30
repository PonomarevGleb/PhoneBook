import json



def show_all():
    global pb
    for i in pb.keys():
        print(i)
        for j in pb[i]:
            print (*j)
        print()


def save():
    global pb
    with open("phonebook.json", "w") as phonebook:
        phonebook.write(json.dumps(pb, ensure_ascii=False))
    print("Телефонная книга была сохранена")


def get_book():
    global pb
    string = input("Укажите имя файла(вместе с путем, если он находится в другой директории), он будет подгружен вместе с текущим: ")
    with open(string, "r") as phonebook:
        pb.update(json.load(phonebook))
    print("Телефонная книга была добавлена. Не забудьте сохранить изменения.") 


def add():
    global pb
    string = input ("Введите Имя, Фамилию, номера телефонов и почтовые адреса через пробел: ")
    string = string.split()
    phones = [string[i] for i in range(2, len(string)) if string[i][-1].isdigit()]
    mails = [string[i] for i in range(2, len(string)) if not string[i][-1].isdigit()]
    string = {string[0]+" "+string[1]: [phones, mails]}
    pb.update(string)
    print("Запись была добавлена. Не забудьте сохранить изменения.") 


def search():
    global pb
    string = input('Введите поле по которому будет производиться поиск (Имя, Фамилия, телефоны, почты): ')
    if string == "Имя":
        string = input('Введите Имя: ')
        for i in pb.keys():
            if string in i:
                print(i, '\nтелефоны:', *pb[i][0], '\nпочтовые адреса:', *pb[i][1])
    elif string == "Фамилия":
        string = input('Введите Фамилию: ')
        for i in pb.keys():
            if string in i:
                print(i, '\nтелефоны:', *pb[i][0], '\nпочтовые адреса:', *pb[i][1])
    elif string == "телефоны":
        string = input('Введите телефон: ')
        for i in pb.keys():
            if string in pb[i][0]:
                print(i, '\nтелефоны:', *pb[i][0], '\nпочтовые адреса:', *pb[i][1])
    elif string == "почты":
        string = input('Введите почту: ')
        for i in pb.keys():
            if string in pb[i][1]:
                print(i, '\nтелефоны:', *pb[i][0], '\nпочтовые адреса:', *pb[i][1])
    else:
        print("Поле введено неправильно")


def delete():
    global pb
    string = input("Введиете Имя и Фамилию через пробел для удаления записи: ")
    del pb[string]
    print(string, ' удален. Не забудьте сохранить изменения.')


def change():
    global pb
    string = input("Введиете Имя и Фамилию записи, в которую хотите внести изменения:\n")
    for j in pb[string]:
        print (*j)
    field_to_change = input('Введите поле в котором будет производиться изменение (Имя, Фамилия, телефоны, почты): ')
    if field_to_change == "Имя":
        new_name = input('Введите новое Имя: ')
        temp = pb[string]
        del pb[string]
        string = string.split()
        new_name = new_name + " " + string[1]
        string = {new_name: temp}
        pb.update(string)
        print("Имя было изменено. Не забудьте сохранить изменения.")             
    elif field_to_change == "Фамилия":
        new_name = input('Введите новую Фамилию: ')
        temp = pb[string]
        del pb[string]
        string = string.split()
        new_name = string[0] + " " + new_name
        string = {new_name: temp}
        pb.update(string)
        print("Фамилия была изменена. Не забудьте сохранить изменения.") 
    elif field_to_change == "телефоны":
        new_name = input('Добавить, Заменить или Удалить?: ')
        if new_name == 'Добавить':
            new_name = input('Введите новый номер: ')
            pb[string][0].append(new_name)
            print(*pb[string][0])
            print("Номер был добавлен. Не забудьте сохранить изменения.") 
        elif new_name == 'Заменить':
            field_to_change = input('Введите номер который хотите заменить: ')
            new_name = input('Введите новый номер: ')
            i = pb[string][0].index(field_to_change)
            pb[string][0][i] = new_name
            print(*pb[string][0])
            print("Номер был изменен. Не забудьте сохранить изменения.")
        elif new_name == 'Удалить':
            field_to_change = input('Введите номер который хотите удалить: ')
            pb[string][0].remove(field_to_change)
            print("Номер был удален. Не забудьте сохранить изменения.")
        else:
            print("Неправильный ввод")
    elif field_to_change == "почты":
        new_name = input('Добавить, Заменить или Удалить?: ')
        if new_name == 'Добавить':
            new_name = input('Введите новую почту: ')
            pb[string][1].append(new_name)
            print(*pb[string][1])
            print("Почта была добавлена. Не забудьте сохранить изменения.") 
        elif new_name == 'Заменить':
            field_to_change = input('Введите почту которую хотите заменить: ')
            new_name = input('Введите новую почту: ')
            i = pb[string][0].index(field_to_change)
            pb[string][1][i] = new_name
            print(*pb[string][1])
            print("Почта была изменена. Не забудьте сохранить изменения.") 
        elif new_name == 'Удалить':
            field_to_change = input('Введите почту которую хотите удалить: ')
            pb[string][1].remove(field_to_change)
            print("Почта была удален. Не забудьте сохранить изменения.")
        else:
            print("Неправильный ввод")
    else:
        print("Поле введено неправильно")


def load():
    global pb
    with open("phonebook.json", "r") as phonebook:
        pb = json.load(phonebook)
    print("Телефонная книга была загружена")  




pb = {}

flag_cycle = True
try:
    print("Телефонная книга начала работу")
    load()
except:
    s = input("Не смог загрузить файл телефонной книги. Создать пустой файл? \n y/n ")
    if s != "y" and s != "Y":
        flag_cycle = False
        print("Завершаю работу. Хорошего дня")
    else:
        f = open("phonebook.json", "w")
        f.close()


while flag_cycle:
    command = input("Введите команду: ")
    if command == "/save":
        save()
    elif command == "/load":
        load()
    elif command == "/add":
        add()
    elif command == "/all":
        show_all()
    elif command == "/import":
        get_book()
    elif command == "/search":
        search()
    elif command == "/delete":
        delete()
    elif command == "/change":
        change()
    elif command == "/help":
        print("Команды: /save - сохранить \n /load - загрузить \n /add - добавить запись \n /all - показать все записи \n /import - импортировать файл с телефонной книгой \n /search - поиск \n /delete - удаление \n /change - изменение \n /stop - завершить работу")
    elif command == "/stop":
        print("Завершаю работу. Хорошего дня")
        flag_cycle = False  
    else:
        print("Неопознаная команда. Попробуйте /help")

