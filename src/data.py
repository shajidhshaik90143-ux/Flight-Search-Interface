from datetime import date, timedelta
import random
import pandas as pd

AIRPORTS = {
    'DEL': ('New Delhi', 'Indira Gandhi International'), 'BOM': ('Mumbai', 'Chhatrapati Shivaji Maharaj International'),
    'BLR': ('Bengaluru', 'Kempegowda International'), 'HYD': ('Hyderabad', 'Rajiv Gandhi International'),
    'MAA': ('Chennai', 'Chennai International'), 'CCU': ('Kolkata', 'Netaji Subhas Chandra Bose International'),
    'GOI': ('Goa', 'Manohar International'), 'PNQ': ('Pune', 'Pune International'),
    'AMD': ('Ahmedabad', 'Sardar Vallabhbhai Patel International'), 'COK': ('Kochi', 'Cochin International'),
    'VGA': ('Vijayawada', 'Vijayawada International'), 'VTZ': ('Visakhapatnam', 'Visakhapatnam International')
}
AIRLINES = [('IndiGo','6E'),('Air India','AI'),('Air India Express','IX'),('Akasa Air','QP'),('SpiceJet','SG'),('Vistara','UK')]
ROUTES = [('DEL','BOM'),('DEL','BLR'),('DEL','HYD'),('DEL','MAA'),('DEL','CCU'),('BOM','BLR'),('BOM','HYD'),('BOM','GOI'),('BOM','PNQ'),('BLR','HYD'),('BLR','MAA'),('BLR','COK'),('HYD','MAA'),('HYD','VGA'),('MAA','COK'),('CCU','BLR'),('AMD','BOM'),('VTZ','HYD'),('VTZ','BLR'),('VGA','BLR')]

def _generate():
    random.seed(42); rows=[]; base=date.today()
    for day_offset in range(31):
        d=base+timedelta(days=day_offset)
        for origin,destination in ROUTES:
            for n in range(2):
                airline,code=AIRLINES[(day_offset+n+len(origin))%len(AIRLINES)]
                dep_hour=random.choice([5,7,9,11,13,15,17,19,21]); dep_min=random.choice([0,15,30,45])
                duration=random.randint(80,230); arr=(dep_hour*60+dep_min+duration); arr_hour=(arr//60)%24; arr_min=arr%60
                stops=random.choices([0,1,2],weights=[60,34,6])[0]
                rows.append({'date':d.isoformat(),'airline':airline,'code':code,'flight_no':f'{code}{random.randint(100,999)}','origin':origin,'destination':destination,'departure':f'{dep_hour:02d}:{dep_min:02d}','arrival':f'{arr_hour:02d}:{arr_min:02d}','duration_min':duration,'stops':stops,'cabin':random.choice(['Economy','Economy','Economy','Premium Economy']),'price':random.randint(2800,8200)+stops*750,'baggage':random.choice(['15 kg','15 kg','20 kg','25 kg']),'seats':random.randint(3,42),'refundable':random.choice([True,False,True]),'aircraft':random.choice(['Airbus A320neo','Airbus A321','Boeing 737 MAX','Airbus A320']),'meal':random.choice(['Buy on board','Complimentary','Buy on board'])})
    return pd.DataFrame(rows)

_FLIGHTS=_generate()
def load_flights(): return _FLIGHTS.copy()
def airport_options(): return AIRPORTS
