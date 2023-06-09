# -*- coding: utf-8 -*-
from Plugins.Extensions.IPTVPlayer.tools.iptvtools import printDBG
from Plugins.Extensions.IPTVPlayer.libs import ph
from Plugins.Extensions.IPTVPlayer.tsiplayer.libs.tstools import TSCBaseHostClass,tscolor,tshost

import re

def getinfo():
    info_={}
    name='Shahid4u'
    hst = 'http://ishahed4u.vip/'
    info_['old_host'] = hst
    hst_ = tshost(name)	
    if hst_!='': hst = hst_
    info_['host']= hst
    info_['name']=name
    info_['version']='2.1 18/07/2022'        
    info_['dev']='Tsiplayer'
    info_['cat_id']='21'
    info_['desc']='أفلام و مسلسلات عربية و اجنبية'
    info_['icon']='https://i.ibb.co/gtSXrs2/shahid4u.png'
    info_['recherche_all']='1'
    #info_['update']='change to ww.shahid4u.net'	

    return info_
    
class TSIPHost(TSCBaseHostClass):
    
    def __init__(self):
        TSCBaseHostClass.__init__(self,{})
        self.MAIN_URL = getinfo()['host']

    def showmenu(self,cItem):
        TAB = [('افلام','/category/افلام/','10',0),('مسلسلات','/category/مسلسلات/','10',1),('برامج تليفزيونية','/category/برامج-تلفزيونية/','20',''),('عروض مصارعة','/category/عروض-مصارعة/','20',''),
        ('NETFlIX','/netflix/','20','')]
        self.add_menu(cItem,'','','','','',TAB=TAB,search=True)

    def showfilter(self,cItem):
        count=cItem.get('count',1)
        data1=cItem.get('data','none')	
        codeold=cItem.get('code',self.MAIN_URL+'/getposts?')	
        if count==1:
            sts, data = self.getPage(self.MAIN_URL)
            if sts:
                data1=re.findall('dropdown select-menu">.*?<ul(.*?)</ul>', data, re.S)
            else:
                data1='' 
        if count==4:
            mode_='20' 
        else:
            mode_='19'
        lst_data1 = re.findall('<li.*?data-tax="(.*?)".*?data-cat="(.*?)".*?bold">(.*?)<',data1[count-1], re.S)	
        for (x1,x2,x3) in lst_data1:
            code=codeold+x1+'='+x2+'&'
            self.addDir({'import':cItem['import'],'category' :'host2', 'url':code, 'title':x3, 'desc':x1, 'icon':cItem['icon'], 'mode':mode_,'count':count+1,'data':data1,'code':code, 'sub_mode':'item_filter','page':-1})					

    def showmenu1(self,cItem):
        self.add_menu(cItem,'<ul class="sub-menu">(.*?)</ul','<li.*?href="(.*?)".*?>(.*?)<','','20',ind_0=cItem['sub_mode'])
        if cItem.get('sub_mode',2)==1:
            self.addDir({'import':cItem['import'],'category' :'host2', 'url': self.MAIN_URL + '/category/%d9%85%d8%b3%d9%84%d8%b3%d9%84%d8%a7%d8%aa-%d8%b9%d8%b1%d8%a8%d9%8a/', 'title':'مسلسلات عربي', 'desc':'', 'icon':cItem['icon'], 'mode':'20'})					
            self.addDir({'import':cItem['import'],'category' :'host2', 'url':'/category/رمضان-2022/', 'title':'رمضان 2022', 'desc':'', 'icon':cItem['icon'], 'mode':'20'})					 
        elif cItem.get('sub_mode',2)==0:
            self.addDir({'import':cItem['import'],'category' :'host2', 'url': self.MAIN_URL + '/category/%D8%A7%D9%81%D9%84%D8%A7%D9%85-%D8%B9%D8%B1%D8%A8%D9%8A/', 'title':'افلام عربي', 'desc':'', 'icon':cItem['icon'], 'mode':'20'})					

    def showitms(self,cItem):
        desc = [('Genre','class="genres">(.*?)</div>','',''),('IMDB','rate ti-star">(.*?)</span>','',''),('Quality','class="quality".*?>(.*?)</span>','','')]
        next = ['<link rel="next".*?href="(.*?)"','20']
        self.add_menu(cItem,'','class="content-box">.*?href="(.*?)".*?title="(.*?)".*?(?:data-image|data-src)="(.*?)".*?<(.*?)</h3>','','21',ord=[0,1,2,3],Desc=desc,Next=next,u_titre=True,EPG=True)		

    def showelms(self,cItem):
        desc = [('Story','post-story">(.*?)</div>','','')]
        self.addVideo({'import':cItem['import'], 'hst':'tshost', 'url':cItem['url'], 'title':'--> '+cItem['title']+' <--', 'desc':cItem['desc'], 'icon':cItem['icon']})
        self.add_menu(cItem,'','class="episode-block">.*?href="(.*?)".*?title="(.*?)".*?(?:src="|image=")(.*?)"','','video',ord=[0,1,2],u_titre=True,EPG=True,Desc=desc,add_vid=False)		
        self.add_menu(cItem,'tab-class" id="seasons">(.*?)<div class="tags','content-box">.*?href="(.*?)".*?title="(.*?)".*?image="(.*?)"','','21',ord=[0,1,2],Titre='Seasons',u_titre=False,EPG=True)		   
        

    def SearchResult(self,str_ch,page,extra):
        url = self.MAIN_URL+'/page/'+str(page)+'/?s='+str_ch
        desc = [('Genre','class="genres">(.*?)</div>','',''),('IMDB','rate ti-star">(.*?)</span>','',''),('Quality','class="quality".*?>(.*?)</span>','','')]
        self.add_menu({'import':extra,'url':url},'','class="content-box">.*?href="(.*?)".*?title="(.*?)".*?data-image="(.*?)".*?<(.*?)</h3>','','21',ord=[0,1,2,3],Desc=desc,u_titre=True,EPG=True)		
        

    def get_links(self,cItem): 	
        urlTab = []	
        url_origin=cItem['url']
        #URL=url_origin.replace('/episode/','/watch/')
        #URL=URL.replace('/film/','/watch/')
        #URL=URL.replace('/post/','/watch/')
        URL = url_origin + 'watch/'
        sts, data = self.getPage(URL)
        if sts:
            server_data = re.findall('<ul class="servers-list">(.*?)</ul>', data, re.S)
            if server_data:
                code_data = re.findall('<li.*?data-i="(.*?)".*?data-id="(.*?)".*?>(.*?)</li', server_data[0], re.S)
                for (i,id_,titre_) in code_data:
                        local = ''
                        if 'السيرفر الخاص' in titre_:
                            titre_ = '|Shahid4U| Local (Oktube)'
                            local = 'local'                        
                        urlTab.append({'name':self.cleanHtmlStr(titre_).strip(), 'url':'hst#tshost#'+i+'|'+id_, 'need_resolve':1, 'type':local})




        #URL=url_origin.replace('/episode/','/download/')
        #URL=URL.replace('/film/','/download/')
        #URL=URL.replace('/post/','/download/')
        URL = url_origin + 'download/'
        sts, data = self.getPage(URL)
        if sts:
            server_data = re.findall('postId:"(.*?)"', data, re.S)
            if server_data:
                url_=self.MAIN_URL+'/ajaxCenter?_action=getdownloadlinks&postId='+server_data[0]
                HTTP_HEADER= {'X-Requested-With':'XMLHttpRequest','Referer':url_origin}
                sts, data_ = self.getPage(url_,{'header':HTTP_HEADER})
                server_data = re.findall('<a href="(.*?)"', str(data_), re.S)
                for (url_1) in server_data:
                    hostUrl=url_1.replace("www.", "")				
                    raw1 =  re.findall('//(.*?)/', hostUrl, re.S)
                    if raw1:				
                        hostUrl=raw1[0]
                    if ('openload' in hostUrl.lower())or('uptobox' in hostUrl.lower()):
                        urlTab.append({'name':hostUrl+' - سرفر تحميل', 'url':url_1, 'need_resolve':1})
            else:
                #code_data = re.findall('class="" data-order="(.*?)" data-embedd="(.*?)">.*?alt="(.*?)"', data, re.S)
                code_data = re.findall('data-embedd="(.*?)".*?alt="(.*?)"', data, re.S)
                
                id_data = re.findall("attr\('data-embedd'\).*?url: \"(.*?)\"", data, re.S)
                if id_data:
                    for (code_,titre_) in code_data:
                        url=id_data[0]+'&serverid='+code_
                        local = ''
                        if 'السيرفر الخاص' in titre_:
                            titre_ = '|Shahid4U| Local (Oktube)'
                            local = 'local'
                        urlTab.append({'name':titre_+'*', 'url':'hst#tshost#'+url, 'need_resolve':1,type:local})		
        return urlTab
         
    def getVideos(self,videoUrl):
        urlTab = []	
        i,id_ = videoUrl.split('|',1)
        HTTP_HEADER= { 'X-Requested-With':'XMLHttpRequest','Referer':self.MAIN_URL }
        post_data = {'i':i,'id':id_}
        post_url = self.MAIN_URL+"/wp-content/themes/Shahid4u/Ajaxat/Single/Server.php"
        sts, data = self.getPage(post_url,{'header':HTTP_HEADER},post_data=post_data)
        if sts:
            printDBG('Data='+data)
            _data2 = re.findall('<iframe.*?(src|SRC)=(.*?) ',data, re.S) 
            if _data2:
                URL_=_data2[0][1]
                URL_=URL_.replace('"','')
                URL_=URL_.replace("'",'')
                if URL_.startswith('//'):
                    URL_='http:'+URL_ 
                urlTab.append((URL_,'1'))
            else:
                data=data.strip()
                if data.startswith('http'):
                    urlTab.append((data,'1'))					
        return urlTab
        
    def getArticle(self, cItem):
        printDBG("Arablionz.getVideoLinks [%s]" % cItem) 
        otherInfo1 = {}
        desc = cItem['desc']
        sts, data = self.getPage(cItem['url'])
        if sts:
            lst_dat=re.findall('class="half-tags">.*?<li>(.*?)</li>(.*?)</ul>', data, re.S)
            for (x1,x2) in lst_dat:
                if 'الجودة' in x1: otherInfo1['quality'] = ph.clean_html(x2)
                if 'السنة' in x1: otherInfo1['year'] = ph.clean_html(x2)
                if 'النوع' in x1: otherInfo1['genres'] = ph.clean_html(x2)			
                if 'ممثلين' in x1: otherInfo1['actors'] = ph.clean_html(x2)
                if 'القسم' in x1: otherInfo1['category'] = ph.clean_html(x2)
                if 'مخرج' in x1: otherInfo1['director'] = ph.clean_html(x2)			
                if 'لمؤلف' in x1: otherInfo1['writer'] = ph.clean_html(x2)            
            lst_dat0=re.findall('post-story">(.*?)</div>', data, re.S)
            if lst_dat0: desc = ph.clean_html(lst_dat0[0])
            else: desc = cItem['desc']
        icon = cItem.get('icon')
        title = cItem['title']				
        return [{'title':title, 'text': desc, 'images':[{'title':'', 'url':icon}], 'other_info':otherInfo1}]


