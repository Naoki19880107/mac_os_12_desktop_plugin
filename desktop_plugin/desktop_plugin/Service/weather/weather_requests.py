import requests
import xml.dom.minidom as minidom

from desktop_plugin.Tool.PathHelper import PathHelper


class weather_requests:
    KEY = 'SBsSbmczsuz1JK-4x'  # API key
    UID = "U785B76FC9"  # 用户ID

    LOCATION = 'ip'  # 所查询的位置，可以使用城市拼音、v3 ID、经纬度等
    API = 'https://api.seniverse.com/v3/weather/now.json'  # API URL，可替换为其他 URL
    UNIT = 'c'  # 单位
    LANGUAGE = 'zh-Hans'  # 查询结果的返回语言
    # i = 0

    @staticmethod
    def __fetchWeather():
        result = requests.get(weather_requests.API, params={
            'key': weather_requests.KEY,
            'location': weather_requests.LOCATION,
            'language': weather_requests.LANGUAGE,
            'unit': weather_requests.UNIT
        })
        return result.json()

    @staticmethod
    def __WriteValue(city, text, temperature):
        dom = minidom.getDOMImplementation().createDocument(None, 'Root', None)
        root = dom.documentElement
        element = dom.createElement('city')
        element.appendChild(dom.createTextNode(city))
        root.appendChild(element)
        element = dom.createElement('text')
        element.appendChild(dom.createTextNode(text))
        root.appendChild(element)
        element = dom.createElement('temperature')
        element.appendChild(dom.createTextNode(temperature))
        root.appendChild(element)
        with open(PathHelper.getCurrentPath()+'/weather.xml', 'w', encoding='utf-8') as f:
            dom.writexml(f, addindent='\t', newl='\n', encoding='utf-8')

    @staticmethod
    def __ReadValue():
        dom = minidom.parse(PathHelper.getCurrentPath()+'/weather.xml')
        root = dom.documentElement
        return root.getElementsByTagName('city')[0].firstChild.data, root.getElementsByTagName('text')[
            0].firstChild.data, root.getElementsByTagName('temperature')[0].firstChild.data

    @staticmethod
    def getWeather():
        # if weather_requests.i == 0 or weather_requests.i % 3600 == 0:
        #     result = weather_requests.__fetchWeather()
        #     try:
        #         city = result['results'][0]['location']['name']
        #         now = result['results'][0]['now']
        #         weather_requests.__WriteValue(city, now['text'], now['temperature'])
        #     except (OSError, KeyError):
        #         pass
        # weather_requests.i = weather_requests.i + 1
        # city, text, temperature = weather_requests.__ReadValue()
        # return city + '' + '天气：' + text + '\n 当地气温：' + temperature + '°c'

        result = weather_requests.__fetchWeather()
        return result['results'][0]['location']['name'] + '' + '天气：' + result['results'][0]['now']['text'] + '\n 当地气温：' + result['results'][0]['now']['temperature'] + '°c'

