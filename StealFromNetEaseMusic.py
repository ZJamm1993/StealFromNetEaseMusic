#coding=utf-8
import os
import urllib
import requests
import json
from Crypto.Cipher import AES
import base64
import md5

from mutagen.id3 import ID3, APIC, TIT2, TPE1, TALB

# first_param = "{rid:\"\", offset:\"0\", total:\"true\", limit:\"100\", csrf_token:\"\"}"
# first_param =  "{s:\"the best of me andrea\",type:10}"

myFilePath = "savedFiles"

iv = "0102030405060708"
nonce = "0CoJUm6Qyw8W8jud" #蜜钥？
publicKey = "010001"
modulus = "00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7"

def encodeParams(jsonstr):
    second_key = 16 * 'F'
    h_encText = AES_encrypt(jsonstr, nonce, iv)
    h_encText = AES_encrypt(h_encText, second_key, iv)
    return h_encText

def AES_encrypt(text, key, iv):
    pad = 16 - len(text) % 16
    text = text + pad * chr(pad)
    encryptor = AES.new(key, AES.MODE_CBC, iv)
    encrypt_text = encryptor.encrypt(text)
    encrypt_text = base64.b64encode(encrypt_text)
    return encrypt_text

# def AES_decrypt(text, key, iv):
#     encrypt_text = base64.b64decode(text)
#     pad = 16 - len(text) % 16
#     text = text[:-pad]
#     encryptor = AES.new(key, AES.MODE_CBC, iv)
#     encrypt_text = encryptor.decrypt(encrypt_text)
#     return encrypt_text

# def decodeParams(params):
#     second_key = 16 * 'F'
#     h_encText = AES_decrypt(params, second_key, iv)
#     h_encText = AES_decrypt(h_encText, nonce, iv)
#     return h_encText

def getJson(url, params):
    print '#####start networking'
    print url
    data = None
    if params:
        print params
        jsonStr = json.dumps(params)
        encodeP = encodeParams(jsonStr)
        data = {
            "params": encodeP,
            "encSecKey": "257348aecb5e556c066de214e531faadd1c55d814f9be95fd06d6bff9f4c7a41f831f6394d5a3fd2e3881736d94a02ca919d952872e7d0a50ebfa1769a7a62d512f5f1ca21aec60bc3819a9c3ffca5eca9a0dba6d6f7249b06f5965ecfff3695b54e1c28f3f624750ed39e7de08fc8493242e26dbc4484a01c76f739e135637c"
        }
        # print "post data:" + json.dumps(data)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0',
        'Referer': 'http://music.163.com/'
    }   
    response = requests.post(url, headers=headers, data=data)
    print '#####end networking'
    return response.content

def search(keyword,type):
    params = {
        # '''
        #     搜索类型；默认为 1 即单曲 , 取值意义 : 
        #     1: 单曲, 
        #     10: 专辑, 
        #     100: 歌手, 
        #     1000: 歌单, 
        #     1002: 用户, 
        #     1004: MV, 
        #     1006: 歌词, 
        #     1009: 电台, 
        #     1014: 视频
        # '''
        's':keyword,
        'type':type, 
        'offset':0
        # 'limit':100,
    }
    url = "http://music.163.com/weapi/search/get?csrf_token="
    return getJson(url,params)

def getAlbum(albumId): #217758
    # url = "http://music.163.com/weapi/v1/album/" + str(albumId)
    # params = {
    #     'csrf_token': ""
    # }
    # return getJson(url,params)
    url = "http://music.163.com/api/album/" + str(albumId)
    return getJson(url,None)
    # {
    # "code":200,
    # "album":{
    #     "songs":[
    #         {
    #             "starred":false,
    #             "popularity":5,
    #             "starredNum":0,
    #             "playedNum":0,
    #             "dayPlays":0,
    #             "hearTime":0,
    #             "mp3Url":"http://m2.music.126.net/hmZoNQaqzZALvVp0rE7faA==/0.mp3",
    #             "rtUrls":null,
    #             "status":0,
    #             "alias":[

    #             ],
    #             "hMusic":{
    #                 "bitrate":320000,
    #                 "playTime":254380,
    #                 "name":"",
    #                 "id":3428815307,
    #                 "size":10176305,
    #                 "extension":"mp3",
    #                 "volumeDelta":0,
    #                 "dfsId":0,
    #                 "sr":44100
    #             },

def getPlaylistDetail(playlistId): #971002652
    # url = 'http://music.163.com/eapi/v3/playlist/detail'
    # params = {
    #     'csrf_token':'',
    #     'n':100000,
    #     'id':playlistId,
    #     's':8
    # }
    # print params
    params = None
    url = "https://music.163.com/api/playlist/detail?id=%d"%playlistId
    return getJson(url,params)

def getSongDetail(songId): #2160833
    params = {
        'c':str([{'id':str(songId)}]),
        'ids':[str(songId)],
        'csrf_token':""
    }
    url = "http://music.163.com//weapi/v3/song/detail"
    return getJson(url,params)

def getSongUrl(songId):
    # params = None
    # url = "http://music.163.com/song/media/outer/url?id=%d.mp3"%songId
    # return url

    url = "http://music.163.com/weapi/song/enhance/player/url?csrf_token="
    params = {
        'ids':[songId],
        'br':"128000",
        'csrf_token':''
    }
    result = getJson(url,params)
    print result
    result = json.loads(result)
    mp3url = result['data'][0]['url']
    return mp3url
    # return getJson(url,params)

def encryptedSongId(id): #dfsId是很长的id，目前已消失
    byte1 = bytearray('3go8&$8*3*3h0k(2)2')
    byte2 = bytearray(id)
    byte1_len = len(byte1)
    for i in xrange(len(byte2)):
        byte2[i] = byte2[i]^byte1[i%byte1_len]
    m = md5.new()
    m.update(byte2)
    result = m.digest().encode('base64')[:-1]
    result = result.replace('/', '_')
    result = result.replace('+', '-')
    return result

def setSongInfo(songfilepath, songtitle, songartist, songalbum, songpicpath):
    songfilepath = myFilePath + "/" + songfilepath
    songpicpath = myFilePath + "/" + songpicpath
    audio = ID3(songfilepath)
    img = open(songpicpath,'r')
    audio.update_to_v23()
    audio['APIC'] = APIC(
                    encoding=3,
                    mime='image/jpeg',
                    type=3, 
                    desc=u'Cover',
                    data=img.read()
                )
    audio['TIT2'] = TIT2(
                    encoding=3,
                    text=[songtitle]
                )
    audio['TPE1'] = TPE1(
                    encoding=3,
                    text=[songartist]
                )
    audio['TALB'] = TALB(
                    encoding=3,
                    text=[songalbum]
                )
    audio.save()
    img.close()
    os.remove(songpicpath)

def downloadFile(source_url, save_path):
    #create dir if need
    if os.path.exists(myFilePath) == False:
        os.mkdir(myFilePath)

    save_path = myFilePath + "/" + save_path
    if os.path.exists(save_path):
        print "file exists, skipped : " + save_path
        return False

    print "downloading file...to " + save_path
    try:
        urllib.urlretrieve(source_url, save_path)
    except urllib.ContentTooShortError:
        print "failed saving: " + save_path
        os.remove(save_path)
        return False
    else:
        pass
    return True


if __name__ == "__main__":

# '''

    #download mp3 in playlist
    myplaylist = getPlaylistDetail(971002652)
    myplaylist = json.loads(myplaylist)
    tracks = myplaylist['result']['tracks']
    print "song count: " + str(len(tracks))

    count = 0
    for song in tracks:
    	s_name = song['name']
    	s_id = song['id']
    	s_artist = song['artists'][0]['name']
    	s_album = song['album']['name']
    	s_pic_url = song['album']['picUrl']
        s_mp3_url = getSongUrl(s_id)

    	print "<song: name: %s, artist: %s, album: %s pic: %s"%(s_name, s_artist, s_album, s_pic_url)

        songname = "%s - %s"%(s_name, s_artist)
        songname = songname.replace("/","")

        mp3filepath = songname + ".mp3"
        jpgfilepath = songname + ".jpg"

        downloadFile(s_mp3_url,mp3filepath)
        downloadFile(s_pic_url,jpgfilepath)
        setSongInfo(mp3filepath, s_name, s_artist, s_album, jpgfilepath)
        
# '''