def format_duration(minutes):
    h,m=divmod(int(minutes),60); return f'{h}h {m:02d}m'
def format_price(value): return f'₹{int(value):,}'
def filter_flights(df,origin,destination,travel_date,passengers,max_price,airlines,max_stops,cabin,refundable_only,depart_window):
    out=df[(df.origin==origin)&(df.destination==destination)&(df.date==travel_date)].copy(); out=out[out.price<=max_price]
    if airlines: out=out[out.airline.isin(airlines)]
    if max_stops!='Any': out=out[out.stops<=int(max_stops)]
    if cabin!='Any': out=out[out.cabin==cabin]
    if refundable_only: out=out[out.refundable]
    if depart_window!='Any':
        lo,hi=map(int,depart_window.split('-')); hours=out.departure.str[:2].astype(int); out=out[(hours>=lo)&(hours<hi)]
    return out
def sort_flights(df,mode):
    if mode=='Cheapest': return df.sort_values(['price','duration_min'])
    if mode=='Fastest': return df.sort_values(['duration_min','price'])
    if mode=='Earliest departure': return df.sort_values('departure')
    if mode=='Latest departure': return df.sort_values('departure',ascending=False)
    return df.sort_values('price')
def flight_to_export(row):
    d=row.to_dict(); d['duration']=format_duration(d['duration_min']); d['price_display']=format_price(d['price']); return d
