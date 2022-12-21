import urllib
import requests
from bs4 import BeautifulSoup
from .models import Post
from PIL import Image
from slugify import slugify
import os
import transliterate
from googletrans import Translator
import datetime
import time
from schedule import Scheduler
import schedule
import threading
from google.cloud import translate_v2


os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r"D:\Рабочий стол\Test_Drives\TranslationAPI\test-drives-310514-ba0e463dd33c.json"
translate_client = translate_v2.Client()
target = 'ru'

#парсинг новостей с сайта www.autonews.ru
#def parse_posts():
#    #Фомируем адресную строку для запроса 
#    sq = 'https://www.autonews.ru/tags/?tag=%D0%9D%D0%BE%D0%B2%D0%BE%D1%81%D1%82%D0%B8'
#    #Получаем HTML страницу
#    doc = urllib.request.urlopen(sq).read().decode('utf-8', errors='ignore')
#    #ищем ссылки на новости
#    soup = BeautifulSoup(doc, 'html5lib')
#    urls = []
#    heads = []
#    posts_text = []
#    body_post = ''
#    img_urls = []
#    for link in soup.find_all('a', attrs={"item-big__link"}):
#        url_new = link.get('href')
#        if not url_new in urls:
#            urls.append(url_new)
#    for post in urls:
#        tx = []
#        url_new = post
#        #ищем заголовки новостей
#        soup = BeautifulSoup(requests.get(url_new).content, 'html.parser')
#        header = soup.find('h1', {'class' : 'js-slide-title'}).get_text().strip()
#        heads.append(header)       
#        #ищем текст новостей
#        doc2 = urllib.request.urlopen(url_new).read().decode('utf-8', errors='ignore')
#        soup = BeautifulSoup(doc2, 'html5lib')
#        for text in soup.select("div[class=l-base__col__main] > p"):
#            p = text.get_text()
#            if p:
#                tx.append(p)
#            body_post = ''.join(tx)
#        posts_text.append(body_post)        
#        #ищем картинки новостей
#        for img in soup.select("div[class=article__main-image__image] > img"):
#            url_img = img.get('src')
#            img_urls.append(url_img)
#        posts = Post.objects.all()
#        lenght = len(heads)
#        for i in range(lenght):
#            post = Post(
#                title = heads[i],
#                slug = slugify((transliterate.translit(heads[i], reversed=True)).lower()),
#                body = posts_text[i],
#                image_jpg = 'images/news/' + slugify(heads[i]) + '.jpg',
#                image_webp = 'images/news/' + slugify(heads[i]) + '.webp',
#                image_webp_small = 'images/news/' + slugify(heads[i]) + '-small' +  '.webp', 
#            )
#            os.makedirs('media/images/news/', exist_ok=True)
#            #Создание картинки
#            try:
#                resource = urllib.request.urlopen(img_urls[i])
#                out = open('media/images/news/' + slugify(heads[i]) + '.jpg', "wb")
#                out.write(resource.read())
#                out.close()
#                #Создание картинки webp
#                image = Image.open('media/images/news/' + slugify(heads[i]) + '.jpg')
#                image = image.convert('RGB')
#                image.save('media/images/news/' + slugify(heads[i]) + '.webp', 'webp')
#                #Создание маленькой картинки webp
#                image_small = image.resize((300, 170))
#                image_small.save('media/images/news/' + slugify(heads[i]) + '-small' + '.webp', 'webp')
#            except:
#                pass
#            if not posts.filter(title=heads[i]).exists():
#                post.save()


#парсинг новостей с сайта www.motor1.com
def parse_posts():
    #Фомируем адресную строку для запроса 
    sq = 'https://www.motor1.com/news/'
    #Получаем HTML страницу
    doc = urllib.request.urlopen(sq).read().decode('utf-8', errors='ignore')
    #ищем ссылки на новости
    soup = BeautifulSoup(doc, 'html5lib')
    urls = []
    body_post = ''
    urls_img = []
    for link in soup.select("div.item.wcom > a"):
        #ссылка на новость
        url_new = 'https://www.motor1.com' + link.get('href')
        if not url_new in urls:
            urls.append(url_new)
    # #ссылка на картинку
    # for img in soup.select("div.item.wcom > img"):
    #     img = img.get('src')
    #     if not img in urls_img:
    #         urls_img.append(img)
    #     print(img)
    #ищем картинки новостей
    #for img in soup.select("div.item > img"):
    #    url_img = img.get('src')
    #    if not url_img in urls_img:
    #        urls_img.append(url_img)

    for post in urls[:1]:
        tx = []
        url_new = post

        #ищем заголовки новостей
        soup = BeautifulSoup(requests.get(url_new).content, 'html.parser')
        header = soup.find('h1', {'class' : 'm1-article-title'}).get_text().strip()
        #перевод заголовка на русский
        output = translate_client.translate(header, target_language=target)
        #translator = Translator(service_urls=['translate.googleapis.com','translate.google.com','translate.google.co.kr'])
        #result = translator.translate(header, src='en', dest='ru')
        head = output['translatedText']
        print(head, datetime.datetime.now())
        
        #ищем текст новостей и описание
        doc2 = urllib.request.urlopen(url_new).read().decode('utf-8', errors='ignore')
        soup = BeautifulSoup(doc2, 'html5lib')
        
        description = soup.find('meta', attrs={'name': 'description'}).get("content", None)        

        for text in soup.select("div.postBody.description.e-content > p"):
            p = text.get_text()
            if p:
                tx.append(p)
            body_post = '\n'.join(tx)
        #перевод текста на русский
        #output2 = translate_client.translate(body_post, target_language=target)
        #post_text = output2['translatedText']

        #translator = Translator(service_urls=['translate.googleapis.com','translate.google.com','translate.google.co.kr'])
        #result2 = translator.translate(body_post, src='en', dest='ru')
        post_text = body_post

        #ищем картинки новостей
        for img in soup.select("div.originalImage.scrollTieBox > picture > img"):
            url_img = img.get('src')
            #if not url_img:
            #    url_img = "C:\Test_Drives\td\media\uploads\2021\01\18\photo_52590on_page.jpeg"
            print(url_img)

        posts = Post.objects.all()
        if not posts.filter(title=head).exists():
            post_news = Post(
                title = head,
                slug = slugify((transliterate.translit(head, 'ru', reversed=True)).lower()),
                body = post_text,
                image_jpg = 'images/news/' + slugify(head) + '.jpg',
                image_webp = 'images/news/' + slugify(head) + '.webp',
                image_webp_small = 'images/news/' + slugify(head) + '-small' +  '.webp', 
                )
            post_news.save()
        os.makedirs('media/images/news/', exist_ok=True)
        #Создание картинки
        try:
            resource = urllib.request.urlopen(url_img)
            out = open('media/images/news/' + slugify(head) + '.jpg', "wb")
            out.write(resource.read())
            out.close()
            #Создание картинки webp
            image = Image.open('media/images/news/' + slugify(head) + '.jpg')
            image = image.convert('RGB')
            image.save('media/images/news/' + slugify(head) + '.webp', 'webp')
            #Создание маленькой картинки webp
            image_small = image.resize((300, 170))
            image_small.save('media/images/news/' + slugify(head) + '-small' + '.webp', 'webp')
        except:
            pass


def job():
    pass
    #print("Работает ......", datetime.datetime.now())
    #parse_posts()

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
    #scheduler.every(2).minutes.do(job)
    #scheduler.every(2).hours.do(job)
    scheduler.every(30).seconds.do(job)
    scheduler.run_continuously()


#def job():
#    parse_posts()

#def start_scheduler():
    #schedule = Scheduler()
    #schedule.every(10).seconds.do(job)
    #schedule.every(3).minutes.do(job)
    #schedule.every().hour.do(job)
    #schedule.every().day.at("10:30").do(job)
    #schedule.every(5).to(10).minutes.do(job)
    #schedule.every().monday.do(job)
    #schedule.every().wednesday.at("13:15").do(job)
    #schedule.every().minute.at(":17").do(job)

    #while True:
    #    schedule.run_pending()
    #    time.sleep(1)
