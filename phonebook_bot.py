import json
import telebot


API_TOKEN = '7179844878:AAHe5HE5tpSUAYnPGtm5GajujMJ1hmiz9qE'
bot = telebot.TeleBot(API_TOKEN)

pb = {}


@bot.message_handler(commands=['start'])
def start_message(message):
    global pb
    bot.send_message(message.chat.id, "Телефонная книга начала работу")
    try:     
        with open("phonebook.json", "r") as phonebook:
            pb = json.load(phonebook)
        bot.send_message(message.chat.id, "Телефонная книга была загружена") 
    except:
        msg = bot.reply_to(message, "Не смог загрузить файл телефонной книги. Создать пустой файл? \n y/n ")
        bot.register_next_step_handler(msg, cant_load)
        
def cant_load(message):
    s = message.text
    if s != "y" and s != "Y":
        bot.send_message(message.chat.id, "Завершаю работу. Хорошего дня")
    else:
        f = open("phonebook.json", "w")
        f.close()


@bot.message_handler(commands=['load'])
def load(message):
    global pb
    with open("phonebook.json", "r") as phonebook:
        pb = json.load(phonebook)
    bot.send_message(message.chat.id, "Телефонная книга была загружена")  


@bot.message_handler(commands=['all'])
def show_all(message):
    global pb
    res = ""
    for i in pb.keys():
        res += f"{i}:"
        for j in pb[i]:
            for k in j:
                res += f" {k}"
            res += "  "   
        res += "\n"
    bot.send_message(message.chat.id, res)
        

@bot.message_handler(commands=['add'])
def add(message):
    msg = bot.reply_to(message, "Введите Имя, Фамилию, номера телефонов и почтовые адреса через пробел: ")
    bot.register_next_step_handler(msg, add_info)

def add_info(message):
    global pb
    input_string = message.text.split()
    phones = [input_string[i] for i in range(2, len(input_string)) if input_string[i][-1].isdigit()]
    mails = [input_string[i] for i in range(2, len(input_string)) if not input_string[i][-1].isdigit()]
    input_string = {input_string[0]+" "+input_string[1]: [phones, mails]}
    pb.update(input_string)
    bot.send_message(message.chat.id, "Запись была добавлена. Не забудьте сохранить изменения.") 


@bot.message_handler(commands=['save'])
def save(message):
    global pb
    with open("phonebook.json", "w") as phonebook:
        phonebook.write(json.dumps(pb, ensure_ascii=False))
    bot.send_message(message.chat.id, "Телефонная книга была сохранена.")


@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, "Команды: \n /start - начать работу бота \n /save - сохранить \n /load - загрузить \n /add - добавить запись \n /all - показать все записи \n /search - поиск \n /delete - удаление \n /change - изменение \n")


@bot.message_handler(commands=['search'])
def search(message):
    msg = bot.reply_to(message, 'Введите поле по которому будет производиться поиск (Имя, Фамилия, телефоны, почты): ')
    bot.register_next_step_handler(msg, search_field)

def search_field(message):
    input_string = message.text
    if input_string == "Имя":
        msg = bot.reply_to(message, 'Введите Имя: ')
        bot.register_next_step_handler(msg, search_field_name)  
    elif input_string == "Фамилия":
        msg = bot.reply_to(message, 'Введите Фамилию: ')
        bot.register_next_step_handler(msg, search_field_surname)
    elif input_string == "телефоны":
        msg = bot.reply_to(message, 'Введите телефон: ')
        bot.register_next_step_handler(msg, search_field_phone)
    elif input_string == "почты":
        msg = bot.reply_to(message, 'Введите почту: ')
        bot.register_next_step_handler(msg, search_field_mail)
    else:
        bot.send_message(message.chat.id, "Поле введено неправильно")

def search_field_name(message):
    global pb
    input_string = message.text
    for i in pb.keys():
        if input_string in i:
            bot.send_message(message.chat.id, f"{i}\nтелефоны: {pb[i][0]}\nпочтовые адреса: {pb[i][1]}")

def search_field_surname(message):
    global pb
    input_string = message.text
    for i in pb.keys():
        if input_string in i:
            bot.send_message(message.chat.id, f"{i}\nтелефоны: {pb[i][0]}\nпочтовые адреса: {pb[i][1]}")

def search_field_phone(message):
    global pb
    input_string = message.text
    for i in pb.keys():
        if input_string in pb[i][0]:
            bot.send_message(message.chat.id, f"{i}\nтелефоны: {pb[i][0]}\nпочтовые адреса: {pb[i][1]}")

def search_field_mail(message):
    global pb
    input_string = message.text
    for i in pb.keys():
        if input_string in pb[i][1]:
            bot.send_message(message.chat.id, f"{i}\nтелефоны: {pb[i][0]}\nпочтовые адреса: {pb[i][1]}")


@bot.message_handler(commands=['delete'])
def delete(message):
    msg = bot.reply_to(message, "Введиете Имя и Фамилию через пробел для удаления записи: ")
    bot.register_next_step_handler(msg, delete_record)

def delete_record(message):
    global pb
    input_string = message.text
    del pb[input_string]
    bot.send_message(message.chat.id, f"{input_string} удален. Не забудьте сохранить изменения.")


@bot.message_handler(commands=['change'])
def change(message):
    msg = bot.reply_to(message, "Введиете Имя и Фамилию записи, в которую хотите внести изменения: ")
    bot.register_next_step_handler(msg, change_second)

def change_second(message):
    global input_string
    input_string = message.text
    res = input_string
    for j in pb[input_string]:
        for k in j:
            res += " " + k
    bot.send_message(message.chat.id, res)
    msg = bot.reply_to(message, 'Введите поле в котором будет производиться изменение (Имя, Фамилия, телефоны, почты): ')
    bot.register_next_step_handler(msg, change_third)

def change_third(message):
    global input_string
    global field_to_change
    field_to_change = message.text
    if field_to_change == "Имя":
        msg = bot.reply_to(message, 'Введите новое Имя: ')
        bot.register_next_step_handler(msg, change_field_name)  
    elif field_to_change == "Фамилия":
        msg = bot.reply_to(message, 'Введите новую Фамилию: ')
        bot.register_next_step_handler(msg, change_field_surname)
    elif field_to_change == "телефоны":
        msg = bot.reply_to(message, 'Добавить, Заменить или Удалить?: ')
        bot.register_next_step_handler(msg, change_field_phone)
    elif field_to_change == "почты":
        msg = bot.reply_to(message, 'Добавить, Заменить или Удалить?: ')
        bot.register_next_step_handler(msg, change_field_mail)
    else:
        bot.send_message(message.chat.id, "Поле введено неправильно")
    
def change_field_name(message):
    global pb
    global input_string
    global field_to_change
    new_name = message.text
    temp = pb[input_string]
    del pb[input_string]
    input_string = input_string.split()
    new_name = new_name + " " + input_string[1]
    input_string = {new_name: temp}
    pb.update(input_string)
    bot.send_message(message.chat.id, "Имя было изменено. Не забудьте сохранить изменения.")  

def change_field_surname(message):
    global pb
    global input_string
    global field_to_change
    new_name = message.text
    temp = pb[input_string]
    del pb[input_string]
    input_string = input_string.split()
    new_name = input_string[0] + " " + new_name
    input_string = {new_name: temp}
    pb.update(input_string)
    bot.send_message(message.chat.id, "Фамилия была изменена. Не забудьте сохранить изменения.") 

def change_field_phone(message):
    action_type = message.text
    if action_type == 'Добавить':
        msg = bot.reply_to(message, 'Введите новый номер: ')
        bot.register_next_step_handler(msg, change_phone_add)
    elif action_type == 'Заменить':
        msg = bot.reply_to(message, 'Введите номер который хотите заменить: ')
        bot.register_next_step_handler(msg, change_phone_replace)
    elif action_type == 'Удалить':
        msg = bot.reply_to(message, 'Введите номер который хотите удалить: ')
        bot.register_next_step_handler(msg, change_phone_delete)
    else:
         bot.send_message(message.chat.id, "Неправильный ввод")

def change_phone_add(message):
    global pb
    global input_string
    new_name = message.text
    pb[input_string][0].append(new_name)
    res = ""
    for i in pb[input_string][0]:
        res += i + " "
    bot.send_message(message.chat.id, res)
    bot.send_message(message.chat.id, "Номер был добавлен. Не забудьте сохранить изменения.") 

def change_phone_replace(message):
    global field_to_change
    field_to_change = message.text
    msg = bot.reply_to(message, 'Введите новый номер: ')
    bot.register_next_step_handler(msg, change_phone_replace_second)

def change_phone_replace_second(message):
    global input_string
    global field_to_change
    new_name = message.text
    i = pb[input_string][0].index(field_to_change)
    pb[input_string][0][i] = new_name
    res = ""
    for i in pb[input_string][0]:
        res += i + " "
    bot.send_message(message.chat.id, res)
    bot.send_message(message.chat.id, "Номер был изменен. Не забудьте сохранить изменения.")

def change_phone_delete(message):
    global pb
    global input_string
    global field_to_change
    field_to_change = message.text
    pb[input_string][0].remove(field_to_change)
    res = ""
    for i in pb[input_string][0]:
        res += i + " "
    bot.send_message(message.chat.id, res)
    bot.send_message(message.chat.id, "Номер был удален. Не забудьте сохранить изменения.")

def change_field_mail(message):
    action_type = message.text
    if action_type == 'Добавить':
        msg = bot.reply_to(message, 'Введите новую почту: ')
        bot.register_next_step_handler(msg, change_mail_add)
    elif action_type == 'Заменить':
        msg = bot.reply_to(message, 'Введите почту которую хотите заменить: ')
        bot.register_next_step_handler(msg, change_mail_replace)
    elif action_type == 'Удалить':
        msg = bot.reply_to(message, 'Введите почту которую хотите удалить: ')
        bot.register_next_step_handler(msg, change_mail_delete)
    else:
         bot.send_message(message.chat.id, "Неправильный ввод")

def change_mail_add(message):
    global pb
    global input_string
    new_name = message.text
    pb[input_string][1].append(new_name)
    res = ""
    for i in pb[input_string][1]:
        res += i + " "
    bot.send_message(message.chat.id, res)
    bot.send_message(message.chat.id, "Почта была добавлена. Не забудьте сохранить изменения.") 

def change_mail_replace(message):
    global field_to_change
    field_to_change = message.text
    msg = bot.reply_to(message, 'Введите новeую почту: ')
    bot.register_next_step_handler(msg, change_mail_replace_second)

def change_mail_replace_second(message):
    global input_string
    global field_to_change
    new_name = message.text
    i = pb[input_string][1].index(field_to_change)
    pb[input_string][1][i] = new_name
    res = ""
    for i in pb[input_string][1]:
        res += i + " "
    bot.send_message(message.chat.id, res)
    bot.send_message(message.chat.id, "Почта была изменена. Не забудьте сохранить изменения.")

def change_mail_delete(message):
    global pb
    global input_string
    global field_to_change
    field_to_change = message.text
    pb[input_string][1].remove(field_to_change)
    res = ""
    for i in pb[input_string][1]:
        res += i + " "
    bot.send_message(message.chat.id, res)
    bot.send_message(message.chat.id, "Почта была удалена. Не забудьте сохранить изменения.")


bot.polling()
