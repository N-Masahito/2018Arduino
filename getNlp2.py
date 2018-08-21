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
    if event.GetId() == 1:
        s_text_6_1.SetLabel('')
        if radio_box_2.GetSelection() == 1:
            input_textctrl = text_1_1.GetValue()
            output_textctrl = nlp(input_textctrl, -1)
            text_2_2.SetLabel(output_textctrl)
            text_1_1.SetLabel(' ')
        elif radio_box_2.GetSelection() == 2:
            input_textctrl = text_1_1.GetValue()
            output_textctrl = nlp(input_textctrl, 1)
            text_2_2.SetLabel(output_textctrl)
            text_1_1.SetLabel(' ')
        else:
            text_2_2.SetLabel(text_1_1.GetValue())
            text_1_1.SetLabel(' ')
    elif event.GetId() == 2:
        s_text_6_2.SetLabel('')
        if radio_box_1.GetSelection() == 1:
            input_textctrl = text_1_2.GetValue()
            output_textctrl = nlp(input_textctrl, -1)
            text_2_1.SetLabel(output_textctrl)
            text_1_2.SetLabel(' ')
        elif radio_box_1.GetSelection() == 2:
            input_textctrl = text_1_2.GetValue()
            output_textctrl = nlp(input_textctrl, 1)
            text_2_1.SetLabel(output_textctrl)
            text_1_2.SetLabel(' ')
        else:
            text_2_1.SetLabel(text_1_2.GetValue())
            text_1_2.SetLabel(' ')


#GUI生成部分
application = wx.App()
frame1 = wx.Frame(None, wx.ID_ANY, 'さとみ', size=(600, 300))
frame2 = wx.Frame(None, wx.ID_ANY, 'なんば', size=(600, 300))

panel1 = wx.Panel(frame1, wx.ID_ANY)
panel2 = wx.Panel(frame2, wx.ID_ANY)


button_array = ('OFF', 'N → P', 'P → N')
radio_box_1 = wx.RadioBox(panel1, 1, '切り替えスイッチ',choices=button_array, style=wx.RA_HORIZONTAL)
radio_box_2 = wx.RadioBox(panel2, 2, '切り替えスイッチ',choices=button_array, style=wx.RA_HORIZONTAL)


s_text_2_1 = wx.StaticText(panel1, wx.ID_ANY, '送信文')
text_1_1 = wx.TextCtrl(panel1, 1, style=wx.TE_PROCESS_ENTER)

s_text_2_2 = wx.StaticText(panel2, wx.ID_ANY, '送信文')
text_1_2 = wx.TextCtrl(panel2, 2, style=wx.TE_PROCESS_ENTER)


text_1_1.Bind(wx.EVT_TEXT_ENTER, enter_textctrl) #ボタンが押されたら，enter_textctrlを呼び出す
s_text_3_1 = wx.StaticText(panel1, wx.ID_ANY, '　　　　　　')
s_text_4_1 = wx.StaticText(panel1, wx.ID_ANY, '受信文')
text_2_1 = wx.TextCtrl(panel1, 1)
s_text_5_1 = wx.StaticText(panel1, wx.ID_ANY, '対義語切り替え不可リスト')
s_text_6_1 = wx.StaticText(panel1, wx.ID_ANY, '')

text_1_2.Bind(wx.EVT_TEXT_ENTER, enter_textctrl) #ボタンが押されたら，enter_textctrlを呼び出す
s_text_3_2 = wx.StaticText(panel2, wx.ID_ANY, '　　　　　　')
s_text_4_2 = wx.StaticText(panel2, wx.ID_ANY, '受信文')
text_2_2 = wx.TextCtrl(panel2, 2)
s_text_5_2 = wx.StaticText(panel2, wx.ID_ANY, '対義語切り替え不可リスト')
s_text_6_2 = wx.StaticText(panel2, wx.ID_ANY, '')

layout1 = wx.BoxSizer(wx.VERTICAL)
layout1.Add(s_text_2_1, flag=wx.ALIGN_LEFT | wx.LEFT, border=10)
layout1.Add(text_1_1, flag=wx.EXPAND | wx.ALL,  border=10)
layout1.Add(s_text_3_1, flag= wx.ALIGN_CENTER | wx.TOP,  border=0)
layout1.Add(s_text_4_1, flag=wx.ALIGN_LEFT | wx.LEFT, border=10)
layout1.Add(radio_box_1, flag=wx.ALIGN_LEFT | wx.BOTTOM, border=0)
layout1.Add(text_2_1, flag=wx.EXPAND | wx.ALL,  border=10)
layout1.Add(s_text_5_1, flag=wx.ALIGN_LEFT | wx.LEFT, border=10)
layout1.Add(s_text_6_1, flag=wx.ALIGN_LEFT | wx.LEFT, border=10)
panel1.SetSizer(layout1)

layout2 = wx.BoxSizer(wx.VERTICAL)
layout2.Add(s_text_2_2, flag=wx.ALIGN_LEFT | wx.LEFT, border=10)
layout2.Add(text_1_2, flag=wx.EXPAND | wx.ALL,  border=10)
layout2.Add(s_text_3_2, flag= wx.ALIGN_CENTER | wx.TOP,  border=0)
layout2.Add(s_text_4_2, flag=wx.ALIGN_LEFT | wx.LEFT, border=10)
layout2.Add(radio_box_2, flag=wx.ALIGN_LEFT | wx.BOTTOM, border=0)
layout2.Add(text_2_2, flag=wx.EXPAND | wx.ALL,  border=10)
layout2.Add(s_text_5_2, flag=wx.ALIGN_LEFT | wx.LEFT, border=10)
layout2.Add(s_text_6_2, flag=wx.ALIGN_LEFT | wx.LEFT, border=10)
panel2.SetSizer(layout2)

frame1.Show()
frame2.Show()
application.MainLoop()
