import urllib2
import httplib2
import re
from lxml import etree
import uniout


class DataGain:
    comments = ''

    def get_content(self, url):
        http = httplib2.Http()
        response, content = http.request(url, 'GET')
        return content
        # return content.decode('unicode-escape').encode('utf-8')

    def get_categorys(self, url):
        content = self.get_content(url)
        print type(content)
        match = re.compile(r'<a href="(.*?)" class="bn_a">(.*?)</a>',
                           re.I | re.M)

        print match.findall(content)

    def get_ccategorys(self, url, index):
        names = []
        links = []
        content = self.get_content(url)
        tree = etree.HTML(content)
        if(index != 5):
            xpath = "//ul[@class='clearfix']"
            a = tree.xpath(xpath)
            names = a[index-1].xpath("li/a/text()")
            links = a[index-1].xpath("li/a/@href")
        else:
            xpath = "id('ask_banner')/div/a"
            a = tree.xpath(xpath)
            names = a.xpath("text()")
            links = a.xpath("@href")
        return self.__transform(names, links)

    def __transform(self, names, links):
        lists = []
        if len(names) == len(links):
            for i in range(len(names)):
                dict = {}
                dict['name'] = names[i]
                dict['link'] = links[i]
                lists.append(dict)
        return lists

    def get_items(slef, url, size):
        content = slef.get_content(url)
        :

def main():
        data = DataGain()
        # data.get_categorys('http://www.thepaper.cn/')
        print data.get_ccategorys("http://www.thepaper.cn/ask_index.jsp", 1)


if __name__ == "__main__":
    main()
