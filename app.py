import json
from datetime import date, timedelta
import streamlit as st
from src.data import load_flights, airport_options
from src.utils import filter_flights, sort_flights, format_duration, format_price, flight_to_export

st.set_page_config(page_title='SkySearch — Flight Search',page_icon='✈️',layout='wide',initial_sidebar_state='expanded')
st.markdown('''<style>
.main{background:#f6f8fc}.block-container{padding-top:1.4rem;max-width:1450px}.hero{padding:1.4rem 1.6rem;border-radius:20px;background:linear-gradient(135deg,#0b1f3a,#164e8c,#2478d8);color:white;margin-bottom:1rem}.hero h1{margin:0;font-size:2.15rem}.hero p{margin:.35rem 0 0;opacity:.88}.search-card,.flight-card{background:white;border:1px solid #e5e9f0;border-radius:18px;padding:1.1rem;margin-bottom:1rem;box-shadow:0 5px 18px rgba(15,23,42,.05)}.airline{font-weight:700}.muted{color:#64748b;font-size:.86rem}.route{font-size:1.45rem;font-weight:750}.price{font-size:1.35rem;font-weight:800;color:#0b5cab}.pill{display:inline-block;padding:.18rem .5rem;border-radius:999px;background:#eef5ff;color:#155eaa;font-size:.75rem;font-weight:650;margin-right:.25rem}.stButton>button{border-radius:10px;font-weight:650}
</style>''',unsafe_allow_html=True)

airports=airport_options(); flights=load_flights()
if 'searched' not in st.session_state: st.session_state.searched=False
if 'selected_flight' not in st.session_state: st.session_state.selected_flight=None
st.markdown('<div class="hero"><h1>✈️ SkySearch</h1><p>Search, compare and inspect flights in one clean dashboard.</p></div>',unsafe_allow_html=True)

with st.container():
    st.markdown('<div class="search-card">',unsafe_allow_html=True)
    c1,c2,c3=st.columns([1,1,1])
    with c1: trip_type=st.radio('Trip type',['Round trip','One way'],horizontal=True)
    with c2: origin=st.selectbox('From',list(airports),format_func=lambda x:f'{x} — {airports[x][0]}',index=list(airports).index('DEL'))
    with c3: destination=st.selectbox('To',list(airports),format_func=lambda x:f'{x} — {airports[x][0]}',index=list(airports).index('BOM'))
    d1,d2,d3,d4=st.columns([1.2,1.2,1,1])
    with d1: travel_date=st.date_input('Departure date',value=date.today(),min_value=date.today(),max_value=date.today()+timedelta(days=30))
    with d2: return_date=st.date_input('Return date',value=min(date.today()+timedelta(days=5),date.today()+timedelta(days=30)),min_value=date.today(),max_value=date.today()+timedelta(days=30),disabled=trip_type=='One way')
    with d3: passengers=st.number_input('Passengers',1,9,1)
    with d4: cabin=st.selectbox('Cabin',['Any','Economy','Premium Economy'])
    if origin==destination: st.warning('Please choose different departure and arrival airports.')
    if st.button('🔎 Search flights',type='primary',use_container_width=True): st.session_state.searched=True; st.session_state.selected_flight=None
    st.markdown('</div>',unsafe_allow_html=True)

with st.sidebar:
    st.header('Filters'); max_price=st.slider('Maximum fare',2000,12000,12000,step=250)
    all_airlines=sorted(flights.airline.unique().tolist()); airlines=st.multiselect('Airlines',all_airlines,default=all_airlines)
    max_stops=st.selectbox('Stops',['Any','0','1','2']); refundable_only=st.checkbox('Refundable fares only')
    depart_window=st.selectbox('Departure time',['Any','00-06','06-12','12-18','18-24']); sort_mode=st.selectbox('Sort by',['Cheapest','Fastest','Earliest departure','Latest departure'])

if st.session_state.searched and origin!=destination:
    result=filter_flights(flights,origin,destination,travel_date.isoformat(),passengers,max_price,airlines,max_stops,cabin,refundable_only,depart_window)
    result=sort_flights(result,sort_mode).reset_index(drop=True)
    st.markdown(f'### {len(result)} flight options')
    if len(result):
        a,b,c,d=st.columns(4); a.metric('Results',len(result)); b.metric('From',format_price(result.price.min())); c.metric('Fastest',format_duration(result.duration_min.min())); d.metric('Airlines',result.airline.nunique())
        for idx,row in result.iterrows():
            st.markdown('<div class="flight-card">',unsafe_allow_html=True); cols=st.columns([1.25,1.1,1.1,1.05,1.0])
            with cols[0]: st.markdown(f'**{row.airline}**'); st.caption(f'{row.code} · {row.flight_no}'); st.markdown(f"<span class='pill'>{row.cabin}</span><span class='pill'>{row.baggage}</span>",unsafe_allow_html=True)
            with cols[1]: st.markdown(f"<div class='route'>{row.departure}</div><div>{row.origin}</div>",unsafe_allow_html=True)
            with cols[2]: st.markdown(f"<div class='muted'>✈ {format_duration(row.duration_min)}</div><div>{'Non-stop' if row.stops==0 else str(row.stops)+' stop(s)'}</div>",unsafe_allow_html=True)
            with cols[3]: st.markdown(f"<div class='route'>{row.arrival}</div><div>{row.destination}</div>",unsafe_allow_html=True)
            with cols[4]:
                st.markdown(f"<div class='price'>{format_price(row.price)}</div><div class='muted'>per passenger</div>",unsafe_allow_html=True)
                if st.button('View details',key=f'details_{idx}',use_container_width=True): st.session_state.selected_flight=row.to_dict()
            st.markdown('</div>',unsafe_allow_html=True)
        st.markdown('### Export results'); export_df=result.copy(); export_df['duration']=export_df.duration_min.map(format_duration); csv=export_df.to_csv(index=False).encode('utf-8'); json_data=json.dumps([flight_to_export(r) for _,r in result.iterrows()],indent=2,ensure_ascii=False)
        e1,e2=st.columns(2)
        with e1: st.download_button('⬇️ Download CSV',csv,'flight_results.csv','text/csv',use_container_width=True)
        with e2: st.download_button('⬇️ Download JSON',json_data,'flight_results.json','application/json',use_container_width=True)
    else: st.info('No flights match the selected filters. Try increasing the maximum fare or allowing more stops.')
elif not st.session_state.searched: st.info('Choose your route and filters, then click **Search flights**.')

if st.session_state.selected_flight:
    r=st.session_state.selected_flight; st.divider(); st.markdown('## ✈️ Flight details'); x1,x2,x3=st.columns(3); x1.metric('Airline',f"{r['airline']} {r['flight_no']}"); x2.metric('Duration',format_duration(r['duration_min'])); x3.metric('Fare',format_price(r['price']))
    left,right=st.columns(2)
    with left:
        st.markdown('#### Itinerary'); st.write(f"**{r['origin']} {r['departure']}** → **{r['destination']} {r['arrival']}**"); st.write(f"Travel date: {r['date']}"); st.write(f"Stops: {'Non-stop' if r['stops']==0 else str(r['stops'])+' stop(s)'}"); st.write(f"Aircraft: {r['aircraft']}")
    with right:
        st.markdown('#### Fare information'); st.write(f"Baggage allowance: **{r['baggage']}**"); st.write(f"Cabin: **{r['cabin']}**"); st.write(f"Meal: **{r['meal']}**"); st.write(f"Refundable: **{'Yes' if r['refundable'] else 'No'}**"); st.write(f"Seats remaining: **{r['seats']}**")
    st.success('Demo booking flow: this project displays simulated inventory and does not issue real tickets.')
st.caption('SkySearch • Portfolio demo • Flight data is simulated for development and demonstration.')
