from selenium import webdriver
import codecs
import csv
import re
from natto import MeCab
import os
import wx


options = webdriver.chrome.options.Options()
options.add_argument("--headless")  # これ消せばブラウザ画面が出ます

driver = webdriver.Chrome(chrome_options=options)

__location__ = os.path.realpath(
                                os.path.join(os.getcwd(), os.path.dirname(__file__)))

def nlp(data,selection):
    result = ""
    nm = MeCab() # nmというMeCabクラスのインスタンスを作成
    negaposi_dic = getNegaPosiDic() # 評価データの読み込み(さっき作った関数を呼び出している。)
    sentenses = re.split("[。！!♪♫★☆>?？（）w]", data)  # 一文ごとに分ける
    for sentense in sentenses: # 文の数だけ繰り返す
        negaposi = 0
        result_all = nm.parse(sentense) # 形態素解析して品詞分解をしている。
        result_words = result_all.split("\n")[:-1]  # 単語ごとに分ける
        for word in result_words:
            word_toarray = re.split('[\t,]', word)
            if word_toarray[0] in negaposi_dic and int(negaposi_dic[word_toarray[0]]) == selection:
                url = "https://thesaurus.weblio.jp/antonym/content/{0}".format(word_toarray[0])
                driver.get(url)
                try:
                    result += driver.find_element_by_class_name('wtghtAntnm').text
                    #result += driver.find_element_by_xpath('//*[@id="main"]/div[4]/div/div[1]/div/table/tbody/tr[1]/td[4]/span/a').text
                except:
                    result += word_toarray[0]
                    tmp = s_text_6.GetLabel()
                    tmp += word_toarray[0]
                    s_text_6.SetLabel(tmp+' ')
            else:
                result += word_toarray[0]
    return result

def getNegaPosiDic():
    with codecs.open(os.path.join(__location__, "./dataset/negaposinoun.csv"), 'r', 'utf-8') as f_in:
        reader = csv.reader(f_in, delimiter=',', lineterminator='\n')
        negaPosiDic = {}
        for i, x in enumerate(reader):
            y = x[0].split(" ")
            negaPosiDic[y[1]] = y[0]
    return negaPosiDic

def enter_textctrl(event):
    s_text_6.Clear()
    if radio_box_1.GetSelection() == 1:
        input_textctrl = text_1.GetValue()
        output_textctrl = nlp(input_textctrl, -1)
        text_2.SetLabel(output_textctrl)
        text_1.Clear()
        print('a')
    elif radio_box_1.GetSelection() == 2:
        input_textctrl = text_1.GetValue()
        output_textctrl = nlp(input_textctrl, 1)
        text_2.SetLabel(output_textctrl)
        text_1.Clear()
        print('b')
    else:
        text_2.SetLabel(text_1.GetValue())
        text_1.Clear()
        print('c')

#GUI生成部分
application = wx.App()
frame = wx.Frame(None, wx.ID_ANY, '切り替え', size=(800, 400))

panel = wx.Panel(frame, wx.ID_ANY)



button_array = ('OFF', 'N → P', 'P → N')
radio_box_1 = wx.RadioBox(panel, 1, '切り替えスイッチ',choices=button_array, style=wx.RA_HORIZONTAL)


s_text_2 = wx.StaticText(panel, wx.ID_ANY, '文章を入力して下さい')
text_1 = wx.TextCtrl(panel, wx.ID_ANY, style=wx.TE_PROCESS_ENTER)
text_1.Bind(wx.EVT_TEXT_ENTER, enter_textctrl) #ボタンが押されたら，enter_textctrlを呼び出す
s_text_3 = wx.StaticText(panel, wx.ID_ANY, '　　　　　　　')
s_text_4 = wx.StaticText(panel, wx.ID_ANY, '出力文')
text_2 = wx.TextCtrl(panel, wx.ID_ANY)
s_text_5 = wx.StaticText(panel, wx.ID_ANY, '対義語切り替え不可リスト')
s_text_6 = wx.StaticText(panel, wx.ID_ANY, '')

layout = wx.BoxSizer(wx.VERTICAL)
layout.Add(radio_box_1, flag=wx.ALIGN_CENTER | wx.ALL, border=10)
layout.Add(s_text_2, flag=wx.ALIGN_LEFT | wx.LEFT, border=10)
layout.Add(text_1, flag=wx.EXPAND | wx.ALL,  border=10)
layout.Add(s_text_3, flag= wx.ALIGN_CENTER | wx.TOP,  border=10)
layout.Add(s_text_4, flag=wx.ALIGN_LEFT | wx.LEFT, border=10)
layout.Add(text_2, flag=wx.EXPAND | wx.ALL,  border=10)
layout.Add(s_text_5, flag=wx.ALIGN_LEFT | wx.LEFT, border=10)
layout.Add(s_text_6, flag=wx.ALIGN_LEFT | wx.LEFT, border=10)
panel.SetSizer(layout)

frame.Show()
application.MainLoop()
