#!/usr/bin/python
# -*- coding:utf-8 -*-
import httplib2
import re
from lxml import etree


class DataGain:
    comments = ''
    main = 'http://www.thepaper.cn/'

    def get_content(self, url):
        http = httplib2.Http()
        response, content = http.request(url, 'GET')
        return content
        # return content.decode('unicode-escape').encode('utf-8')

    def get_categorys(self, url):
        content = self.get_content(url)
        list = re.findall(r'<a href="(.*?)" class="bn_a(?: on)?"(?: id="select")?>(.*?)</a>',
                          content)
        lis = []
        for l in list:
            dict = {}
            dict['names'] = l[1]
            dict['links'] = l[0]
            lis.append(dict)
        return lis

    def get_ccategorys(self, url='http://www.thepaper.cn/ask_index.jsp',
                       index=0):
        names = []
        links = []
        content = self.get_content(url)
        tree = etree.HTML(content)
        if(index < 4):
            xpath = "//ul[@class='clearfix']"
            a = tree.xpath(xpath)
            names = a[index].xpath("li/a/text()")
            links = a[index].xpath("li/a/@href")
        else:
            xpath = "id('ask_banner')/div/a"
            names = tree.xpath(xpath + "/text()")
            links = tree.xpath(xpath + "/@href")
        return self.__transform(names, links)

    def __transform(self, names, links):
        list = []
        if len(names) == len(links):
            for i in range(len(names)):
                dict = {}
                dict['name'] = names[i]
                dict['link'] = links[i]
                list.append(dict)
        return list

    def get_datas(self, link, index):
        content = self.__get_datacontent(link, index)
        tree = etree.HTML(content)
        list = []
        elemments = tree.xpath("//div[@class='news_li']")
        for i in range(len(elemments)):
            dict = {}
            dict['img'] = elemments[i].xpath("descendant::img/@src")
            dict['title'] = elemments[i].xpath("h2/a/text()")
            dict['link'] = elemments[i].xpath("h2/a/@href")
            dict['category'] = elemments[i].xpath("div[2]/a/text()")
            dict['category_link'] = elemments[i].xpath("div[2]/a/@href")
            dict['isCategory'] = elemments.xpath("div[2]/a/@href") == link
            dict['time'] = elemments[i].xpath("descendant::span/text()")
            list.append(dict)
        return list

    def get_allcategory(self, url=main):
        list = self.get_categorys(url)
        for i in range(len(list)):
            #0 是精选，５是订阅
            if i == 0 | i == 5:
                list[i]['child'] = []
            else:
                list[i]['child'] = self.get_ccategorys(index=i-1)
        return list

    def __get_datacontent(self, link, index):
        ids = 0
        suffix = ""
        a = re.match(r"(\w+)_(\d+)", link)
        if a is not None:
            ids = a.group(2)
            kind = a.group(1)
            if kind == "list":
                suffix = "load_index.jsp?nodeids=" + ids + "&pageidx=" + index
            else:
                suffix = "load_index.jsp?nodeid=" + ids + "&pageidx=" + index
        return self.get_content(main+suffix)


def main():
        data = DataGain()
        # data.get_categorys('http://www.thepaper.cn/')
        f = file('data.txt', "w+")
        list = data.get_allcategory()
        for l in list:
            f.write(repr(l))
            f.write("\n")
        f.close()
        print data.comments


if __name__ == "__main__":
    main()
