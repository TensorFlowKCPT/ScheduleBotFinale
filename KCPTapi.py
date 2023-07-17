import requests
import logger
import datetime

@staticmethod
def GetAllGroups():
    '''
    Возвращает словарь со списком групп и их id

    Пример:
    [
    {
        "ID": "0",
        "Name": "АТ 20-11"
    },
    {
        "ID": "1",
        "Name": "АТ 21-11"
    },
    {
        "ID": "2",
        "Name": "АТ 22-11"
    },
    {
        "ID": "3",
        "Name": "ДО 20-11-1"
    }
    ]
    '''
    response = requests.get('https://shed.kcpt72.ru/api/json/classes_json.php', verify=False)
    if response.status_code == 200 and response.json()!=[]:
        # Обработка успешного ответа
        return response.json()
    else:
        logger.Log('Ошибка при выполнении запроса на получение списка групп: ', response.status_code)
        raise FileNotFoundError

@staticmethod
def GetAllTeachers():
    '''
    Возвращает словарь со списком пеподавателей и их id
    
    Пример:
    [
    {
        "ID": "7",
        "Surname": "Айметдинов",
        "FirstName": "Булат",
        "SecondName": "Илдарович"
    },
    {
        "ID": "8",
        "Surname": "Андреева",
        "FirstName": "Светлана",
        "SecondName": "Рудольфовна"
    },
    {
        "ID": "9",
        "Surname": "Апхадзе",
        "FirstName": "Нино",
        "SecondName": "Алексеевна"
    }
    ]
    '''
    response = requests.get('https://shed.kcpt72.ru/api/json/teachers_json.php', verify=False)
    if response.status_code == 200 and response.json()!=[]:
        # Обработка успешного ответа
        return response.json()
    else:
        logger.Log('Ошибка при выполнении запроса на получение списка преподавателей: ', response.status_code)
        raise FileNotFoundError

@staticmethod
def GetScheduleById(Date:datetime.datetime,GroupId):
    '''
    Принимает:
        Дата:DateTime
        idГруппы:int
    Возвращает расписание, сразу с изменениями
    Пример:
    [
    {
        "Группа": "ИБАС 22-11",
        "Подгруппа": "1",
        "Дата": "2023-02-07",
        "День": "2",
        "Урок": "1",
        "Фамилия": "Гуляев",
        "Имя": "Иван",
        "Отчество": "Павлович",
        "Предмет": "МДК.02.02 Криптографические средства защиты информации",
        "Кабинет": "312",
        "ИЗМЕНЕНИЕ": "Да"
    },
    {
        "Группа": "ИБАС 22-11",
        "Подгруппа": "0",
        "Дата": "2023-02-07",
        "День": "2",
        "Урок": "2",
        "Фамилия": "Бочанов",
        "Имя": "Виктор",
        "Отчество": "Федорович",
        "Предмет": "МДК.01.04 Эксплуатация автоматизированных(информационных) систем в защищенном исполнении",
        "Кабинет": "401",
        "ИЗМЕНЕНИЕ": "Нет"
    },
    {
        "Группа": "ИБАС 22-11",
        "Подгруппа": "0",
        "Дата": "2023-02-07",
        "День": "2",
        "Урок": 3,
        "Фамилия": "Бочанов",
        "Имя": "Виктор",
        "Отчество": "Федорович",
        "Предмет": "МДК.01.04 Эксплуатация автоматизированных(информационных) систем в защищенном исполнении",
        "Кабинет": "401"
    }
    ]
    '''
    
    response = requests.get('https://shed.kcpt72.ru/api/json/class_day_json.php?date='+Date.strftime('%Y-%m-%d')+'&id='+str(GroupId), verify=False)
    if response.status_code == 200 and response.json()!=[]:
        # Обработка успешного ответа
        result = response.json()
        return result
    else:
        logger.Log('Ошибка при выполнении запроса на получение расписания для группы: '+str(GroupId)+' на '+Date.strftime('%d.%m.20%y')+': '+ str(response.status_code))
        raise FileNotFoundError

@staticmethod
def GetScheduleByName(Date:datetime.datetime,GroupName:str):
    '''
    Принимает:
        Дата:DateTime
        НазваниеГруппы:str
    Возвращает расписание, сразу с изменениями
    Пример:
    [
    {
        "Группа": "ИБАС 22-11",
        "Подгруппа": "1",
        "Дата": "2023-02-07",
        "День": "2",
        "Урок": "1",
        "Фамилия": "Гуляев",
        "Имя": "Иван",
        "Отчество": "Павлович",
        "Предмет": "МДК.02.02 Криптографические средства защиты информации",
        "Кабинет": "312",
        "ИЗМЕНЕНИЕ": "Да"
    },
    {
        "Группа": "ИБАС 22-11",
        "Подгруппа": "0",
        "Дата": "2023-02-07",
        "День": "2",
        "Урок": "2",
        "Фамилия": "Бочанов",
        "Имя": "Виктор",
        "Отчество": "Федорович",
        "Предмет": "МДК.01.04 Эксплуатация автоматизированных(информационных) систем в защищенном исполнении",
        "Кабинет": "401",
        "ИЗМЕНЕНИЕ": "Нет"
    },
    {
        "Группа": "ИБАС 22-11",
        "Подгруппа": "0",
        "Дата": "2023-02-07",
        "День": "2",
        "Урок": 3,
        "Фамилия": "Бочанов",
        "Имя": "Виктор",
        "Отчество": "Федорович",
        "Предмет": "МДК.01.04 Эксплуатация автоматизированных(информационных) систем в защищенном исполнении",
        "Кабинет": "401"
    }
    ]
    '''
    dictionary = {item["Name"]:item["ID"] for item in GetAllGroups()}
    GroupId=dictionary[GroupName]
    response = requests.get('https://shed.kcpt72.ru/api/json/class_day_json.php?date='+Date.strftime('%Y-%m-%d')+'&id='+str(GroupId), verify=False)
    if response.status_code == 200 and response.json()!=[]:
        # Обработка успешного ответа
        result = response.json()
        return result
    else:
        logger.Log('Ошибка при выполнении запроса на получение расписания для группы: '+GroupId+' на '+Date.strftime('%d.%m.20%y')+': '+str(response.status_code))
        raise FileNotFoundError

@staticmethod
def GetTeacherScheduleById(Date:datetime.datetime,TeacherId:int):
    '''
    Принимает:
        Дата:DateTime
        id Препода:int
    Возвращает расписание преподавателя
    Пример:
    [
    {
        "Группа": "ИБАС  21-11",
        "Подгруппа": "2",
        "Дата": "2023-02-07",
        "День": "2",
        "Урок": "1",
        "Фамилия": "Гуляев",
        "Имя": "Иван",
        "Отчество": "Павлович",
        "Предмет": "Язык программирования JavaScript",
        "Кабинет": "",
        "ИЗМЕНЕНИЕ": "Нет"
    }
    ]
    '''
    response = requests.get('https://shed.kcpt72.ru/api/json/teacher_day_json.php?date='+Date.strftime('%Y-%m-%d')+'&id='+str(TeacherId), verify=False)
    if response.status_code == 200 and response.json()!=[]:
        # Обработка успешного ответа
        result = response.json()
        return result
    else:
        logger.Log('Ошибка при выполнении запроса на получение расписания для преподавателя: '+str(TeacherId)+' на '+str(Date.strftime('%d.%m.20%y'))+': '+ str(response.status_code))
        raise FileNotFoundError
