terminal1:
#git clone https://github.com/vidstrancar/lweenc
#cd lweenc
#mkdir client1
#mkdir client2
#python3 server.py


terminal2:
#cd lweenc
#cd client1
#python3 klient.py
#register vid

v trenutni mapi nastane datoteka 'privates.csv', kjer sta zapisana javni in zasebni ključ uporabnika vid. javni ključ se pošlje na server,
kjer se ta shrani v datoteko 'public_keys.csv'.


terminal3:
#cd lweenc
#cd client1
#python3 klient.py
#register tilen
#get vid

terminal3 zaprosi server za javni ključ uporabnika vid. ta se shrani v datoteko 'public_keys.csv'.


terminal3:
#private vid kako si kaj?

terminal3 šifrira z lwe sporočilo 'kako si kaj?' in ga pošlje serverju. ta ga broadcasta vsem povezanim odjemalcem. le uporabnik 'vid' ga bo uspešno odšifriral.


