import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.ensemble import RandomForestRegressor
import pickle

#load model
# filename = 'carprice_model.pha'
filename = 'x_model.sav'
loaded_model = pickle.load(open(filename, 'rb'))
    
def predictCar(brand,province,colour,mile,old):
#     brand = 'Toyota,Corolla'
#     province = 'กรุงเทพและปริมณฑล'
#     colour = 'ขาว'
#     mile = 147500.0
#     old = 8
    def find_basic_data_car(brand,province,colour,mile,old):
    
        def findMax(v):
        #     v = 'engine'
            max_name = ''
            max_n = 0
            for i in df[v].unique():
                if df[df[v]==i].shape[0] > max_n:
                    max_n = df[df[v]==i].shape[0]
                    max_name = i
            return max_name

        df = pd.read_csv("car_clean.csv",header=0)
        df = df[df.brand == brand]
        if len(df[df.old == old]) > 0:
            df = df[df.old == old]

        engine = findMax('engine')
        gear = findMax('gear')
        seat = findMax('seat')
        fuel = findMax('fuel')

        return engine,gear,seat,fuel




    engine,gear,seat,fuel = find_basic_data_car(brand,province,colour,mile,old)
    
    print('engine :', engine)
    print('gear :', gear)
    print('seat :', seat)
    print('fuel :', fuel)
    
    post = 0

    df = pd.read_csv("car_clean.csv",header=0)

    x = df.drop(['price'],axis=1)
    y = df['price']
    y = np.ravel(y);

    # t = ['Toyota,Corolla',147500.0,8,1986,'A',5,'กรุงเทพและปริมณฑล','ขาว','Petrol',1] #5567
    t = [brand,mile,old,engine,gear,seat,province,colour,fuel,post]
    h = ['brand','mile','old','engine','gear','seat','province','colour','fuel','post']
    df2 = pd.DataFrame([t], columns=h)
    x2 = x.append(df2, ignore_index=True)



    scaler = MinMaxScaler(feature_range=(0,1))


    x2["mile"]=scaler.fit_transform(x2[["mile"]])
    x2["old"]=scaler.fit_transform(x2[["old"]])
    x2["engine"]=scaler.fit_transform(x2[["engine"]])
    x2["post"]=scaler.fit_transform(x2[["post"]])
    
    x2 = pd.get_dummies(x2, dummy_na = False, columns=['brand', 'gear', 'seat','province','colour','fuel'])

    y_pred2 = loaded_model.predict([x2.loc[x2.shape[0]-1]])

    return y_pred2[0]

from firebase import Firebase

config = {
  "apiKey": "AIzaSyBGv_05cA2Qm1QEuKUZ4U-hFCiyxc1e_8A",
  "authDomain": "car-price-bbaa2.firebaseapp.com",
  "databaseURL": "https://car-price-bbaa2.firebaseio.com",
  "storageBucket": "car-price-bbaa2.appspot.com",
  "serviceAccount": "car-price-bbaa2-firebase-adminsdk-hk1k5-7dd02ad457.json"
    
}

firebase = Firebase(config)
db = firebase.database()


def set_events():
    all_events = db.child("events").get()
    e = []
    for i in all_events.each():
        e.append(i.key())
    return set(e)

result = set_events()
while True:
    add = set_events() - result
    if len(add) > 0:
        print('add :', add)
        for i in add:
            x = db.child("events/"+str(i)).get()
            brand = x.val()['brand']
            year = x.val()['year']
            mile = x.val()['mile']
            colour = x.val()['colour']
            province = x.val()['province']

            old = 2020-int(year)

            print(type(brand))
            print(year)
            print(mile)
            print(type(colour))
            print(province)

            p = predictCar(brand,province,colour,mile,old)
            print('price {i} :::::::',p)
            db.child("events").child(str(i)+'/y').set(p)

        result = set_events()
        