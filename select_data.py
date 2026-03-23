from connection_file import create_connection
from connection_file import res_fn
from connection_file import res_scalar_fn
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def select_date(traffic_df):
    min_dt = traffic_df["Date Of Stop"].min().date()
    max_dt = traffic_df["Date Of Stop"].max().date()

    start_date = st.date_input(
    "Choose Start Date",
    value=min_dt,
    min_value=min_dt,
    max_value=max_dt    )

    end_date = st.date_input(
    "Choose End Date",
    value=max_dt,
    min_value=min_dt,
    max_value=max_dt)

    
    if st.button("View Records in Date Range"):
        mask = (traffic_df["Date Of Stop"] >= pd.to_datetime(start_date)) & \
               (traffic_df["Date Of Stop"] <= pd.to_datetime(end_date))
        filtered_df = traffic_df.loc[mask]
        st.info(f"There are {len(filtered_df)} records in this Date Range")
        st.success("The First 1000 records are: ")
        st.dataframe(filtered_df.head(1000))



def select_unique_location(traffic_df):
 conn=create_connection()
 query="select distinct Location_clean from traffic_violations_cleaned"
 results=res_scalar_fn(conn,query)
 #print("results for location are ",results)
 print(results[0][0])
 results_clean=[i[0] for i in results]
 return results_clean


def select_location(traffic_df,location_choice):
   conn=create_connection()
   query=f"select * from traffic_violations_cleaned where Location_clean='{location_choice}' "
   df=res_fn(conn,query)
   return df

def unique_vehicle_type_fn(traffic_df):
 conn=create_connection()
 query="select distinct VehicleType_clean from traffic_violations_cleaned"
 results=res_scalar_fn(conn,query)
 print(results[0][0])
 results_clean=[i[0] for i in results]
 return results_clean


def select_vehicle_type(traffic_df,vehicle_type_choice):
   conn=create_connection()
   query=f"select * from traffic_violations_cleaned where VehicleType_clean='{vehicle_type_choice}' "
   df=res_fn(conn,query)
   return df


def unique_gender_fn(traffic_df):
 conn=create_connection()
 query="select distinct Gender_clean from traffic_violations_cleaned"
 results=res_scalar_fn(conn,query)
 print(results[0][0])
 results_clean=[i[0] for i in results]
 print("results_clean is ",results_clean)

 return results_clean

def select_gender(traffic_df,gender_choice):
   conn=create_connection()
   query=f"select * from traffic_violations_cleaned where Gender_clean ='{gender_choice}' "
   df=res_fn(conn,query)
   return df

def unique_race_fn(traffic_df):
 conn=create_connection()
 query="select distinct Race from traffic_violations_cleaned"
 results=res_scalar_fn(conn,query)
 print(results[0][0])
 results_clean=[i[0] for i in results]
 return results_clean

def select_race(traffic_df,race_choice):
   conn=create_connection()
   query=f"select * from traffic_violations_cleaned where Race='{race_choice}' "
   df=res_fn(conn,query)
   return df

def unique_vc_fn(traffic_df):
 conn=create_connection()
 query="select distinct Violation_Category from traffic_violations_cleaned"
 results=res_scalar_fn(conn,query)
 print(results[0][0])
 results_clean=[i[0] for i in results]
 return results_clean

    
def select_vc(traffic_df,vc_choice):
   conn=create_connection()
   query=f"select * from traffic_violations_cleaned where Violation_Category='{vc_choice}' "
   df=res_fn(conn,query)
   return df


def av_vt(traffic_df):
   # Count occurrences per category-DataFrame 
   Vehicle_Type_df = traffic_df['VehicleType_clean'].value_counts().reset_index()
   Vehicle_Type_df.columns = ['Vehicle_Type', 'Count']


   Vehicle_Type_df['Percent'] = (Vehicle_Type_df['Count'] / Vehicle_Type_df['Count'].sum()) * 100
   
   # Output
   print(Vehicle_Type_df)  # preview top categories

   fig,ax=plt.subplots(figsize=(15,6))
   sns.barplot(data=Vehicle_Type_df,x="Vehicle_Type",y="Percent",color="blue")
   ax.set_title("Top Vehicle_Types with the Count Percentage")
   ax.set_xlabel("Vehicle_Type")
   ax.set_ylabel("Percent")
   ax.set_yscale('log')
   # Rotate labels vertically for clarity
   plt.xticks(rotation=90)
   # Prevent labels from being cut off
   plt.tight_layout()

   return fig




def av_gender(traffic_df):
   # Count occurrences per category-DataFrame 
   Gender_Type_df = traffic_df['Gender_clean'].value_counts().reset_index()
   Gender_Type_df.columns = ['Gender_Type', 'Count']

   # Output
   print(Gender_Type_df)  # preview top categories

   fig,ax=plt.subplots(figsize=(8,6))
   sns.barplot(data=Gender_Type_df,x="Gender_Type",y="Count",color="blue")
   ax.set_title("Gender_Types with the Count")
   ax.set_xlabel("Gender_Type")
   ax.set_ylabel("Count")
   ax.set_yscale('log')
   return fig



def av_race(traffic_df):
   # Count occurrences per category-DataFrame 
   Race_Type_df = traffic_df['Race'].value_counts().reset_index()
   Race_Type_df.columns = ['Race', 'Count']

   # Output
   print(Race_Type_df)  # preview top categories

   fig,ax=plt.subplots(figsize=(8,6))
   sns.barplot(data=Race_Type_df,x="Race",y="Count",color="blue")
   ax.set_title("Race_Types with the Count")
   ax.set_xlabel("Race_Type")
   ax.set_ylabel("Count")
   plt.xticks(rotation=45)
   return fig





def av_vc(traffic_df):
  # Count occurrences per category-DataFrame 
   violation_counts_df = traffic_df['Violation_Category'].value_counts().reset_index()
   violation_counts_df.columns = ['ViolationCategory', 'Count']

  # Output
   print(violation_counts_df)  # preview top categories

   fig,ax=plt.subplots(figsize=(8,6))
   sns.barplot(data=violation_counts_df,x="ViolationCategory",y="Count",color="red")
   ax.set_title("Top Violation Categories with the Count")
   ax.set_xlabel("Violation-Category")
   ax.set_ylabel("Count")
   plt.xticks(rotation=45)
   return fig

def high_risk_zones(traffic_df):

   
   risk_df = (
    traffic_df.groupby(['Location_clean', 'Latitude', 'Longitude'])[
        ['Fatal', 'Accident', 'Personal Injury', 'Property Damage',
         'Contributed To Accident', 'Alcohol', 'Belts']
    ]
    .sum()   # True/False → 1/0, so sum gives counts
    .reset_index()
    )
   # After building risk_df
   risk_df['RiskScore'] = (
    risk_df['Fatal'] * 5 +                # highest severity
    risk_df['Accident'] * 3 +             # major crashes
    risk_df['Personal Injury'] * 2 +      # injuries
    risk_df['Property Damage'] * 1 +      # minor severity
    risk_df['Contributed To Accident'] * 2 +  # causal factor
    risk_df['Alcohol'] * 4 +              # alcohol-related violations
    risk_df['Belts'] * 2                  # seat belt violations
   )
   risk_df=risk_df.sort_values('RiskScore',ascending=False)
   

   #Geographical Hotspots of Traffic Violation Plot
   import matplotlib.pyplot as plt

   fig1, ax = plt.subplots(figsize=(10,8))
   scatter = ax.scatter(
    risk_df['Longitude'], risk_df['Latitude'],
    c=risk_df['RiskScore'], cmap='hot', s=50
)
   plt.colorbar(scatter, ax=ax, label="Risk Score")
   ax.set_title("Geographical Hotspots of Traffic Violations")
   ax.set_xlabel("Longitude")
   ax.set_ylabel("Latitude")
  
   log_scale = st.checkbox("Use log scale for Risk Score")
   fig2, ax = plt.subplots()
   risk_df["RiskScore"].hist(bins=100, ax=ax, color="skyblue", edgecolor="black")
   if log_scale:
    ax.set_xscale("log")
    ax.set_xlabel("Risk Score")
    ax.set_ylabel("Frequency")
    ax.set_title("Distribution of Risk Scores")

  
   return fig1,fig2,risk_df


def freq_makes_models(traffic_df):
   make_count_df = traffic_df['Make_clean'].value_counts().reset_index(name="Count").sort_values("Count",ascending=False)
   
   models_per_make = (
    traffic_df.groupby('Make_clean')['Model_clean']
    .nunique()
    .reset_index(name='Num_of_Unique_Models')
    .sort_values("Num_of_Unique_Models",ascending=False)
)

   print(models_per_make.head())
   return  make_count_df,models_per_make

def select_highest_traffic_incident(traffic_df):
    incident_count_df = (
        traffic_df.groupby(["Location_clean","Latitude","Longitude"])
                  .size()
                  .reset_index(name="incident_count")
                  .sort_values("incident_count", ascending=False)
    )
    incident_count_df=incident_count_df.reset_index(drop=True)
    # Get the row with max incidents as a DataFrame, not Series
    max_incident_row_df = incident_count_df.head(1).reset_index(drop=True)
    
    return max_incident_row_df, incident_count_df


def select_demo_corr_violation_type(traffic_df):
   
   # Group by Location, Latitude, Longitude
   corr_df = traffic_df.groupby(["Location_clean", "Latitude", "Longitude"])['Violation_Category'].agg(
    Count='count',          # number of violations
    Unique_Categories=lambda x: x.unique().tolist(),  # unique categories only
    Num_Unique_Categories=lambda x: x.nunique()  # length of unique categories

     ).reset_index().sort_values('Num_Unique_Categories',ascending=False)

   print(corr_df.head())
   
   return corr_df




def select_time_of_day(traffic_df):
    
    # Convert to datetime
    traffic_df['Time Of Stop'] = pd.to_datetime(traffic_df['Time Of Stop'], errors="coerce")

    # Define custom time-of-day bins
    def time_of_day(t):
        h = t.hour
        if h >= 21 or h < 6:
            return "Night (9 PM–6 AM)"
        elif h < 12:
            return "Morning (6 AM–12 PM)"
        elif h < 16:
            return "Afternoon (12 PM–4 PM)"
        else:
            return "Evening (4 PM–9 PM)"

    traffic_df['TimeOfDay'] = traffic_df['Time Of Stop'].apply(time_of_day)

    # Group by time of day
    time_of_day_df = (
        traffic_df.groupby('TimeOfDay')['Violation_Category']
        .count()
        .reset_index(name='Violation_Count_By_Time')
    )

    # Define chronological order
    time_order = [
        
        "Morning (6 AM–12 PM)",
        "Afternoon (12 PM–4 PM)",
        "Evening (4 PM–9 PM)",
        "Night (9 PM–6 AM)"
    ]

    # Reindex to enforce order
    time_of_day_df = time_of_day_df.set_index('TimeOfDay').loc[time_order].reset_index()

    # Plot with order
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.barplot(
        data=time_of_day_df,
        x="TimeOfDay",
        y="Violation_Count_By_Time",
        color="blue",
        order=time_order
    )
    ax.set_title("Violation Frequency Variation By Time of Day")
    ax.set_xlabel("Time of Day")
    ax.set_ylabel("Violation Count")
    plt.xticks(rotation=45)

    print(time_of_day_df)
    return fig, time_of_day_df




def select_day_of_week(traffic_df):
    # Extract weekday name
    traffic_df['Weekday'] = traffic_df['Date Of Stop'].dt.day_name()

    # Group by weekday
    weekday_df = (
        traffic_df.groupby('Weekday')['Violation_Category']
        .count()
        .reset_index(name='Violation_Count_By_Day')
    )

    # Define chronological order
    weekday_order = [
        "Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"
    ]

    # Reindex to enforce order
    weekday_df = weekday_df.set_index('Weekday').loc[weekday_order].reset_index()

    # Plot with order
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.barplot(
        data=weekday_df,
        x="Weekday",
        y="Violation_Count_By_Day",
        color="blue",
        order=weekday_order
    )
    ax.set_title("Violation Frequency Variation By Day of Week")
    ax.set_xlabel("Day of Week")
    ax.set_ylabel("Violation Count")
    plt.xticks(rotation=45)

    print(weekday_df)
    return fig, weekday_df



def select_by_month(traffic_df):
   # Extract weekday name from Date Of Stop
  traffic_df['Month'] = traffic_df['Date Of Stop'].dt.month_name()


  # Group by weekday and count violations
  month_df = (
    traffic_df.groupby('Month')['Violation_Category']
    .count()
    .reset_index(name='Violation_Count_By_Month')
    
   )
  
  # Define chronological order
  month_order = [
        "January","February","March","April","May","June",
        "July","August","September","October","November","December"
    ]

    # Reindex to enforce Jan → Dec order
  month_df = month_df.set_index('Month').loc[month_order].reset_index()

  fig,ax=plt.subplots(figsize=(8,6))
  sns.barplot(data=month_df,x="Month",y='Violation_Count_By_Month',color="blue")
  ax.set_title("Violation Frequency variation By Month")
  ax.set_xlabel("Month")
  ax.set_ylabel("Violation Count By Month")
  plt.xticks(rotation=45)

  print(month_df)
  return fig, month_df


def select_vehicles_violations(traffic_df):
   vehicle_df = (
    traffic_df.groupby('VehicleType_clean')['Violation_Category']
    .count()
    .reset_index(name='Violation_Count_By_Vehicle')
    .sort_values('Violation_Count_By_Vehicle',ascending=False)
    
   )
   print("vehicle df is ",vehicle_df)

   fig,ax=plt.subplots(figsize=(8,6))
   sns.barplot(data=vehicle_df.head(10),x="VehicleType_clean",y='Violation_Count_By_Vehicle',color="blue")
   ax.set_title("TOP 10 VehicleTypes Involved  in frequent Traffic Violations")
   ax.set_xlabel("VehicleType")
   ax.set_ylabel("Violation Count By VehicleType")
   ax.set_yscale('log')
   plt.xticks(rotation=45)

   return fig,vehicle_df