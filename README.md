terminal1:<br/>
#git clone https://github.com/vidstrancar/lweenc<br/>
#cd lweenc<br/>
#mkdir client1<br/>
#cp * client1<br/>
#mkdir client2<br/>
#cp * client2<br/>
#python3 server.py<br/>
<br/>
<br/>
terminal2:<br/>
#cd lweenc<br/>
#cd client1<br/>
#python3 klient.py<br/>
#register vid<br/>
<br/>
v trenutni mapi nastane datoteka 'privates.csv', kjer sta zapisana javni in zasebni ključ uporabnika vid. javni ključ se pošlje na server,
kjer se ta shrani v datoteko 'public_keys.csv'.<br/>
<br/>
<br/>
terminal3:<br/>
#cd lweenc<br/>
#cd client1<br/>
#python3 klient.py<br/>
#register tilen<br/>
#get vid<br/>
<br/>
terminal3 zaprosi server za javni ključ uporabnika vid. ta se shrani v datoteko 'public_keys.csv'.<br/>
<br/>
<br/>
terminal3:<br/>
#private vid kako si kaj?<br/>
<br/>
terminal3 šifrira z lwe sporočilo 'kako si kaj?' in ga pošlje serverju. ta ga broadcasta vsem povezanim odjemalcem. le uporabnik 'vid' ga bo uspešno odšifriral.<br/>


