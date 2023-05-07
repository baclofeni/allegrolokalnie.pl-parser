import requests
import time
from bs4 import BeautifulSoup
#from requests_html import HTMLSession
#proxies = {
# 'http': 'http://hagtY9:7mVRZw@212.102.152.33:8000',
#  'https': 'https://hagtY9:7mVRZw@212.102.152.33:8000',
#}

session = requests.Session()
#session.proxies.update(proxies)
product_name = input("Чё ищем? ")
min_price = input("Минимальная цена ")
max_price = input("Максимальная цена ")
a = int(input("Сколько страниц парсмим? (с 1-й до ...) "))
session = HTMLSession()

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
}

phone_numbers = []


for page in range(1, a):  # change the range to adjust the number of pages to scrape
    search_url = f"https://allegrolokalnie.pl/oferty/q/{product_name}?price_from={min_price}&price_to={max_price}&page={page}"
    response = requests.get(search_url, headers=headers)

    soup = BeautifulSoup(response.content, "html.parser")

    product_listings = soup.find_all("article")

    for listing in product_listings:
        name = listing.find("h3", class_="mlc-itembox__title")
        price = listing.find("span", class_="ml-offer-price__dollars")
        link = 'https://allegrolokalnie.pl' + listing.find("a", {"class": "mlc-card mlc-itembox"}).get("href")

        # Visit the product page
        r = session.get(link)
        r.html.render()

        # Check for the button
        button = r.html.find('.ml-clear-btn.mlc-seller-details-contact__wrapper')
        if button:
            print("Есть номер! Ща напишем... ")

            # Execute the JavaScript to show the phone number
            script = """
            var button = document.querySelector('.ml-clear-btn.mlc-seller-details-contact__wrapper');
            button.click();
            """
            r.html.render(script=script)

            # Copy and show the phone number
            phone_number = r.html.find('.mlc-seller-details-contact__text', first=True).text
            print(f"{link}       {phone_number}")
            phone_numbers.append(f"{link}; {phone_number}")
        else:
            print("Отсоси")


    time.sleep(5)

# display the list of phone numbers
print("Номера телефонов: ")
for phone_number in phone_numbers:
    print(phone_number)
