# -*- coding: utf-8 -*-
from Plugins.Extensions.IPTVPlayer.tools.iptvtools import printDBG
from Plugins.Extensions.IPTVPlayer.tsiplayer.libs.tstools import TSCBaseHostClass,tscolor,tshost
from Plugins.Extensions.IPTVPlayer.libs.e2ijson import loads as json_loads
from Components.config import config
import re,os


def getinfo():
    info_={}
    name = 'LinkBox'
    hst = 'https://www.linkbox.to'
    info_['old_host'] = hst
    hst_ = tshost(name)	
    if hst_!='': hst = hst_
    info_['host']    = hst
    info_['name']    = name
    info_['version'] = '1.0 02/04/2023'        
    info_['dev']     = 'RGYSoft'
    info_['cat_id']  = '21'
    txt = 'LinkBox - A Box Linking The World. Stockage cloud gratuit, synchronisation et partage'
    info_['desc']    = txt
    info_['icon']    = 'https://i.ibb.co/sWPGRVd/Sans-titre.png'
    return info_
    
    
class TSIPHost(TSCBaseHostClass):
    def __init__(self):
        TSCBaseHostClass.__init__(self,{})
        self.MAIN_URL = getinfo()['host']

    def showmenu(self,cItem):
        self.addDir({'import':cItem['import'],'category' : 'host2','url':'','shareToken':'_ig_2z1IFpK_4702801_f98c','good_for_fav':True,'title':'Netflix','desc':'','icon':cItem.get('icon',''),'mode':'10'})
        self.addDir({'import':cItem['import'],'category' : 'host2','url':'','shareToken':'xgLMOew','good_for_fav':True,'title':'Egybest','desc':'','icon':cItem.get('icon',''),'mode':'10'})
        self.addDir({'import':cItem['import'],'category' : 'host2','url':'','shareToken':'app01e2f1adf1aca7a5a2a5a5a4a2adf2aca7a5a2a5a5a4a2','good_for_fav':True,'title':'ONE cima TV','desc':'','icon':cItem.get('icon',''),'mode':'10'})
        self.addDir({'import':cItem['import'],'category' : 'host2','url':'','shareToken':'DERRaVk','good_for_fav':True,'title':'إجي بيست','desc':'','icon':cItem.get('icon',''),'mode':'10'})
        self.addDir({'import':cItem['import'],'category' : 'host2','url':'','shareToken':'ypev9W9','good_for_fav':True,'title':'مسلسلات و أفلام أجنبية','desc':'','icon':cItem.get('icon',''),'mode':'10'})
        self.addDir({'import':cItem['import'],'category' : 'host2','url':'','shareToken':'ho3FrEE','good_for_fav':True,'title':'For You','desc':'','icon':cItem.get('icon',''),'mode':'10'})
        self.addDir({'import':cItem['import'],'category' : 'host2','url':'','shareToken':'bNA04cJ','good_for_fav':True,'title':'AflamHQ','desc':'','icon':cItem.get('icon',''),'mode':'10'})
        self.addDir({'import':cItem['import'],'category' : 'host2','url':'','shareToken':'SD9p5bO','good_for_fav':True,'title':'Marvel Morocco','desc':'','icon':cItem.get('icon',''),'mode':'10'})
        self.addDir({'import':cItem['import'],'category' : 'host2','url':'','shareToken':'UiLE7sU','good_for_fav':True,'title':'Cinema Baghdad','desc':'','icon':cItem.get('icon',''),'mode':'10'})
        self.addDir({'import':cItem['import'],'category' : 'host2','url':'','shareToken':'app01e2f1adf1aca4a3a2a1a7aea4adf2aca4a3a2a1a7aea4','good_for_fav':True,'title':'Cinema Club Movies','desc':'','icon':cItem.get('icon',''),'mode':'10'})
        self.addDir({'import':cItem['import'],'category' : 'host2','url':'','shareToken':'app01e2f1adf1aca4a1afaea4a5a1adf2aca4a1afaea4a5a1','good_for_fav':True,'title':'Cinema Club Series','desc':'','icon':cItem.get('icon',''),'mode':'10'})
        self.addDir({'import':cItem['import'],'category' : 'host2','url':'','shareToken':'app01e2f1adf1aca1afaea6a7adf2aca1afaea6a7','good_for_fav':True,'title':'Star Cinema','desc':'','icon':cItem.get('icon',''),'mode':'10'})
        self.addDir({'import':cItem['import'],'category' : 'host2','url':'','shareToken':'_ig_app01e2f1adf0f2acf0e6a5f5fdf5a6a6a6a3f0a3_237634_f725','good_for_fav':True,'title':'Cima Now TV','desc':'','icon':cItem.get('icon',''),'mode':'10'})
        self.addDir({'import':cItem['import'],'category' : 'host2','url':'','shareToken':'app01e2f1adf1aca5a2aea1a2a6a3adf2aca5a2aea1a2a6a3','good_for_fav':True,'title':'سينما أونلاين','desc':'','icon':cItem.get('icon',''),'mode':'10'})
        self.addDir({'import':cItem['import'],'category' : 'host2','url':'','shareToken':'_ig_app01e2f1adf0f2acf0e6a5faeca2a6a6e6eef3fb_4890590_e417','good_for_fav':True,'title':'أفلام','desc':'','icon':cItem.get('icon',''),'mode':'10'})
        self.addDir({'import':cItem['import'],'category' : 'host2','url':'','shareToken':'app01e2f1adf2acaea7a5a2a3a5a4adf1acaea7a5a2a3a5a4','good_for_fav':True,'title':'مجتمع الأفلام و المسلسلات','desc':'','icon':cItem.get('icon',''),'mode':'10'})
        self.addDir({'import':cItem['import'],'category' : 'host2','url':'','shareToken':'app01e2f1adf2acafafa4a2a3a2adf1acafafa4a2a3a2','good_for_fav':True,'title':'عشاق الأفلام','desc':'','icon':cItem.get('icon',''),'mode':'10'})
        self.addDir({'import':cItem['import'],'category' : 'host2','url':'','shareToken':'_ig_app01e2f1adf0f2acf0e6a5fda0aea6a6a6f3afe0_2674587_0ddd','good_for_fav':True,'title':'Netflix','desc':'','icon':cItem.get('icon',''),'mode':'10'})
        self.addDir({'import':cItem['import'],'category' : 'host2','url':'','shareToken':'_ig_app01e2f1adf0f2acf0e6a5fbf9e5a6a6a6eefdf8_3589656_8ed8','good_for_fav':True,'title':'Egybest إجي بيست','desc':'','icon':cItem.get('icon',''),'mode':'10'})
        self.addDir({'import':cItem['import'],'category' : 'host2','url':'','shareToken':'app01e2f1adf1aca7a4a5a3a1a3aeadf2aca7a4a5a3a1a3ae','good_for_fav':True,'title':'Cinema Crown','desc':'','icon':cItem.get('icon',''),'mode':'10'})
        self.addDir({'import':cItem['import'],'category' : 'host2','url':'','shareToken':'app01e2f1adf1aca7a1a1a4a2a7a0adf2aca7a1a1a4a2a7a0','good_for_fav':True,'title':'البيت سينما','desc':'','icon':cItem.get('icon',''),'mode':'10'})
        self.addDir({'import':cItem['import'],'category' : 'host2','url':'','shareToken':'app01e2f1adf1aca4a3a5aea3aea0adf2aca4a3a5aea3aea0','good_for_fav':True,'title':'Cinemaclub إنمي','desc':'','icon':cItem.get('icon',''),'mode':'10'})
        self.addDir({'import':cItem['import'],'category' : 'host2','url':'','shareToken':'app01e2f1adf2acaeafa3a3afa3adf1acaeafa3a3afa3','good_for_fav':True,'title':'The Movie night','desc':'','icon':cItem.get('icon',''),'mode':'10'})
        self.addDir({'import':cItem['import'],'category' : 'host2','url':'','shareToken':'_ig_app01e2f1adf0f2acf0e6a5fde4e1a6a6a6e3e3af_2934696_5b94','good_for_fav':True,'title':'Atwa','desc':'','icon':cItem.get('icon',''),'mode':'10'})
        self.addDir({'import':cItem['import'],'category' : 'host2','url':'','shareToken':'_ig_app01e2f1adf0f2acf0e6a5fde3aea6a6a6aff7f2_3576258_c91a','good_for_fav':True,'title':'دراما نيوز','desc':'','icon':cItem.get('icon',''),'mode':'10'})
        self.addDir({'import':cItem['import'],'category' : 'host2','url':'','shareToken':'app01e2f1adf2aca7a3a6a0a1a1a5adf1aca7a3a6a0a1a1a5','good_for_fav':True,'title':'EGY-BEST','desc':'','icon':cItem.get('icon',''),'mode':'10'})
        self.addDir({'import':cItem['import'],'category' : 'host2','url':'','shareToken':'_ig_app01e2f1adf0f2acf0e6a5f9e4f1a6a6a5fcfba2_4250624_a55c','good_for_fav':True,'title':'Kowaya Cinema','desc':'','icon':cItem.get('icon',''),'mode':'10'})
        self.addDir({'import':cItem['import'],'category' : 'host2','url':'','shareToken':'_ig_app01e2f1adf0f2acf0e6a5e7e5e1a6a6a4a1eefe_10100689_6184','good_for_fav':True,'title':'Cinema Dose','desc':'','icon':cItem.get('icon',''),'mode':'10'})
        self.addDir({'import':cItem['import'],'category' : 'host2','url':'','shareToken':'app01e2f1adf1aca0a3a1a1a0a0adf2aca0a3a1a1a0a0','good_for_fav':True,'title':'Cinema sold','desc':'','icon':cItem.get('icon',''),'mode':'10'})
        self.addDir({'import':cItem['import'],'category' : 'host2','url':'','shareToken':'app01e2f1adf1aca3a7afa4a0a0a0adf2aca3a7afa4a0a0a0','good_for_fav':True,'title':'كل المسلسلات و الأفلام','desc':'','icon':cItem.get('icon',''),'mode':'10'})
        self.addDir({'import':cItem['import'],'category' : 'host2','url':'','shareToken':'app01e2f1adf2acaeaea5a2aea4afadf1acaeaea5a2aea4af','good_for_fav':True,'title':'أنميات','desc':'','icon':cItem.get('icon',''),'mode':'10'})
        self.addDir({'import':cItem['import'],'category' : 'host2','url':'','shareToken':'app01e2f1adf1aca5aea7afa0a6a5adf2aca5aea7afa0a6a5','good_for_fav':True,'title':'Cinema mix','desc':'','icon':cItem.get('icon',''),'mode':'10'})
        self.addDir({'import':cItem['import'],'category' : 'host2','url':'','shareToken':'_ig_app01e2f1adf0f2acf0e6a5fcaff5a6a6a6afa7fe_2609502_fdae','good_for_fav':True,'title':'فرجني شكرا','desc':'','icon':cItem.get('icon',''),'mode':'10'})
        self.addDir({'import':cItem['import'],'category' : 'host2','url':'','shareToken':'_ig_app01e2f1adf0f2acf0e6a5f9faa2a6a6a2e6f4e2_2751140_2b6c','good_for_fav':True,'title':'اجي بيست','desc':'','icon':cItem.get('icon',''),'mode':'10'})
        self.addDir({'import':cItem['import'],'category' : 'host2','url':'','shareToken':'_ig_app01e2f1adf0f2acf0e6a5fae2fda6a6a6f1a3ae_1077534_cc7b','good_for_fav':True,'title':'أفلام ومسلسلات أجنبية','desc':'','icon':cItem.get('icon',''),'mode':'10'})
        self.addDir({'import':cItem['import'],'category' : 'host2','url':'','shareToken':'_ig_app01e2f1adf0f2acf0e6a5fbe6fda6a6a6eef4ff_6032611_496c','good_for_fav':True,'title':'مسلسلات أجنبية أكشن إثارة','desc':'','icon':cItem.get('icon',''),'mode':'10'})
        self.addDir({'import':cItem['import'],'category' : 'host2','url':'','shareToken':'_ig_app01e2f1adf0f2acf0e6a5fdf3aea6a6a5e6f8af_3519730_d7ac','good_for_fav':True,'title':'تلفازك المتنقل','desc':'','icon':cItem.get('icon',''),'mode':'10'})
        self.addDir({'import':cItem['import'],'category' : 'host2','url':'','shareToken':'app01e2f1adf2aca0aeaeafa2a1adf1aca0aeaeafa2a1','good_for_fav':True,'title':'إنميات+تصنيفات الإنمي','desc':'','icon':cItem.get('icon',''),'mode':'10'})
        self.addDir({'import':cItem['import'],'category' : 'host2','url':'','shareToken':'app01e2f1adf2aca7aea5a5a6a6a3adf1aca7aea5a5a6a6a3','good_for_fav':True,'title':'عالم موبيس','desc':'','icon':cItem.get('icon',''),'mode':'10'})
        self.addDir({'import':cItem['import'],'category' : 'host2','url':'','shareToken':'paG344x','good_for_fav':True,'title':'Shahid4u','desc':'','icon':cItem.get('icon',''),'mode':'10'})
        self.addDir({'import':cItem['import'],'category' : 'host2','url':'','shareToken':'app01e2f1adf1aca2a4a7afa5afa7adf2aca2a4a7afa5afa7','good_for_fav':True,'title':'Showtime Movies','desc':'','icon':cItem.get('icon',''),'mode':'10'})
        self.addDir({'import':cItem['import'],'category' : 'host2','url':'','shareToken':'app01e2f1adf1aca5a4a7aea7a0a4adf2aca5a4a7aea7a0a4','good_for_fav':True,'title':'Bein Movies','desc':'','icon':cItem.get('icon',''),'mode':'10'})
        self.addDir({'import':cItem['import'],'category' : 'host2','url':'','shareToken':'app01e2f1adf2aca4a7a5a7a0aeafadf1aca4a7a5a7a0aeaf','good_for_fav':True,'title':'أفلام مجان نت','desc':'','icon':cItem.get('icon',''),'mode':'10'})
        self.addDir({'import':cItem['import'],'category' : 'host2','url':'','shareToken':'app01e2f1adf2aca5aea1a5aea0a2adf1aca5aea1a5aea0a2','good_for_fav':True,'title':'مسلسلات و أفلام 2023','desc':'','icon':cItem.get('icon',''),'mode':'10'})

    def showmenu1(self,cItem):
        nb_elm = 50
        shareToken = cItem.get('shareToken','')
        pid        = cItem.get('pid',0)
        page       = cItem.get('page',1)
        url = self.MAIN_URL + '/api/file/share_out_list/?sortField=name&sortAsc=1&pageNo='+str(page)+'&pageSize='+str(nb_elm)+'&'+'shareToken='+shareToken+'&pid='+str(pid)+'&needTpInfo=1&scene=singleGroup&name=&platform=web&pf=web&lan=en'
        sts, data = self.getPage(url)
        if sts:
            data = json_loads(data) 
            data = data.get('data',{})
            data = data.get('list',[])
            if not data: data = []
            elm_count = 0
            for elm in data:
                titre = elm.get('name','')
                type_ = elm.get('type','')
                pid   = elm.get('id','')
                desc  = ''
                icon  = elm.get('cover',cItem.get('icon',''))
                if '&x-image-process' in icon: icon = icon.split('&x-image-process',1)[0]
                link  = elm.get('url','')
                elm_count = elm_count + 1
                if type_=='dir':
                    self.addDir({'import':cItem['import'],'category' : 'host2','url':'','shareToken':shareToken,'pid':pid,'good_for_fav':True,'title':titre,'desc':'','icon':cItem.get('icon',''),'mode':'10'})
                elif type_=='video':
                    self.addVideo({'import':cItem['import'],'category' : 'video','url': link,'good_for_fav':True,'title':titre,'desc':desc,'icon':icon,'hst':'direct'})	
                else:
                    print('pas dir:'+titre)
            if elm_count + 1 > nb_elm:
                self.addDir({'import':cItem['import'],'category' : 'host2','url':'','shareToken':shareToken,'pid':cItem.get('pid',0),'page':page+1,'good_for_fav':True,'title':'Next','desc':'','icon':cItem.get('icon',''),'mode':'10'})
