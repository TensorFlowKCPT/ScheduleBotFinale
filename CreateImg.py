from PIL import Image, ImageDraw, ImageFont
import textwrap
import datetime


@staticmethod

def GetUrokTime(Date:datetime,UrokNumber:int):
    '''
    Принимает дату и порядковый номер урока (Именно в этом порядке, иначе вернет None)
    Возвращает время урока в формате str("8:15-9:00")
    '''
    NormalList = {1:"8:15-9:00",
                  2:"9:00-9:45",
                  3:"9:55-10:40",
                  4:"10:40-11:25",
                  5:"11:40-12:25",
                  6:"12:25-13:10",
                  7:"13:30-14:15",
                  8:"14:15-15:00",
                  9:"15:15-16:00",
                  10:"16:00-16:45",
                  11:"16:55-17:40",
                  12:"17:40-18:25",
                  13:"18:35-19:10"}
    SubbotaList = {1:"8:15-9:00",
                   2:"9:00-9:45",
                   3:"9:50-10:35",
                   4:"10:35-11:20",
                   5:"11:35-12:20",
                   6:"12:20-13:05",
                   7:"13:20-14:05",
                   8:"14:05-14:50",
                   9:"15:05-15:50",
                   10:"15:50-16:35",
                   11:"16:40-17:25",
                   12:"17:25-18:10",
                   13:"18:15-19:00"
                   }
    if Date.strftime('%A')=='Saturday':
        return SubbotaList[int(UrokNumber)]
    else:
        return NormalList[int(UrokNumber)]

def getGroupScheduleAsImg(Schedule):
    header = ["Урок", "Предмет", "Каб.", "Преподаватель", "Время", "Подгруппа"]
    table_data = []
    max_width = 20
    max_width_kab = 3

    for urok in Schedule:
        name_lines = textwrap.wrap(urok["Предмет"], max_width)
        kabinet_lines = textwrap.wrap(urok["Кабинет"], max_width_kab)
        prepod_lines = textwrap.wrap(urok["Фамилия"] + " " + urok["Имя"]+ " " + urok["Отчество"] , max_width)
        row = [int(urok["Урок"]), name_lines, kabinet_lines, prepod_lines, GetUrokTime(datetime.datetime.strptime(urok["Дата"], "%Y-%m-%d"), int(urok["Урок"])), urok["Подгруппа"]]
        table_data.append(row)

        prev_urok = urok

    y = 30 * sum([max([len(row[i]) for i in range(1, 4)]) for row in table_data]) + len(table_data) + 1
    image = Image.new('RGB', (1110, y + 350), color=(255, 255, 255))
    draw = ImageDraw.Draw(image)

    font = ImageFont.truetype('arial.ttf', size=18)

    x = 10
    y = 10

    cell_width = [60, 265, 50, 400, 110, 200]  # Ширина ячеек для каждого столбца
    cell_height = 30

    logo_image = Image.open("Logo.png")
    logo_width, logo_height = logo_image.size
    new_logo_width = int(logo_width * 0.9)
    new_logo_height = int(logo_height * 0.9)
    logo_image = logo_image.resize((new_logo_width, new_logo_height))
    x_logo = (image.width - new_logo_width) // 2
    y_logo = (image.height - new_logo_height) // 2
    image.paste(logo_image, (x_logo, y_logo))

    for i in range(len(header)):
        header_width, header_height = draw.textsize(header[i], font=font)
        text_x = x + (cell_width[i] - header_width) // 2
        text_y = y + (cell_height - header_height) // 2
        draw.rectangle((x, y, x + cell_width[i], y + cell_height), outline=(0, 0, 0))
        draw.text((text_x, text_y), header[i], font=font, fill=(0, 0, 0))
        x += cell_width[i]
    x = 10
    y += cell_height

    for row in table_data:
        max_lines = max([len(row[i]) for i in range(1, 4)])
        for i in range(len(row)):
            draw.rectangle((x, y, x + cell_width[i], y + cell_height * (max_lines + 1)), outline=(0, 0, 0))
            if i == 0:
                draw.text((x + 5, y + 5), str(row[i]), font=font, fill=(0, 0, 0))
            elif i == 1 or i == 2 or i == 3:
                for j, line in enumerate(row[i]):
                    draw.text((x + 5, y + 5 + j * cell_height), line, font=font, fill=(0, 0, 0))
            else:
                draw.text((x + 5, y + 5), str(row[i]), font=font, fill=(0, 0, 0))
            x += cell_width[i]
        x = 10
        y += cell_height * (max_lines + 1)
    
    image.save("TableGroup.png")
    return image

def getTeacherScheduleAsImg(Schedule):
    header = ["Урок", "Группа", "Подгруппа", "Преподаватель", "Предмет", "Кабинет", "Изменения", "Время"]
    table_data = []

    for urok in Schedule:
        prepod_lines = textwrap.wrap(urok["Фамилия"] + " " + urok["Имя"]+ " " + urok["Отчество"] , 25)
        row = [int(urok["Урок"]),textwrap.wrap(urok["Группа"],9), urok["Подгруппа"], prepod_lines, "\n".join(textwrap.wrap(urok["Предмет"], 27)), "".join(textwrap.wrap(urok["Кабинет"], 3)),urok["ИЗМЕНЕНИЕ"], GetUrokTime(datetime.datetime.strptime(urok["Дата"], "%Y-%m-%d"), urok["Урок"])]
        table_data.append(row)

    y = 30 * sum([max([len(row[i]) for i in range(1, 4)]) for row in table_data]) + len(table_data) + 1
    image = Image.new('RGB', (1920, y + 400), color=(255, 255, 255))
    draw = ImageDraw.Draw(image)

    font = ImageFont.truetype('arial.ttf', size=18)

    x = 10
    y = 10

    cell_width = [60, 320, 100, 270, 270, 120, 120, 110]  # Ширина ячеек для каждого столбца
    cell_height = 40

    logo_image = Image.open("Logo.png")
    logo_width, logo_height = logo_image.size
    new_logo_width = int(logo_width * 0.9)
    new_logo_height = int(logo_height * 0.9)
    logo_image = logo_image.resize((new_logo_width, new_logo_height))
    x_logo = (image.width - new_logo_width) // 2
    y_logo = (image.height - new_logo_height) // 2
    image.paste(logo_image, (x_logo, y_logo))

    for i in range(len(header)):
        header_width, header_height = draw.textsize(header[i], font=font)
        text_x = x + (cell_width[i] - header_width) // 2
        text_y = y + (cell_height - header_height) // 2
        draw.rectangle((x, y, x + cell_width[i], y + cell_height), outline=(0, 0, 0))
        draw.text((text_x, text_y), header[i], font=font, fill=(0, 0, 0))
        x += cell_width[i]
    x = 10
    y += cell_height

    for row in table_data:
        max_lines = max([len(row[i]) for i in range(1, 4)])
        for i in range(len(row)):
            draw.rectangle((x, y, x + cell_width[i], y + cell_height * (max_lines + 1)), outline=(0, 0, 0))
            if i == 0:
                draw.text((x + 5, y + 5), str(row[i]), font=font, fill=(0, 0, 0))
            elif i == 1 or i == 2 or i == 3:
                for j, line in enumerate(row[i]):
                    draw.text((x + 5, y + 5 + j * cell_height), line, font=font, fill=(0, 0, 0))
            else:
                draw.text((x + 5, y + 5), str(row[i]), font=font, fill=(0, 0, 0))
            x += cell_width[i]
        x = 10
        y += cell_height * (max_lines + 1)
    
    image.save("TableTeacher.png")
    return image
