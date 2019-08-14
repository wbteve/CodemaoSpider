import requests
import json
import os

try:
    error_code = '0'
    w_id = input('请输入作品ID：')
    error_code = '1'
###获取带有素材ID的BCMC文件###
    def download_bcmc(url):
        global name
        name = url.split('/')[-1]
    #    print(name)
        net_file = requests.get(url).content.decode()
        return net_file

    api = 'https://api.codemao.cn/tiger/work/source/public/'+w_id
    _json = requests.get(api).json()
    base_url = _json['source_urls'][0]
    #print(base_url)
    error_code = '2'
    print('BCMC文件获取成功！')

###从带有素材ID的BCMC文件中获取图片素材ID###
    bcmc = download_bcmc(base_url)
    bcmcjson=json.loads(bcmc)
    try:
        styles = bcmcjson['theatre']["styles"]
    except:
        styles = bcmcjson['resources']
    #print(styles)
    error_code = '3'
    print('图片素材ID获取成功！')

###从带有素材ID的BCMC文件中获取音乐素材ID###
    try:
        audio = bcmcjson['audio']
    except:
        pass
    error_code = '4'
    print('音乐素材ID获取成功')

    ###下载图片素材###
    print('开始下载图片！')
    path = os.getcwd()+'\\'+w_id
    if os.path.exists(path):
        pass
    else:
        os.mkdir(path)
    if os.path.exists(path +'\\图片\\'):
        pass
    else:
        os.mkdir(path +'\\图片\\')
    def download_image(url,path,name):
        image_name = name+'.jpg'
        with open(path +'\\图片\\'+image_name,'wb') as f:
            r = requests.get(url).content
            f.write(r)

    count_max = len(styles)
    count = 1

    try:
        for i in styles:
            #    print(styles[i]['url'])
            styles[i]['url']
            print('图片下载中({}/{})......'.format(str(count),str(count_max)))
            download_image(styles[i]['url'],path,styles[i]['name'])
            count+=1
    except:
        custom_sprites = styles['custom_sprites']
        count_max = 0
        for i in custom_sprites:
            count_max+=len(custom_sprites[i])
        for i in custom_sprites:
            for i1 in custom_sprites[i]:
                print('图片下载中({}/{})......'.format(str(count),str(count_max)))
                download_image(custom_sprites[i][i1]['img'],path,i1)
                count+=1
        print('开始下载背景！') #旧平台背景和角色图片是分开放的，这里要注意
        count_max = 0
        count = 1
        custom_scenes = styles['custom_scenes']
        for i in custom_scenes:
            count_max+=len(custom_scenes[i])
        for i in custom_scenes:
            for i1 in custom_scenes[i]:
                print('背景下载中({}/{})......'.format(str(count),str(count_max)))
                download_image(custom_scenes[i][i1]['img'],path,i1)
                count+=1
    error_code = '5'
###下载音乐素材###
    print('开始下载音乐！')
    if os.path.exists(path +'\\音乐\\'):
        pass
    else:
        os.mkdir(path +'\\音乐\\')
    def download_audio(url,path,name):
        audio_name = name +'.mp3'
        with open(path +'\\音乐\\'+audio_name,'wb') as f:
            r = requests.get(url).content
            f.write(r)
    try:
        count_max = len(audio)
        count = 1
        for i in audio:
            print('音乐下载中({}/{})......'.format(str(count),str(count_max)))
        #    print(audio[i]['url'])
            download_audio(audio[i]['url'],path,audio[i]['name'])
            count+=1
    except:
        audio = styles['custom_audio']
        count = 1
        count_max = 0
        for i in audio:
            count_max+=len(audio[i])
        for i in audio:
            for i1 in audio[i]:
                print('音乐下载中({}/{})......'.format(str(count),str(count_max)))
                download_audio(i1[1],path,i1[0])
    print('下载完毕！已保存至{}，欢迎下次使用！'.format(path))
###错误码解析###
except:
    print('错误！Error code:{}'.format(error_code))
    if error_code == '0':
    	print('请输入正确的ID！')
    elif error_code == '1':
    	print('BCMC文件获取失败,请输入正确的ID！')
    elif error_code == '2':
    	print('图片ID获取失败！')
    	print(bcmc)
    elif error_code == '3':
    	print('音乐ID获取失败！')
    elif error_code == '4':
    	print('图片下载失败，请检查网络设置！')
    elif error_code == '5':
    	print('音乐下载失败，请检查网络设置！')
