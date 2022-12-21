from urllib.parse import quote
import urllib
import re, os
import requests
from django.db.models.fields import SlugField
from .models import Brand, Car, CarVideo
from datetime import datetime, timedelta
from PIL import Image
import datetime
import time
from schedule import Scheduler
import schedule
import threading

now = datetime.datetime.now()


#функция поиска данных видео
def findyoutube(x, filtr):
    carvideo = CarVideo.objects.all()
    mas = []
    #Фомируем адресную строку для запроса 
    sq = 'https://www.youtube.com/results?search_query=' + quote(x) + filtr
    #Получаем HTML страницу с результатом поиска в youtube
    doc = urllib.request.urlopen(sq).read().decode('utf-8', errors='ignore')
    #ищем ссылки на обложки видео
    img = re.findall("\"thumbnail\":{\"thumbnails\":\[\{\"url\":\"https://i.ytimg.com(.+?)\"", doc)
    img_urls = []
    for i in img:
        i = 'https://i.ytimg.com' + i
        img_urls.append(i)
    #Ищем ссылки видео на странице
    id_videos = re.findall("\?v\=(.+?)\"", doc)
    #ищем заголовки видео
    mas_titles = re.findall("\"title\":{\"runs\":\[\{\"text\":\"(.+?)\"", doc)[:20]
    titles = []
    #Список минус слов
    exceptions = [
        'Реклама', 
        'Unlimited', 
        'Forza', 
        'GTA', 
        'multiplayer',
        'NEED',
        'gameplay',
        'Virtual',
        'поиска',
        'Детям',
        'Music',
        'TV',
        'музыкантов',
        'клавиши',
        'Воспроизведение',
        'Общие',
        'Субтитры',
        'Панорамные',
        'авторов',
        'nfs',
        'game',
        ]
    for title in mas_titles:
        i = 0
        for exc in exceptions:
            if not str.lower(exc) in str.lower(title):
                i = i + 1    
        if i == len(exceptions):
            if not title in carvideo.filter(title_video=title):
                titles.append(title)
    #ищем количество просмотров
    numbers = []
    number_of_views = re.findall("\"shortViewCountText\":{\"accessibility\":{\"accessibilityData\":{\"label\":\"(.+?) ", doc)
    for y in number_of_views:
        y = y.replace(",", ".")
        y = y.replace(u'\xa0', u'')
        y = y.replace("тыс.", "")
        y = y.replace("Нет", "0")
        y = y.replace("No", "0")
        y = y.replace("K", "")
        if 'млн' in y:
            y = float(y.replace("млн", ""))*1000000
        elif 'M' in y:
            y = float(y.replace("M", ""))*1000000
        elif 'тыс.' in y:
            y = float(y.replace("тыс.", ""))*1000
        else:
            y = float(y)
        if type(y) is float:
            numbers.append(y)
        elif type(y) is str: 
            pass
    number_of_views = numbers
    #Cоздаем массив 
    if not(id_videos is None):
       for ii in id_videos:
           if(len(ii) < 25):
               mas.append(ii)
    #Чистка массива от дублей
    mas = dict(zip(mas,mas)).values()
    links= []
    for y in mas: 
        links.append('https://www.youtube.com/embed/' + y)
    #Определение размера обложки (720, default, и т.п.) для преобразования в webp
    hq = re.findall("hq(.+?)\.", str(img))
    #Число дней, месяцев, лет с даты выхода видео
    date = re.findall("\"publishedTimeText\":{\"simpleText\":\"(\d+)\ ", doc)
    #Текст после даты выхода видео (день, неделя, месяц, год.. назад)
    text_date = re.findall("\"publishedTimeText\":{\"simpleText\":\".+? (.+?)\ ", doc)

    return links, titles, number_of_views, img_urls, id_videos, hq, date, text_date


#функция сохранения данных видео
def save_video(titles, number_of_views, image_urls, id_videos, brand, car, hq, date, text_date):
    carvideo = CarVideo.objects.all()
    lenght = len(titles)
    days = ['день', 'дня', 'дней', 'day', 'days',]
    week = ['неделя', 'недели', 'недель', 'неделю', 'week', 'weeks',]
    month = ['месяц', 'месяца', 'месяцев', 'month', 'months',]
    year = ['год', 'года', 'лет', 'years', 'year',]
    number_days = 1
    for i in range(lenght):
        try:
            if text_date[i] in days:
                number_days = int(date[i])
            elif text_date[i] in week:
                number_days = int(date[i]) * 7
            elif text_date[i] in month:
                number_days = int(date[i]) * 30
            elif text_date[i] in year:
                number_days = int(date[i]) * 365
            else:
                number_days = 0
        except:
            number_days = 0
        #Сегодня
        today = datetime.datetime.date(now)
        #Дата выхода видео
        date_realise = (today - timedelta(number_days))
        try:
            image_url = image_urls[i]
        except:
            image_url = ''
        try:
            id_video = id_videos[i][:11]
        except:
            id_video = ''
        try:
            number_of_view = number_of_views[i]
        except:
            number_of_view = 0
        try:
            h = hq[i]
        except:
            h = ''
        video = CarVideo(
            age = date_realise,
            title_video = titles[i],
            id_videos = id_video,
            number_of_views = number_of_view,
            image_urls = image_url,
            image_jpg = 'images/{}/{}/'.format(brand, car) + id_video + '.jpg',
            image_webp = 'images/{}/{}/'.format(brand, car) + id_video +  '.webp',
            image_webp_small = 'images/{}/{}/'.format(brand, car) + id_video + '-small' +  '.webp', 
            url = 'https://www.youtube.com/embed/' + id_video,
            brand = brand,
            car = car,
            hq = h,
            available = True,
            )
        #Если карточки с данными видео не существует, создаем ее
        if not carvideo.filter(id_videos=id_video).exists() and not id_video == '' and number_of_view >= 300:
            #Сохраняем карточку с данными видео если больше или равно 300 просмотров
            #if not id_video == '' and number_of_view >= 300:
            video.save()

            os.makedirs('media/images/{}/{}/'.format(brand, car), exist_ok=True)
            #Создание картинки jpg
            try:
                resource = urllib.request.urlopen(image_urls[i])
                out = open('media/images/{}/{}/'.format(brand, car) + id_video + '.jpg', "wb")
                out.write(resource.read())
                out.close()
                #Создание картинки webp
                image = Image.open('media/images/{}/{}/'.format(brand, car) + id_video + '.jpg')
                image = image.convert('RGB')
                image.save('media/images/{}/{}/'.format(brand, car) + id_video + '.webp', 'webp')
                #Создание маленькой картинки webp
                image_small = image.resize((300, 170))
                image_small.save('media/images/{}/{}/'.format(brand, car) + id_video + '-small' + '.webp', 'webp')
            except:
                pass
            

#функция для определения устройства пользователя
def my_view(request):

    # Let's assume that the visitor uses an iPhone...
    request.user_agent.is_mobile # returns True
    request.user_agent.is_tablet # returns False
    request.user_agent.is_touch_capable # returns True
    request.user_agent.is_pc # returns False
    request.user_agent.is_bot # returns False

    # Accessing user agent's browser attributes
    request.user_agent.browser  # returns Browser(family=u'Mobile Safari', version=(5, 1), version_string='5.1')
    request.user_agent.browser.family  # returns 'Mobile Safari'
    request.user_agent.browser.version  # returns (5, 1)
    request.user_agent.browser.version_string   # returns '5.1'

    # Operating System properties
    request.user_agent.os  # returns OperatingSystem(family=u'iOS', version=(5, 1), version_string='5.1')
    request.user_agent.os.family  # returns 'iOS'
    request.user_agent.os.version  # returns (5, 1)
    request.user_agent.os.version_string  # returns '5.1'

    # Device properties
    request.user_agent.device  # returns Device(family='iPhone')
    request.user_agent.device.family  # returns 'iPhone'


#периодический запуск парсинга видео
def job():
    #print("Работает ......", datetime.datetime.now())

    brands = Brand.objects.all()
    cars = Car.objects.all()

    #фильтр за все время по количеству просмотров
    filtr = '&sp=CAMSAhAB'
    for brand in brands[:1]:
        cars = Car.objects.filter(brand=brand, available=True)
        for car in cars[:1]:
            links, titles, number_of_views, image_urls, id_videos, hq, date, text_date = findyoutube('Тест драйв ' + str(brand) + str(car), filtr)
            #Запись в модель CarVideo новых данных
            save_video(titles, number_of_views, image_urls, id_videos, brand, car, hq, date, text_date)

    #фильтр за все время по дате загрузки
    filtr = '&sp=CAI%253D'
    for brand in brands[:1]:
        cars = Car.objects.filter(brand=brand, available=True)
        for car in cars[:3]:
            links, titles, number_of_views, image_urls, id_videos, hq, date, text_date = findyoutube('Тест драйв ' + str(brand) + str(car), filtr)
            #Запись в модель CarVideo новых данных
            save_video(titles, number_of_views, image_urls, id_videos, brand, car, hq, date, text_date)


#периодический автозапуск парсера 
def run_continuously(self, interval=1):
    cease_continuous_run = threading.Event()

    class ScheduleThread(threading.Thread):

        @classmethod
        def run(cls):
            while not cease_continuous_run.is_set():
                self.run_pending()
                time.sleep(interval)

    continuous_thread = ScheduleThread()
    continuous_thread.setDaemon(True)
    continuous_thread.start()
    return cease_continuous_run

Scheduler.run_continuously = run_continuously

def start_scheduler():
    scheduler = Scheduler()
    scheduler.every().monday.at("01:15").do(job)
    #scheduler.every(30).minutes.do(job)
    #scheduler.every(2).hours.do(job)
    #scheduler.every(30).seconds.do(job)
    scheduler.run_continuously()
