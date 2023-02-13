#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import requests
import json
import hashlib
import time
from GraphChat import ChatBotGraph
from hanziconv import HanziConv


# In[2]:


table = pd.read_csv('table.csv')
table_rcmd = pd.read_csv('table_rcmd.csv')


# In[3]:


#script_df = pd.DataFrame(script)
script_df = pd.read_csv('script.csv')


# In[4]:


dialogs = {}


# In[5]:


dialogs[1] = {'stage':0,'store_features':[],'needs':[]}


# In[6]:


def fuzzy(needs):
    return '您好！我們認爲富樂士林比較適合您'


# In[7]:


def checkType(q,uid):
    sentences = []
    dialogs[uid]['temp_table'] = table
    dialogs[uid]['temp_table']['question'] = q
    for item in dialogs[1]['temp_table']['sentence']:
        sentences.append([q,item])
    payload2 = json.dumps({
         'sentences':sentences
    })
    # infer
    res2 = json.loads(requests.post('http://192.168.109.18:5001/getAnswer',data = payload2).text)
    # process
    dialogs[uid]['result'] = []
    dialogs[uid]['probability'] = []
    for item in eval(res2['content']):
        dialogs[uid]['result'].append(item[0])
        dialogs[uid]['probability'].append(item[1])
    dialogs[uid]['temp_table']['result'] = pd.Series(dialogs[1]['result'])
    dialogs[uid]['temp_table']['probability'] = pd.Series(dialogs[1]['probability'])
    # prepare to return
    try:
        max_fit_prob = dialogs[uid]['temp_table'][dialogs[1]['temp_table'].result == '1']['probability'].max()
        #dialogs[uid]['temp_table'][(dialogs[1]['temp_table'].result == '1') & (dialogs[1]['temp_table'].probability == max_fit_prob)]
        return dialogs[uid]['temp_table'][(dialogs[1]['temp_table'].result == '1') & (dialogs[1]['temp_table'].probability == max_fit_prob)].iloc[0]['meaning']
        # return str(dialogs[uid]['temp_table'])
    except:
        return None


# In[8]:


# 負責最終的推薦
def rcmd(uid):
    needs_type = list(table_rcmd['type'])
    dialogs[uid]["features_slices"] = []
    temp = []
    for sentence in dialogs[uid]['store_features']:
        for sub in sentence.split('，'):
            dialogs[uid]["features_slices"].append(sub)
    # 此處的key後期有用
    for question in [
        {'price':'how about the price'},
        {'env':'how about the environment'},
        {'style':'what does he want to eat'},
        {'cp':'what is the cp value'},
        {'qt':'how about the queue time'}]:
        payload1 = json.dumps({
             'question': list(question.values())[0],
             'context': translate_z2e('，'.join(dialogs[uid]["features_slices"]))
        })
        # 通過回答分數排除錯亂的結果
        if json.loads(requests.post('http://163.14.137.78:1300/getAnswer',data = payload1).text)['score'] > 0.28:
            #暫存answer
            answer = json.loads(requests.post('http://163.14.137.78:1300/getAnswer',data = payload1).text)['answer']
            dialogs[uid]['needs'].append(answer)
            # 把當前回答填充到temp，以便融合進推薦比對表進行相似度匹配
            for need in needs_type:
                # 只翻譯一次節約時間
                translated = translate_e2z(answer)
                if list(question.keys())[0] == need:
                    temp.append(translated)
        else:
            dialogs[uid]['needs'].append('nothing')
            # 如果沒有得到本次的question的key指代的單項答案，temp填充“無”
            for need in needs_type:
                if list(question.keys())[0] == need:
                    temp.append('無' + need)
    # 記錄中文要求，直接轉換temp來節約翻譯時間
    for need in dialogs[uid]['needs']:
        dialogs[uid]['needs_cn'] = list(set(temp))
    return fuzzy(temp)


# In[9]:


#此方法最終只輸出一個str
def dialog(q,uid):
    # stage == 0
    try:
        # 本地變數
        if dialogs[uid]['stage'] == 0 and checkType(q,1) == 'greeting':
            return '歡迎回到對話！'
        else:
            pass
    except:
        # 本地變數
        dialogs[uid] = {'stage':0,'store_features':[],'needs':[]}
        return '您好，似乎是初次見面，我叫DiningBot，可以聽取您的用餐場所要求后幫助也許有選擇困難的您考慮餐廳~？'
    # 檢測打招呼
    # if stage == 0 and CheckType(q) == "Greeting":
    #     session = script_df[script_df.Input == q]
    #     return session.iloc[0]['Output']
    # 詢問店家就這麼做
    if dialogs[uid]['stage'] == 0 and checkType(q,uid) == "shop":
        # 本地變數
        dialogs[uid]['stage'] = 1
        # session = script_df[script_df.Input == q]
        # return session.iloc[0]['Output']
        return 'OK，那麽就麻煩您説一下您對餐廳的要求吧~比如環境，cp值，排隊時間，餐點樣式之類的。'
    # stage == 1
    # 詢問商店特徵就這麼做
    # if dialogs[uid]['stage'] == 1 and checkType(q,uid) != 'stop':
    if dialogs[uid]['stage'] == 1 and q != '沒了':
        dialogs[uid]['store_features'].append(q)
        return '收到！請問還要補充嗎？'
    # elif dialogs[uid]['stage'] == 1 and checkType(q,uid) == 'stop':
    elif dialogs[uid]['stage'] == 1 and q == '沒了':
        dialogs[uid]['stage'] = 2
        # 推荐
        return rcmd(uid)
    else:
        pass
    # stage == 2
    if dialogs[uid]['stage'] == 2:
        # modified 20220116
        # return '不好意思，請問想重新推薦嗎？'
        handler = ChatBotGraph()
        # return HanziConv.toTraditional(handler.chat_main(HanziConv.toSimplified(q)))
        return HanziConv.toTraditional(handler.chat_main(q))


# In[11]:


# print(dialog('你好',1))


# In[12]:


# print(dialog('我需要推薦餐廳',1))


# In[13]:


# print(dialog('价格不要太高',1))


# In[14]:


# print(dialog('環境好',1))


# In[15]:


# print(dialog('我想吃火鍋',1))


# In[16]:


# print(dialog('cp值高',1))


# In[17]:


# print(dialog('排隊時間可以長',1))


# In[18]:


def translate_z2e(query):
    appid = '20220102001044938'
    q = query
    salt='123456'
    key = '4i3lYa4aSyuH2TCcmaBh'
    mid = appid + q + salt + key
    hl = hashlib.md5()
    hl.update(mid.encode(encoding='utf-8'))
    sign = hl.hexdigest()
    url = f'https://api.fanyi.baidu.com/api/trans/vip/translate?q={q}&from=zh&to=en&appid={appid}&salt={salt}&sign={sign}'
    return eval(requests.get(url).text)['trans_result'][0]['dst']


# In[19]:


def translate_e2z(query):
    appid = '20220102001044938'
    q = query
    salt='123456'
    key = '4i3lYa4aSyuH2TCcmaBh'
    mid = appid + q + salt + key
    hl = hashlib.md5()
    hl.update(mid.encode(encoding='utf-8'))
    sign = hl.hexdigest()
    url = f'https://api.fanyi.baidu.com/api/trans/vip/translate?q={q}&from=en&to=zh&appid={appid}&salt={salt}&sign={sign}'
    return eval(requests.get(url).text)['trans_result'][0]['dst']


# In[20]:


# print(dialog('停下',1))


# In[21]:


# print(dialog('等一下',1))


# In[22]:


# payload1 = json.dumps({
#      'question': 'how about the cp value',
#      'context': 'CP value high'
# })
# print(json.loads(requests.post('http://163.14.137.78:1300/getAnswer',data = payload1).text))


# In[23]:


# print(translate_e2z('The environment should be good'))


# In[24]:


# print(translate_z2e('cp值高'))


# In[25]:


# checkType('沒了',1)

