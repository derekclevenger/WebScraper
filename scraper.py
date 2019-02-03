import requests
import re
import atexit
url = "https://google.com"
URL = [url]
urls = {URL[0]: 1}
regex = r"^(?:http(s)?:\/\/)?[\w.-]+(?:\.[\w\.-]+)+[\w\-\._~:/?#[\]@!\$&'\(\)\*\+,;=.]+$"


def findUrls(html, list):
    for word in html.split():
        if "href" in word and "https" in word:
            p = re.compile(regex)
            url = getUrl(word)
            try:
                w = p.match(url)
            except:
                print(w)
            if w:
                if url not in list:
                    urls[url] = 1
                    list.append(url)
                else:
                    urls[url] += 1
    return list


def getUrl(word):
    x = word.replace("href=\"", "")
    try:
        end = x.index("\"")
        y = x[:end]
        return y
    except:
        print(x)


def scrape(list):
        for x in list:
            response = requests.get(x)
            if response.status_code == 200:
                findUrls(response.text, list)


@atexit.register
def exit_handler():
    f = open("url_count.txt", "w+")
    for k, v in urls.items():
        f.write(k + ': ' + str(v) + '\n')
    f.close()


if __name__ == '__main__':
        scrape(URL)
        atexit.register(exit_handler())


