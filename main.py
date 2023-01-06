import time
import bs4
import requests as r
import telebot
from config import ADMIN_ID


projects = {}
categories = [
    "business",
    "development",
    "engineering-architecture",
    "design",
    "marketing",
    "writing-translation",
    "support",
    "training"
]
categories = {
    "business": "",
    "development": "",
    "engineering-architecture": "",
    "design": "",
    "marketing": "",
    "writing-translation": "",
    "support": "",
    "training": ""
}

sorts = {
    "latest": "",
    "oldest": "",
    "less_bids": "",
    "more_bids": "",
}
# ?keyword=search
# ?category=___
# ?sort=___
# ?budget_min=50&budget_max=2500
# ?duration=0
# ?skills=arabic

PROJECTS_URL = "https://mostaql.com/projects?category=development&sort=latest"
headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.0.0 Safari/537.36",
}
s = r.session()
s.headers.update(headers)

API_KEY = "5713781198:AAGFKLtm3md9OJ44GMItl_HX7tKEKAXe-3Y"
bot = telebot.TeleBot(API_KEY, parse_mode="HTML")
print("BOT started...")


def format_project(project_dict: dict) -> str:
    return f"""<b>
📌 {project_dict['title']}

🔗 الرابط: <a href='{project_dict['url']}'>__ إضغط هنا __</a>

_ لحالة: {project_dict['state']}

_ الميزانية: {project_dict['budget']}

_ زمن المشروع: {project_dict['duration']}

👥 العروض: {project_dict['offers'] if project_dict['offers'] != "أضف أول عرض" else "0"}

📅 بتاريخ: {project_dict['date']}

👤 من: {project_dict['user']}

📝 وصف: {project_dict['desc']}
</b>"""


def get_projects():
    new_projects = []
    data = s.get(PROJECTS_URL)
    projects_page = bs4.BeautifulSoup(data.content, 'html.parser')
    table = projects_page.find(name="table", attrs={"class": "projects-table"}).find("tbody")
    results: list[bs4.element.Tag] = table.find_all("tr")

    for result in results:
        item = result.find('td')

        desc = item.findChildren()[-1].text.strip()
        node_2 = item.findChildren()[0].find('div').find('ul').find_all('li')
        user = node_2[0].text.strip()
        offers = node_2[2].text.strip()
        date = node_2[1].text.strip().replace('\n', '')
        date = " ".join(filter(bool, date.split(" ")))

        node_1 = item.findChildren()[0].find('div').find('h2').find('a')
        title = node_1.text.strip()
        url = node_1['href']
        key = url.split('/project/')[-1]

        data = s.get(url)
        project_page = bs4.BeautifulSoup(data.content, 'html.parser')
        table = project_page.find(name="table", attrs={"class": "table table-borderless mrg--an text-meta"}).find("tbody")
        results: list[bs4.element.Tag] = table.find_all("tr")
        # حالة المشروع	مفتوح
        # تاريخ النشر	منذ 4 دقائق
        # الميزانية	$100.00 - $250.00
        # مدة التنفيذ	1 يوم
        # متوسط العروض	$100.00
        # عدد العروض	3
        state = results[0].findChildren()[-1].text.strip()
        budget = results[2].findChildren()[-1].text.strip()
        duration = results[3].findChildren()[-1].text.strip()

        if key not in projects.keys():
            projects[key] = {
                    "key": key,
                    "title": title,
                    "desc": desc,
                    "user": user,
                    "date": date,
                    "offers": offers,
                    "url": url,
                    "state": state,
                    "budget": budget,
                    "duration": duration,
            }
            new_projects.append({
                "key": key,
                "title": title,
                "desc": desc,
                "user": user,
                "date": date,
                "offers": offers,
                "url": url,
                "state": state,
                "budget": budget,
                "duration": duration,
            })

    return new_projects


def send(items):
    for item in items:
        bot.send_message(ADMIN_ID, format_project(item), disable_web_page_preview=True)


def start():
    while True:
        new_projects = get_projects()
        send(new_projects[::-1])
        time.sleep(60 * 2)


start()


while True:
    try:
        bot.polling(none_stop=True, interval=0, timeout=0)
    except NameError as _:
        print('NameError', _)
    except Exception as _:
        print(_)
        time.sleep(10)
