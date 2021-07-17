#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  4 22:48:51 2021

@author: toygar
"""
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import numpy as np
from seffaflik.elektrik import uretim

#%% COAL

df = pd.read_csv('CoalKGUP.csv')
df2 = pd.read_csv('CoalEAK.csv')

"""
Eğer CoalEAKKGUP dosyası çalıştırılırsa bir alltaki satırlar açılacak,
sonra tekrar kapatılacak. Bunun dışında normal süreç devam eder.
"""
# df = df.drop('Unnamed: 0', axis = 1)
# df2 = df2.drop('Unnamed: 0', axis = 1)

df = df.set_index('DateTime')
df2 = df2.set_index('DateTime')


organizationID = ['40X100000000603N',
           '40X000000009083S',
           '40X0000000083216',
           '40X0000000006013',
           '40X0000000048313',
           '40X0000000090611',
           '40X000000008339O',
           '40X000000006498E',
           '40X000000011535G',
           '40X0000000067008',
           '40X000000010377D',
           '40X000000008360X',
           '40X000000007900W',
           '40X000000009162W',
           '40X000000007639H',
           '40X0000000132578',
           '40X0000000110333',
           '40X000000006999T',
           '40X000000000149W',
           '40X000000000369I'
           ]

today = datetime.today().strftime('%Y-%m-%d')
presentday = datetime.now()
tomorrow = (presentday + timedelta(1)).strftime('%Y-%m-%d')
#%% KGUP

kgup1 = uretim.kgup(baslangic_tarihi=today, bitis_tarihi=tomorrow, organizasyon_eic = "40X000000000195P")
kgup1['DateTime'] = pd.to_datetime(kgup1.Tarih) + kgup1.Saat.astype('timedelta64[h]')
kgup1 = kgup1.set_index('DateTime')
kgup1 = pd.DataFrame(kgup1['Linyit'])
kgup1 = kgup1.replace(np.nan, 0)

kgup3 = uretim.kgup(baslangic_tarihi=today, bitis_tarihi=tomorrow, organizasyon_eic = "40X000000000282U")
kgup3['DateTime'] = pd.to_datetime(kgup3.Tarih) + kgup3.Saat.astype('timedelta64[h]')
kgup3 = kgup3.set_index('DateTime')
kgup3 = pd.DataFrame(kgup3['Linyit'])
kgup3 = kgup3.replace(np.nan, 0)


kgup1 = kgup1.reset_index(drop=False)
kgup3 = kgup3.reset_index(drop=False)

kgup1 = pd.merge(kgup1, kgup3, how="outer", on=["DateTime", "DateTime"])
kgup1 = kgup1.set_index('DateTime')


for i in range(len(organizationID)):
    kgup2 = uretim.kgup(baslangic_tarihi=today, bitis_tarihi=tomorrow, organizasyon_eic = organizationID[i])
    kgup2['DateTime'] = pd.to_datetime(kgup2.Tarih) + kgup2.Saat.astype('timedelta64[h]')
    kgup2 = kgup2.drop('Tarih', axis = 1)
    kgup2 = kgup2.drop('Saat', axis = 1)
    kgup2 = kgup2.set_index('DateTime')
    kgup2 = pd.DataFrame(kgup2['Toplam'])
    kgup2 = kgup2.reset_index(drop=False)
    kgup1 = pd.merge(kgup1, kgup2, how="outer", on=["DateTime", "DateTime"])
    print("İşlem tamamlandı")
    
kgup1 = kgup1.set_index('DateTime')
kgup1 = kgup1.set_axis(['EUAS','ENERJISA TUFANBEYLI','ZETES EREN',
                      'ORHANELI TUNCBILEK','YATAGAN', 'SILOPI',
                      'ICDAS BEKIRLI', 'SOMA', 'YENIKOY KEMERKOY',
                      'SEYITOMER','HIDROGEN SOMA','KANGAL','CAN KOMUR',
                      'CATALAGZI','YUNUS EMRE','AKSA GOYNUK',
                      'ATLAS','ISKEN','CENAL','IZDEMIR','COLAKOGLU','ICDAS TERSANE'], axis=1, inplace=False)

df = df.reset_index(drop=False)
kgup1 = kgup1.reset_index(drop=False)

df['DateTime'] = pd.to_datetime(df.DateTime)
kgup1['DateTime'] = pd.to_datetime(kgup1.DateTime)

df = df.set_index('DateTime')
kgup1 = kgup1.set_index('DateTime')

df = pd.concat([df, kgup1])
df = df.reset_index(drop=False)
df.drop_duplicates(subset="DateTime",keep = "last", inplace = True)
df = df.set_index('DateTime')

df.to_csv('CoalKGUP.csv', index = True)

#%% EAK

eak1 = uretim.kgup(baslangic_tarihi=today, bitis_tarihi=tomorrow, organizasyon_eic = "40X000000000195P")
eak1['DateTime'] = pd.to_datetime(eak1.Tarih) + eak1.Saat.astype('timedelta64[h]')
eak1 = eak1.set_index('DateTime')
eak1 = pd.DataFrame(eak1['Linyit'])
eak1 = eak1.replace(np.nan, 0)

eak3 = uretim.kgup(baslangic_tarihi=today, bitis_tarihi=tomorrow, organizasyon_eic = "40X000000000282U")
eak3['DateTime'] = pd.to_datetime(eak3.Tarih) + eak3.Saat.astype('timedelta64[h]')
eak3 = eak3.set_index('DateTime')
eak3 = pd.DataFrame(eak3['Linyit'])
eak3 = eak3.replace(np.nan, 0)


eak1 = eak1.reset_index(drop=False)
eak3 = eak3.reset_index(drop=False)

eak1 = pd.merge(eak1, eak3, how="outer", on=["DateTime", "DateTime"])
eak1 = eak1.set_index('DateTime')

for i in range(len(organizationID)):
    eak2 = uretim.eak(baslangic_tarihi=today, bitis_tarihi=tomorrow, organizasyon_eic = organizationID[i])
    eak2['DateTime'] = pd.to_datetime(eak2.Tarih) + eak2.Saat.astype('timedelta64[h]')
    eak2 = eak2.drop('Tarih', axis = 1)
    eak2 = eak2.drop('Saat', axis = 1)
    eak2 = eak2.set_index('DateTime')
    eak2 = pd.DataFrame(eak2['Toplam'])
    eak2 = eak2.reset_index(drop=False)
    eak1 = pd.merge(eak1, eak2, how="outer", on=["DateTime", "DateTime"])
    print("İşlem tamamlandı")
    
eak1 = eak1.set_index('DateTime')
eak1 = eak1.set_axis(['EUAS','ENERJISA TUFANBEYLI','ZETES EREN',
                      'ORHANELI TUNCBILEK','YATAGAN', 'SILOPI',
                      'ICDAS BEKIRLI', 'SOMA', 'YENIKOY KEMERKOY',
                      'SEYITOMER','HIDROGEN SOMA', 'KANGAL','CAN KOMUR',
                      'CATALAGZI','YUNUS EMRE','AKSA GOYNUK',
                      'ATLAS','ISKEN','CENAL','IZDEMIR','COLAKOGLU','ICDAS TERSANE'], axis=1, inplace=False)
df2 = df2.reset_index(drop=False)
eak1 = eak1.reset_index(drop=False)

df2['DateTime'] = pd.to_datetime(df2.DateTime)
eak1['DateTime'] = pd.to_datetime(eak1.DateTime)

df2 = df2.set_index('DateTime')
eak1 = eak1.set_index('DateTime')

df2 = pd.concat([df2, eak1])
df2 = df2.reset_index(drop=False)
df2.drop_duplicates(subset="DateTime",keep = "last", inplace = True)
df2 = df2.set_index('DateTime')

df2.to_csv('CoalEAK.csv', index = True)



#%% PLOT

kuruluguc = ['940','450','8370','615','630','405','1605','990','1073','600','510','457','330','320','290','270','1200','1308','1320','370','380','405']

length=24

for iteration in range(len(kuruluguc)):
    kg = np.empty(length)
    kg.fill(kuruluguc[iteration])
    x_ax = range(length)
    plt.plot(x_ax, df[df.columns[iteration]].tail(length), linewidth=2, label="KGÜP")
    plt.plot(x_ax, kg, linewidth=2, label="Kurulu Güç")
    plt.plot(x_ax, df2[df.columns[iteration]].tail(length), linewidth=2, label="EAK")
    plt.title("{} {} KGUP-EAK".format(df.columns[iteration], tomorrow))
    plt.ylabel('MWh')
    plt.xlabel('Hours')
    plt.legend(loc='best',fancybox=True, shadow=True)
    plt.grid(True)
    #plt.savefig('{}24.png'.format(col))
    plt.show()
    
#%% EXPORTING PDF
x = pd.read_csv('CoalKGUP.csv')

x.tail(24).to_excel("Coal_KGUP.xlsx")

fig, ax =plt.subplots(figsize=(12,4))
ax.axis('off')
the_table = ax.table(cellText=x[x.columns[0:11]].tail(24).values,colLabels=x.columns[0:11],loc='center', cellLoc='center')
the_table.set_fontsize(35)
plt.savefig("Coal1_KGUP.pdf", format="pdf", bbox_inches = 'tight')

fig, ax =plt.subplots(figsize=(12,4))
ax.axis('off')
the_table = ax.table(cellText=x[x.columns[11:30]].tail(24).values,colLabels=x.columns[11:30],loc='center', cellLoc='center')
the_table.set_fontsize(35)
plt.savefig("Coal2_KGUP.pdf", format="pdf", bbox_inches = 'tight')


#%% GAS

df = pd.read_csv('GasKGUP.csv')
df2 = pd.read_csv('GasEAK.csv')

# df = df.drop('Unnamed: 0', axis = 1)
# df2 = df2.drop('Unnamed: 0', axis = 1)

df = df.set_index('DateTime')
df2 = df2.set_index('DateTime')


organizationID = ['40X000000010814H',
           '40X000000000378H',
           '40X100000000181N',
           '40X000000000282U',
           '40X000000010372N',
           '40X000000000166W',
           '40X000000000396F',
           '40X000000000294N',
           '40X000000006839E',
           '40X0000000094882',
           '40X000000003625B',
           '40X100000001964N',
           '40X000000011810K',
           '40X0000000118168',
           '40X000000011997F',
           '40X000000011811I'
           ]

today = datetime.today().strftime('%Y-%m-%d')

presentday = datetime.now()
tomorrow = (presentday + timedelta(1)).strftime('%Y-%m-%d')
#%% KGUP

kgup1 = uretim.kgup(baslangic_tarihi=today, bitis_tarihi=tomorrow, organizasyon_eic = "40X000000000195P")
kgup1['DateTime'] = pd.to_datetime(kgup1.Tarih) + kgup1.Saat.astype('timedelta64[h]')
kgup1 = kgup1.set_index('DateTime')
kgup1 = pd.DataFrame(kgup1['Doğalgaz'])
kgup1 = kgup1.replace(np.nan, 0)

for i in range(len(organizationID)):
    kgup2 = uretim.kgup(baslangic_tarihi=today, bitis_tarihi=tomorrow, organizasyon_eic = organizationID[i])
    kgup2['DateTime'] = pd.to_datetime(kgup2.Tarih) + kgup2.Saat.astype('timedelta64[h]')
    kgup2 = kgup2.drop('Tarih', axis = 1)
    kgup2 = kgup2.drop('Saat', axis = 1)
    kgup2 = kgup2.set_index('DateTime')
    kgup2 = pd.DataFrame(kgup2['Doğalgaz'])
    kgup2 = kgup2.reset_index(drop=False)
    kgup1 = pd.merge(kgup1, kgup2, how="outer", on=["DateTime", "DateTime"])
    print("İşlem tamamlandı")
    
kgup1 = kgup1.set_index('DateTime')
kgup1 = kgup1.set_axis(['EUAS', 'KAZANSODA', 'HAMITABAT', 
                        'HABAS', 'ENERJISA BANDIRMA', 
                        'ACWA', 'AK ENERJI ERZIN', 
                        'AKSA ANTALYA', 'BILGIN SAMSUN',
                        'YENI ELEKTRIK','IC ANADOLU','RWE TURCAS',
                        'CENGIZ 610','ENKA ADAPAZARI', 'BAYMINA','İZMİR', 'GEBZE'], axis=1, inplace=False)

df = df.reset_index(drop=False)
kgup1 = kgup1.reset_index(drop=False)

df['DateTime'] = pd.to_datetime(df.DateTime)
kgup1['DateTime'] = pd.to_datetime(kgup1.DateTime)

df = df.set_index('DateTime')
kgup1 = kgup1.set_index('DateTime')

df = pd.concat([df, kgup1])
df = df.reset_index(drop=False)
df.drop_duplicates(subset="DateTime",keep = "last", inplace = True)
df = df.set_index('DateTime')
df.to_csv('GasKGUP.csv', index = True)

#%% EAK

eak1 = uretim.kgup(baslangic_tarihi=today, bitis_tarihi=tomorrow, organizasyon_eic = "40X000000000195P")
eak1['DateTime'] = pd.to_datetime(eak1.Tarih) + eak1.Saat.astype('timedelta64[h]')
eak1 = eak1.set_index('DateTime')
eak1 = pd.DataFrame(eak1['Doğalgaz'])
eak1 = eak1.replace(np.nan, 0)

for i in range(len(organizationID)):
    eak2 = uretim.eak(baslangic_tarihi=today, bitis_tarihi=tomorrow, organizasyon_eic = organizationID[i])
    eak2['DateTime'] = pd.to_datetime(eak2.Tarih) + eak2.Saat.astype('timedelta64[h]')
    eak2 = eak2.drop('Tarih', axis = 1)
    eak2 = eak2.drop('Saat', axis = 1)
    eak2 = eak2.set_index('DateTime')
    eak2 = pd.DataFrame(eak2['Doğalgaz'])
    eak2 = eak2.reset_index(drop=False)
    eak1 = pd.merge(eak1, eak2, how="outer", on=["DateTime", "DateTime"])
    print("İşlem tamamlandı")
    
eak1 = eak1.set_index('DateTime')
eak1 = eak1.set_axis(['EUAS', 'KAZANSODA', 'HAMITABAT', 
                        'HABAS', 'ENERJISA BANDIRMA', 
                        'ACWA', 'AK ENERJI ERZIN', 
                        'AKSA ANTALYA', 'BILGIN SAMSUN',
                        'YENI ELEKTRIK','IC ANADOLU','RWE TURCAS',
                        'CENGIZ 610','ENKA ADAPAZARI', 'BAYMINA','İZMİR', 'GEBZE'], axis=1, inplace=False)
df2 = df2.reset_index(drop=False)
eak1 = eak1.reset_index(drop=False)

df2['DateTime'] = pd.to_datetime(df2.DateTime)
eak1['DateTime'] = pd.to_datetime(eak1.DateTime)

df2 = df2.set_index('DateTime')
eak1 = eak1.set_index('DateTime')

df2 = pd.concat([df2, eak1])
df2 = df2.reset_index(drop=False)
df2.drop_duplicates(subset="DateTime",keep = "last", inplace = True)
df2 = df2.set_index('DateTime')

df2.to_csv('GasEAK.csv', index = True)

#%% PLOT

kuruluguc = [3739,379,1220,2088,1543,927,904,900,887,865,853,797,610,770,798,1520,1540]

length=24

for iteration in range(len(kuruluguc)):
    kg = np.empty(length)
    kg.fill(kuruluguc[iteration])
    x_ax = range(length)
    plt.plot(x_ax, df[df.columns[iteration]].tail(length), linewidth=2, label="KGÜP")
    plt.plot(x_ax, kg, linewidth=2, label="Kurulu Güç")
    plt.plot(x_ax, df2[df2.columns[iteration]].tail(length), linewidth=2, label="EAK")
    plt.title("{} {} KGUP-EAK".format(df.columns[iteration], tomorrow))
    plt.ylabel('MWh')
    plt.xlabel('Hours')
    plt.legend(loc='best',fancybox=True, shadow=True)
    plt.grid(True)
    #plt.savefig('{}24.png'.format(col))
    plt.show()
#%% EXPORTING PDF

x = pd.read_csv('GasKGUP.csv')

x.tail(24).to_excel("Gas_KGUP.xlsx")

fig, ax =plt.subplots(figsize=(12,4))
ax.axis('off')
the_table = ax.table(cellText=x[x.columns[0:9]].tail(24).values,colLabels=x.columns[0:9],loc='center', cellLoc='center')
the_table.set_fontsize(35)
plt.savefig("Gas1_KGUP.pdf", format="pdf", bbox_inches = 'tight')

fig, ax =plt.subplots(figsize=(12,4))
ax.axis('off')
the_table = ax.table(cellText=x[x.columns[9:18]].tail(24).values,colLabels=x.columns[9:18],loc='center', cellLoc='center')
the_table.set_fontsize(35)
plt.savefig("Gas2_KGUP.pdf", format="pdf", bbox_inches = 'tight')

#%% HYDRO

df = pd.read_csv('HidroKGUP.csv')
df2 = pd.read_csv('HidroEAK.csv')

"""
Eğer HidroEAKKGUP dosyası çalıştırılırsa bir alltaki satırlar açılacak,
sonra tekrar kapatılacak. Bunun dışında normal süreç devam eder.
"""

# df = df.drop('Unnamed: 0', axis = 1)
# df2 = df2.drop('Unnamed: 0', axis = 1)

df = df.set_index('DateTime')
df2 = df2.set_index('DateTime')

organizationID = ['40X000000011074Q',
           '40X0000000082430',
           '40X0000000001348',
           '40X0000000056340',
           '40X000000012897E',
           '40X0000000038342',
           '40X000000009422W',
           '40X0000000056502',
           '40X000000000282U',
           '40X000000000195P',
           '40X000000000195P',
           '40X000000000195P',
           '40X000000000195P',
           '40X000000000195P'
           ]

uevcb = ['40W0000000007330',
         '40W000000000736V',
         '40W000000000744W',
         '40W000003196807U',
         '40W000000335652A',]

today = datetime.today().strftime('%Y-%m-%d')
presentday = datetime.now()
tomorrow = (presentday + timedelta(1)).strftime('%Y-%m-%d')
#%% KGUP

kgup1 = uretim.kgup(baslangic_tarihi=today, bitis_tarihi=tomorrow, organizasyon_eic = "40X000000000195P")
kgup1['DateTime'] = pd.to_datetime(kgup1.Tarih) + kgup1.Saat.astype('timedelta64[h]')
kgup1 = kgup1.set_index('DateTime')
kgup1 = pd.DataFrame(kgup1['Barajlı'])
kgup1 = kgup1.replace(np.nan, 0)

j = 0
count = 1

for i in range(len(organizationID)):
    
    if count < 10:
        kgup2 = uretim.kgup(baslangic_tarihi=today, bitis_tarihi=tomorrow, organizasyon_eic = organizationID[i])
        kgup2['DateTime'] = pd.to_datetime(kgup2.Tarih) + kgup2.Saat.astype('timedelta64[h]')
        kgup2 = kgup2.drop('Tarih', axis = 1)
        kgup2 = kgup2.drop('Saat', axis = 1)
        kgup2 = kgup2.set_index('DateTime')
        kgup2 = pd.DataFrame(kgup2['Barajlı'])
        kgup2 = kgup2.reset_index(drop=False)
        kgup1 = pd.merge(kgup1, kgup2, how="outer", on=["DateTime", "DateTime"])
        print("İşlem tamamlandı")
        count = count + 1
    
    else:
        kgup2 = uretim.kgup(baslangic_tarihi=today, bitis_tarihi=tomorrow, organizasyon_eic = organizationID[i], uevcb_eic = uevcb[j])
        kgup2['DateTime'] = pd.to_datetime(kgup2.Tarih) + kgup2.Saat.astype('timedelta64[h]')
        kgup2 = kgup2.drop('Tarih', axis = 1)
        kgup2 = kgup2.drop('Saat', axis = 1)
        kgup2 = kgup2.set_index('DateTime')
        kgup2 = pd.DataFrame(kgup2['Barajlı'])
        kgup2 = kgup2.reset_index(drop=False)
        kgup1 = pd.merge(kgup1, kgup2, how="outer", on=["DateTime", "DateTime"])
        print("İşlem tamamlandı")
        j = j + 1
        count = count + 1
    
kgup1 = kgup1.set_index('DateTime')
kgup1 = kgup1.set_axis(['EUAS', 'KALEHAN KALE ENERJI', 'KALEHAN BEYHAN1', 
                        'OYMAPINAR', 'BOYABAT', 
                        'KALEHAN ASAGI KALEKOY', 'LIMAK', 
                        'DOGUS ARTVIN', 'SANKO','ENERJISA',
                        'ATATURK', 'KARAKAYA', 'KEBAN', 
                        'BIRECIK', 'DERINER'], axis=1, inplace=False)

df = df.reset_index(drop=False)
kgup1 = kgup1.reset_index(drop=False)

df['DateTime'] = pd.to_datetime(df.DateTime)
kgup1['DateTime'] = pd.to_datetime(kgup1.DateTime)

df = df.set_index('DateTime')
kgup1 = kgup1.set_index('DateTime')

df = pd.concat([df, kgup1])
df = df.reset_index(drop=False)
df.drop_duplicates(subset="DateTime",keep = "last", inplace = True)
df = df.set_index('DateTime')

df.to_csv('HidroKGUP.csv', index = True)

#%% EAK

eak1 = uretim.kgup(baslangic_tarihi=today, bitis_tarihi=tomorrow, organizasyon_eic = "40X000000000195P")
eak1['DateTime'] = pd.to_datetime(eak1.Tarih) + eak1.Saat.astype('timedelta64[h]')
eak1 = eak1.set_index('DateTime')
eak1 = pd.DataFrame(eak1['Barajlı'])
eak1 = eak1.replace(np.nan, 0)

j = 0
count = 1

for i in range(len(organizationID)):
    
    if count < 10:
        
        eak2 = uretim.eak(baslangic_tarihi=today, bitis_tarihi=tomorrow, organizasyon_eic = organizationID[i])
        eak2['DateTime'] = pd.to_datetime(eak2.Tarih) + eak2.Saat.astype('timedelta64[h]')
        eak2 = eak2.drop('Tarih', axis = 1)
        eak2 = eak2.drop('Saat', axis = 1)
        eak2 = eak2.set_index('DateTime')
        eak2 = pd.DataFrame(eak2['Barajlı'])
        eak2 = eak2.reset_index(drop=False)
        eak1 = pd.merge(eak1, eak2, how="outer", on=["DateTime", "DateTime"])
        print("İşlem tamamlandı")
        count = count + 1
        
    else:
        eak2 = uretim.eak(baslangic_tarihi=today, bitis_tarihi=tomorrow, organizasyon_eic = organizationID[i], uevcb_eic = uevcb[j])
        eak2['DateTime'] = pd.to_datetime(eak2.Tarih) + eak2.Saat.astype('timedelta64[h]')
        eak2 = eak2.drop('Tarih', axis = 1)
        eak2 = eak2.drop('Saat', axis = 1)
        eak2 = eak2.set_index('DateTime')
        eak2 = pd.DataFrame(eak2['Barajlı'])
        eak2 = eak2.reset_index(drop=False)
        eak1 = pd.merge(eak1, eak2, how="outer", on=["DateTime", "DateTime"])
        print("İşlem tamamlandı")
        j = j + 1
        count = count + 1
        
        
eak1 = eak1.set_index('DateTime')
eak1 = eak1.set_axis(['EUAS', 'KALEHAN KALE ENERJI', 'KALEHAN BEYHAN1', 
                        'OYMAPINAR', 'BOYABAT', 
                        'KALEHAN ASAGI KALEKOY', 'LIMAK', 
                        'DOGUS ARTVIN', 'SANKO','ENERJISA',
                        'ATATURK', 'KARAKAYA', 'KEBAN', 
                        'BIRECIK', 'DERINER'], axis=1, inplace=False)

df2 = df2.reset_index(drop=False)
eak1 = eak1.reset_index(drop=False)

df2['DateTime'] = pd.to_datetime(df2.DateTime)
eak1['DateTime'] = pd.to_datetime(eak1.DateTime)

df2 = df2.set_index('DateTime')
eak1 = eak1.set_index('DateTime')

df2 = pd.concat([df2, eak1])
df2 = df2.reset_index(drop=False)
df2.drop_duplicates(subset="DateTime",keep = "last", inplace = True)
df2 = df2.set_index('DateTime')

df2.to_csv('HidroEAK.csv', index = True)

#%% PLOT

kuruluguc = [10687,627,582,540,513,500,420,332,331,1350,2405,1800,1330,672,670]

length=24

for iteration in range(len(kuruluguc)):
    kg = np.empty(length)
    kg.fill(kuruluguc[iteration])
    x_ax = range(length)
    plt.plot(x_ax, df[df.columns[iteration]].tail(length), linewidth=2, label="KGÜP")
    plt.plot(x_ax, kg, linewidth=2, label="Kurulu Güç")
    plt.plot(x_ax, df2[df.columns[iteration]].tail(length), linewidth=2, label="EAK")
    plt.title("{} {} KGUP-EAK".format(df.columns[iteration], tomorrow))
    plt.ylabel('MWh')
    plt.xlabel('Hours')
    plt.legend(loc='best',fancybox=True, shadow=True)
    plt.grid(True)
    #plt.savefig('{}24.png'.format(col))
    plt.show()

#%% EXPORTING PDF

x = pd.read_csv('HidroKGUP.csv')

x.tail(24).to_excel("Hydro_KGUP.xlsx")

fig, ax =plt.subplots(figsize=(12,4))
ax.axis('off')
the_table = ax.table(cellText=x[x.columns[0:8]].tail(24).values, colLabels = x.columns[0:8], loc='center', cellLoc='center')
the_table.set_fontsize(35)
plt.savefig("Hydro1_KGUP.pdf", format="pdf", bbox_inches = 'tight')

fig, ax =plt.subplots(figsize=(12,4))
ax.axis('off')
the_table = ax.table(cellText=x[x.columns[8:16]].tail(24).values, colLabels = x.columns[8:16], loc='center', cellLoc='center')
the_table.set_fontsize(35)
plt.savefig("Hydro2_KGUP.pdf", format="pdf", bbox_inches = 'tight')
