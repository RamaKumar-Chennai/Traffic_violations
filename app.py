import streamlit as st
import pandas as pd
from connection_file import create_connection
from connection_file import res_fn
from connection_file import res_scalar_fn
from select_data import select_date
from select_data import select_unique_location
from select_data import select_location
from select_data import unique_vehicle_type_fn
from select_data import select_vehicle_type
from select_data import unique_race_fn
from select_data import select_race
from select_data import unique_gender_fn
from select_data import select_gender
from select_data import unique_vc_fn
from select_data import select_vc

from select_data import av_vc
from select_data import av_vt
from select_data import av_gender
from select_data import av_race

from select_data import high_risk_zones

from select_data import freq_makes_models

from select_data import select_highest_traffic_incident
from select_data import select_demo_corr_violation_type
from select_data import select_time_of_day
from select_data import select_day_of_week
from select_data import select_by_month
from select_data import select_vehicles_violations


st.title("🚦 Traffic Violations Insight System")
@st.cache_data
def load_data():
    df = pd.read_csv(r"D:\VS_CODE\Traffic_violations\Traffic_Violations_cleaned.csv")
    df["Date Of Stop"] = pd.to_datetime(df["Date Of Stop"])
    return df

 # Call once, cached
traffic_df = load_data() 

# Sidebar navigation
menu = st.sidebar.radio(
    "Choose the Option",
    ["Home", "Filter by Category","Analytical Views","Summary Statistics","Violation -Deeper Analysis"],index=None)

if menu=="Home":
 st.markdown(
    """
    

    Welcome to the **Traffic Violations Insight System** —  
    a data‑driven dashboard designed to analyze, visualize, and provide actionable insights into traffic violation records.

    ### Key Features
    - 📊 Interactive charts and tables for violation trends  
    - 🗺️ Geospatial mapping of accident hotspots  
    - 🔍 Search and filter by driver, city, or violation type  
    - 📈 KPI cards for quick recruiter‑friendly summaries  

    ---
    Use the sidebar to explore different datasets and gain deeper insights into traffic safety patterns.
    """
)
elif menu== "Filter by Category":

  
 filter_type=st.sidebar.selectbox("Enter the Filter Category",['Date', 'Location', 'Vehicle Type', 'Gender', 'Race', 'Violation Category'],index=None)
 if filter_type=='Date':
   select_date(traffic_df)
 elif filter_type=='Location':
    
    results=select_unique_location(traffic_df)
    location_choice=st.selectbox("Enter the Location Here",results,index=None)
    if location_choice:
      df=select_location(traffic_df,location_choice)
      if df.empty:
        st.error(f"No Violation Records for the location {location_choice} found")
      else:
       st.success(f"The Violation Records for the location {location_choice} :")
       st.dataframe(df)
 elif filter_type=='Vehicle Type':
   unique_vehicle_type= unique_vehicle_type_fn(traffic_df)
   vehicle_type_choice=st.selectbox("Enter the Vehicle Type Here",unique_vehicle_type,index=None)
   if vehicle_type_choice:
    df=select_vehicle_type(traffic_df,vehicle_type_choice)
    if df.empty:
        st.error(f"No Violation Records for the Vehicle Type - {vehicle_type_choice} found")
    else:
       st.success(f"The Number of Violation Records for the Vehicle Type - {vehicle_type_choice} : {len(df)}")
       st.success("The First 1000 Records :")
       st.dataframe(df.head(1000))

 elif filter_type=='Gender':
  unique_gender= unique_gender_fn(traffic_df)
  gender_choice=st.selectbox("Enter the Gender Here",unique_gender,index=None)
 
  if gender_choice:
    
    df=select_gender(traffic_df,gender_choice)
    if df.empty:
        st.error(f"No Violation Records for the Gender Type - {gender_choice} found")
    else:
       st.success(f"The Number of Violation Records for the Gender Type - {gender_choice} : {len(df)}")
       st.success("The First 1000 Records :")
       st.dataframe(df.head(1000))
 elif filter_type=='Race':
   unique_race= unique_race_fn(traffic_df)
   race_choice=st.selectbox("Enter the Race Here",unique_race,index=None)
   if race_choice:
    df=select_race(traffic_df,race_choice)
    if df.empty:
        st.error(f"No Violation Records for the Race Type - {race_choice} found")
    else:
       st.success(f"The Number of Violation Records for the Race - {race_choice} : {len(df)}")
       st.success("The First 1000 Records :")
       st.dataframe(df.head(1000))
 elif filter_type=='Violation Category':
   unique_vc= unique_vc_fn(traffic_df)
   vc_choice=st.selectbox("Enter the Violation Category Here",unique_vc,index=None)
   if vc_choice:
    df=select_vc(traffic_df,vc_choice)
    if df.empty:
        st.error(f"No Violation Records for the Violation Category Type - {vc_choice} found")
    else:
       st.success(f"The Number of Violation Records for the Violation Category - {vc_choice} : {len(df)}")
       st.success("The First 1000 Records :")
       st.dataframe(df.head(1000))

   


elif menu== "Analytical Views":
  av_choice=st.sidebar.radio("Enter your Choice Here",["Vehicle Type", "Gender", "Race", "Violation Category"],index=None)
  

  if av_choice=="Vehicle Type": 
    fig=av_vt(traffic_df)
    st.pyplot(fig)


  elif av_choice=="Gender": 
    fig=av_gender(traffic_df)
    st.pyplot(fig)


  elif av_choice=="Race": 
    fig=av_race(traffic_df)
    st.pyplot(fig)

  elif av_choice=="Violation Category":
    fig=av_vc(traffic_df)
    st.pyplot(fig)

      
elif menu== "Summary Statistics":
 ss_choice=st.sidebar.radio("Enter Your Choice Here",["Total violations and Violations Involving Accidents, Fatals, Personal Injury,Property Damage","High-Risk Zones","Most Frequently Cited Vehicle Makes/Models"],index=None)
 if ss_choice=="Total violations and Violations Involving Accidents, Fatals, Personal Injury,Property Damage":
   st.info(f"Total Number of Violations :  {len(traffic_df)}") 

   accident_count=(traffic_df["Accident"]==True).sum()   
   st.success(f"Violations Involving Accidents : {accident_count}")

   fatal_count=(traffic_df["Fatal"]==True).sum()   
   st.success(f"Violations Involving Fatals : {fatal_count}")
   
   
 
   fatal_accident_count=((traffic_df["Fatal"]==True) & (traffic_df["Accident"]==True)).sum()   
   st.success(f"Violations Involving Fatals and Accidents: {fatal_accident_count}")

      
  
   Personal_Injury_count=(traffic_df["Personal Injury"]==True).sum()   
   st.success(f"Violations Involving Personal Injury : {Personal_Injury_count}")
 
 
   Property_Damage_count=(traffic_df["Property Damage"]==True).sum()   
   st.success(f"Violations Involving Property Damage : {Property_Damage_count}")


   all_count=((traffic_df["Accident"]==True) & (traffic_df["Fatal"]==True) & (traffic_df["Personal Injury"] ==True) & (traffic_df["Property Damage"] ==True)).sum()   
   st.success(f"Violations Involving Accident,Fatals,Personal Injury,Property Damage : {all_count}")

      
 elif ss_choice=="High-Risk Zones":
   
  fig1,fig2,df=high_risk_zones(traffic_df)
  st.error("High Risk Zones")
  st.dataframe(df)
  
  #Distribution of Risk Score column
  st.subheader("Distribution of Risk Score column")
  st.write(df["RiskScore"].describe())

  st.pyplot(fig1)

  st.subheader("📊 Distribution of Risk Scores")
  st.pyplot(fig2)

 elif ss_choice=="Most Frequently Cited Vehicle Makes/Models":
   make_df,model_df=freq_makes_models(traffic_df)
   st.success("Most Frequently Cited Vehicle Makes")
   st.dataframe(make_df)

   st.success("Unique Models for the Most Frequently Cited  Makes")
   st.dataframe(model_df)



elif menu=="Violation -Deeper Analysis":
  vda_choice=st.sidebar.radio("Enter your choice here",["Areas or Coordinates with Highest Traffic Incidents","Locations with Highest Number of Unique Violation Categoies","Violation Frequency variation","Types of Vehicles most often involved in Violations"],index=None)
  if vda_choice=="Areas or Coordinates with Highest Traffic Incidents":
     max_incident_row_df,incident_count_df=select_highest_traffic_incident(traffic_df)
     
     st.success("Areas / Coordinates with  the Highest Traffic Incidents")
     st.dataframe(incident_count_df)

     st.success("Area / Coordinate with  the Highest Traffic Incidents")
     st.dataframe(max_incident_row_df)

  elif vda_choice=="Locations with Highest Number of Unique Violation Categoies":
    corr_df=select_demo_corr_violation_type(traffic_df)
    st.dataframe(corr_df)
  elif vda_choice=="Violation Frequency variation":
    violation_freq_choice=st.sidebar.radio("Enter your choice here",["By Time of Day","By Weekday","By Month"],index=None)
    if violation_freq_choice=="By Time of Day":
      fig,df=select_time_of_day(traffic_df)
      st.success("Violation Frequency variation By Time of Day : ")
      st.dataframe(df,hide_index=True)
      st.pyplot(fig)
    elif violation_freq_choice=="By Weekday":
      fig,df=select_day_of_week(traffic_df)
      st.success("Violation Frequency variation By Day of Week : ")
      st.dataframe(df,hide_index=True)
      st.pyplot(fig)
    elif violation_freq_choice=="By Month":
      fig,df=select_by_month(traffic_df)
      st.success("Violation Frequency variation By Month : ")
      st.dataframe(df,hide_index=True)
      st.pyplot(fig)
  elif vda_choice=="Types of Vehicles most often involved in Violations":
      fig,df=select_vehicles_violations(traffic_df)  
      st.dataframe(df,hide_index=True)
      st.pyplot(fig)
     