from celery import task
from urllib.parse import quote
import urllib
import re, os
from .views import CarVideo
from datetime import datetime, timedelta
from PIL import Image


now = datetime.now()

@task
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
    number_of_views = re.findall("\"shortViewCountText\":{\"simpleText\":\"(.+?) ", doc)
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


@task
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
        today = datetime.date(now)
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
        if not carvideo.filter(id_videos=id_video).exists():
            
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
            #Сохраняем карточку с данными видео если больше или равно 300 просмотров
            if not id_video == '' and number_of_view >= 300:
                video.save()