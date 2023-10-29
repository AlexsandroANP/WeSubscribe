import json
import os
import re

from scripts        import TipsINFO
import fetch
import time


@ TipsINFO('Subscribed List Update')
def Subscriptions(WeChatRobot,WeSubscribeDirectory,PagesArchiveDirectory):
    WechatSubscriptions  = WeChatRobot.GetOfficialAccountList()
    FileName             = f'{WeSubscribeDirectory}\subscriptions.json'
    SubscribedList       = []

    # Initiate "subscriptions.json"
    if not os.path.exists(FileName):
        with open(FileName, 'w') as f:
            json.dump(SubscribedList, f)
            print('= Not Exist \t\tsubscriptions.Json\n= Make a File \tsubscriptions.Json\n=')
    else:
        print('= Did Exist \t\tsubscriptions.Json\n= Update the File \tsubscriptions.Json\n=')

    # Find out or Creat Folder for Saving Pages from wxSubscription
    for element in WechatSubscriptions:
        SubscribedDict               = {}
        SubscribedDict['wxid']       = element['wxid'] 
        SubscribedDict['wxNickName'] = element['wxNickName']
        SubscribedList.append(SubscribedDict)
        if not os.path.exists(os.path.join(PagesArchiveDirectory, element['wxNickName'])):
            os.makedirs(os.path.join(PagesArchiveDirectory, element['wxNickName']))
            print(f"= Not Exist \t\t{element['wxNickName']}\n= Make a Folder \t{element['wxNickName']}\n=")
        else:
            print(f"= Did Exist \t\t{element['wxNickName']}\n= Update the Folder \t{element['wxNickName']}\n=")
    
    with open(FileName, 'w', encoding='utf-8') as file:
        SubscribedList = str(SubscribedList)
        SubscribedList = SubscribedList.replace("'",'"')
        file.write(SubscribedList)










@ TipsINFO('Pages Update')
#def UpdateData(WeChatRobot,wxid,wxNickName,PagesArchiveDirectory):
def UpdateData(WeChatRobot,WeSubscribeDirectory,PagesArchiveDirectory):
    SubscriptionsJson     = f'{WeSubscribeDirectory}\subscriptions.json'
    with open(SubscriptionsJson, 'r',encoding='utf-8') as f:
        SubscriptionsList = json.load(f)
    for Subscription in SubscriptionsList:
        wxid              = Subscription.get('wxid')
        wxNickName        = Subscription.get('wxNickName')
        messages          = WeChatRobot.GetHistoryPublicMsg(wxid,'').get('MsgList').get('Msg')
        JsonName          = f'{PagesArchiveDirectory}\{wxNickName}\{wxNickName}.json'

        # Check if {wxNickName}.json exsis or not.
        if not os.path.exists(JsonName):
            InitialJson = []
            with open(JsonName, 'w') as f:
                json.dump(InitialJson, f)
                print(f'= Not Exists  \t\t{JsonName}')
                print(f'= Creating \t\t{JsonName}')

        with open(JsonName, 'r') as file:
            JsonFile = json.load(file)
            print(f'= Did Exists \t\t{JsonName}\n- ----------')
                 
        # Unpack Information from wxFeeds            
        for msg in messages:
            TimeStamp                    = msg.get("AppMsg").get("BaseInfo").get("UpdateTime")
            DetailInfo                   = msg.get("AppMsg").get("DetailInfo")
            for details in DetailInfo:
                FeedTitle                = details.get("Title")
                FeedDigest               = details.get("Digest")
                FeedUrl                  = details.get("ContentUrl")
                FeedDate                 = TimeStamp
                PageTitle                = re.sub(r'[:\?*/<>|\\/"”“]', '_', FeedTitle)
                FileName                 = f'{PagesArchiveDirectory}\{wxNickName}\{FeedDate} {PageTitle}.html'
                print(f'= FeedTitle\t\t{FeedTitle}\n= PageTitle\t\t{PageTitle}\n= FileName\t\t{FileName}')

                # Check if FeedDict Has Been Logged or Not
                FeedDict                 = {}
                FeedDict['FeedTitle']    = FeedTitle
                FeedDict['FeedDigest']   = FeedDigest
                FeedDict['FeedUrl']      = FeedUrl
                FeedDict['FeedDate']     = FeedDate
                FeedDict['PageTitle']    = PageTitle
                FeedDict['FileName']     = FileName
                if FeedDict in JsonFile:
                    print(f'= In Log \t\t{PageTitle}')
                else:
                    JsonFile.append(FeedDict)
                    print(f'= Out of Log \t\t{PageTitle}')

                # Check HtmlPage Exists or Not
                if os.path.exists(FileName):
                    print(f'= Did Exists\t\t{FileName}\n- ----------')
                else:
                    print(f'= Not Exists\t\t{FileName}') 
                    fetch.FetchPage(FeedUrl,FileName)


                    
        with open(JsonName, 'w') as file:
            json.dump(JsonFile, file, indent=4) 
            print(f'= Updated \t\t{JsonName}\n\n==========')
            file.close()
    
    