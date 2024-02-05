from urllib.request import urlopen
from bs4 import BeautifulSoup

def extractHTML(url):
    if not url.startswith("./"):
        html = urlopen(url).read()
    else:
        with open(url, "r", encoding="utf-8") as file:
            html = file.read()

    soup = BeautifulSoup(html, features="html.parser")

    for script in soup(["script", "style"]):
        script.extract()

    text = soup.get_text()

    lines = (line.strip() for line in text.splitlines())

    alltext = ""
    for line in lines:
        alltext = alltext + line + "\n"
    print(alltext)
    return alltext

# Example usage:
# extractHTML("https://example.com")
# or
# extractHTML("./local_file.html")
