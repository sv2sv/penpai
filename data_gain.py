#!/usr/bin/python
# -*- coding:utf-8 -*-
import httplib2
import re
from lxml import etree
import ujson


class DataGain:
    main = 'http://www.thepaper.cn/'

    def get_content(self, url):
        http = httplib2.Http('.cache')
        response, content = http.request(url, 'GET')
        return content

    def get_categorys(self, url=main):
        content = self.get_content(url)
        list = re.findall(r'<a href="(.*?)" class="bn_a(?: on)?' +
                          '"(?: id="select")?>(.*?)</a>', content)
        lis = []
        for l in list:
            dict = {}
            dict['name'] = l[1]
            dict['link'] = l[0]
            lis.append(dict)
        return lis

    def get_ccategorys(self, url='http://www.thepaper.cn/ask_index.jsp',
                       index=0):
        names = []
        links = []
        content = self.get_content(url)
        tree = etree.HTML(content)
        # 问吧是最后一个，订阅没有子节点，分开解析
        if(index < 5):
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
        size = len(list)
        count = 0
        for i in range(len(list)):
            # 0 是精选，6是订阅
            if i == 0 or i == size-2:
                print list[i]['name']
                list[i]['child'] = []
            else:
                list[i]['child'] = self.get_ccategorys(index=count)
                count += 1
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

    def get_dict(self, url=main):
        dict = {}
        for l in self.get_categorys():
            dict[l['name']] = l['link']
        for i in range(8):
            for l in self.get_ccategorys(index=i):
                dict[l['name']] = l['link']
        print dict
        return dict


def main():
        data = DataGain()
        data.get_dict()
        js = ujson.dumps(data.get_allcategory(), ensure_ascii=False)
        with open('data.json', 'w') as file:
            file.write(js)


if __name__ == "__main__":
    main()
