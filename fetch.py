from bs4                 import BeautifulSoup
from configparser        import ConfigParser
import re
import requests

from scripts             import Holdon

@Holdon('Fetch a Page')
def FetchPage(FeedUrl,FileName):
    # Setting for Request
    # Step1: Vist Any Wechat Subscription Story Page like 
    #        'https://mp.weixin.qq.com/s/YaU0RPcqA8PvqSb31NL0eg'.
    #
    # Step2: Vist 'https://curlconverter.com/',
    #        and Select "Language" as "Python + Requests"
    #         
    # Step3: Follow the Insctructions and Fill All Parameters below.
    
    cookies = {}
    headers = {}


    context   = ''
    response  = requests.get(FeedUrl,cookies=cookies,headers=headers)

    try:
        soup                 = BeautifulSoup(response.text, 'html.parser')
        divs                 = soup.find('div', {'id': 'img-content', 'class': 'rich_media_wrp'})
        for section in divs:
            section          = str(section)
            section          = re.sub('data-src=', 'src=', str(section))
            section          = re.sub('="//res.', '="http://res.', str(section))
            section          = re.sub('visibility: hidden', 'visibility: visible', str(section))
            section          = re.sub('visibility:hidden', 'visibility:visible', str(section))
            section          = re.sub('display:none', 'display:block', str(section))
            section          = re.sub('display: none', 'display: block', str(section))
            context         += section
        if context          == None:
            print(f'= Not a Supported Page \t{FileName}')


        with open(FileName, 'w', encoding='utf-8') as file:
            file.write(context)
    
    except TypeError:
        print(f'= Fetch Failed, Pass \t{FileName}')



