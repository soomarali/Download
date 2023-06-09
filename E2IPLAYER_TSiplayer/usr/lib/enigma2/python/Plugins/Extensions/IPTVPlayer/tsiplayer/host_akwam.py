# -*- coding: utf-8 -*-
from Plugins.Extensions.IPTVPlayer.tools.iptvtools import printDBG,MergeDicts
from Plugins.Extensions.IPTVPlayer.libs import ph
from Plugins.Extensions.IPTVPlayer.components.iptvplayerinit import GetIPTVSleep
from Plugins.Extensions.IPTVPlayer.tools.iptvtypes import strwithmeta
from Plugins.Extensions.IPTVPlayer.libs.e2ijson import loads as json_loads
from Plugins.Extensions.IPTVPlayer.tsiplayer.libs.tstools import TSCBaseHostClass,gethostname,tscolor,tshost
from Plugins.Extensions.IPTVPlayer.tsiplayer.libs.urlparser    import urlparser as ts_urlparser
from Plugins.Extensions.IPTVPlayer.components.recaptcha_v2helper import CaptchaHelper
try:
    from Plugins.Extensions.IPTVPlayer.tsiplayer.libs.vstream.requestHandler import cRequestHandler
    from Plugins.Extensions.IPTVPlayer.tsiplayer.libs.vstream.config import GestionCookie
except:
    pass 
    
import re
from Plugins.Extensions.IPTVPlayer.tsiplayer.libs.utils import Quote
import time


###################################################
#01# HOST https://akoam.net
###################################################	
def getinfo():
    info_={}
    name = 'Akwam (New)'
    hst = 'https://five.ak4ar.fun'
    info_['old_host'] = hst
    hst_ = tshost(name)	
    if hst_!='': hst = hst_
    info_['host']= hst
    info_['name']=name
    info_['version']='2.0 18/07/2022'    
    info_['dev']='RGYSoft'
    info_['cat_id']='21'
    info_['desc']='أفلام, مسلسلات و انمي عربية و اجنبية'
    info_['icon']='https://i.ibb.co/0qgtD2Z/akwam.png'
    info_['recherche_all']='1'
    #info_['update']='Fix Links Extract'
    return info_
    
    
class TSIPHost(TSCBaseHostClass, CaptchaHelper):
    def __init__(self):
        TSCBaseHostClass.__init__(self,{'cookie':'akwam2.cookie'})
        self.USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0'
        self.MAIN_URL = getinfo()['host']
        self.HEADER = {'User-Agent': self.USER_AGENT, 'DNT':'1', 'Accept': 'text/html', 'Accept-Encoding':'gzip, deflate','Referer':self.getMainUrl(), 'Origin':self.getMainUrl()}
        self.AJAX_HEADER = MergeDicts(self.HEADER, {'X-Requested-With': 'XMLHttpRequest', 'Accept-Encoding':'gzip, deflate', 'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8', 'Accept':'application/json, text/javascript, */*; q=0.01'})
        self.defaultParams = {'header':self.HEADER,'no_redirection':True,'with_metadata':True, 'use_cookie': True, 'load_cookie': True, 'save_cookie': True, 'cookiefile': self.COOKIE_FILE}
        self.cacheLinks = {}
        #self.getPage = self.cm.getPage


    def getPage1(self,baseUrl, addParams = {}, post_data = None):
        baseUrl = self.std_url(baseUrl)
        baseUrl = re.sub('(akwam\..{2,4}?)/', self.MAIN_URL.replace('https://','')+'/', baseUrl)
        i=0
        while True:
            printDBG('count='+str(i))
            if addParams == {}: addParams = dict(self.defaultParams)
            #origBaseUrl = baseUrl
            #baseUrl = self.cm.iriToUri(baseUrl)
            addParams['cloudflare_params'] = {'cookie_file':self.COOKIE_FILE, 'User-Agent':self.USER_AGENT}
            sts, data = self.cm.getPageCFProtection(baseUrl, addParams, post_data)
            if sts:
                break
            else:
                i=i+1
                if i>2: break
        return sts, data


    def getPage(self, baseUrl, addParams = {}, post_data = None):
        baseUrl=self.std_url(baseUrl)
        if addParams == {}: addParams = dict(self.defaultParams)
        sts,data = self.cm.getPage(baseUrl, addParams, post_data)
        printDBG(str(data.meta))
        code = data.meta.get('status_code','')  
        while ((code == 302) or (code == 301)):
            new_url = data.meta.get('location','')
            if not new_url.startswith('http'):
                new_url = self.MAIN_URL + new_url
            new_url=self.std_url(new_url)
            sts,data = self.cm.getPage(new_url, addParams, post_data)
            code = data.meta.get('status_code','')
            printDBG(str(data.meta))
        return sts, data
        
    def showmenu0(self,cItem):
        self.addDir({'import':cItem['import'],'category' :'host2','title':'أفلام'   ,'icon':cItem['icon'],'mode':'20','sub_mode':0,'url':self.MAIN_URL+'/movies'})
        self.addDir({'import':cItem['import'],'category' :'host2','title':'مسلسلات' ,'icon':cItem['icon'],'mode':'20','sub_mode':1,'url':self.MAIN_URL+'/series'})	
        self.addDir({'import':cItem['import'],'category' :'host2','title':'تلفزيون'  ,'icon':cItem['icon'],'mode':'20','sub_mode':2,'url':self.MAIN_URL+'/shows'})
#		self.addDir({'import':cItem['import'],'category' :'host2','title':'المميزة'  ,'icon':cItem['icon'],'url':self.MAIN_URL,'mode':'21'})	
        self.addDir({'import':cItem['import'],'category' :'host2','title':'منوعات'  ,'icon':cItem['icon'],'url':self.MAIN_URL+'/shows','mode':'30'})	
        self.addDir({'import':cItem['import'],'category' :'search','title':tscolor('\c00????30') + _('Search'),'search_item':True,'page':1,'hst':'tshost','icon':cItem['icon']})

    def showmenu1(self,cItem):
        sub_mode=cItem.get('sub_mode', 0)
        if False:
            sts, data = self.getPage(self.MAIN_URL)
            if sts:
                lst_data = re.findall('class="menu">(.*?)</div>',data, re.S)
                if  lst_data:
                    lst_data1 = re.findall('<a.*?href="(.*?)".*?>(.*?)<',lst_data[sub_mode], re.S)
                    for (url,titre) in lst_data1:
                        self.addDir({'import':cItem['import'],'category' : 'host2','title':cItem['title'] +' | '+ titre,'url':url,'desc':'','icon':cItem['icon'],'mode':'30'})		
        self.addDir({'import':cItem['import'],'category' : 'host2','title':'ALL','url':cItem['url'],'desc':'','icon':cItem['icon'],'mode':'30'})
        self.addDir({'import':cItem['import'],'category' : 'host2','title':'By Filtre','desc':'','icon':cItem['icon'],'mode':'22','sub_mode':sub_mode})		
        if sub_mode==1:        
            self.addDir({'category': 'host2', 'title': tscolor('\c00????30')+'Ramadan 2022', 'url': self.MAIN_URL+'/series?section=0&category=87&rating=0&year=2022&language=0&formats=0&quality=0', 'mode': '30','import':cItem['import'], 'icon': cItem['icon'], 'type': 'category', 'desc': ''})
            self.addDir({'category': 'host2', 'title': 'Ramadan 2021', 'url': self.MAIN_URL+'/series?section=0&category=87&rating=0&year=202&language=0&formats=0&quality=0', 'mode': '30','import':cItem['import'], 'icon': cItem['icon'], 'type': 'category', 'desc': ''})
            
    def showfilter(self,cItem):
        count=cItem.get('count',0)
        data=cItem.get('data',[])
        total = cItem.get('total',0)
        url=cItem.get('url','')
        sub_mode=cItem.get('sub_mode', 0)
        car='&'
        if count==0:
            car='?'
            if sub_mode==0: url= self.MAIN_URL+'/movies'
            elif sub_mode==1: url= self.MAIN_URL+'/series'
            elif sub_mode==2: url= self.MAIN_URL+'/shows'	
            sts, data0 = self.getPage(url)
            if sts:
                films_list = re.findall('<select.*?name="(.*?)".*?value="(.*?)".*?>(.*?)<(.*?)</select>', data0, re.S)
                if films_list:
                    data = films_list
                    total = len(data) 
        if data != []:
            name  = data[count][0]
            code  = data[count][1]
            titre = data[count][2]
            elms  = data[count][3]
            self.addMarker({'title':tscolor('\c0000??00')+titre,'desc':'','icon':cItem['icon']})
            op_list = re.findall('<option(.*?)>(.*?)</option>', elms, re.S)
            mode = '22'
            printDBG('count='+str(count))
            printDBG('total='+str(total))
            if count+1==total: mode = '30'
            self.addDir({'import':cItem['import'],'count':count+1,'data':data,'category' : 'host2','url': url+car+name+'=0','title':'All','desc':'','icon':cItem['icon'],'hst':'tshost','mode':mode,'total':total})	
            for (val,option) in op_list:
                val_list = re.findall('"(.*?)"', val, re.S)
                if val_list: valeur = val_list[0]
                else: valeur=option
                urlo=url+car+name+'='+valeur
                self.addDir({'import':cItem['import'],'count':count+1,'data':data,'category' : 'host2','url': urlo,'title':option,'desc':'','icon':cItem['icon'],'hst':'tshost','mode':mode,'total':total})	

    def showmenu2(self,cItem):
        sub_mode=cItem.get('sub_mode', '0')
        url0=cItem['url']	
        titre0=cItem['title']
        self.addDir({'import':cItem['import'],'category' : 'host2','title':' الكل - '+titre0,'url':url0,'desc':'','icon':cItem['icon'],'mode':'30'})
                            
        sts, data = self.getPage(url0)
        if sts:
            lst_data = re.findall('لأقسام الفرعية</span>(.*?)</ul>',data, re.S)
            if  lst_data:
                lst_data1 = re.findall('href="(.*?)">(.*?)<',lst_data[0], re.S)
                for (url,titre) in lst_data1:
                    self.addDir({'import':cItem['import'],'category' : 'host2','title':titre,'url':url,'desc':'','icon':cItem['icon'],'mode':'30'})

    def showitms(self,cItem):
        #printDBG('citem='+str(cItem))
        page = cItem.get('page', 1)
        if page==1: Url = cItem['url']
        else:
            if '?' in cItem['url']:
                Url = cItem['url']+'&page='+str(page)
            else:
                Url = cItem['url']+'?page='+str(page)
        if Url.startswith('/'): Url = self.MAIN_URL + Url
        sts, data = self.getPage(Url)
        if sts:
            lst_data=re.findall('class="entry-box.*?>(.*?)-src="(.*?)".*?href="(.*?)".*?<h3.*?>(.*?)</h3>', data, re.S)
            count=0			
            for (desc,image,url,titre) in lst_data:
                rating = ''
                quality = ''
                lst_inf=re.findall('rating">(.*?)</span>', desc, re.S)
                if lst_inf: rating = ph.clean_html(lst_inf[0])
                lst_inf=re.findall('quality">(.*?)</span>', desc, re.S)
                if lst_inf: quality = ph.clean_html(lst_inf[0])				
                desc = tscolor('\c0000????')+'Rating: '+tscolor('\c00??????')+rating+'\n'
                desc = desc + tscolor('\c0000????')+'Quality: '+tscolor('\c00??????')+quality+'\n'
                titre=self.cleanHtmlStr(titre)
                self.addDir({'import':cItem['import'],'category' : 'host2','title':titre,'url':url,'desc':desc,'icon':image,'mode':'31','good_for_fav':True,'EPG':True,'hst':'tshost'})
                count=count+1
            if count>1:	
                self.addDir({'import':cItem['import'],'category' : 'host2','title':'Page Suivante','url':cItem['url'],'page':page+1,'mode':'30'})

    def showelms(self,cItem):
        url0=cItem['url']	
        sts, data = self.getPage(url0)
        if sts:
            trailer_data=re.findall('youtube.com/watch.v=(.*?)["\']', data, re.S)
            if trailer_data:
                self.addVideo({'category' : 'host2','title':'TRAILER','url':'https://www.youtube.com/watch?v='+trailer_data[0],'desc':'','icon':cItem['icon'],'hst':'none'})	
            if 'id="downloads">' in data:
                self.addVideo({'import':cItem['import'],'category' : 'host2','title':cItem['title'].replace(tscolor('\c0000??00')+ '[New Site] '+tscolor('\c00??????'),''),'url':cItem['url'],'desc':cItem['desc'],'icon':cItem['icon'],'hst':'tshost','good_for_fav':True})				
            else:
                lst_data=re.findall('class="bg-primary2.*?href="(.*?)".*?>(.*?)</a>(.*?)<img.*?"(.*?)"', data, re.S)			
                if lst_data:
                    for (url,titre1,inf,image) in lst_data:
                        self.addVideo({'import':cItem['import'],'category' : 'host2','title':titre1,'url':url,'desc':ph.clean_html(inf),'icon':image,'hst':'tshost','good_for_fav':True})				

    def SearchResult(self,str_ch,page,extra):
        elms = []        
        url_=self.MAIN_URL+'/search?q='+str_ch+'&page='+str(page)
        sts, data = self.getPage(url_)
        if sts:
            lst_data=re.findall('class="entry-box.*?>(.*?)data-src="(.*?)".*?href="(.*?)".*?<h3.*?>(.*?)</h3>', data, re.S)		
            for (desc,image,url,titre) in lst_data:
                rating = ''
                quality = ''
                lst_inf=re.findall('rating">(.*?)</span>', desc, re.S)
                if lst_inf: rating = ph.clean_html(lst_inf[0])
                lst_inf=re.findall('quality">(.*?)</span>', desc, re.S)
                if lst_inf: quality = ph.clean_html(lst_inf[0])				
                desc = tscolor('\c0000????')+'Rating: '+tscolor('\c00??????')+rating+'\n'
                desc = desc + tscolor('\c0000????')+'Quality: '+tscolor('\c00??????')+quality+'\n'
                titre=self.cleanHtmlStr(titre)
                elm = {'import':extra,'category' : 'host2','title':titre,'url':url,'desc':desc,'icon':image,'mode':'31','good_for_fav':True,'EPG':True,'hst':'tshost'}
                elms.append(elm)
                self.addDir(elm)
        return elms

    def MediaBoxResult(self,str_ch,year_,extra):
        urltab=[]
        str_ch_o = str_ch
        str_ch = Quote(str_ch_o+' '+year_)
        result = self.SearchResult(str_ch,1,'')
        if result ==[]:
            str_ch = Quote(str_ch_o)
            result = self.SearchResult(str_ch,1,'')
        for elm in result:
            titre     = elm['title']
            url       = elm['url']
            desc      = elm.get('desc','')
            image     = elm.get('icon','')
            mode      = elm.get('mode','') 
            if str_ch_o.lower().replace(' ','') == titre.replace('-',' ').replace(':',' ').lower().replace(' ',''):
                trouver = True
            else:
                trouver = False
            name_eng='|'+tscolor('\c0060??60')+'Akwam (NEW)'+tscolor('\c00??????')+'| '+titre				
            element = {'titre':titre,'import':extra,'good_for_fav':True,'EPG':True, 'hst':'tshost', 'category':'host2', 'url':url, 'title':name_eng, 'desc':desc, 'icon':image, 'mode':mode}
            if trouver:
                urltab.insert(0, element)					
            else:
                urltab.append(element)	
        return urltab	 
        
    def get_links(self,cItem): 	
        urlTab = []
        URL=cItem['url']
        urlTab = self.cacheLinks.get(URL, [])
        if urlTab == []:
            sts, data = self.getPage(URL)
            if sts:
                url_dat_1=re.findall('<ul class="header-tabs(.*?)</ul>', data, re.S)		
                if url_dat_1: url_dat_1=re.findall('<li.*?>(.*?)</li>', url_dat_1[0], re.S)
                url_dat_2=re.findall('class="tab-content.*?href="(.*?)".*?href="(.*?)"', data, re.S)			
                titre='[ '
                for x in url_dat_1:
                    titre = titre + ph.clean_html(x) +' \ '
                titre = titre[:-2]+']'
                if url_dat_2:
                    urlTab.append({'name':'|Watch Server| '+titre, 'url':'hst#tshost#'+url_dat_2[0][0], 'need_resolve':1,'type':"local"})
                    i=0
                    for elm in url_dat_2:
                        titre =  ph.clean_html(url_dat_1[i])
                        urlTab.append({'name':'|Downl Server| '+titre, 'url':'hst#tshost#'+elm[1], 'need_resolve':1,'type':"local"})
                        i=i+1
            self.cacheLinks[str(cItem['url'])] = urlTab
        return urlTab	

    def get_links1(self,cItem): 	
        urlTab = []
        URL=cItem['url']
        urlTab = self.cacheLinks.get(URL, [])
        if urlTab == []:
            sts, data = self.getPage(URL)
            if sts:
                url_dat_1=re.findall('<ul class="header-tabs(.*?)</ul>', data, re.S)		
                if url_dat_1: url_dat_1=re.findall('<li.*?>(.*?)</li>', url_dat_1[0], re.S)
                url_dat_2=re.findall('class="tab-content.*?href="(.*?)"', data, re.S)			
                if (url_dat_1 and url_dat_2) and (len(url_dat_1) == len(url_dat_2)):
                    for (x,y) in zip(url_dat_1,url_dat_2):
                        titre = ph.clean_html(x)
                        urlTab.append({'name':'|Watch Server| '+titre, 'url':'hst#tshost#'+y, 'need_resolve':1,'type':"local"})
                        urlTab.append({'name':'|Downl Server| '+titre, 'url':'hst#tshost#'+y.replace('/watch/','/download/'), 'need_resolve':1,'type':"local"})
                        #break #a revoir
            self.cacheLinks[str(cItem['url'])] = urlTab
        return urlTab	


    def getVideos1(self,videoUrl):
        urlTab = []	
        if True:
            sts, data = self.getPage(videoUrl)
            if sts:
                url_dat=re.findall('<h2.*?href="(.*?)"', data, re.S)
                if url_dat:
                    url = url_dat[0]
                    if url.startswith('http'): sts, data = self.getPage(url)
                    if sts:
                        #printDBG('data='+data)
                        url_dat=re.findall('</video>.*?class="container">.*?href="(.*?)"', data, re.S)
                        if url_dat:	
                            URL_= url_dat[0].replace('vlc://','')							
                            urlTab.append((URL_,'0'))
                        else:
                            url_dat=re.findall('class="btn-loader">.*?href="(.*?)"', data, re.S)
                            if url_dat:
                                URL_= url_dat[0]
                                
                                urlTab.append((URL_,'0'))							
        return urlTab

    def extract_links(self,data,videoUrl):
        urlTab=[]
        url_dat=re.findall('<source.*?src=["\'](.*?)["\'].*?size=["\'](.*?)["\']', data, re.S)
        if url_dat:
            for url,size in url_dat:
                URL_ = strwithmeta(size+'P|'+url,{'Referer':videoUrl})
                urlTab.append((URL_,'4'))
        else:
            url_dat=re.findall('class="btn-loader">.*?href="(.*?)"', data, re.S)
            if url_dat:
                URL_= strwithmeta(url_dat[0],{'Referer':videoUrl})					
                urlTab.append((URL_,'0'))
        printDBG('Links='+str(urlTab))
        
        return urlTab
    
    def getVideos(self,videoUrl):
        urlTab = []	
        if True:
            sts, data = self.getPage(videoUrl)
            if sts:
                urlTab = self.extract_links(data,videoUrl)
                if urlTab == []:    
                    url_dat=re.findall('<div class="content.*?href="(.*?)"(.*?)(?:<center>|</body>)', data, re.S)
                    if url_dat:
                        url1 = url_dat[0][0]
                        data2 = url_dat[0][1]
                        url_dat2=re.findall('<a href="(.*?)"', data2, re.S)
                        if url_dat2:
                            url1 = url_dat2[-1]
                    if not url_dat:
                        url_dat=re.findall('<h2.*?href="(.*?)"', data, re.S)
                        url1 = url_dat[0]
                    if url_dat:
                        sts, data = self.getPage(url1)
                        if sts:
                            #printDBG('data='+data)
                            sitekey = self.cm.ph.getSearchGroups(data, '''data\-sitekey=['"]([^'^"]+?)['"]''')[0]
                            if sitekey != '':
                                printDBG('sitekey='+sitekey)
                                token, errorMsgTab = self.processCaptcha(sitekey, self.cm.meta['url'])
                                post_data = {}
                                if token != '':
                                    post_data['g-recaptcha-response'] = token
                                    actionUrl = self.MAIN_URL+'/verify'
                                    sts0, data0 = self.getPage(actionUrl, post_data=post_data)
                                    GetIPTVSleep().Sleep(1)
                                    sts, data = self.getPage(url1)
                            if sts:
                                urlTab = self.extract_links(data,videoUrl)		
        return urlTab
        
    def getArticle(self,cItem):
        printDBG("AkoAm.getVideoLinks [%s]" % cItem) 
        otherInfo1 = {}
        title = cItem['title']
        icon = cItem.get('icon','')
        desc = cItem.get('desc','')
        sts, data = self.getPage(cItem['url'])
        if sts:
            lst_dat=re.findall('class="font-size-16 text-white mt-2">(.*?)</span>', data, re.S)
            for elm in lst_dat:
                elm = ph.clean_html(elm)
                if (':' in elm) and ('مدة' in elm): otherInfo1['duration'] = elm.split(':',1)[1].strip()
                elif (':' in elm) and ('اللغة' in elm): otherInfo1['language'] = elm.split(':',1)[1].strip()
                elif (':' in elm) and ('ترجمة' in elm): otherInfo1['translation'] = elm.split(':',1)[1].strip()
                elif (':' in elm) and ('جودة' in elm): otherInfo1['quality'] = elm.split(':',1)[1].strip()
                elif (':' in elm) and ('انتاج' in elm): otherInfo1['production'] = elm.split(':',1)[1].strip()	
                elif (':' in elm) and ('سنة' in elm): otherInfo1['year'] = elm.split(':',1)[1].strip()
                
            lst_dat0=re.findall('class="font-size-16 d-flex align-items-center mt-3">(.*?)</div>', data, re.S)
            if lst_dat0: otherInfo1['genre'] = ph.clean_html(lst_dat0[0])

            lst_dat0=re.findall('header-link text-white">.*?<h2>(.*?)</div>', data, re.S)	
            if lst_dat0: desc = ph.clean_html(lst_dat0[0])
        
        return [{'title':title, 'text': desc, 'images':[{'title':'', 'url':icon}], 'other_info':otherInfo1}]

            
    def start(self,cItem):      
        mode=cItem.get('mode', None)
        if mode=='00':
            self.showmenu0(cItem)
        if mode=='20':
            self.showmenu1(cItem)
        if mode=='21':
            self.showmenu2(cItem)
        if mode=='22':
            self.showfilter(cItem)
        if mode=='30':
            self.showitms(cItem)
        if mode=='31':
            self.showelms(cItem)				
        return True




























