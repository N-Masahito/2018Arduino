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

def nlp(data):
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
            if word_toarray[7] in negaposi_dic and int(negaposi_dic[word_toarray[7]]) < 0:
                url = "https://thesaurus.weblio.jp/antonym/content/{0}".format(word_toarray[7])
                driver.get(url)
                result += driver.find_element_by_class_name('wtghtAntnm').text
                else:
                    result += word_toarray[7]
    return result

def getNegaPosiDic():
    with codecs.open(os.path.join(__location__, "./dataset/yougen.csv"), 'r', 'utf-8') as f_in:
        reader = csv.reader(f_in, delimiter=',', lineterminator='\n')
        negaPosiDic = {}
        for i, x in enumerate(reader):
            y = x[0].split(" ")
            negaPosiDic[y[1]] = y[0]
    with codecs.open(os.path.join(__location__, "./dataset/noun.csv"), 'r', 'utf-8') as f_in:
        reader = csv.reader(f_in, delimiter=',', lineterminator='\n')
        for i, x in enumerate(reader):
            y = x[0].split(" ")
            negaPosiDic[y[1]] = y[0]
    return negaPosiDic

def click_togglebutton(event):
    if t_button.GetValue() == True:
        t_button.SetLabel('ON!')
    else:
        t_button.SetLabel('OFF')

def enter_textctrl(event):
    if t_button.GetValue() == True:
        input_textctrl = text_1.GetValue()
        output_textctrl = nlp(input_textctrl)
        text_2.SetLabel(output_textctrl)
        s_text_3.SetLabel('切り替え完了！')
    else:
        text_2.SetLabel(text_1.GetValue())
        s_text_3.SetLabel('切り替えＯＦＦ')

#GUI生成部分
application = wx.App()
frame = wx.Frame(None, wx.ID_ANY, 'ネガポジ切り替え', size=(800, 400))

panel = wx.Panel(frame, wx.ID_ANY)

s_text_1 = wx.StaticText(panel, wx.ID_ANY, 'スイッチ')
t_button = wx.ToggleButton(panel, wx.ID_ANY, 'OFF')
t_button.SetValue(False)

t_button.Bind(wx.EVT_TOGGLEBUTTON, click_togglebutton) #ボタンが押されたら，click_togglebuttonを呼び出す
s_text_2 = wx.StaticText(panel, wx.ID_ANY, '文章を入力して下さい')
text_1 = wx.TextCtrl(panel, wx.ID_ANY, style=wx.TE_PROCESS_ENTER)
text_1.Bind(wx.EVT_TEXT_ENTER, enter_textctrl) #ボタンが押されたら，enter_textctrlを呼び出す
s_text_3 = wx.StaticText(panel, wx.ID_ANY, '　　　　　　　')
s_text_4 = wx.StaticText(panel, wx.ID_ANY, '出力文')
text_2 = wx.TextCtrl(panel, wx.ID_ANY)

layout = wx.BoxSizer(wx.VERTICAL)
layout.Add(s_text_1, flag=wx.ALIGN_CENTER | wx.TOP,  border=10)
layout.Add(t_button, flag=wx.ALIGN_CENTER | wx.BOTTOM, border=10)
layout.Add(s_text_2, flag=wx.ALIGN_LEFT | wx.LEFT, border=10)
layout.Add(text_1, flag=wx.EXPAND | wx.ALL,  border=10)
layout.Add(s_text_3, flag= wx.ALIGN_CENTER | wx.TOP,  border=10)
layout.Add(s_text_4, flag=wx.ALIGN_LEFT | wx.LEFT, border=10)
layout.Add(text_2, flag=wx.EXPAND | wx.ALL,  border=10)
panel.SetSizer(layout)

frame.Show()
application.MainLoop()
