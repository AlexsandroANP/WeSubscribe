from configparser        import ConfigParser
import os
import time
import functools
import random
import sys 

from ComWeChatRobot.com import wxRobot

# Where a file named "config.ini" at, like ==> 'C:\Users\wesubscribe\config.ini'
ConfigName = r''

config     = ConfigParser()
config.read(ConfigName,'UTF-8') 

def TipsINFO(ActionName):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start  = time.ctime()
            begin  = time.time()
            result = func(*args, **kwargs)
            print(f'- ----------\n= Finished :)\t{ActionName}')
            print(f'= Start at\t{start}\n= End at \t{time.ctime()}')
            print(f'= It takes \t{round(time.time()-begin,2)}s')
            print('==========\n')
            return result
        return wrapper
    return decorator


def Holdon(ActionName):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start           = time.ctime()
            begin           = time.time()
            MinHoldonTime   = config.getint('FetchParameter','MinHoldonTime')
            MaxHoldonTime   = config.getint('FetchParameter','MaxHoldonTime')
            HoldingOn       = random.randint(MinHoldonTime,MaxHoldonTime)
            time.sleep(random.random())
            for i in range(HoldingOn):
                RestSec = HoldingOn-i
                if RestSec < 10:
                    RestSec = '0'+str(HoldingOn-i)
                print(f'= Waiting \t\t{RestSec}s\r', end='', flush=True)
                time.sleep(1)
                print('\b'*len(str(RestSec)), end='')
            result = func(*args, **kwargs)
            print(f'=\n= Finished :)\t{ActionName}')
            print(f'= Start at\t{start}\n= End at \t{time.ctime()}')
            print(f'= It takes \t{time.time()-begin} seconds')
            print('----------\n')
            return result
        return wrapper
    return decorator


@ TipsINFO('WeChatRobot Initial')
def WeChatRobot():
    WxPid                  = wxRobot.get_wechat_pid_list()
    if len(WxPid)          == 0:
        WeChatRobot        = wxRobot.start_wechat()
        if WeChatRobot     ==  None:
            print('= WeChat \t Not in Running')
        else:
            print('= WeChat \t Is Running')
    elif len(WxPid)        == 1:
        WxPid              = WxPid[0]
        WeChatRobot        = wxRobot.WeChatRobot(WxPid)
    else:
        print(f'= WeChat PID \t{WxPid} \tCheck if Only One Wechat Is Rinning')

    WeChatRobot_status     = WeChatRobot.StartService()
    if WeChatRobot_status  == 0:
        print('= WeChatRobot \tInitiate Successfully')
    else:
        print(f'= WeChatRobot \tInitiate Failed，Error Code \t{WeChatRobot_status}')

    login_status           = WeChatRobot.IsWxLogin()
    if login_status        == False:
        print(f'= WeChat \tNot Login \tTry Login Again')
    elif login_status      == True:
        #NotifyMe(WeChatRobot,'WeSubscribe 的 Wechat 已登入')
        print(f'= WeChat \tLogined \t\t Check Your Wechat for Notification')
    else:
        print(f'= WeChat \tFail to Login \tCheck if Anything Went Wrong')

    return WeChatRobot



def NotifyMe(WeChatRobot, SendMsg):
    my_wxid    = 'wxid_h1z6z3jrzku021'
    status     = WeChatRobot.SendText(my_wxid, SendMsg)
    if status == 0:
        print(f'\n= Delivered Message Successfully：\t{SendMsg}') 
    else:
        print(f'\n= Fail to Delivered Message：\t{SendMsg}')


def WorkingDirectory(WhichDir):
    if os.path.exists(ConfigName):
        config = ConfigParser()
        config.read(ConfigName,'UTF-8') 
        try:
            WD = config['WorkingDirectory'][WhichDir]
            return WD
        except KeyError:
            print(f"=====\n= Key Not Found! \t{WhichDir}")
            print('= A Default Folder Will Be Created/Uesed for Running WeSubscribe.\n=')
            if WhichDir == 'WeSubscribe':
                WeSubscribeDirectory = os.getcwd()
                return WeSubscribeDirectory
            elif WhichDir == 'PagesArchive':
                if not os.path.exists(os.path.join(os.getcwd(), 'pages_archive')):
                    os.makedirs(os.path.join(os.getcwd(), 'pages_archive'))
                    print('= Not Exist \t\tpages_archive\n= Make a Folder \tpages_archive\n=')
                    PagesArchiveDirectory = f'{os.getcwd()}\pages_archive'
                    return PagesArchiveDirectory
            elif WhichDir == 'RssFeeds': 
                if not os.path.exists(os.path.join(os.getcwd(), 'rssfeeds')):
                    os.makedirs(os.path.join(os.getcwd(), 'rssfeeds'))
                    print('= Not Exist \t\trssfeeds\n= Make a Folder \trssfeeds\n=')
                    RssFeedsDirectory = f'{os.getcwd()}\rssfeeds'
                    return RssFeedsDirectory
            else:
                print('= Try Setting Parameters in "config.ini",and Check Anything Could Be Wrong.')
    else:
        print("= Failed to Find out 'Config.ini' for WeSubscribe,\n Check if Parameter 'ConfigName' is an accessible file.")