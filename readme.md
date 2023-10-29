中文 [https://mp.weixin.qq.com/s/SK4_O7_O6uTa9dIm5ot2DQ]

## What for?
Since WeChat Subscriptions no longer pushes its messages by timeline, instead of using mysterious algorithms, the reading experience has become worse and worse.

Empowering by these so-called Better User Experience algorithms, it becomes wiser and wiser and makes decisions to filter unwise stories away from you.

So, why makes things so complicated?
Less is more, and RSS forever!


WeSubcribe, this program, aims to convert WeChat Subscription Push into RSS feeds. 

Users can control what they read and when they read it.

WeSubscribe relies on ComWeChatRobot for its core functionality.

Great Thanks to the developers of ComWeChatRobot!



## User Guidance 
Tks again, to mates who willing to try WeSubscribe.

Below is the guidance to help mates to get the scripts into gear.

Step by step, one by one.



### Prepare: WeSubscribe
1. Download the ZIP package of WeSubscribe from GitHub for free.
2. Unpack the ZIP package.

### Prepare: Wechat
1. Search for WeChat 3.7.0.30 on GitHub.
2. Install and run WeChat 3.7.0.30.

### Prepare: ComWechatRobot 
1. Visit *ljc545w* on Github and download *ComWeChatRobot 3.7.0.30-0.0.9* (https://github.com/ljc545w/ComWeChatRobot)  

2. Unpack the downloaded ZIP package.

3. Run CMD as an administrator and type the following command if the package is unpacked in the root directory of C:

    ```
    C:\ComWeChatRobot\com\CWeChatRobot.exe /regserver 
    ```


### Prepare: Settings
1. Copy folder *ComWeChatRobot* into folder *WeSubscribe*
2. Open and edit *fetch.py*, and follow instructions, the comment, to complete "cookies" and "headers". Save the changes.
3. Open and edit *scripts.py*, and follow instructions, the comment, to complete "ConfigName". Save the changes.
4. Open and edit *config.ini*, and follow instructions, the comment, to complete "ConfigName". Save the changes.


## Ready to Run it
If all of the previous steps are followed, everything should be working properly.

Open and run *main.py*. It may fail to run because of missing modules. Just download and install them.

If the script stops and errors occur, the terminal should provide more information. Be patient and try to solve it. 

The script may take a long time to finish running, depending on the length of your Subscriptions list.

Thank you again for trying WeSubscribe!

## Further More
Self-hosted RSS readers such as FreshRSS are recommended. OPML files can be imported to RSS readers and feeds can be read on other RSS readers such as NetNewsWire using the API.
