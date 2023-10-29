from bs4            import BeautifulSoup
from datetime       import datetime, timezone, timedelta
from dateutil.tz    import tzoffset
from feedgen.feed   import FeedGenerator
from xml.etree      import ElementTree 
from pypinyin       import lazy_pinyin
import os      


from scripts        import TipsINFO
import json


@TipsINFO(f'Generate Feed')
def GenerateRss(WeSubscribeDirectory,RssFeedsFolder,PagesArchive):
    SubscriptionsJson     = f'{WeSubscribeDirectory}\subscriptions.json'
    with open(SubscriptionsJson, 'r',encoding='utf-8') as f:
        SubscriptionsList = json.load(f)
    for Subscription in SubscriptionsList:
        wxNickName        = Subscription.get('wxNickName')
        JsonName          = f'{PagesArchive}\{wxNickName}\{wxNickName}.json'
        with open(JsonName, 'r') as file:
            JsonFile      = json.load(file)
            print(f'\n==========\n= wxNickName\t\t{wxNickName}\n= Loaded\t\t{JsonName}')

        fg = FeedGenerator()
        fg.title(wxNickName)
        fg.description(f"This is {wxNickName}, and enjoy reading! :)")
        fg.updated(datetime.now(timezone(timedelta(hours=+8.0))))
        fg.pubDate(datetime.now(timezone(timedelta(hours=+8.0))))
        fg.generator('WeSubscribe','Beta and inTest')
        fg.link( href='https://mp.weixin.qq.com/', rel='alternate' )
        fg.language('zh-cn')
        fg.copyright(f'{wxNickName} \tAll rights reserved.')
        for FeedDict in JsonFile:
            FeedTitle       = FeedDict['FeedTitle']      
            FeedUrl         = FeedDict['FeedUrl']      
            FeedDate        = FeedDict['FeedDate']     
            FileName        = FeedDict['FileName']
            print(f'= FeedTitle\t\t{FeedTitle}')
            try:
                description     = RssDescription(FileName)
                fe = fg.add_entry()
                fe.id(FeedUrl)
                fe.title(FeedTitle)
                fe.description(description)
                fe.link(href=f'{FeedUrl}')
                fe.pubDate(datetime.fromtimestamp(FeedDate,tzoffset(None, +8.0 * 3600)))
                fe.rights(wxNickName)

            except FileNotFoundError as er1: 
                print(f'= Not Support wxFeed \t{FeedTitle}')
                print(f'= Error \t\t {er1}')
                   

        
        FileNamePinyin = ''
        for char in wxNickName:
            for charPinyin in lazy_pinyin(char):
                FileNamePinyin += charPinyin
       
        fg.rss_file(f'{RssFeedsFolder}\{FileNamePinyin}.xml',encoding='utf-8') 
        print(f'= Ready\t\t\t{FileNamePinyin}\t\t\n')



def RssDescription(FileName):
    with open(FileName, 'r', encoding='utf-8') as file:
        content = file.read()
        soup    = BeautifulSoup(content, 'html.parser')
        divs    = soup.find('div', 
                            {'id': 'js_content', 
                             'class': ['rich_media_wrp', 
                             'js_underline_content', 
                             'autoTypeSetting24psection']}
                             )
    return str(divs)






@TipsINFO('Generate a OPML')
def GenerateOPML(RssFeedsFolder,VisitPath):
    opmlName                = f'{RssFeedsFolder}\output.opml'
    # the head element
    head = f'<head>\n<title>WeSubscribe RSS</title>\n<dateCreated>{datetime.now(timezone(timedelta(hours=+8.0)))}</dateCreated>\n</head>' 
    # the body element
    body = '<body>\n'
    for FileName in os.listdir(RssFeedsFolder):
        if FileName.endswith(".xml"):  
            xmlFile = ElementTree.parse(os.path.join(RssFeedsFolder, FileName))
            xmlRoot = xmlFile.getroot()
            channel = xmlRoot.find("channel")   
            TiTle   = channel.find("title").text
            uRl = f'{VisitPath}/{FileName}'
            outline = f'<outline text="{TiTle}" type="rss" xmlUrl="{uRl}"/>\n'
            body += outline
    body = body + '</body>'
    opml = f'<?xml version="1.0" encoding="UTF-8"?>\n<opml version="2.0">\n{head}\n{body}</opml>'

    with open(opmlName,'w',encoding="utf-8") as opml_file:
        opml_file.write(opml)
        opml_file.close()










