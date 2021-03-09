from tkinter import* 
from tkinter import ttk
import tkinter as tk
import sqlite3 ##veritanına verileri kaydetmek içinn sqlite3 kullanıyoruz


con = sqlite3.connect("uygulamapy1.db")
cursor = con.cursor()
 
#global veri tanımları 
window =Tk ##ana pencere 
kullaniciad ="" 
kullanicisifre=""
sonuc=""
kullanici="" #kullanici adı ve şifresinden oluşan bir string tanımlıyoruz bu site kaydeden kullanıcının bilgisidir
siteadi="" 
siteadres=""
sitesifre="" 
liste=ttk.Treeview 

def tabloolustur():  ##sisteme yeni kaydolan kullanıcıları kaydetmek için tablo oluşturduk ad ve şifre alanları olucak
    cursor.execute("CREATE TABLE IF NOT EXISTS kullanici (kullaniciad TEXT , sifre TEXT )")
    con.commit()


def sitetablosu():  ##sisteme yeni kaydolan kullanıcıların adına göre veritabanına site kaydetmek için tablo oluşturduk 
    cursor.execute("CREATE TABLE IF NOT EXISTS site (kullanici TEXT, sitead TEXT ,adres Text, sifre TEXT)")
    con.commit() 


def degerekle():  ##kullanıcıyı veritabanına ekleme fonksiyonu
     ad=kullaniciad.get() ##entry verilerini almak için .get metodu kullandık 
     textsifre= kullanicisifre.get() 
     sifre=cipher_encrypt(textsifre, 4) ##girilen şifreyi veritabanına kaydetmek için encrpy işlemi yapıyoruz
     if(len(ad)!=0 and len(sifre)!=0): ##kullanıcı veri girmediyse hiçbişey yapmaz
            oku=cursor.execute("SELECT count(*) as 'giris' FROM kullanici where kullaniciad=? and sifre=?",(ad,sifre))
            for i in oku.fetchall(): ##veritabanı verilerini alır 
                giris=i[0]
            if(giris==0):
                cursor.execute("INSERT INTO  kullanici(kullaniciad ,sifre) VALUES (?,?)", (ad, sifre))
                con.commit()
                print("Kayıt Eklendi.") 
                sonuc.config(text="KAYIT EKLENDİ.",bg='#778899')
                global kullanici #3kullanacağımız değişkenin glabalden geldiğini tanımlar
                kullanici=ad+sifre
                menubtn=Button(window) ##giriş yaptıktan sonra menu butonu oluşur
                menubtn.config(text = "MENU", command=menu, bg='white',activebackground = 'red', activeforeground = 'white',width=50,height=3) 
                menubtn.place(x=80, y=180) 
            else:
                print("Kullanıcı ve Sifre Zaten Kayıtlı! ")
                sonuc.config(text="KULLANICI VE ŞİFRE ZATEN KAYITLI!",bg='#778899')
  
                
def kontrol():
    ##entry ile girilen verileri .get() metodu ile alıyoruz
    ad=kullaniciad.get()
    textsifre= kullanicisifre.get() 
    sifre=cipher_encrypt(textsifre, 4) ##girilen şifreyi veritabanındaki şifreyle karşılaştırmak için encrpy işlemi yapıyoruz
    if(len(ad)!=0 and len(sifre)!=0): 
            oku=cursor.execute("SELECT count(*) as 'giris' FROM kullanici where kullaniciad='"+ad+"' and sifre='"+sifre+"'")
            for i in oku.fetchall():
                giris=i[0]
            if(giris==1):
                print("Giriş Başarılı.")
                sonuc.config(text="GİRİŞ BAŞARILI.",bg='#778899')
                global kullanici
                kullanici=ad+sifre
                menubtn=Button(window)
                menubtn.config(text = "MENU", command=menu, bg='white',activebackground = 'red', activeforeground = 'white',width=50,height=3) 
                menubtn.place(x=80, y=180) 
            else:
                print("Hatalı Giriş Yaptınız Bilgileri Kontrol Ediniz!")
                sonuc.config(text="HATALI GİRİŞ YAPTINIZ BİLGİLERİ KONTOL EDİNİZ!",bg='#778899')


def siteEkle():  ##kullanıcıyı veritabanına ekleme fonksiyonu
    sitead= siteadi.get()
    adres= siteadres.get()
    sifretext= sitesifre.get()
    sifre= cipher_encrypt(sifretext, 4)
    if(len(kullanici)!=0 and len(sitead)!=0 and len(adres)!=0 and len(sifre)!=0):
            oku=cursor.execute("SELECT count(*) as 'kontrol' FROM site where kullanici=? AND sitead=? AND adres=? AND sifre=?",(kullanici, sitead, adres, sifre))
            for i in oku.fetchall():
                kontrol=i[0]
            if(kontrol==0):
                cursor.execute("INSERT INTO  site (kullanici, sitead ,adres , sifre ) VALUES (?,?,?,?)", (kullanici, sitead, adres, sifre))
                con.commit()
                print("KAYIT EKLENDİ!") 
                sonuc.config(text="KAYIT EKLENDİ.",bg='#778899')   
            else:
                print("Site Zaten Kayıtlı! ")
                sonuc.config(text="SİTE ZATEN KAYITLI!",bg='#778899')

# kullanıcıya göre site bilgileri listelenir kullanıcı kendine ait olmayan site bilgilerine erişemez
def sitelistele():
    liste.delete(*liste.get_children()) #treeview i temizle
    sqlite="""SELECT * FROM site WHERE kullanici=? """
    cursor.execute(sqlite, (kullanici,))
    kayit=cursor.fetchall()
    print("Kayıtlı Site Sayısı: ", len(kayit))
    for row in kayit:
        print("Site Adı: ", row[1])
        print("Site Adresi: ", row[2]) 
        sitesifresi=cipher_decrypt(row[3], 4)
        print("Sifresi: ", sitesifresi)
        print("\n")  

        liste.insert("", 0, values=(row[1], row[2] ,sitesifresi))
        
    
def sitedegistir():   ## site şifresi değiştirme fonksiyonu
    site= siteadi.get()
    adres= siteadres.get()
    sifretext= sitesifre.get()
    yenisifre= cipher_encrypt(sifretext, 4)
    if(len(kullanici)!=0 and len(site)!=0 and len(yenisifre)!=0):
        oku=cursor.execute("SELECT count(*) as 'kontrol' FROM site WHERE kullanici=? and sitead=?",(kullanici, site))
        for i in oku.fetchall():
            kontrol=i[0]
            if(kontrol==1):
                cursor.execute("UPDATE site SET sifre=?, adres=? WHERE sitead= ? AND kullanici= ? ",(yenisifre,adres, site, kullanici))
                con.commit()
                print("Kayıt Güncellendi!") 
                sonuc.config(text="KAYIT GÜNCELLENDİ.",bg='#778899')   
            else: 
                print("Site Kayıtlı Değil!")
                sonuc.config(text="SİTE KAYITLI DEĞİL!",bg='#778899')   


# Şifreleme İşlevi fonksiyonları karakterin Unicode temsilini bulmak için kullanılan ve bunun tersi olan iki yerleşik işlevi tanımlar .
def cipher_encrypt(plain_text, key):
    encrypted = ""
    for c in plain_text:
        if c.isupper(): #büyük harf mi kontrol edin
            c_index = ord(c) - ord('A')
            # mevcut karakteri anahtar konumlarına göre değiştir
            c_shifted = (c_index + key) % 26 + ord('A')
            c_new = chr(c_shifted)
            encrypted += c_new
        elif c.islower(): #küçük harfli bir karakter olup olmadığını kontrol edin 
            #[0-25) aralığında dizin elde etmek için 'a'nın unicode'unu çıkarın
            c_index = ord(c) - ord('a') 
            c_shifted = (c_index + key) % 26 + ord('a')
            c_new = chr(c_shifted)
            encrypted += c_new
        elif c.isdigit():
            # eğer bir sayı ise, gerçek değerini değiştir
            c_new = (int(c) + key) % 10
            encrypted += str(c_new)
        else:
            # ne alfabetik ne de bir sayı ise, öyle bırak
            encrypted += c

    return encrypted


# Şifre Çözme İşlevi fonksiyonu
def cipher_decrypt(ciphertext, key):
    decrypted = ""
    for c in ciphertext:
        if c.isupper(): 
            c_index = ord(c) - ord('A')
            # orijinal konumunu almak için mevcut karakteri anahtar konumlarıyla sola kaydırın
            c_og_pos = (c_index - key) % 26 + ord('A')
            c_og = chr(c_og_pos)
            decrypted += c_og
        elif c.islower(): 
            c_index = ord(c) - ord('a') 
            c_og_pos = (c_index - key) % 26 + ord('a')
            c_og = chr(c_og_pos)
            decrypted += c_og
        elif c.isdigit():
            # eğer bir sayı ise, gerçek değerini değiştir
            c_og = (int(c) - key) % 10
            decrypted += str(c_og)
        else:
            # ne alfabetik ne de bir sayı ise, öyle bırak
            decrypted += c
    return decrypted


def girissayfasi():  ##kulanıcın karışalacağı ana pencere ekran 
    global window
    window=Tk(className='ŞİFRE SAKLAMA-YÖNETİM UYGULAMASI') ##pencere başlığı
    window.geometry("500x300") ##boyutu
    window.configure(bg='#778899')##pencere rengi #ff7f00 #ffd4aa #c6e2ff ee82ee
    window.resizable(width=FALSE, height=FALSE) ##pecrenin boyutu kullanıcı tarafından değiştirilemez
    Label(window, text="ŞİFRE SAKLAMA VE YÖNETİM UYGULAMASI",bg='#f8f8ff' ).place(x=120, y=10) 
   
    kad = Label(window ,text="Kullanıcı Adınızı Girin",bg='#f8f8ff').place(x=80, y=50) ##kullanıcı adı label 
    sif = Label(window, text="Kullanıcı Şifresini Girin",bg='#f8f8ff').place(x=80, y= 90) ##kullanıcı şifresi label 

    global kullaniciad
    kullaniciad= Entry(window)
    kullaniciad.place(x=250, y=50) ##kullanıcı adını alıyoruz 

    global kullanicisifre
    kullanicisifre = Entry(window)
    kullanicisifre.place(x=250, y=90) ##şifreyi alıyoruz

    girisbtn = Button(window, text = u"GİRİŞ", command=kontrol, activebackground = "red", activeforeground = "white", bg='white').place(x = 418, y = 50)  ##giriş botonu
    kaydolbtn = Button(window, text = u"KAYDOL", command=degerekle, activebackground = "red", activeforeground = "white", bg='white').place(x = 410, y = 86)  ##kayıt butonu
    
    ##sistem mesajalarını göstermek için label 
    global sonuc 
    sonuc = Label(window )
    sonuc.config(text="",bg='#778899')
    sonuc.place(x=80, y=150) 
   
    
    ##çıkış butonu pencereyi kapatır
    kapatbtn= Button(text = "KAPAT", command=window.quit, bg='white',activebackground = 'red', activeforeground = 'white') 
    kapatbtn.place(x=450, y=270) 
    window.mainloop()


def menu (): 
    window2=Toplevel() ##pencere başlığı  #birden fazla pencere oluşturmak için toplevel kullanılır
    window2.geometry("600x550") ##boyutu
    window2.configure(bg='#778899')##pencere rengi 
    window2.resizable(width=FALSE, height=FALSE) 
    Label(window2, text="ŞİFRE SAKLAMA VE YÖNETİM UYGULAMASI MENÜ ",height=2,bg='#f8f8ff').place(x=150, y=40) 


    site_ekle= Button(window2, text = u"Site Ekle", command= SiteEklePenceresi, activebackground = "red", activeforeground = "white", bg='white', width=50,height=5).place(x=100, y=100)  ##giriş botonu
    site_listele = Button(window2, text = u"Site Listele", command= SiteListesiPenceresi, activebackground = "red", activeforeground = "white", bg='white', width=50,height=5).place(x=100, y=200)  ##kayıt butonu 
    değişiklik_yap = Button(window2, text = u"Değişiklik Yap", command=SiteGuncellePenceresi, activebackground = "red", activeforeground = "white", bg='white', width=50,height=5).place(x=100, y=300)  ##kayıt butonu 


    window2.mainloop()


def SiteEklePenceresi():
    window3=Toplevel() ##pencere başlığı
    window3.geometry("500x250") ##boyutu
    window3.configure(bg='#778899')##pencere rengi 
    window3.resizable(width=FALSE, height=FALSE) 
    Label(window3, text="ŞİFRE SAKLAMA VE YÖNETİM UYGULAMASI SİTE EKLE ",height=1,bg='#f8f8ff').place(x=100, y=15) 

    sad = Label(window3, text="Site Adı").place(x=120, y=50) ##site adı label 
    sadres = Label(window3, text="Site Adresi").place(x=120, y= 90) ##site adresi label 
    ssif = Label(window3, text="Site Şifresi").place(x=120, y= 130) ##site şifresi label 

    global siteadi
    siteadi= Entry(window3)
    siteadi.place(x=250, y=50) ##site adını alıyoruz 

    global siteadres
    siteadres = Entry(window3)
    siteadres.place(x=250, y=90) ##site adresini alıyoruz

    global sitesifre
    sitesifre=  Entry(window3)
    sitesifre.place(x=250, y=130) ##site şifre alıyoruz

    kaydetbtn = Button(window3, text = u"KAYDET",command=siteEkle, activebackground = "red", activeforeground = "white", bg='white').place(x = 330, y = 180)  ##kaydet butonu

    global sonuc 
    sonuc = Label(window3 )
    sonuc.config(text="",bg='#778899')
    sonuc.place(x=120, y=180) 

    window3.mainloop() 



def SiteListesiPenceresi ():
    window4=Toplevel() ##pencere başlığı
    window4.geometry("700x500") ##boyutu
    window4.configure(bg='#778899')##pencere rengi 
    window4.resizable(width=TRUE, height=FALSE) 
    Label(window4, text="ŞİFRE SAKLAMA VE YÖNETİM UYGULAMASI SİTE LİSTESİ ",width=85,height=2,bg='#f8f8ff').place(x=50, y=20) 

    global liste 
    style = ttk.Style() ##listeleme yaptığımız treeview için stil özellikleri tanımladık
    style.configure("mystyle.Treeview", highlightthickness=1, bd=0, font=('Calibri', 10)) # Modify the font of the body
    style.configure("mystyle.Treeview.Heading", font=('Calibri', 11,'bold')) # Modify the font of the headings

    liste=ttk.Treeview(window4,style="mystyle.Treeview", column=("column1", "column2", "column3"), show='headings')
    liste.heading("#1", text="SİTE ADI")
    liste.heading("#2", text="SİTE ADRESİ")
    liste.heading("#3", text="SİTE ŞİFRESİ")
    liste.place(x = 50 ,y = 95)

    sitelistele()

    window4.mainloop() 



def SiteGuncellePenceresi(): 

    window5=Toplevel() ##pencere başlığı
    window5.geometry("550x250") ##boyutu
    window5.configure(bg='#778899')##pencere rengi 
    window5.resizable(width=FALSE, height=FALSE) 
    Label(window5, text="ŞİFRE SAKLAMA VE YÖNETİM UYGULAMASI SİTE DEĞİŞİKLİK ",height=1,bg='#f8f8ff').place(x=100, y=15) 

    sad = Label(window5, text="Değiştireciğiniz Site Adı").place(x=120, y=50) ##kullanıcı adı label 
    sadres = Label(window5, text="Yeni Site Adresi").place(x=120, y= 90) ##kullanıcı şifresi label 
    ssif = Label(window5, text="Yeni Site Şifresi").place(x=120, y= 130) ##kullanıcı şifresi label 

    global siteadi
    siteadi= Entry(window5)
    siteadi.place(x=270, y=50) ##site adını alıyoruz 

    global siteadres
    siteadres = Entry(window5)
    siteadres.place(x=270, y=90) ##site adresi alıyoruz

    global sitesifre
    sitesifre=  Entry(window5)
    sitesifre.place(x=270, y=130) ##site şifresi alıyoruz

    kaydetbtn = Button(window5, text = u"GÜNCELLE",command=sitedegistir, activebackground = "red", activeforeground = "white", bg='white').place(x = 340, y = 180)  ##kayıt butonu

    global sonuc 
    sonuc = Label(window5 )
    sonuc.config(text="",bg='#778899')
    sonuc.place(x=120, y=180) 

    window5.mainloop() 


tabloolustur() 
girissayfasi()


con.close() ##veritabanı bağlantısını kapattık 

