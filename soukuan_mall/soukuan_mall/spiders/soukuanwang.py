# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
import datetime
import json
import math
import pymysql
import re
import scrapy
import time
from scrapy import Selector,Request
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals
import smtplib
from email.mime.text import MIMEText
import sys
sys.path.append("../")
from soukuan_mall.items import SoukuanMallItem
from soukuan_mall.settings import mysql_host,mysql_port,mysql_db_user,mysql_db_pwd,mysql_db_name,mysql_db_charset


class SoukuanwangSpider(scrapy.Spider):
    name = 'soukuanwang'
    allowed_domains = ['www.vvic.com']
    start_urls = ['http://www.vvic.com/']

    def __init__(self):

        """ 监听信号量 """
        super(SoukuanwangSpider, self).__init__()
        dispatcher.connect(self.send_email, signals.spider_closed)


        self.info = {
            "20000035": ["女装", "上装/外套", "T恤", "1", "", "", ""],
            "20000018": ["女装", "上装/外套", "衬衫", "1", "", "", ""],
            "20000019": ["女装", "上装/外套", "蕾丝衫/雪纺衫", "1", "", "", ""],
            "20000068": ["女装", "上装/外套", "卫衣/绒衫", "1", "", "", ""],
            "20000017": ["女装", "上装/外套", "毛衣", "1", "", "", ""],
            "20000038": ["女装", "上装/外套", "毛针织衫", "1", "", "", ""],
            "20000037": ["女装", "上装/外套", "毛针织套装", "1", "", "", ""],
            "20000389": ["女装", "上装/外套", "时尚套装", "1", "", "", ""],
            "20000025": ["女装", "上装/外套", "休闲运动套装", "1", "", "", ""],
            "20000024": ["女装", "上装/外套", "其它套装", "1", "", "", ""],
            "20000129": ["女装", "上装/外套", "短外套", "1", "", "", ""],
            "20000128": ["女装", "上装/外套", "牛仔短外套", "1", "", "", ""],
            "20000174": ["女装", "上装/外套", "毛呢外套", "1", "", "", ""],
            "20000070": ["女装", "上装/外套", "棉衣/棉服", "1", "", "", ""],
            "20000069": ["女装", "上装/外套", "羽绒服", "1", "", "", ""],
            "20000175": ["女装", "上装/外套", "羽绒马夹", "1", "", "", ""],
            "20000071": ["女装", "上装/外套", "风衣", "1", "", "", ""],
            "20000176": ["女装", "上装/外套", "马夹", "1", "", "", ""],
            "20000067": ["女装", "上装/外套", "西装", "1", "", "", ""],
            "20000073": ["女装", "上装/外套", "皮衣", "1", "", "", ""],
            "20000074": ["女装", "上装/外套", "皮草", "1", "", "", ""],
            "20000364": ["女装", "上装/外套", "背心吊带", "1", "", "", ""],
            "20000370": ["女装", "上装/外套", "抹胸", "1", "", "", ""],
            "20000055": ["女装", "上装/外套", "旗袍", "1", "", "", ""],
            "20000028": ["女装", "上装/外套", "民族服装/舞台装", "1", "", "", ""],
            "20000052": ["女装", "上装/外套", "唐装/中式服饰上衣", "1", "", "", ""],
            "20000072": ["女装", "上装/外套", "学生校服", "1", "", "", ""],
            "20000027": ["女装", "上装/外套", "礼服/晚装", "1", "", "", ""],
            "20000131": ["女装", "上装/外套", "酒店工作制服", "1", "", "", ""],
            "20000005": ["女装", "上装/外套", "大码外套/马甲", "1", "", "", ""],
            "20000012": ["女装", "上装/外套", "大码毛针织衫", "1", "", "", ""],
            "20000007": ["女装", "上装/外套", "大码T恤", "1", "", "", ""],
            "20000013": ["女装", "上装/外套", "大码套装", "1", "", "", ""],
            "20000008": ["女装", "上装/外套", "大码衬衫", "1", "", "", ""],
            "20000011": ["女装", "上装/外套", "大码卫衣/绒衫", "1", "", "", ""],
            "20000002": ["女装", "上装/外套", "大码雪纺衫/雪纺衫", "1", "", "", ""],
            "20000014": ["女装", "上装/外套", "其他大码女装", "1", "", "", ""],
            "20000039": ["女装", "上装/外套", "中老年蕾丝衫/雪纺衫", "1", "", "", ""],
            "20000042": ["女装", "上装/外套", "中老年T恤", "1", "", "", ""],
            "20000046": ["女装", "上装/外套", "中老年外套/马甲", "1", "", "", ""],
            "20000048": ["女装", "上装/外套", "中老年套装", "1", "", "", ""],
            "20000106": ["女装", "裙装", "连衣裙", "1", "", "", ""],
            "20000006": ["女装", "裙装", "大码连衣裙", "1", "", "", ""],
            "20000041": ["女装", "裙装", "中老年连衣裙", "1", "", "", ""],
            "20000001": ["女装", "裙装", "半身裙", "1", "", "", ""],
            "20000000": ["女装", "裙装", "牛仔半身裙", "1", "", "", ""],
            "20000010": ["女装", "裙装", "大码半身裙", "1", "", "", ""],
            "20000044": ["女装", "裙装", "中老年半身裙", "1", "", "", ""],
            "20000036": ["女装", "裙装", "毛针织裙", "1", "", "", ""],
            "20000022": ["女装", "裙装", "职业女裙套装", "1", "", "", ""],
            "20000054": ["女装", "裙装", "唐装/中式服饰裙子", "1", "", "", ""],
            "20000026": ["女装", "裙装", "婚纱", "1", "", "", ""],
            "20000021": ["女装", "裤装", "牛仔裤", "1", "", "", ""],
            "20000020": ["女装", "裤装", "休闲裤", "1", "", "", ""],
            "20000057": ["女装", "裤装", "打底裤", "1", "", "", ""],
            "20000009": ["女装", "裤装", "大码裤子", "1", "", "", ""],
            "20000291": ["女装", "裤装", "西装裤/正装裤", "1", "", "", ""],
            "20000053": ["女装", "裤装", "唐装/中式服饰裤子", "1", "", "", ""],
            "20000023": ["女装", "裤装", "职业女裤套装", "1", "", "", ""],
            "20000040": ["女装", "裤装", "中老年裤子", "1", "", "", ""],
            "20000340": ["女装", "裤装", "羽绒裤", "1", "", "", ""],
            "20000341": ["女装", "裤装", "棉裤", "1", "", "", ""],
            "20000078": ["男装", "上装/外套", "卫衣", "2", "", "", ""],
            "20000076": ["男装", "上装/外套", "夹克", "2", "", "", ""],
            "20000034": ["男装", "上装/外套", "针织衫/毛衣", "2", "", "", ""],
            "20000424": ["男装", "上装/外套", "休闲运动套装", "2", "", "", ""],
            "20000421": ["男装", "上装/外套", "其他套装", "2", "", "", ""],
            "20000117": ["男装", "上装/外套", "背心", "2", "", "", ""],
            "20000116": ["男装", "上装/外套", "马甲", "2", "", "", ""],
            "20000120": ["男装", "上装/外套", "风衣", "2", "", "", ""],
            "20000123": ["男装", "上装/外套", "皮衣", "2", "", "", ""],
            "20000125": ["男装", "上装/外套", "棉衣", "2", "", "", ""],
            "20000335": ["男装", "上装/外套", "毛呢大衣", "2", "", "", ""],
            "20000079": ["男装", "上装/外套", "西服", "2", "", "", ""],
            "20000113": ["男装", "上装/外套", "西服套装", "2", "", "", ""],
            "20000115": ["男装", "上装/外套", "西装马甲", "2", "", "", ""],
            "20000127": ["男装", "上装/外套", "羽绒服", "2", "", "", ""],
            "20000056": ["男装", "上装/外套", "工装制服", "2", "", "", ""],
            "20000077": ["男装", "上装/外套", "大码卫衣", "2", "", "", ""],
            "20000033": ["男装", "上装/外套", "大码针织衫/毛衣", "2", "", "", ""],
            "20000423": ["男装", "上装/外套", "大码休闲运动套装", "2", "", "", ""],
            "20000420": ["男装", "上装/外套", "大码其他套装", "2", "", "", ""],
            "20000124": ["男装", "上装/外套", "大码棉衣", "2", "", "", ""],
            "20000126": ["男装", "上装/外套", "大码羽绒服", "2", "", "", ""],
            "20000119": ["男装", "上装/外套", "大码风衣", "2", "", "", ""],
            "20000122": ["男装", "上装/外套", "大码皮衣", "2", "", "", ""],
            "20000334": ["男装", "上装/外套", "大码毛呢大衣", "2", "", "", ""],
            "20000075": ["男装", "上装/外套", "中老年夹克", "2", "", "", ""],
            "20000032": ["男装", "上装/外套", "中老年针织衫/毛衣", "2", "", "", ""],
            "20000422": ["男装", "上装/外套", "中老年休闲运动套装", "2", "", "", ""],
            "20000118": ["男装", "上装/外套", "中老年风衣", "2", "", "", ""],
            "20000031": ["男装", "衬衫/T恤", "T恤", "2", "", "", ""],
            "20000030": ["男装", "衬衫/T恤", "大码T恤", "2", "", "", ""],
            "20000029": ["男装", "衬衫/T恤", "中老年T恤", "2", "", "", ""],
            "20000109": ["男装", "衬衫/T恤", "衬衫", "2", "", "", ""],
            "20000108": ["男装", "衬衫/T恤", "大码衬衫", "2", "", "", ""],
            "20000107": ["男装", "衬衫/T恤", "中老年衬衫", "2", "", "", ""],
            "20000090": ["男装", "衬衫/T恤", "Polo衫", "2", "", "", ""],
            "20000089": ["男装", "衬衫/T恤", "大码Polo衫", "2", "", "", ""],
            "20000088": ["男装", "衬衫/T恤", "中老年Polo衫", "2", "", "", ""],
            "20000016": ["男装", "裤装", "休闲裤", "2", "", "", ""],
            "20000015": ["男装", "裤装", "大码休闲裤", "2", "", "", ""],
            "20000081": ["男装", "裤装", "牛仔裤", "2", "", "", ""],
            "20000080": ["男装", "裤装", "大码牛仔裤", "2", "", "", ""],
            "20000112": ["男装", "裤装", "西裤", "2", "", "", ""],
            "20000111": ["男装", "裤装", "皮裤", "2", "", "", ""],
            "20000339": ["男装", "裤装", "棉裤", "2", "", "", ""],
            # "10000137": ["鞋", "女鞋", "低帮鞋", "3", "", "", ""],
            # "10000135": ["鞋", "女鞋", "靴子", "3", "", "", ""],
            # "10000136": ["鞋", "女鞋", "高帮鞋", "3", "", "", ""],
            # "10000141": ["鞋", "女鞋", "低帮帆布鞋", "3", "", "", ""],
            # "10000140": ["鞋", "女鞋", "高帮帆布鞋", "3", "", "", ""],
            # "10000138": ["鞋", "女鞋", "拖鞋", "3", "", "", ""],
            # "10000139": ["鞋", "女鞋", "凉鞋", "3", "", "", ""],
            # "10000133": ["鞋", "女鞋", "雨鞋", "3", "", "", ""],
            # "10000128": ["鞋", "男鞋", "低帮鞋", "3", "", "", ""],
            # "10000126": ["鞋", "男鞋", "靴子", "3", "", "", ""],
            # "10000127": ["鞋", "男鞋", "高帮鞋", "3", "", "", ""],
            # "10000132": ["鞋", "男鞋", "低帮帆布鞋", "3", "", "", ""],
            # "10000131": ["鞋", "男鞋", "高帮帆布鞋", "3", "", "", ""],
            # "10000129": ["鞋", "男鞋", "拖鞋", "3", "", "", ""],
            # "10000130": ["鞋", "男鞋", "凉鞋", "3", "", "", ""],
            "20000058": ["内衣/家居", "内衣", "文胸", "4", "", "", ""],
            "20000059": ["内衣/家居", "内衣", "内裤", "4", "", "", ""],
            "20000060": ["内衣/家居", "内衣", "文胸套装", "4", "", "", ""],
            "20000065": ["内衣/家居", "内衣", "抹胸", "4", "", "", ""],
            "40000154": ["内衣/家居", "内衣", "短袜/打底袜/丝袜/美腿袜", "4", "", "", ""],
            "20000083": ["内衣/家居", "内衣", "吊带", "4", "", "", ""],
            "20000085": ["内衣/家居", "内衣", "背心", "4", "", "", ""],
            "20000082": ["内衣/家居", "内衣", "T恤", "4", "", "", ""],
            "20000165": ["内衣/家居", "内衣", "睡衣/家居服套装", "4", "", "", ""],
            "20000064": ["内衣/家居", "内衣", "睡衣上装", "4", "", "", ""],
            "20000161": ["内衣/家居", "内衣", "睡裤/家居裤", "4", "", "", ""],
            "20000163": ["内衣/家居", "内衣", "睡裙", "4", "", "", ""],
            "20000166": ["内衣/家居", "内衣", "睡袍/浴袍", "4", "", "", ""],
            "20000164": ["内衣/家居", "内衣", "中老年睡衣/家居服套装", "4", "", "", ""],
            "20000063": ["内衣/家居", "内衣", "中老年睡衣上装", "4", "", "", ""],
            "20000160": ["内衣/家居", "内衣", "中老年睡裤/家居裤", "4", "", "", ""],
            "20000162": ["内衣/家居", "内衣", "中老年睡裙", "4", "", "", ""],
            "20000170": ["内衣/家居", "内衣", "保暖套装", "4", "", "", ""],
            "20000062": ["内衣/家居", "内衣", "保暖上装", "4", "", "", ""],
            "20000169": ["内衣/家居", "内衣", "保暖裤", "4", "", "", ""],
            "20000171": ["内衣/家居", "内衣", "塑身连体衣", "4", "", "", ""],
            "20000168": ["内衣/家居", "内衣", "塑身分体套装", "4", "", "", ""],
            "20000061": ["内衣/家居", "内衣", "塑身上衣", "4", "", "", ""],
            "20000167": ["内衣/家居", "内衣", "塑身美体裤", "4", "", "", ""],
            "40000015": ["内衣/家居", "内衣", "塑身腰封/腰夹", "4", "", "", ""],
            "40000169": ["内衣/家居", "内衣", "乳贴", "4", "", "", ""],
            "40000170": ["内衣/家居", "内衣", "肩带", "4", "", "", ""],
            "40000171": ["内衣/家居", "内衣", "插片/胸垫", "4", "", "", ""],
            "20000103": ["儿童用品", "童装", "套装", "5", "", "", ""],
            "20000158": ["儿童用品", "童装", "亲子装/亲子时装", "5", "", "", ""],
            "20000374": ["儿童用品", "童装", "连衣裙", "5", "", "", ""],
            "20000387": ["儿童用品", "童装", "半身裙", "5", "", "", ""],
            "20000173": ["儿童用品", "童装", "T恤", "5", "", "", ""],
            "20000096": ["儿童用品", "童装", "衬衫", "5", "", "", ""],
            "20000102": ["儿童用品", "童装", "毛针织衫", "5", "", "", ""],
            "20000091": ["儿童用品", "童装", "卫衣/绒衫", "5", "", "", ""],
            "20000104": ["儿童用品", "童装", "牛仔外套", "5", "", "", ""],
            "20000105": ["儿童用品", "童装", "普通外套", "5", "", "", ""],
            "20000141": ["儿童用品", "童装", "风衣", "5", "", "", ""],
            "20000095": ["儿童用品", "童装", "马甲", "5", "", "", ""],
            "20000093": ["儿童用品", "童装", "夹克", "5", "", "", ""],
            "20000092": ["儿童用品", "童装", "皮衣", "5", "", "", ""],
            "20000094": ["儿童用品", "童装", "呢大衣", "5", "", "", ""],
            "20000402": ["儿童用品", "童装", "羽绒服", "5", "", "", ""],
            "20000398": ["儿童用品", "童装", "羽绒马甲", "5", "", "", ""],
            "20000331": ["儿童用品", "童装", "西服/小西装", "5", "", "", ""],
            "20000098": ["儿童用品", "童装", "棉袄/棉服", "5", "", "", ""],
            "20000180": ["儿童用品", "童装", "牛仔裤", "5", "", "", ""],
            "20000181": ["儿童用品", "童装", "棉裤", "5", "", "", ""],
            "20000182": ["儿童用品", "童装", "裤子", "5", "", "", ""],
            "20000345": ["儿童用品", "童装", "背心吊带", "5", "", "", ""],
            "20000097": ["儿童用品", "童装", "披风/斗篷", "5", "", "", ""],
            "40000004": ["儿童用品", "童装", "帽子", "5", "", "", ""],
            "20000369": ["儿童用品", "童装", "家居服套装", "5", "", "", ""],
            "20000375": ["儿童用品", "童装", "家居裙/睡裙", "5", "", "", ""],
            "20000352": ["儿童用品", "童装", "内衣套装", "5", "", "", ""],
            "20000361": ["儿童用品", "童装", "内裤", "5", "", "", ""],
            "40000141": ["儿童用品", "童装", "儿童袜子(0-16岁)", "5", "", "", ""],
            "20000099": ["儿童用品", "童装", "连身衣/爬服/哈衣", "5", "", "", ""],
            "20000190": ["儿童用品", "童装", "婴儿礼盒", "5", "", "", ""],
            "10000144": ["儿童用品", "童鞋", "皮鞋", "5", "", "", ""],
            "10000064": ["儿童用品", "童鞋", "跑步鞋", "5", "", "", ""],
            "10000088": ["儿童用品", "童鞋", "休闲鞋", "5", "", "", ""],
            "10000143": ["儿童用品", "童鞋", "帆布鞋", "5", "", "", ""],
            "10000148": ["儿童用品", "童鞋", "靴子", "5", "", "", ""],
            "10000146": ["儿童用品", "童鞋", "凉鞋", "5", "", "", ""],
            "10000145": ["儿童用品", "童鞋", "拖鞋", "5", "", "", ""],
            "10000149": ["儿童用品", "童鞋", "亲子鞋", "5", "", "", ""],
            "10000150": ["儿童用品", "童鞋", "学步鞋", "5", "", "", ""],
            "10000065": ["儿童用品", "童鞋", "运动板鞋", "5", "", "", ""],
            "10000066": ["儿童用品", "童鞋", "运动帆布鞋", "5", "", "", ""],
            "10000068": ["儿童用品", "童鞋", "运动沙滩鞋/凉鞋", "5", "", "", ""],
            "10000089": ["儿童用品", "童鞋", "其它运动鞋", "5", "", "", ""],
            "40000011": ["配件箱包", "服装配饰", "围巾/丝巾/披肩", "6", "", "", ""],
            "40000016": ["配件箱包", "服装配饰", "帽子", "6", "", "", ""],
            "40000012": ["配件箱包", "服装配饰", "手套", "6", "", "", ""],
            "40000017": ["配件箱包", "服装配饰", "耳套", "6", "", "", ""],
            "40000029": ["配件箱包", "服装配饰", "二件套", "6", "", "", ""],
            "40000030": ["配件箱包", "服装配饰", "三件套", "6", "", "", ""],
            "40000014": ["配件箱包", "服装配饰", "腰带/皮带/腰链", "6", "", "", ""],
            "40000020": ["配件箱包", "服装配饰", "假领", "6", "", "", ""],
            "30000096": ["配件箱包", "服装配饰", "包挂件", "6", "", "", ""],
            "40000033": ["配件箱包", "服装配饰", "其他配件", "6", "", "", ""],
            # "20000246": ["运动户外", "运动", "比基尼", "7", "", "", ""],
            # "20000250": ["运动户外", "运动", "连体泳衣", "7", "", "", ""],
            # "20000248": ["运动户外", "运动", "分体泳衣", "7", "", "", ""],
            # "20000251": ["运动户外", "运动", "男士泳衣", "7", "", "", ""],
            # "20000252": ["运动户外", "运动", "儿童泳衣/裤", "7", "", "", ""],
            # "20000249": ["运动户外", "运动", "中老年连体泳衣", "7", "", "", ""],
            # "20000382": ["运动户外", "运动", "沙滩外套", "7", "", "", ""],
            # "20000320": ["运动户外", "运动", "沙滩裤", "7", "", "", ""],
            # "40000102": ["运动户外", "运动", "泳帽", "7", "", "", ""],
            # "40000101": ["运动户外", "运动", "泳镜", "7", "", "", ""],
            # "20000255": ["运动户外", "运动", "裹裙/披纱", "7", "", "", ""],
            # "20000240": ["运动户外", "运动", "瑜伽服", "7", "", "", ""],
            # "20000225": ["运动户外", "运动", "钢管舞服", "7", "", "", ""],
            # "20000292": ["运动户外", "运动服", "运动套装", "7", "", "", ""],
            # "20000139": ["运动户外", "运动服", "运动茄克", "7", "", "", ""],
            # "20000178": ["运动户外", "运动服", "运动T恤", "7", "", "", ""],
            # "20000134": ["运动户外", "运动服", "运动卫衣/套头衫", "7", "", "", ""],
            # "20000293": ["运动户外", "运动服", "运动POLO衫", "7", "", "", ""],
            # "20000179": ["运动户外", "运动服", "运动连衣裙", "7", "", "", ""],
            # "20000140": ["运动户外", "运动服", "运动外套", "7", "", "", ""],
            # "20000135": ["运动户外", "运动服", "运动风衣", "7", "", "", ""],
            # "20000136": ["运动户外", "运动服", "运动棉衣", "7", "", "", ""],
            # "20000302": ["运动户外", "运动服", "运动长裤", "7", "", "", ""],
            # "20000303": ["运动户外", "运动服", "运动中长裤／短裤", "7", "", "", ""],
            # "20000296": ["运动户外", "运动服", "健身套装", "7", "", "", ""],
            # "20000294": ["运动户外", "运动服", "健身衣", "7", "", "", ""],
            # "20000295": ["运动户外", "运动服", "健身裤", "7", "", "", ""],
            # "20000310": ["运动户外", "运动服", "棒球服", "7", "", "", ""],
            # "40000142": ["运动户外", "运动服", "运动袜", "7", "", "", ""],
            # "40000042": ["运动户外", "运动服", "其他服饰配件", "7", "", "", ""],
            # "10000004": ["运动户外", "运动鞋", "跑步鞋", "7", "", "", ""],
            # "10000032": ["运动户外", "运动鞋", "休闲鞋", "7", "", "", ""],
            # "10000031": ["运动户外", "运动鞋", "板鞋", "7", "", "", ""],
            # "10000007": ["运动户外", "运动鞋", "其它运动鞋", "7", "", "", ""],
            # "30000050": ["运动户外", "运动包", "单肩背包", "7", "", "", ""],
            # "30000049": ["运动户外", "运动包", "双肩背包", "7", "", "", ""],
            # "30000052": ["运动户外", "运动包", "挎包/拎包/休闲包", "7", "", "", ""],
            # "30000051": ["运动户外", "运动包", "手包", "7", "", "", ""],
            # "40000126": ["美妆饰品", "美妆", "项链", "8", "", "", ""],
            # "40000127": ["美妆饰品", "美妆", "项坠/吊坠", "8", "", "", ""],
            # "40000128": ["美妆饰品", "美妆", "手链", "8", "", "", ""],
            # "40000129": ["美妆饰品", "美妆", "手镯", "8", "", "", ""],
            # "40000136": ["美妆饰品", "美妆", "脚链", "8", "", "", ""],
            # "40000130": ["美妆饰品", "美妆", "戒指/指环", "8", "", "", ""],
            # "40000132": ["美妆饰品", "美妆", "耳环", "8", "", "", ""],
            # "40000133": ["美妆饰品", "美妆", "耳钉", "8", "", "", ""],
            # "40000131": ["美妆饰品", "美妆", "发饰", "8", "", "", ""],
            # "40000137": ["美妆饰品", "美妆", "胸针", "8", "", "", ""],
            # "40000139": ["美妆饰品", "美妆", "其它首饰", "8", "", "", ""],
            # "40000140": ["美妆饰品", "美妆", "其他DIY饰品配件", "8", "", "", ""],
            "20000144": ["孕妇装", "孕妇装", "连衣裙", "9", "", "", ""],
            "20000321": ["孕妇装", "孕妇装", "孕妇裤/托腹裤", "9", "", "", ""],
            "20000148": ["孕妇装", "孕妇装", "套装", "9", "", "", ""],
            "20000147": ["孕妇装", "孕妇装", "T恤", "9", "", "", ""],
            "20000145": ["孕妇装", "孕妇装", "毛衣", "9", "", "", ""],
            "20000146": ["孕妇装", "孕妇装", "针织衫", "9", "", "", ""],
            "20000151": ["孕妇装", "孕妇装", "卫衣/绒衫", "9", "", "", ""],
            "20000143": ["孕妇装", "孕妇装", "外套/风衣", "9", "", "", ""],
            "20000152": ["孕妇装", "孕妇装", "马甲", "9", "", "", ""],
            "20000325": ["孕妇装", "孕妇装", "棉衣", "9", "", "", ""],
            "20000324": ["孕妇装", "孕妇装", "羽绒服", "9", "", "", ""],
            "20000326": ["孕妇装", "孕妇装", "大衣", "9", "", "", ""],
            "20000323": ["孕妇装", "孕妇装", "半身裙", "9", "", "", ""],
            "20000150": ["孕妇装", "孕妇装", "衬衫", "9", "", "", ""],
            "20000153": ["孕妇装", "孕妇装", "吊带/背心", "9", "", "", ""],
            "20000149": ["孕妇装", "孕妇装", "雪纺衫", "9", "", "", ""],
            "20000360": ["孕妇装", "孕妇装", "家居服套装", "9", "", "", ""],
            "20000350": ["孕妇装", "孕妇装", "家居裙", "9", "", "", ""],
            "20000365": ["孕妇装", "孕妇装", "家居服上装", "9", "", "", ""],
            "20000383": ["孕妇装", "孕妇装", "家居裤", "9", "", "", ""],
            "20000380": ["孕妇装", "孕妇装", "家居袍", "9", "", "", ""],
            "20000328": ["孕妇装", "孕妇装", "其它", "9", "", "", ""],
            "20000412": ["孕妇装", "孕妇装", "哺乳衣", "9", "", "", ""],
            "20000243": ["孕妇装", "孕妇装", "哺乳文胸", "9", "", "", ""],
            "20000348": ["孕妇装", "孕妇装", "哺乳吊带", "9", "", "", ""],
            "20000157": ["孕妇装", "孕妇装", "防辐射围裙", "9", "", "", ""],
            "20000156": ["孕妇装", "孕妇装", "防辐射肚兜/护胎宝", "9", "", "", ""],
            "20000244": ["孕妇装", "孕妇装", "内裤", "9", "", "", ""],
            "40000155": ["孕妇装", "孕妇装", "孕妇袜/连裤袜/打底袜", "9", "", "", ""],
            "20000087": ["孕妇装", "孕妇装", "(文胸-内裤)套装", "9", "", "", ""],
            "20000354": ["孕妇装", "孕妇装", "秋衣裤套装", "9", "", "", ""],
            "20000384": ["孕妇装", "孕妇装", "秋衣", "9", "", "", ""],
            "40000163": ["孕妇装", "孕妇装", "束腹带", "9", "", "", ""],
            "20000385": ["孕妇装", "孕妇装", "塑身裤", "9", "", "", ""],
            "40000115": ["孕妇装", "孕妇装", "产妇帽", "9", "", "", ""],
            "20000051": ["孕妇装", "孕妇装", "其它孕妇装", "9", "", "", ""],
            "30000001": ["配件箱包", "箱包", "女士包袋", "6", "", "", ""],
            "30000000": ["配件箱包", "箱包", "男士包袋", "6", "", "", ""],
            "30000009": ["配件箱包", "箱包", "双肩背包", "6", "", "", ""],
            "30000004": ["配件箱包", "箱包", "钱包", "6", "", "", ""],
            "30000003": ["配件箱包", "箱包", "旅行袋", "6", "", "", ""],
            "30000002": ["配件箱包", "箱包", "旅行箱", "6", "", "", ""],
            "30000006": ["配件箱包", "箱包", "手机包", "6", "", "", ""],
            "30000005": ["配件箱包", "箱包", "卡包", "6", "", "", ""],
            "30000007": ["配件箱包", "箱包", "钥匙包", "6", "", "", ""],
            "30000008": ["配件箱包", "箱包", "证件包", "6", "", "", ""],
            "30000100": ["配件箱包", "箱包", "箱包相关配件", "6", "", "", ""],
        }

        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'accept-encoding': 'gzip, deflate, br',
        }

        self.attr = dict()

        self.client = pymysql.connect(
            host=mysql_host,
            port=mysql_port,
            user=mysql_db_user,  # 使用自己的用户名
            passwd=mysql_db_pwd,  # 使用自己的密码
            db=mysql_db_name,  # 数据库名
            charset=mysql_db_charset
        )

        self.cur = self.client.cursor()
        self.brand_info = {'广州女装批发': '6'}

        ppx_tables = [
            "mall_goods_common",
            "mall_goods",
            "mall_goods_images"
        ]
        self.start_ret = []
        for item in ppx_tables:
            sql = "SELECT count(1) FROM %s " % item
            self.cur.execute(sql)
            start_ret = self.cur.fetchone()
            self.start_ret.append(start_ret)

    def start_requests(self):
        market_list = ['19', '12', '49', '10', '13', '14', '15', '31', '11', '17', '52', '18', '34', '20', '16', '48','23', '25', '51', '47', '53', '50', '54', '36', '43', '39', '45', '28', '26', '35', '42', '38']
        for vcid in self.info:
            pid = self.info[vcid][3]
            for market in market_list:
                url = 'https://www.vvic.com/apic/search/asy?pid={}&vcid={}&bid={}&searchCity=gz&currentPage=1'.format(pid, vcid, market)
                print(url)

                headers = {
                    'user-agent': self.headers,
                    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                    'accept-encoding': 'gzip, deflate, br',
                }

                yield Request(url=url,
                              headers=headers,
                              callback=self.get_pages,
                              dont_filter=True,
                              meta={"vcid": vcid, "pid": pid, "market": market})

    def get_pages(self, response):
        pid = response.meta["pid"]
        vcid = response.meta["vcid"]
        market = response.meta["market"]

        json_data = json.loads(response.text)
        pagesize = json_data["data"]["search_page"]["pageSize"]
        recordcound = json_data["data"]["search_page"]["recordCount"]
        pages = math.ceil(int(recordcound) / int(pagesize))
        print(pages)

        for page in range(1, int(pages) + 1):
            url = 'https://www.vvic.com/apic/search/asy?merge=1&isTheft=0&pid={}&vcid={}&bid={}&searchCity=gz&currentPage={}'.format(pid, vcid, market, page)
            print(url)
            headers = {
                'user-agent': self.headers,
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'accept-encoding': 'gzip, deflate, br',
            }
            yield Request(url=url,
                          headers=headers,
                          callback=self.get_show_list,
                          meta={"vcid": vcid, "pid": pid, "market": market})

    def get_show_list(self, response):
        now = datetime.datetime.now()
        print(now)
        if now.minute == 30:
            self.send_emails()

        json_data = json.loads(response.text)
        data = json_data["data"]["search_page"]["recordList"]
        for i in data:
            id = i["item_id"]
            url = "https://www.vvic.com/item/{}".format(id)
            print(id)

            # 查询商品是否存在
            sql_exsits = "select goods_commonid,goods_image,goods_image_old from mall_goods_common where goods_url='%s'" % (url)
            self.cur.execute(sql_exsits)
            ret = self.cur.fetchone()
            if ret:
                pass
            else:
                headers = {
                    'user-agent': self.headers,
                    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                    'accept-encoding': 'gzip, deflate, br',
                }
                yield Request(url=url,
                              headers=headers,
                              callback=self.get_details,
                              # callback=self.select_price,
                              meta={"vcid": response.meta["vcid"],
                                    "pid": response.meta["pid"],
                                    "market": response.meta["market"],
                                    "id": id})


    def get_details(self, response):
        id = response.meta["id"]
        vcid = response.meta["vcid"]
        response = Selector(response)
        goods = SoukuanMallItem()
        # 商品基本信息
        goods['goods_url'] = "https://www.vvic.com/item/{}".format(id)
        goods['gc_name'] = vcid

        goods['goods_name'] = response.xpath("//div[@class='d-name']//strong/text()").extract()[0]
        goods['goods_brand'] = '广州女装批发'
        goods['goods_image'] = response.xpath("//div[@class='tb-pic-main']/a/@href").extract_first()
        goods['goods_images'] = response.xpath("//div[@class='thumbnail']//div[@class='tb-thumb-item ']/a/img/@mid").extract()
        goods['goods_jingle'] = ''
        goods['goods_price'] = float(response.xpath("//strong[@class='d-sale']/text()").extract_first())
        goods['goods_desc'] = response.xpath("//div[@class='fr con-info j-con-info']/div[1]").extract_first()
        goods['goods_storage'] = 100
        goods['goods_costprice'] = response.xpath("//strong[@class='d-sale']/text()").extract_first()

        # 商品属性
        attr_dd = response.xpath("//dd[@class='fl choice']")
        for i_item in attr_dd:
            # 处理特殊样式
            name = i_item.xpath(".//div[@class='name color']/text()").extract_first()
            if not name is None:
                value = i_item.xpath(".//div[@class='value color-choice']/ul/li/a/img/@alt").extract()
            else:
                name = i_item.xpath(".//div[@class='name']/text()").extract_first()
                value = i_item.xpath(".//div[@class='value goods-choice']//ul//li/a/text()").extract()
            self.attr[name] = value
        goods['goods_attr'] = self.attr
        goods_desc_img = response.xpath("//script[@id='descTemplate']/text()").extract_first()

        goods['goods_desc'] = goods['goods_desc'] + goods_desc_img
        shop_info = response.xpath("//div[@class='d-attr clearfix']/ul/li/text()").extract()
        goods['shop_info'] = ",".join([str(e).replace("\n", "").replace(' ', '') for e in shop_info])
        goods['goods_salenum'] = response.xpath("//p[@class='v-sale-total']/text()").extract_first()
        goods['goods_serial'] = response.xpath("//div[@class='value ff-arial']/text()").extract_first()
        # 获取商铺的其它信息
        goods['shop_name'] = response.xpath("//h2[@class='shop-name ']/span/text()").extract_first()
        goods['shop_range'] = response.xpath("//em[@class='text-top-num']/text()").extract_first()
        goods['shop_ali'] = response.xpath("//div[@class='text']/span[@class='fl']/text()").extract_first()
        shop_mobile_list = response.xpath("//li[@class='tel-list']/div[@class='text']/p//span[@class]/text()").extract()
        goods['shop_mobile'] = "".join([str(e) for e in shop_mobile_list])
        shopinfotmp = response.xpath("//ul[@class='mt10']/li")
        goods['shop_address'] = shopinfotmp[len(shopinfotmp) - 1].xpath(".//div[@class='text']/text()").extract_first()
        try:
            goods_up_time = response.xpath('//dl[@class="summary clearfix"]/dd[2]/div[2]/text()').extract()[0]
            up_time = re.findall(r"(\d{4}-\d{2}(-\d{2}))", goods_up_time)[0][0]
            goods["goods_up_time"] = time.mktime(time.strptime(up_time, "%Y-%m-%d"))
        except:
            goods["goods_up_time"] = ""

        yield goods

    def send_email(self,spider,reason):

        ppx_tables = [
                    "mall_goods_common",
                    "mall_goods",
                    "mall_goods_images",]
        self.end_ret = []
        for item in ppx_tables:
            sql = "SELECT count(1) FROM %s " % item
            self.cur.execute(sql)
            end_ret = self.cur.fetchone()
            self.end_ret.append(end_ret)

        mail_host = "smtp.163.com"
        mail_user = "rockyy2019@163.com"
        mail_pass = "vPzyOywR78"
        sender = 'rockyy2019@163.com'
        receivers = ['rocky-yu@qq.com']
        stats_info = self.crawler.stats._stats  # 爬虫结束时控制台信息
        content = "爬虫[%s]已经关闭，原因是: %s.\n以下为运行信息：\n %s \n\n start_ret:%s \n end_ret:%s" % (spider.name, reason, stats_info, self.start_ret, self.end_ret)
        title = spider.name
        message = MIMEText(content, 'plain', 'utf-8')
        message['From'] = "{}".format(sender)
        message['To'] = ",".join(receivers)
        message['Subject'] = title
        try:
            smtpObj = smtplib.SMTP_SSL(mail_host, 465)  # 启用SSL发信, 端口一般是465
            smtpObj.login(mail_user, mail_pass)
            smtpObj.sendmail(sender, receivers, message.as_string())
            print("mail has been send successfully.")
        except smtplib.SMTPException as e:
            print(e)


    def send_emails(self):
        ppx_tables = [
                    "mall_goods_common",
                    "mall_goods",
                    "mall_goods_images",]
        self.end_ret = []
        for item in ppx_tables:
            sql = "SELECT count(1) FROM %s " % item
            self.cur.execute(sql)
            end_ret = self.cur.fetchone()
            self.end_ret.append(end_ret)

        mail_host = "smtp.163.com"
        mail_user = "rockyy2019@163.com"
        mail_pass = "vPzyOywR78"
        sender = 'rockyy2019@163.com'
        receivers = ['rocky-yu@qq.com']
        # content = "三级分类{}-市场{}爬取完毕；\n sql:{}".format(vcid,market,self.end_ret)
        content = "sql:{}".format(self.end_ret)
        title = "soukaun_mall"
        message = MIMEText(content, 'plain', 'utf-8')
        message['From'] = "{}".format(sender)
        message['To'] = ",".join(receivers)
        message['Subject'] = title
        try:
            smtpObj = smtplib.SMTP_SSL(mail_host, 465)  # 启用SSL发信, 端口一般是465
            smtpObj.login(mail_user, mail_pass)
            smtpObj.sendmail(sender, receivers, message.as_string())
            print("mail has been send successfully.")
        except smtplib.SMTPException as e:
            print(e)