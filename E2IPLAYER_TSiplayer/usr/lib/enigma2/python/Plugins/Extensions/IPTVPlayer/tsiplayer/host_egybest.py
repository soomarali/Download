# -*- coding: utf-8 -*-
from Plugins.Extensions.IPTVPlayer.tools.iptvtools import printDBG,GetCookieDir
from Plugins.Extensions.IPTVPlayer.libs import ph
from Plugins.Extensions.IPTVPlayer.tools.iptvtypes import strwithmeta
from Plugins.Extensions.IPTVPlayer.tsiplayer.libs.tstools import TSCBaseHostClass,tscolor,tshost,VidStream,atob
from Components.config import config
from Plugins.Extensions.IPTVPlayer.tools.e2ijs import js_execute
import base64
import re
import urllib
from Plugins.Extensions.IPTVPlayer.components.iptvplayerinit import GetIPTVSleep
from Plugins.Extensions.IPTVPlayer.libs.urlparserhelper            import getDirectM3U8Playlist
from Plugins.Extensions.IPTVPlayer.libs.urlparser import urlparser
from Plugins.Extensions.IPTVPlayer.tsiplayer.libs.utils import string_escape

def getinfo():
    info_={}
    name = 'Egy.Best'
    hst = 'https://egybest.tech'
    info_['old_host'] = hst
    hst_ = tshost(name)	
    if hst_!='': hst = hst_
    info_['host']= hst
    info_['name']=name
    info_['version']='2.0 18/07/2022'        
    info_['dev']='RGYSoft | Thx to >> @maxbambi & @zadmario <<'
    info_['cat_id']='21'
    info_['desc']='أفلام عربية و اجنبية + مسلسلات اجنبية'
    info_['icon']='https://i.ibb.co/z2SXTd8/souayah-Egy-Best-film.png'
    info_['recherche_all']='1'
    #info_['update']='Fix Vidstream Server'
        
    return info_
    
    
class TSIPHost(TSCBaseHostClass):
    def __init__(self):
        TSCBaseHostClass.__init__(self,{'cookie':'egybest007.cookie'})
        self.USER_AGENT = 'Mozilla/5.0 (Linux; Android 7.0; PLUS Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.98 Mobile Safari/537.36'
        self.MAIN_URL =  getinfo()['host']
        self.VID_URL  = 'https://vidstream.kim'
        self.varconst = 'a0'
        self.SiteName   = 'EgyBest'
        self.HTTP_HEADER = {'User-Agent': self.USER_AGENT, 'DNT':'1', 'Accept': 'text/html', 'Accept-Encoding':'gzip, deflate', 'Referer':self.getMainUrl(), 'Origin':self.getMainUrl()}
        self.AJAX_HEADER = dict(self.HTTP_HEADER)
        self.AJAX_HEADER.update( {'X-Requested-With': 'XMLHttpRequest', 'Accept-Encoding':'gzip, deflate', 'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8', 'Accept':'application/json, text/javascript, */*; q=0.01'} )
        self.defaultParams = {'header':self.HTTP_HEADER, 'with_metadata':True,'no_redirection':True, 'use_cookie': True, 'load_cookie': True, 'save_cookie': True, 'cookiefile': self.COOKIE_FILE}

    def getPage(self, baseUrl, addParams = {}, post_data = None):
        if addParams == {}: addParams = dict(self.defaultParams)
        addParams['cloudflare_params'] = {'cookie_file':self.COOKIE_FILE, 'User-Agent':self.USER_AGENT}
        i=0
        data=''
        while ((len(str(data))<20) and (i<4)):
            sts,data = self.cm.getPageCFProtection(baseUrl, addParams, post_data)
            i=i+1
        return sts,data

    def showmenu0(self,cItem):
        hst='host2'
        img=cItem['icon']	
        Cimaclub_TAB=[{'category':hst,'title': 'Films'    ,'mode':'20'  ,'icon':img ,'sub_mode':'film'},
                    {'category':hst,'title': 'Series'   ,'mode':'20' ,'icon':img ,'sub_mode':'serie'},
                    {'category':hst,'title': 'Animes'   ,'mode':'20' ,'icon':img ,'sub_mode':'anime'},                    
                    {'category':'search'  ,'title': _('Search'),'search_item':True,'page':1,'hst':'tshost','icon':img},
                    ]
        self.listsTab(Cimaclub_TAB, {'import':cItem['import'],'name':hst})
        #self.addDir({'import':cItem['import'], 'name':'categories', 'category':hst, 'url':'https://wilo.egybest.xyz/movie/gemini-man-2019/?ref=movies-p1', 'title':'Test Link', 'desc':'','hst':'tshost', 'icon':'', 'mode':'31'} )							
        
        
    def showmenu1(self,cItem):
        base=self.MAIN_URL
        gnr2=cItem['sub_mode']
        hst='host2'
        img=cItem['icon']			 
        url=self.MAIN_URL+'/'
        sts1, data = self.getPage(url)
                
        if gnr2=='film':
            sts, data2 = self.getPage(self.MAIN_URL+'/movies/')
            if sts:
                lst_data1 = re.findall('<div class="sub_nav">(.*?)<div id="movies',data2, re.S)
                if  lst_data1:
                    self.addDir({'import':cItem['import'],'name':'categories', 'category' :'host2', 'url':'', 'title':'\c00????00'+'By Filter', 'desc':'', 'icon':img, 'mode':'21', 'count':1,'data':lst_data1[0],'code':'','type_':'movies'})						
        
            self.addMarker({'title':'\c0000??00Main','icon':'','desc':''})				
            egy_films=[ {'title': 'أفلام جديدة'       , 'url':self.MAIN_URL+'/movies/'      , 'mode':'30', 'page':1},						  
                        {'title': 'احدث الاضافات'     , 'url':self.MAIN_URL+'/movies/latest' , 'mode':'30', 'page':1},						  
                        {'title': 'أفضل الافلام', 'url':self.MAIN_URL+'/movies/top'  , 'mode':'30', 'page':1},						  
                        {'title': 'الاكثر شهرة' , 'url':self.MAIN_URL+'/movies/popular' , 'mode':'30', 'page':1},
                        ]							
            self.listsTab(egy_films, {'import':cItem['import'],'name':'categories', 'category':hst, 'desc':'', 'icon':img})		
            self.addMarker({'title':'\c0000??00Trendinge','icon':'','desc':''})				
            egy_films=[ {'title': 'الاكثر مشاهدة الان'       , 'url':self.MAIN_URL+'/trending/'      , 'mode':'30', 'page':1},						  
                        {'title': 'الاكثر مشاهدة اليوم'     , 'url':self.MAIN_URL+'/trending/today' , 'mode':'30', 'page':1},						  
                        {'title': 'الاكثر مشاهدة هذا الاسبوع', 'url':self.MAIN_URL+'/trending/week'  , 'mode':'30', 'page':1},						  
                        {'title': 'الاكثر مشاهدة هذا الشهر' , 'url':self.MAIN_URL+'/trending/month' , 'mode':'30', 'page':1},						  
                        ]
            self.listsTab(egy_films, {'import':cItem['import'],'name':'categories', 'category':hst, 'desc':'', 'icon':img})
            if sts1:
                self.addMarker({'title':'\c0000??00Genre','icon':'','desc':''})					
                lst_data1 = re.findall('mgb table full">.*?href="(.*?)">(.*?)<.*?td">.*?href="(.*?)">(.*?)<',data, re.S)
                i=0
                for (url1,titre1,url2,titre2) in lst_data1:
                    if i<10:
                        self.addDir({'import':cItem['import'],'name':'categories', 'category' :hst, 'url':url1, 'title':titre1, 'desc':titre1, 'icon':img, 'mode':'30', 'page':1})				
                        self.addDir({'import':cItem['import'],'name':'categories', 'category' :hst, 'url':url2, 'title':titre2, 'desc':titre2, 'icon':img, 'mode':'30', 'page':1})
                        i=i+1
            
 
        if gnr2=='serie':
            sts, data2 = self.getPage(self.MAIN_URL+'/tv/')
            if sts:
                lst_data1 = re.findall('<div class="sub_nav">(.*?)<div id="movies',data2, re.S)
                if  lst_data1:
                    self.addDir({'import':cItem['import'],'name':'categories', 'category' :hst, 'url':'', 'title':'\c00????00'+'By Filter', 'desc':'', 'icon':img, 'mode':'21', 'count':1,'data':lst_data1[0],'code':'','type_':'tv'})						
        
            self.addMarker({'title':'\c0000??00Main','icon':'','desc':''})				
            egy_films=[ {'title': 'احدث الحلقات'  , 'url':self.MAIN_URL+'/tv/'            , 'mode':'30', 'page':1},						  
                        {'title': 'مسلسلات جديدة'  , 'url':self.MAIN_URL+'/tv/new'         , 'mode':'30', 'page':1},						  
                        {'title': 'أفضل المسلسلات' , 'url':self.MAIN_URL+'/tv/top'         , 'mode':'30', 'page':1},						  
                        {'title': 'الاكثر شهرة'    , 'url':self.MAIN_URL+'/tv/popular'     , 'mode':'30', 'page':1},	
                        {'title': 'رمضان 2022'    , 'url':self.MAIN_URL+'/ramadan-2022/'  , 'mode':'30', 'page':1},	
                        ]
            self.listsTab(egy_films, {'import':cItem['import'],'name':'categories', 'category':hst, 'desc':'', 'icon':img})				

        if gnr2=='anime':
            sts, data2 = self.getPage(self.MAIN_URL+'/animes/')
            if sts:
                lst_data1 = re.findall('<div class="sub_nav">(.*?)<div id="movies',data2, re.S)
                if  lst_data1:
                    self.addDir({'import':cItem['import'],'name':'categories', 'category' :hst, 'url':'', 'title':'\c00????00'+'By Filter', 'desc':'', 'icon':img, 'mode':'21', 'count':1,'data':lst_data1[0],'code':'','type_':'animes'})						
        
            self.addMarker({'title':'\c0000??00Main','icon':'','desc':''})				
            egy_films=[ {'title': 'احدث الحلقات'  , 'url':self.MAIN_URL+'/animes/'        , 'mode':'30', 'page':1},						  
                        {'title': 'مسلسلات جديدة'  , 'url':self.MAIN_URL+'/animes/new'     , 'mode':'30', 'page':1},						  
                        {'title': 'أفضل المسلسلات' , 'url':self.MAIN_URL+'/animes/top'     , 'mode':'30', 'page':1},						  
                        {'title': 'الاكثر شهرة'    , 'url':self.MAIN_URL+'/animes/popular' , 'mode':'30', 'page':1},	
                        ]
            self.listsTab(egy_films, {'import':cItem['import'],'name':'categories', 'category':hst, 'desc':'', 'icon':img})	
    def showmenu2(self,cItem):	
        hst='host2'
        img=cItem['icon']	
        count=cItem['count']
        data=cItem['data']	
        codeold=cItem['code']	
        type_=cItem['type_']			
        lst_data1 = re.findall('class="dropdown">(.*?)</div></div>',data, re.S)	
        if lst_data1:
            data2=lst_data1[count-1]
            if count==7:
                url=self.MAIN_URL+'/'+type_+'/'+codeold
                self.addDir({'import':cItem['import'],'name':'categories', 'category' :hst, 'url':url, 'title':'الكل', 'desc':codeold, 'icon':img, 'mode':'30', 'page':1})					
            else:
                self.addDir({'import':cItem['import'],'name':'categories', 'category' :hst, 'url':'', 'title':'الكل', 'desc':codeold, 'icon':img, 'mode':'21', 'count':count+1,'data':data,'code':codeold,'type_':type_})
            lst_data2 = re.findall('href=".*?'+type_+'/(.*?)".*?>(.*?)<',data2, re.S)					
            for (code,titre) in lst_data2:
                if codeold!='':
                    code = codeold+'-'+code
                if count==7:
                    url=self.MAIN_URL+'/'+type_+'/'+code
                    self.addDir({'import':cItem['import'],'name':'categories', 'category' :hst, 'url':url, 'title':titre, 'desc':code, 'icon':img, 'mode':'30', 'page':1})					
                else:	
                    self.addDir({'import':cItem['import'],'name':'categories', 'category' :hst, 'url':'', 'title':titre, 'desc':code, 'icon':img, 'mode':'21', 'count':count+1,'data':data,'code':code,'type_':type_})
        
    def showitms(self,cItem):
        hst='host2'
        img=cItem['icon']	
        base=self.MAIN_URL
        page=cItem.get('page',1)
        url0=cItem['url']
        if url0.startswith('/'):
            url0 = self.MAIN_URL+url0
        url=url0+'?page='+str(page)+'&output_format=json&output_mode=movies_list'
        sts, data = self.getPage(url)
        if sts:
            data=data.replace('\\"','"')	
            data=data.replace('\\/','/')				
            lst_data=re.findall('<a href="(.*?)"(.*?)src="(.*?)".*?title">(.*?)<.*?ribbon.*?<span>(.*?)<', data, re.S)			
            for (url1,rate,image,name_eng,qual) in lst_data:
                lst_data0=re.findall('rating">(.*?)</i>', rate, re.S)
                if lst_data0: rate=lst_data0[0]
                else: rate = ''
                desc=tscolor('\c00????00')+'Rating: '+tscolor('\c00??????')+self.cleanHtmlStr(rate)+'/10 | '+tscolor('\c00????00')+'Qual: '+tscolor('\c00??????')+qual
                #x1,titre=self.uniform_titre(str(name_eng.decode('unicode_escape')))
                x1,titre=self.uniform_titre(string_escape(str(name_eng)))
                titre=titre.replace('()','')
                self.addDir({'import':cItem['import'],'good_for_fav':True, 'name':'categories', 'category':hst, 'url':base+url1, 'title':titre, 'desc':desc,'EPG':True,'hst':'tshost', 'icon':image, 'mode':'31'} )							
            self.addDir({'import':cItem['import'],'name':'categories', 'category':hst, 'url':url0, 'title':tscolor('\c0090??20')+_('Next page'), 'page':page+1, 'desc':'', 'icon':img, 'mode':'30'})	

    def showelems(self,cItem):
        desc=''
        base=self.MAIN_URL
        
        img=cItem['icon']
        url0=cItem['url']
        if not url0.startswith('http'): url0 = self.MAIN_URL+url0	
        titre=cItem['title']
        titre=titre.replace('|'+tscolor('\c0060??60')+'EgyBest'+tscolor('\c00??????')+'| ','') #for mediabox
        sts, data = self.getPage(url0)
        if sts:
            desc=''
            tmp  = self.cm.ph.getDataBeetwenNodes(data, ('<div', '>', 'full_movie'), ('</table', '>'), False)[1]
            keysMap = {'اللغة • البلد'            :'Country: ',
                       'التصنيف'                  :'Type: ',
                       'النوع'                    :'Genres: ', 
                       'التقييم العالمي'          :'Rating: ',
                       'المدة'                    :'Duration: ',
                       'الجودة'                   :'Quality: ',
                       'الترجمة'                  :'Translation: '}

            tmp = self.cm.ph.getAllItemsBeetwenMarkers(tmp, '<tr>', '</tr>')
            for item in tmp:
                item = item.split('</td>', 1)
                if len(item) != 2: continue
                keyMarker = ph.clean_html(item[0]).replace(':', '').strip()
                printDBG("+++ keyMarker[%s]" % keyMarker)
                value = ph.clean_html(item[1]).replace(' , ', ', ')
                key = keysMap.get(keyMarker, '')
                if key != '' and value != '': desc = desc+tscolor('\c00????00')+key+tscolor('\c00??????')+value	+' | '	
            
            
        
                
            cat_data0=re.findall('القصة</strong>.*?<div.*?">(.*?)</div>', data, re.S)
            if cat_data0:
                desc1=cat_data0[0]
                desc=desc+'\n'+tscolor('\c00????00')+'Info: '+tscolor('\c0000????')+self.cleanHtmlStr(desc1)
                                
            cat_data2=re.findall('<div id="yt_trailer".*?url="(.*?)".*?src="(.*?)"', data, re.S)
            for (URl,IMg) in cat_data2:					
                self.addVideo({'import':cItem['import'],'good_for_fav':True,'name':'categories','category' : 'video','url': URl,'title':'Trailer','desc':desc,'icon':IMg,'hst':'none'})						
                            
            if (('/series/' in url0) or ('/season/' in url0) or ('/anime/' in url0) ):			
                if ('/season/' in url0) and ('<table dir=' in data):
                    cat_data=re.findall('<table dir=(.*?)</table>', data, re.S)
                else:
                    cat_data=re.findall('movies_small">(.*?)</div>', data, re.S)	
                if cat_data:
                    if 'class="ep_title">' not in cat_data[0]:
                        el_data=re.findall('<a href="(.*?)".*?src="(.*?)".*?title">(.*?)<', cat_data[0], re.S)
                        for (url1,image,name_eng) in el_data:					
                            self.addDir({'import':cItem['import'],'good_for_fav':True, 'name':'categories', 'category':'host2', 'url':url1, 'title':self.cleanHtmlStr(name_eng.strip()), 'desc':desc, 'icon':img, 'mode':'31'} )							
                    else:
                        el_data=re.findall('<a href="(.*?)".*?ep_num">(.*?)<.*?>(.*?)</td>', cat_data[0], re.S)
                        for (url1,ep,name) in el_data:					
                            self.addDir({'import':cItem['import'],'good_for_fav':True, 'name':'categories', 'category':'host2', 'url':url1, 'title':self.cleanHtmlStr(ep.strip()) +' - ' + self.cleanHtmlStr(name.strip()), 'desc':desc, 'icon':img, 'mode':'31'} )							      
            elif ('/episode/' in url0):
                self.addVideo({'import':cItem['import'],'good_for_fav':True,'name':'categories','category' : 'video','url': url0,'title':titre,'desc':desc,'icon':img,'hst':'tshost'})			
                self.addMarker({'title':'\c0000??00' + 'جميع الحلقات','icon':'','desc':''})
                cat_data=re.findall('movies_small">(.*?)</div>', data, re.S)
                if cat_data:
                    el_data=re.findall('<a href="(.*?)".*?src="(.*?)".*?title">(.*?)<', cat_data[0], re.S)
                    for (url1,image,name_eng) in el_data:
                        if (self.cleanHtmlStr(name_eng.strip()) != ''):
                            self.addDir({'import':cItem['import'],'good_for_fav':True, 'name':'categories', 'category':'host2', 'url':url1, 'title':self.cleanHtmlStr(name_eng.strip()), 'desc':desc, 'icon':img, 'mode':'31'} )							
            else:
                self.addVideo({'import':cItem['import'],'good_for_fav':True,'name':'categories','category' : 'video','url': url0,'title':titre,'desc':desc,'icon':img,'hst':'tshost'})			
        
        
        
    def SearchResult(self,str_ch,page,extra):
        elms = []
        printDBG('extra='+extra)
        url_=self.MAIN_URL+'/explore/?page='+str(page)+'&output_format=json&q='+str_ch+'&output_mode=movies_list'
        url_=self.std_url(url_)
        sts, data = self.getPage(url_)	
        if sts:
            data=data.replace('\\"','"')	
            data=data.replace('\\/','/')				
            printDBG('data = '+data+'#')
            lst_data=re.findall('<a href="(.*?)"(.*?)src="(.*?)".*?title">(.*?)<.*?ribbon.*?<span>(.*?)<', data, re.S)			
            for (url1,rate,image,name_eng,qual) in lst_data:
                #desc='Rating:'+self.cleanHtmlStr(rate)+'  Qual:'+qual
                printDBG('name_eng = '+name_eng+'#')
                lstr_data=re.findall('rating">(.*?)</i>', rate, re.S)
                if lstr_data: rate= lstr_data[0]
                else: rate = '?'
                desc=tscolor('\c00????00')+'Rating: '+tscolor('\c00??????')+self.cleanHtmlStr(rate)+'/10 | '+tscolor('\c00????00')+'Qual: '+tscolor('\c00??????')+qual
                x1,titre=self.uniform_titre(str(name_eng.decode('unicode_escape')),1)
                desc = x1+desc
                titre=titre.replace('()','')				
                if 'series/' in url1: titre=titre+ tscolor('\c00????00')+' (SERIE)'
                if 'anime/' in url1: titre=titre+ tscolor('\c00????00')+' (ANIME)'
                url1=self.MAIN_URL+url1
                #url1=url1.replace('best//','best/')
                elm = {'import':extra,'good_for_fav':True,'EPG':True, 'name':'categories', 'category':'host2', 'url':url1, 'title':titre, 'desc':desc, 'icon':image, 'mode':'31','hst':'tshost'}
                self.addDir(elm)
                elms.append(elm)
        return elms       



    def MediaBoxResult1(self,str_ch,year_,extra):
        urltab=[]
        str_ch_o = str_ch
        str_ch = urllib.quote(str_ch_o+' '+year_)
        trouver=False
        i=1
        while (not trouver) and (i<3):
            url_=self.MAIN_URL+'/explore/?page='+str(i)+'&output_format=json&q='+str_ch+'&output_mode=movies_list'
            sts, data = self.getPage(url_)	
            if sts:
                data=data.replace('\\"','"')	
                data=data.replace('\\/','/')				
                lst_data=re.findall('<a href="(.*?)".*?rating">(.*?)</i>.*?src="(.*?)".*?title">(.*?)<.*?ribbon.*?<span>(.*?)<', data, re.S)			
                for (url1,rate,image,name_eng,qual) in lst_data:
                    desc=tscolor('\c00????00')+'Rating: '+tscolor('\c00??????')+self.cleanHtmlStr(rate)+'/10 | '+tscolor('\c00????00')+'Qual: '+tscolor('\c00??????')+qual
                    x1,titre0=self.uniform_titre(str(name_eng.decode('unicode_escape')),year_op=2)
                    desc=x1.replace('\n','')+' | '+desc			
                    if 'series/' in url1: titre=titre0+ tscolor('\c00????00')+'(SERIE)'
                    else: titre=titre0
                    url1=self.MAIN_URL+url1
                    titre_='|'+tscolor('\c0060??60')+'EgyBest'+tscolor('\c00??????')+'| '+titre
                    printDBG('star compart:'+titre+':'+x1+' vs '+year_+':'+str_ch_o)
                    if (titre.replace('-',' ').replace(':',' ').replace('.',' ').lower().replace(' ','') == str_ch_o.lower().replace(' ','')) and (x1==year_):
                        urltab.insert(0,{'titre':titre0,'import':extra,'good_for_fav':True,'EPG':True, 'name':'categories', 'category':'host2', 'url':url1, 'title':titre_, 'desc':desc, 'icon':image, 'mode':'31','hst':'tshost'} )							
                        trouver=True
                        break
                    else:
                        urltab.append({'titre':titre0,'import':extra,'good_for_fav':True,'EPG':True, 'name':'categories', 'category':'host2', 'url':url1, 'title':titre_, 'desc':desc, 'icon':image, 'mode':'31','hst':'tshost'} )							
            i=i+1
        
        return urltab

        
    def get_links(self,cItem): 			
        urlTab = []
        URL=cItem['url']
        printDBG(' ----------> Link='+URL)	
        sts, data = self.getPage(URL)
        if sts:
            Liste_els0 = re.findall('<iframe.*?src="(.*?)"', data, re.S)
            if Liste_els0:			
                urlTab.append({'name':'|HLS| Vidstream', 'url':'hst#tshost#'+Liste_els0[0], 'need_resolve':1,'type':'local'})
            if False:
                Liste_els2 = re.findall('=\[\'([0-9a-zA-Z]{1,40})\'\]', data, re.S)            
                Liste_els0 = re.findall('<table(.*?)</table>', data, re.S)
                if (Liste_els0 and Liste_els2):
                    code = Liste_els2[0]
                    Liste_els1 = re.findall('<tr>.*?<td>(.*?)<td class.*?url="(.*?)"', Liste_els0[-1], re.S)
                    for (titre,url) in Liste_els1:
                        urlTab.append({'name':'|'+ph.clean_html(titre)+'| Vidstream', 'url':'hst#tshost#'+url+'&v=1'+'%%%'+cItem['url']+'%%%'+code, 'need_resolve':1,'type':'local'})
                
        return urlTab

         
    def getVideos(self,videoUrl):
        HTTP_HEADER= {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0',
                      'Accept': 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                      'Accept-Encoding':'gzip, deflate'
                     }
        
        http_params={'header':HTTP_HEADER, 'with_metadata':True, 'cookiefile':self.COOKIE_FILE, 'use_cookie': True, 'load_cookie': True, 'save_cookie': True}

        printDBG(' -----------> URL = '+videoUrl)
        urlTab = []	
        referer = self.MAIN_URL
        if '%%%' in videoUrl: videoUrl,referer,code = videoUrl.split('%%%',2)
        if not videoUrl.startswith('http'): videoUrl=self.MAIN_URL+videoUrl
        if 'watch/?v' in videoUrl:
            #try:
            printDBG('try resolve url0: '+videoUrl)
            urlTab = self.parserVIDSTREAM(videoUrl,'egy')
            #except Exception as e:
            #printDBG('ERREUR:'+str(e))
        else:
            addParams0 = dict(self.defaultParams)
            addParams0['header']['Referer']=referer
            http_params['header']['Referer']=referer
            sts, data = self.cm.getPage(self.MAIN_URL+'/'+atob(code),http_params)
            printDBG('data_meta0='+str(data.meta))
            GetIPTVSleep().Sleep(5)
            sts, data = self.cm.getPage(videoUrl,http_params)
            if sts:
                printDBG('data='+str(data))
                printDBG('data_meta1='+str(data.meta))
                
                if False:
                    URL = data.meta['location']
                    VID_URL = urlparser.getDomain(URL, onlyDomain=False)
                    if VID_URL.endswith('/'): VID_URL = VID_URL[:-1]
                    self.VID_URL = VID_URL
                    printDBG('HOST vstream = '+self.VID_URL)
                    try:				
                        printDBG('try resolve url1: '+URL)
                        urlTab = self.parserVIDSTREAM(URL)
                    except Exception as e:
                        printDBG('ERREUR:'+str(e))				     
        return urlTab	 							
        
    def getArticle(self, cItem):
        printDBG("EgyBest.getArticleContent [%s]" % cItem)
        desc = ''
        retTab = []
        otherInfo = {}
        sts, data = self.getPage(cItem['url'])
        if sts:
            desc = ph.clean_html(self.cm.ph.getDataBeetwenNodes(data, ('<strong', '</div>', 'القصة'), ('</div', '>'), False)[1])
            tmp  = self.cm.ph.getDataBeetwenNodes(data, ('<div', '>', 'full_movie'), ('</table', '>'), False)[1]
            icon  = self.cm.ph.getDataBeetwenNodes(tmp, ('<div', '>', 'movie_img'), ('</div', '>'), False)[1]
            icon  = self.getFullIconUrl(self.cm.ph.getSearchGroups(icon, '''src=['"]([^'^"]+?)['"]''')[0])
            title = ph.clean_html(self.cm.ph.getDataBeetwenNodes(tmp, ('<div', '>', 'movie_title'), ('</div', '>'), False)[1])

            keysMap = {'اللغة • البلد'            :'country',
                       'التصنيف'                  :'type',
                       'النوع'                    :'genres', 
                       'التقييم العالمي'          :'rating',
                       'المدة'                    :'duration',
                       'الجودة'                   :'quality',
                       'الترجمة'                  :'translation'}

            tmp = self.cm.ph.getAllItemsBeetwenMarkers(tmp, '<tr>', '</tr>')
            for item in tmp:
                item = item.split('</td>', 1)
                if len(item) != 2: continue
                keyMarker = ph.clean_html(item[0]).replace(':', '').strip()
                printDBG("+++ keyMarker[%s]" % keyMarker)
                value = ph.clean_html(item[1]).replace(' , ', ', ')
                key = keysMap.get(keyMarker, '')
                if key != '' and value != '': otherInfo[key] = value

            # actors
            tTab = []
            tmp = self.cm.ph.getAllItemsBeetwenNodes(data, ('<div', '>', 'cast_item'), ('</span', '>'))
            for t in tmp:
                t = ph.clean_html(t)
                if t != '': tTab.append(t)
            if len(tTab): otherInfo['actors'] = ', '.join(tTab)

        title = cItem['title']
        if desc == '':  desc = cItem.get('desc', '')
        cItem.get('icon', '')

        return [{'title':ph.clean_html( title ), 'text': ph.clean_html( desc ), 'images':[{'title':'', 'url':self.getFullUrl(icon)}], 'other_info':otherInfo}]

    
    def start(self,cItem):      
        mode=cItem.get('mode', None)
        if mode=='00':
            self.showmenu0(cItem)
        if mode=='20':
            self.showmenu1(cItem)
        if mode=='21':
            self.showmenu2(cItem)
        if mode=='30':
            self.showitms(cItem)			
        if mode=='31':
            self.showelems(cItem)

    def parserVIDSTREAM(self, url,hst='vidstream'):
        if hst=='vidstream':
            COOKIE_FILE = GetCookieDir('vidstream55.cookie')
            main_url=self.VID_URL
        else:
            COOKIE_FILE = self.COOKIE_FILE
            main_url=self.MAIN_URL	
        printDBG('parserVIDSTREAM_Tsiplayer_egybest baseUrl[%s]' % url)
        HTTP_HEADER= {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0',
                      'Accept': 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                      'Accept-Encoding':'gzip, deflate'
                     }
        
        http_params={'header':HTTP_HEADER, 'with_metadata':True, 'cookiefile':COOKIE_FILE, 'use_cookie': True, 'load_cookie': True, 'save_cookie': True}

        sts, data = self.cm.getPage(url, http_params)

        if not sts:
            return
        url2 = re.findall("<source src=[\"'](.*?)[\"']", data)
        #printDBG('Data0='+data)
        if (not url2) or ('/' not in url2[0]):
            # look for javascript
            script =''
            tmp_script = re.findall("<script.*?>(.*?)</script>", data, re.S)
            for s in tmp_script:
                if s.startswith('function'):
                    script = s
                    break
            if script:
                printDBG(script)
                printDBG("------------ Gettttttt")
                OUT = VidStream(script)		
                printDBG("------------ OUT"+str(OUT))
                if 'ERR' in str(OUT): printDBG('Error: %s' % OUT.replace('ERR:',''))
                else:
                    AJAX_HEADER = {
                        'Accept': '*/*',
                        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                        'Origin': self.cm.getBaseUrl(url),
                        'Referer': url,
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0',
                        'X-Requested-With': 'XMLHttpRequest'}
                    printDBG('OUT = %s' % str(OUT))
                    cookies_ = self.cm.getCookieItems(self.COOKIE_FILE)
                    #printDBG('cookies_1='+str(cookies_))
                    sts, data = self.cm.getPage(main_url+OUT[0], http_params)                    
                    #sts, data = self.cm.getPage('https://s.vidstream.to/style.css', http_params)
                    printDBG('cookies_2='+str(cookies_)) 
                    zone = self.cm.ph.getSearchGroups(data, '''name=['"]zone['"] value=['"]([^'^"]+?)['"]''')[0]
                    rb = self.cm.ph.getSearchGroups(data, '''name=['"]rb['"] value=['"]([^'^"]+?)['"]''')[0]
                    #printDBG("------------ zone[%s] rb[%s]" % (zone, rb))
                    cv_url = main_url+ OUT[1]
                    sts, ret = self.cm.getPage(cv_url, {'header':AJAX_HEADER, 'cookiefile':COOKIE_FILE, 'use_cookie': True, 'load_cookie': True, 'save_cookie': True}, OUT[2])
                    if sts:
                        printDBG("------------ ret[%s]" % ret)
                        if 'ok' in ret:
                            if '?' in url:
                                url2 = url + "&r="
                            else:
                                url2 = url + "?r="
                            # retry to load the page
                            GetIPTVSleep().Sleep(1)
                            http_params['header']['Referer'] = url
                            sts, data = self.cm.getPage(url2, http_params)
        printDBG('Data1='+data)
        urlTab=[]
        url3 = re.findall("<source src=[\"'](.*?)[\"']", data)
        if url3:
            printDBG("------------ url3 %s" % url3)
            url3 = self.cm.getFullUrl(url3[0], self.cm.getBaseUrl(url))
            if 'mp4' in url3: urlTab.append((url3,'0'))
            else:             urlTab.append((url3,'3'))
        return urlTab
