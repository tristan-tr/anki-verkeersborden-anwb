import requests
from bs4 import BeautifulSoup

def extract_data_from_table(url, output_file):
    response = requests.get(url)
    if response.status_code != 200:
        print("Error: Unable to fetch the webpage.")
        return

    soup = BeautifulSoup(response.text, 'html.parser')
    tbody_elements = soup.find_all('tbody', class_ = tbody_class)
    
    if not tbody_elements: #tbody_elements is empty, tbody_class is likely wrong
        print("Error: No tbody elements found, please update the tbody class name")
        return

    with open(output_file, 'w', encoding='utf-8') as file:
        for tbody in tbody_elements:
            tr_elements = tbody.find_all('tr')
            for tr in tr_elements:
                td_elements = tr.find_all('td')
                if len(td_elements) >= 2:
                    img_link = td_elements[0].find('img').get('src')
                    table_data = ''.join(str(content) for content in td_elements[2].contents) # get html text
                    file.write(f'"<img src=""{img_link}"">";"{table_data}"\n')

if __name__ == "__main__":
    url = "https://www.anwb.nl/vakantie/nederland/reisvoorbereiding/verkeersborden"
    output_file = "verkeersborden_importable.txt"
    tbody_class = "sc-fxwrCY hwVzSn"
    extract_data_from_table(url, output_file)
    print(f"Data extracted and written to {output_file}.")