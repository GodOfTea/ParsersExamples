import requests
import csv
from bs4 import BeautifulSoup as bs

headers = \
    {
        "accept": "*/*",
        "user-agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36"
    }

baseUrl = "https://hh.ru/search/vacancy?search_period=3&area=3&text=python&page=0"

def hh_parse(baseUrl, headers):
    vacancies = []
    urls = []
    urls.append(baseUrl)
    session = requests.Session()
    request = session.get(baseUrl, headers=headers)

    if request.status_code == 200:
        soup = bs(request.content, "lxml")
        try:
            pagination = soup.find_all("a", attrs={"data-qa": "pager-page"})
            count = int(pagination[-1].text)
            for i in range(count):
                url = f"https://hh.ru/search/vacancy?search_period=3&area=3&text=python&page={i}"
                if url not in urls:
                    urls.append(url)
        except:
            pass
        for url in urls:
            request = session.get(url, headers=headers)
            soup = bs(request.content, "lxml")
            divs = soup.find_all("div", attrs={"data-qa": "vacancy-serp__vacancy"})
            for div in divs:
                try:
                    tittle = div.find("a", attrs={"data-qa": "vacancy-serp__vacancy-title"}).text
                    href = div.find("a", attrs={"data-qa": "vacancy-serp__vacancy-title"})["href"]
                    company = div.find("a", attrs={"data-qa": "vacancy-serp__vacancy-employer"}).text
                    description1 = div.find("div", attrs={"data-qa": "vacancy-serp__vacancy_snippet_responsibility"}).text
                    description2 = div.find("div", attrs={"data-qa": "vacancy-serp__vacancy_snippet_requirement"}).text
                    content = description1 + " " + description2

                    vacancies.append \
                        ({
                            "tittle": tittle,
                            "href": href,
                            "company": company,
                            "content": content
                        })
                except:
                    pass

            print(len(vacancies))
    else:
        print("ERROR")
    return vacancies

def files_writer(vacancies):
    with open("parsedVacancies.csv", "w") as file:
        aPen = csv.writer(file)
        aPen.writerow(("Вакансия", "URL", "Компания", "Описание"))
        for vacancie in vacancies:
            aPen.writerow((vacancie["tittle"], vacancie["href"], vacancie["company"], vacancie["content"]))

vacancies = hh_parse(baseUrl, headers)
files_writer(vacancies)