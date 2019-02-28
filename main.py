import webapp2, urllib2, sys, urllib, cookielib, json, time, os
from array import *
sys.path.append('libs')
import mechanize
from bs4 import BeautifulSoup
from google.appengine.api import urlfetch, memcache
urlfetch.set_default_fetch_deadline(60)
from PIL import Image

#br.addheaders = [('referer', 'https://academics.vit.ac.in')]

class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write('<center><h1><u>!!!Welcome!!!</u></h1><h3>FacAdemics Test Backend App Engine Console/API</h3><br>(c)Prerit Kimtani And FacAdemics 2014</center>')

class VersionDetail(webapp2.RequestHandler):
    def get(self):
        sub = {}
        sub.update({'version': 'Security Test'})
        sub.update({'working website': 'prerithelp.net76.net/facademics_test'})
        sub.update({'security': 'Level 1'})
        sub.update({'summary': 'Complete JSON Data'})
        self.response.write(json.dumps(sub))
        
def keyReGen(id, date):
    # This method is used to regenerate the 'Level 1' security key for decryption.
    myAscii = {'01':'%', '02':'>', '03':'#', '04':'&', '05':'*', '06':'+', '07':'1', '08':'2', '09':'3', '10':'4', '11':'5', 
    '12':'6', '13':'7', '14':'8', '15':'9', '16':'!', '17':'0', '18':'A', '19':'B', '20':'C', '21':'D', '22':'E', '23':'F', 
    '24':'G', '25':'H', '26':'I', '27':'J', '28':'K', '29':'L', '30':'M', '31':'N', '32':'O', '33':'P', '34':'Q', '35':'R', 
    '36':'S', '37':'T', '38':'U', '39':'V', '40':'W', '41':'X', '42':'Y', '43':'Z', '44':'a', '45':'b', '46':'c', '47':'d', 
    '48':'e', '49':'f', '50':'g', '51':'h', '52':'i', '53':'j', '54':'k', '55':'l', '56':'m', '57':'n', '58':'o', '59':'p', 
    '60':'q', '61':'r', '62':'s', '63':'t', '64':'u', '65':'v', '66':'w', '67':'x', '68':'y', '69':'z', '70':'?', '71':'_', 
    '72':'@', '73':'/', '74':'<', '75':'$'}
    myCharMap = {'A':'1', 'B':'2', 'C':'3', 'D':'4', 'E':'5', 'F':'6', 'G':'7', 'H':'8', 'I':'9', 'J':'10', 'K':'11', 'L':'12', 
    'M':'13', 'N':'14', 'O':'15', 'P':'16', 'Q':'17', 'R':'18', 'S':'19', 'T':'20', 'U':'21', 'V':'22', 'W':'23', 'X':'24', 
    'Y':'25', 'Z':'26', 'a':'27', 'b':'28', 'c':'29', 'd':'30', 'e':'31', 'f':'32', 'g':'33', 'h':'34', 'i':'35', 'j':'36', 
    'k':'37', 'l':'38', 'm':'39', 'n':'40', 'o':'41', 'p':'42', 'q':'43', 'r':'44', 's':'45', 't':'46', 'u':'47', 'v':'48', 
    'w':'49', 'x':'50', 'y':'51', 'z':'52'}
    idNew = ''
    # Below we check if the passed id contains any character. If yes then a specific integer is assigned from myCharMap
    # Elif instead of only one if to make code look good to see
    for d in id:
        if d=='A' or d=='B' or d=='C' or d=='D' or d=='E' or d=='F' or d=='G' or d=='H' or d=='I' or d=='J' or d=='K':
            idNew = idNew + myCharMap[d]
        elif d=='L' or d=='M' or d=='N' or d=='O' or d=='P' or d=='Q' or d=='R' or d=='S' or d=='T' or d=='U' or d=='V':
            idNew = idNew + myCharMap[d]
        elif d=='W' or d=='X' or d=='Y' or d=='Z' or d=='a' or d=='b' or d=='c' or d=='d' or d=='e' or d=='f' or d=='g' or d=='h':
            idNew = idNew + myCharMap[d]
        elif d=='i' or d=='j' or d=='k' or d=='l' or d=='m' or d=='n' or d=='o' or d=='p' or d=='q' or d=='r' or d=='s' or d=='t':
            idNew = idNew + myCharMap[d]
        elif d=='u' or d=='v' or d=='w' or d=='x'  or d=='y' or d=='z':
            idNew = idNew + myCharMap[d]
        else:
            idNew = idNew + d
    id = idNew
    keyValue=''
    toDate = int(date)
    looper = '1234567891011121314'
    looper2= '123456789101112131412342341212342424'
    # This loop converts the given id to approx 32 bits
    for l in looper:
        if len(id)<32:
            idI = int(id)
            if toDate==01 or toDate==03 or toDate==05:
                toDate = 12 #this is done randomly because if toDate is 1 or small then it will create inappropriate result
            elif toDate==02 or toDate==04 or toDate==06:
                toDate= 13 #this is done randomly because if toDate is small then it will create inappropriate results
            idt = idI/toDate
            for i in looper2:
                if len(str(idt))>2:
                    idt = idt/toDate
                else:
                    id = id + str(idt)
                    break
        else:
            break
    # If after the above loop, length of id is not 32 then the difference of bits is appended from start
    if len(id) <= 32:
        #keyValue = len(id)
        limit = 32-len(id)
        id = id + id[:limit]
    else :
        limit = len(id) - 32
        limit = len(id) - limit
        id = id[:limit]
        #keyValue = len(id)
    #keyValue = len(id)
    n = 0
    #Below the converted 32-bit id is again converted to a 16-bit using myAscii chart, hence gives the required key
    for l in looper2:
        key = id[n:n+2]
        if key=='00':
            key = '01'
        elif key >'75':
            key = '75'
        elif key == '':
            break
        keyValue = keyValue + myAscii[key]
        n = n+2
    keyAsci =''
    for k in keyValue:
        keyAsci = keyAsci + str(ord(k))
    keyValue =keyAsci
    return keyValue

def keyGen(id):
    # This method is used to generate the 'Level 1' security key.
    # A 16-bit key is generated based on the faculty id, my own dictionary of ascii characters and current date in UTC TimeZone.
    myAscii = {'01':'%', '02':'>', '03':'#', '04':'&', '05':'*', '06':'+', '07':'1', '08':'2', '09':'3', '10':'4', '11':'5', 
    '12':'6', '13':'7', '14':'8', '15':'9', '16':'!', '17':'0', '18':'A', '19':'B', '20':'C', '21':'D', '22':'E', '23':'F', 
    '24':'G', '25':'H', '26':'I', '27':'J', '28':'K', '29':'L', '30':'M', '31':'N', '32':'O', '33':'P', '34':'Q', '35':'R', 
    '36':'S', '37':'T', '38':'U', '39':'V', '40':'W', '41':'X', '42':'Y', '43':'Z', '44':'a', '45':'b', '46':'c', '47':'d', 
    '48':'e', '49':'f', '50':'g', '51':'h', '52':'i', '53':'j', '54':'k', '55':'l', '56':'m', '57':'n', '58':'o', '59':'p', 
    '60':'q', '61':'r', '62':'s', '63':'t', '64':'u', '65':'v', '66':'w', '67':'x', '68':'y', '69':'z', '70':'?', '71':'_', 
    '72':'@', '73':'/', '74':'<', '75':'$'}
    myCharMap = {'A':'1', 'B':'2', 'C':'3', 'D':'4', 'E':'5', 'F':'6', 'G':'7', 'H':'8', 'I':'9', 'J':'10', 'K':'11', 'L':'12', 
    'M':'13', 'N':'14', 'O':'15', 'P':'16', 'Q':'17', 'R':'18', 'S':'19', 'T':'20', 'U':'21', 'V':'22', 'W':'23', 'X':'24', 
    'Y':'25', 'Z':'26', 'a':'27', 'b':'28', 'c':'29', 'd':'30', 'e':'31', 'f':'32', 'g':'33', 'h':'34', 'i':'35', 'j':'36', 
    'k':'37', 'l':'38', 'm':'39', 'n':'40', 'o':'41', 'p':'42', 'q':'43', 'r':'44', 's':'45', 't':'46', 'u':'47', 'v':'48', 
    'w':'49', 'x':'50', 'y':'51', 'z':'52'}
    idNew = ''
    # Below we check if the passed id contains any character. If yes then a specific integer is assigned from myCharMap
    # Elif instead of only one if to make code look good to see
    for d in id:
        if d=='A' or d=='B' or d=='C' or d=='D' or d=='E' or d=='F' or d=='G' or d=='H' or d=='I' or d=='J' or d=='K':
            idNew = idNew + myCharMap[d]
        elif d=='L' or d=='M' or d=='N' or d=='O' or d=='P' or d=='Q' or d=='R' or d=='S' or d=='T' or d=='U' or d=='V':
            idNew = idNew + myCharMap[d]
        elif d=='W' or d=='X' or d=='Y' or d=='Z' or d=='a' or d=='b' or d=='c' or d=='d' or d=='e' or d=='f' or d=='g' or d=='h':
            idNew = idNew + myCharMap[d]
        elif d=='i' or d=='j' or d=='k' or d=='l' or d=='m' or d=='n' or d=='o' or d=='p' or d=='q' or d=='r' or d=='s' or d=='t':
            idNew = idNew + myCharMap[d]
        elif d=='u' or d=='v' or d=='w' or d=='x'  or d=='y' or d=='z':
            idNew = idNew + myCharMap[d]
        else:
            idNew = idNew + d
    id = idNew
    keyValue=''
    toDate = int(time.strftime('%d'))
    looper = '1234567891011121314'
    looper2= '123456789101112131412342341212342424'
    # This loop converts the given id to approx 32 bits
    for l in looper:
        if len(id)<32:
            idI = int(id)
            if toDate==01 or toDate==03 or toDate==05:
                toDate = 12 #this is done randomly because if toDate is 1 or small then it will create inappropriate result
            elif toDate==02 or toDate==04 or toDate==06:
                toDate= 13 #this is done randomly because if toDate is small then it will create inappropriate results
            elif toDate==07 or toDate==8 or toDate==9:
                toDate = toDate*2 #this is done randomly because to convert toDate to double digits
            idt = idI/toDate
            for i in looper2:
                if len(str(idt))>2:
                    idt = idt/toDate
                else:
                    id = id + str(idt)
                    break
        else:
            break
    # If after the above loop, length of id is not 32 then the difference of bits is appended from start
    if len(id) <= 32:
        #keyValue = len(id)
        limit = 32-len(id)
        id = id + id[:limit]
    else :
        limit = len(id) - 32
        limit = len(id) - limit
        id = id[:limit]
        #keyValue = len(id)
    #keyValue = len(id)
    n = 0
    #Below the converted 32-bit id is again converted to a 16-bit using myAscii chart, hence gives the required key
    for l in looper2:
        key = id[n:n+2]
        if key=='00':
            key = '01'
        elif key >'75':
            key = '75'
        elif key == '':
            break
        keyValue = keyValue + myAscii[key]
        n = n+2
    keyValue = keyValue + str(toDate)
    return keyValue

def decrypt(encryptData, key):
    # This method is respobsible for decryption of data at 'Level 1' security.
    myAscii = {'01':'%', '02':'>', '03':'#', '04':'&', '05':'*', '06':'+', '07':'1', '08':'2', '09':'3', '10':'4', '11':'5', 
    '12':'6', '13':'7', '14':'8', '15':'9', '16':'!', '17':'0', '18':'A', '19':'B', '20':'C', '21':'D', '22':'E', '23':'F', 
    '24':'G', '25':'H', '26':'I', '27':'J', '28':'K', '29':'L', '30':'M', '31':'N', '32':'O', '33':'P', '34':'Q', '35':'R', 
    '36':'S', '37':'T', '38':'U', '39':'V', '40':'W', '41':'X', '42':'Y', '43':'Z', '44':'a', '45':'b', '46':'c', '47':'d', 
    '48':'e', '49':'f', '50':'g', '51':'h', '52':'i', '53':'j', '54':'k', '55':'l', '56':'m', '57':'n', '58':'o', '59':'p', 
    '60':'q', '61':'r', '62':'s', '63':'t', '64':'u', '65':'v', '66':'w', '67':'x', '68':'y', '69':'z', '70':'?', '71':'_', 
    '72':'@', '73':'/', '74':'<', '75':'$'}
    myCharMap = {'A':'1', 'B':'2', 'C':'3', 'D':'4', 'E':'5', 'F':'6', 'G':'7', 'H':'8', 'I':'9', 'J':'10', 'K':'11', 'L':'12', 
    'M':'13', 'N':'14', 'O':'15', 'P':'16', 'Q':'17', 'R':'18', 'S':'19', 'T':'20', 'U':'21', 'V':'22', 'W':'23', 'X':'24', 
    'Y':'25', 'Z':'26', 'a':'27', 'b':'28', 'c':'29', 'd':'30', 'e':'31', 'f':'32', 'g':'33', 'h':'34', 'i':'35', 'j':'36', 
    'k':'37', 'l':'38', 'm':'39', 'n':'40', 'o':'41', 'p':'42', 'q':'43', 'r':'44', 's':'45', 't':'46', 'u':'47', 'v':'48', 
    'w':'49', 'x':'50', 'y':'51', 'z':'52'}
    value = int(encryptData) - int(key)
    origVal = ''
    #make ascii values in 'value' in a set of 3 then convert back to string.
    value = str(value)
    #decryptData = value
    n=0
    x = chr(int(value[n:n+3]))
    for i in encryptData:
        if n+3<=len(value):
            origVal = origVal + chr(int(value[n:n+3]))
            n=n+3
        else:
            break
    decryptData = origVal
    return decryptData

class Key(webapp2.RequestHandler):
    def get(self, facid):
        k = keyGen(facid)
        self.response.write(k)

class ReKey(webapp2.RequestHandler):
    def get(self, facid, date):
        key = keyReGen(facid, date[len(date)-2:len(date)])
        originalValue = decrypt(date[:len(date)-2], key)
        passwd = originalValue
        self.response.write(passwd)

class performLogin(webapp2.RequestHandler):
    def get(self, facid, encryptData):
        urlfetch.set_default_fetch_deadline(60)
        key = keyReGen(facid, encryptData[len(encryptData)-2:len(encryptData)])
        originalValue = decrypt(encryptData[:len(encryptData)-2], key)
        passwd = originalValue
        br = mechanize.Browser()
        cj = cookielib.CookieJar()
        br.set_cookiejar(cj)
        br.set_handle_equiv(True)
        br.set_handle_redirect(True)
        br.set_handle_referer(True)
        br.set_handle_robots(False)
        r = br.open('http://prerithelp.net76.net/facademics_test/homepage.php?msg=')
        html = r.read()
        soup = BeautifulSoup(html)
        userCookieName = facid + "name"
        userCookieValue = facid + "value"
        for cook in cj:
            if not memcache.get(userCookieName):
                memcache.add(userCookieName, cook.name, 600)
                memcache.add(userCookieValue, cook.value, 600)
                
            else:
                memcache.set(userCookieName, cook.name)
                memcache.set(userCookieValue, cook.value)
        
        self.response.headers['Content-Type'] = 'text/html'
        br.select_form('login')
        usr = 'userId'
        br.form[usr] = facid
        br.form['password'] = passwd
        home = br.submit()
        if(home.geturl() == 'http://prerithelp.net76.net/facademics_test/welcome_user.php'):
            self.response.write('success')
        else:
            if(home.geturl() == 'http://prerithelp.net76.net/facademics_test/homepage.php?msg=invalid'):
                self.response.write('invalid')
            else:
                self.response.write(home.geturl())

class SubjectJSON(webapp2.RequestHandler):
    def get(self, facid):
        cookienamekey = facid + "name"
        self.response.headers['Access-Control-Allow-Origin'] = '*'
        cookievaluekey = facid + "value"
        if not memcache.get(cookienamekey):            
            self.response.write("Timed Out")
        else:
            thevalue = memcache.get(cookievaluekey)
            thecookiename = memcache.get(cookienamekey)
            if (memcache.get(cookienamekey)):
                br1 = mechanize.Browser()
                ck = cookielib.Cookie(version=0, name=thecookiename, value=thevalue, port=None, port_specified=False,
                                      domain='prerithelp.net76.net', domain_specified=False, domain_initial_dot=False,
                                      path='/', path_specified=True, secure=False, expires=None, discard=True,
                                      comment=None, comment_url=None, rest={'HttpOnly': None}, rfc2109=False)
                newcj = cookielib.CookieJar()
                newcj.set_cookie(ck)
                br1.set_cookiejar(newcj)
                br1.set_handle_equiv(True)
                br1.set_handle_redirect(True)
                br1.set_handle_referer(True)
                ttUrl = br1.open('http://prerithelp.net76.net/facademics_test/subjectapi.php')
                br1.set_handle_robots(False)
                if (ttUrl.geturl() == "http://prerithelp.net76.net/facademics_test/subjectapi.php"):
                    self.response.write(ttUrl.read())
                else:
                    self.response.write('nosession')

class DateJSON(webapp2.RequestHandler):
    def get(self, facid, classnumber):
        cookienamekey = facid + "name"
        self.response.headers['Access-Control-Allow-Origin'] = '*'
        cookievaluekey = facid + "value"
        if not memcache.get(cookienamekey):            
            self.response.write("Timed Out")
        else:
            thevalue = memcache.get(cookievaluekey)
            thecookiename = memcache.get(cookienamekey)
            if (memcache.get(cookienamekey)):
                br1 = mechanize.Browser()
                ck = cookielib.Cookie(version=0, name=thecookiename, value=thevalue, port=None, port_specified=False,
                                      domain='prerithelp.net76.net', domain_specified=False, domain_initial_dot=False,
                                      path='/', path_specified=True, secure=False, expires=None, discard=True,
                                      comment=None, comment_url=None, rest={'HttpOnly': None}, rfc2109=False)
                newcj = cookielib.CookieJar()
                newcj.set_cookie(ck)
                br1.set_cookiejar(newcj)
                br1.set_handle_equiv(True)
                br1.set_handle_redirect(True)
                br1.set_handle_referer(True)
                ttUrl = br1.open('http://prerithelp.net76.net/facademics_test/datejson.php?classnumber='+classnumber)
                br1.set_handle_robots(False)
                if (ttUrl.geturl() == "http://prerithelp.net76.net/facademics_test/datejson.php?classnumber="+classnumber):
                    self.response.write(ttUrl.read())
                else:
                    self.response.write('nosession')

class StudentJSON(webapp2.RequestHandler):
    def get(self, facid, classnumber):
        cookienamekey = facid + "name"
        self.response.headers['Access-Control-Allow-Origin'] = '*'
        cookievaluekey = facid + "value"
        if not memcache.get(cookienamekey):            
            self.response.write("Timed Out")
        else:
            thevalue = memcache.get(cookievaluekey)
            thecookiename = memcache.get(cookienamekey)
            if (memcache.get(cookienamekey)):
                br1 = mechanize.Browser()
                ck = cookielib.Cookie(version=0, name=thecookiename, value=thevalue, port=None, port_specified=False,
                                      domain='prerithelp.net76.net', domain_specified=False, domain_initial_dot=False,
                                      path='/', path_specified=True, secure=False, expires=None, discard=True,
                                      comment=None, comment_url=None, rest={'HttpOnly': None}, rfc2109=False)
                newcj = cookielib.CookieJar()
                newcj.set_cookie(ck)
                br1.set_cookiejar(newcj)
                br1.set_handle_equiv(True)
                br1.set_handle_redirect(True)
                br1.set_handle_referer(True)
                ttUrl = br1.open('http://prerithelp.net76.net/facademics_test/studentsjson.php?classnumber='+classnumber)
                br1.set_handle_robots(False)
                if (ttUrl.geturl() == "http://prerithelp.net76.net/facademics_test/studentsjson.php?classnumber="+classnumber):
                    self.response.write(ttUrl.read())
                else:
                    self.response.write('nosession')

class Post(webapp2.RequestHandler):
    def get(self, facid, classnumber, date, values):
        date = date.lower()
        month= date[3:4:]
        if(month=='a'):
            year = date[9:13:]
            month = '04'
        else:
            month = '05'
            year = date[7:11:]
        d = date[:2:]
        date=year+'-'+month+'-'+d
        cookienamekey = facid + "name"
        self.response.headers['Access-Control-Allow-Origin'] = '*'
        cookievaluekey = facid + "value"
        if not memcache.get(cookienamekey):            
            self.response.write("Timed Out")
        else:
            thevalue = memcache.get(cookievaluekey)
            thecookiename = memcache.get(cookienamekey)
            if (memcache.get(cookienamekey)):
                br1 = mechanize.Browser()
                ck = cookielib.Cookie(version=0, name=thecookiename, value=thevalue, port=None, port_specified=False,
                                      domain='prerithelp.net76.net', domain_specified=False, domain_initial_dot=False,
                                      path='/', path_specified=True, secure=False, expires=None, discard=True,
                                      comment=None, comment_url=None, rest={'HttpOnly': None}, rfc2109=False)
                newcj = cookielib.CookieJar()
                newcj.set_cookie(ck)
                br1.set_cookiejar(newcj)
                br1.set_handle_equiv(True)
                br1.set_handle_redirect(True)
                br1.set_handle_referer(True)
                br1.set_handle_robots(False)
                homeUrl = "http://prerithelp.net76.net/facademics_test/welcome_user.php"
                attUrl = "http://prerithelp.net76.net/facademics_test/attend.php?classnumber="+classnumber+"&date="+date
                opened = br1.open(attUrl)
                if(opened.geturl()==attUrl):
                    br1.select_form('tek_attend')
                    postData = list(values)
                    key=''
                    value = ''
                    pD = ''
                    #below code looks for the control(select list) of name given and then puts value
                    for p in postData:
                        if(p=='p'):
                            key=key.upper()
                            br1.find_control(name=key).value = ["present"]
                            key=''
                        elif(p=='a'):
                            key=key.upper()
                            br1.find_control(name=key).value = ["absent"]
                            key=''
                        else:
                            key=key+p
                    home=br1.submit()
                    if(home.geturl()==homeUrl):
                        self.response.write('s')
                    else:
                        self.response.write('f')
                else:
                    self.response.write('nosession')

class AttenJSON(webapp2.RequestHandler):
    def get(self, facid, classnumber, date):
        year = date[6::]
        month= date[3:5:]
        d = date[:2:]
        date=year+'-'+month+'-'+d
        cookienamekey = facid + "name"
        self.response.headers['Access-Control-Allow-Origin'] = '*'
        cookievaluekey = facid + "value"
        if not memcache.get(cookienamekey):            
            self.response.write("Timed Out")
        else:
            thevalue = memcache.get(cookievaluekey)
            thecookiename = memcache.get(cookienamekey)
            if (memcache.get(cookienamekey)):
                br1 = mechanize.Browser()
                ck = cookielib.Cookie(version=0, name=thecookiename, value=thevalue, port=None, port_specified=False,
                                      domain='prerithelp.net76.net', domain_specified=False, domain_initial_dot=False,
                                      path='/', path_specified=True, secure=False, expires=None, discard=True,
                                      comment=None, comment_url=None, rest={'HttpOnly': None}, rfc2109=False)
                newcj = cookielib.CookieJar()
                newcj.set_cookie(ck)
                br1.set_cookiejar(newcj)
                br1.set_handle_equiv(True)
                br1.set_handle_redirect(True)
                br1.set_handle_referer(True)
                ttUrl = br1.open('http://prerithelp.net76.net/facademics_test/attendjson.php?classnumber='+classnumber+'&date='+date)
                br1.set_handle_robots(False)
                if (ttUrl.geturl() == "http://prerithelp.net76.net/facademics_test/attendjson.php?classnumber="+classnumber+'&date='+date):
                    self.response.write(ttUrl.read())
                else:
                    self.response.write('nosession')

app = webapp2.WSGIApplication([
    ('/', MainHandler), ('/version', VersionDetail),
    ('/key/(.*)', Key), ('/rekey/(.*)/(.*)', ReKey),
    ('/login/(.*)/(.*)', performLogin),
    ('/subject/(.*)', SubjectJSON),
    ('/student/(.*)/(.*)', StudentJSON),
    ('/date/(.*)/(.*)', DateJSON),
    ('/attendance/(.*)/(.*)/(.*)', AttenJSON),
    ('/post/(.*)/(.*)/(.*)/(.*)',  Post),
], debug=True)