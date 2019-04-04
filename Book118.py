import re
import io
import sys
import threadpool
import requests
from requests.packages import urllib3
from PIL import Image


class Book118:
    def __init__(self, pool_size=64):
        urllib3.disable_warnings()
        self.pdf_info = {}
        self.domain = ''
        self.total = 0
        self.img_list = []
        self.pool = threadpool.ThreadPool(pool_size)
        self.s = requests.Session()

    def __get_pdf_info(self, pid):
        view_page = self.s.get('https://max.book118.com/index.php', params={
            'g': 'Home',
            'm': 'View',
            'a': 'viewUrl',
            'cid': pid,
            'flag': 1,
            'mark': 0
        }, verify=False)
        self.domain = re.findall(r'//(.*?)\..*', view_page.text)[0]
        raw_html = self.s.get('https:' + view_page.text, verify=False)
        res = re.findall(r'<input type="hidden" id="(.*?)" value="(.*?)".*?/>', raw_html.text)
        for lst in res:
            self.pdf_info[lst[0]] = lst[1]

    def __get_page(self, index=0):
        res = self.s.get('https://' + self.domain + '.book118.com/PW/GetPage/', params={
            'f': self.pdf_info['Url'],
            'isMobile': False,
            'sn': index,
            'readLimit': self.pdf_info['ReadLimit'],
            'furl': self.pdf_info['Furl']
        }, verify=False).json()
        if self.total == 0:
            self.total = res['PageCount']
            self.img_list = [None for _ in range(self.total)]
            if self.total > 1:
                for req in threadpool.makeRequests(self.__get_page, range(1, self.total)):
                    self.pool.putRequest(req)

        res = self.s.get('http://' + self.domain + '.book118.com/img/', params={'img': res['NextPage']}, verify=False)
        self.img_list[index] = Image.open(io.BytesIO(res.content))
        print(index + 1, '/', self.total, 'download finish')

    def get_pdf(self, pid, pdf_name="book.pdf"):
        print("getting pdf info...")
        self.__get_pdf_info(pid)
        self.__get_page()
        self.pool.wait()
        print("making pdf...")
        if self.img_list:
            self.img_list[0].save(pdf_name, "PDF", resolution=100.0, save_all=True, append_images=self.img_list[1:])
        self.total = 0
        self.img_list = []


if __name__ == "__main__":
    Book118().get_pdf(sys.argv[1], "book.pdf" if len(sys.argv) == 2 else sys.argv[2])
