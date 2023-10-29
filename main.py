from scripts             import WeChatRobot,WorkingDirectory
from comwesubscribe      import Subscriptions,UpdateData
from feed2rss            import GenerateRss,GenerateOPML


# Initial This Script
WeChatRobot             = WeChatRobot()
WeSubscribeDirectory    = WorkingDirectory('WeSubscribe')
PagesArchiveDirectory   = WorkingDirectory('PagesArchive')
RssFeedsDirectory       = WorkingDirectory('RssFeeds')
print(f'= WeSubscribeDirectory\t\t{WeSubscribeDirectory}\n= PagesArchiveDirectory\t\t{PagesArchiveDirectory}\n= RssFeedsDirectory\t\t{RssFeedsDirectory}\n')


# Update Subscriptions List
Subscriptions(WeChatRobot,WeSubscribeDirectory,PagesArchiveDirectory)

# Update Subscription Stories
UpdateData(WeChatRobot,WeSubscribeDirectory,PagesArchiveDirectory)

# Make RSSfeeds
GenerateRss(WeSubscribeDirectory,RssFeedsDirectory,PagesArchiveDirectory)


# VisitPath is a Url Prefix of rssfeeds
# Example: http://127.0.0.1/rssfeeds
VisitPath = ''

# Make a OPML Subscription File
GenerateOPML(RssFeedsDirectory,VisitPath)


print(f'Stop Service\tWeChatRobotd\t{WeChatRobot.StopService()}')
print('= DONE')