import requests
from lxml import etree
import pymysql


# 创建链接对象
def get_conn():
    conn = pymysql.Connection(
        host="localhost",  # 主机名（IP）
        port=3306,  # 端口
        user="root",  # 账户
        password="416814",  # 密码
        autocommit=True  # 自动提交（确认）
    )
    conn.select_db("weather")  # 选择数据库
    cursor = conn.cursor()  # 获取游标对象
    return conn, cursor


# 关闭链接
def close_coon(coon, cursor):
    cursor.close()
    coon.close()


# 爬取数据并存入数据库
def spider(url, headers):
    conn, cursor = get_conn()

    response = requests.get(url=url, headers=headers)
    response.encoding = 'utf-8'

    requests.adapters.DEFAULT_RETRIES = 15
    s = requests.session()
    s.keep_alive = False

    page_text = response.text
    tree = etree.HTML(page_text)
    li_list = tree.xpath('/html/body/div[7]/div[2]/div[2]/ul/li')
    for li in li_list:
        province_city_url = 'https://tianqi.2345.com/' + li.xpath('./a/@href')[0]
        province_city_name = li.xpath('./a/@title')[0]
        province_city_response = requests.get(url=province_city_url, headers=headers)
        province_city_response.encoding = 'utf-8'
        province_city_text = province_city_response.text
        province_city_tree = etree.HTML(province_city_text)
        tr_list = province_city_tree.xpath('/html/body/div[7]/div[2]/div[2]/div[1]/table/tr')
        for tr in tr_list:
            temp = []
            city_proper_name = tr.xpath('./td[1]/a/@title')[0]
            city_proper_name = city_proper_name.rstrip('天气')
            temp.append(city_proper_name)
            city_proper_url = 'https://tianqi.2345.com' + tr.xpath('./td[1]/a/@href')[0]
            city_proper_response = requests.get(url=city_proper_url, headers=headers)
            city_proper_text = city_proper_response.text
            city_proper_tree = etree.HTML(city_proper_text)
            city_proper_weather_url = 'https://tianqi.2345.com' + city_proper_tree.xpath(
                '//*[@id="today-main-deatil"]/div[2]/div[1]/div[2]/div[2]/a[3]/@href')[0]
            city_proper_weather_response = requests.get(url=city_proper_weather_url, headers=headers)
            city_proper_weather_text = city_proper_weather_response.text
            city_proper_weather_tree = etree.HTML(city_proper_weather_text)
            weather_li_list = city_proper_weather_tree.xpath(
                '//*[@id="seven-main-detail"]/div[2]/div[1]/div[1]/div[2]/ul/li')
            for weather_li in weather_li_list[1:]:
                date_data = weather_li.xpath('./a/em/text()')[0].strip()
                date_data = date_data.replace('/', '-')
                weather_data = weather_li.xpath('./a/i/text()')[0]
                temperature_data = weather_li.xpath('./a/span[@class="tem-show"]/text()')[0]
                wind_scale_data = weather_li.xpath('./a/span[@class="wind-name"]/text()')[0]
                air_quality_data = weather_li.xpath('./a/span[@class="wea-qulity"]/text()')[0]
                all_weather_data = '天气:' + weather_data + '，温度:' + temperature_data + '，风级:' + wind_scale_data + '，空气质量:' + air_quality_data
                cursor.execute("insert into temperature_data values(%s,%s,%s)",
                               (city_proper_name, date_data, all_weather_data))
    close_coon(conn, cursor)


# 从数据库获取数据
def get_data():
    city_name_list = []
    date_list = []
    weather_list = []
    coon, cursor = get_conn()
    cursor.execute("select * from temperature_data")
    temp1 = cursor.fetchall()
    for item in temp1:
        city_name_list.append(item[0])
        date_list.append(item[1])
    city_name_list = list({}.fromkeys(city_name_list).keys())
    date_list = list({}.fromkeys(date_list).keys())
    for i in range(0, 7):
        today_date = date_list[i]
        cursor.execute("select city_name,weather from temperature_data where date=%s", today_date)

        weather_list.append(cursor.fetchall())
    close_coon(coon, cursor)
    return date_list, weather_list


url = 'https://tianqi.2345.com/china.htm'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 '
                  'Safari/537.36'
}
# spider(url=url, headers=headers)
