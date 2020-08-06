from selenium import webdriver
import re
import requests
from time import time

bro = webdriver.Chrome()

down_pos = "D://网易云/"  #下载位置
music_type = "(m4a|mp3)"    #识别的曲目扩展名（采用正则表达式语言，越多越好）
song_name = ['你若成风','萌二代']   #歌曲列表

def search_song(song_name,singer_name=''):
    global bro
    
    bro.get("https://music.163.com/#/search/m/?s="+song_name+"&type=1")
    bro.switch_to.frame("contentFrame")  #切换框架
    
    songlist_raw = bro.find_element_by_class_name("srchsongst").find_elements_by_class_name("text")   #歌曲列表对象（原始）
    
    songlist = []    #歌曲列表
    for song in songlist_raw:
        try:    #数据清洗：剔除错误音乐数据
            song_url = song.find_element_by_tag_name('a').get_attribute('href')  #歌曲信息获取
            song_name = song.find_element_by_tag_name('b').get_attribute('title')
            songlist.append([song_name,song_url])
        except:
            continue
    
    return songlist

'''song_info:歌曲信息列表([名称，地址])'''
def get_song(song_info):
    global bro,music_type
    
    bro.get(song_info[1])   #进入歌曲
    bro.switch_to.frame('contentFrame')
    
    '''音乐操作列表'''
    song_operation_raw = bro.find_element_by_id('content-operation').find_elements_by_tag_name('a')
    song_operation = {'播放':song_operation_raw[0]}   #操作集锦
    song_operation['播放'].click() #播放音乐
   
    '''获取音乐资源'''
    check_out = False
    while(True):
        log = bro.get_log('browser')
        starttime = time()
        for i in log:
            try:
                #print(i['message'])
                #print("\n\n")
                url = re.search(r'http.+\.'+music_type,i['message']).group(0)    #音乐地址
                check_out = True
                break
            except:
                if (time()-starttime >= 5):
                    raise Expection.NameError("获取资源链接超时")
                continue
        if (check_out == True):
            break
    return url

'''下载歌曲'''
'''目前采用requests库，下载效率较低'''
def download_song(name,url):
    global bro,down_pos

    r = requests.get(url,headers={'user-agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.163 Safari/535.1'})
    with open(down_pos+name+url[-4:],"wb") as f:
        f.write(r.content)
        print("下载完毕：",down_pos+name+url[-4:])
        

def main():
    global bro,song_name
    
    for name in song_name:   #多曲子
        while(True):    #防异常
            try:
                '''主程序'''
                song_list = search_song(name)
                url = get_song(song_list[0])
                print(url,"\n")
                #download_song(name,url)   #歌曲下载模块
                break
            except:
                continue

main()
    