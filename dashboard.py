import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import plotly.graph_objects as go

sns.set(style='dark')

bike_sharing_day_data = pd.read_csv("https://raw.githubusercontent.com/Earlyyyyy/dicoding-submission-data-analytics-streamlit/main/dashboard/bike_sharing_day.csv")
bike_sharing_hour_data = pd.read_csv("https://raw.githubusercontent.com/Earlyyyyy/dicoding-submission-data-analytics-streamlit/main/dashboard/bike_sharing_hour.csv")

bike_sharing_day_data['dateday'] = pd.to_datetime(bike_sharing_day_data['dateday'])

min_date = bike_sharing_day_data["dateday"].min()
max_date = bike_sharing_day_data["dateday"].max()

with st.sidebar:
    st.sidebar.header("Filter :")
    start_date, end_date = st.date_input(
        label="Date :",
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

filtered_data = bike_sharing_day_data[(bike_sharing_day_data["dateday"] >= pd.to_datetime(start_date)) &
                                      (bike_sharing_day_data["dateday"] <= pd.to_datetime(end_date))]

st.title("Dashboard Bike-Sharing :bike:")
st.markdown("---")
st.subheader(" How was the trend towards bike-sharing usage from 2011 to 2012?")
st.markdown("---")

users_by_month = filtered_data.groupby(by=["year", "month"]).agg({
    "count": "sum"
}).reset_index()

fig = go.Figure()

for year in users_by_month['year'].unique():
    data_year = users_by_month[users_by_month['year'] == year]
    fig.add_trace(go.Scatter(x=data_year['month'],
                             y=data_year['count'],
                             mode='lines+markers',
                             name=f"Year {year + 2011}",
                             hoverinfo='x+y'))

fig.update_layout(
    title="Count bike-sharing usage in 2011 to 2012",
    xaxis_title="Month",
    yaxis_title="Number of users",
    xaxis=dict(
        tickmode='array',
        tickvals=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
        ticktext=["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    ),
    hovermode="x"
)

st.plotly_chart(fig)

weather_data = filtered_data.groupby('weather_category')['count'].sum()
weather_dict = weather_data.to_dict()

weather_label = list(weather_dict.keys())
weather_values = list(weather_dict.values())

st.markdown("---")
st.subheader("How do weather conditions relate to bike-sharing service usage trends?")
st.markdown("---")
fig = go.Figure(data=[go.Pie(labels=weather_label,
                            values=weather_values,
                            textinfo='label+percent',
                            hoverinfo='label+value+percent',
                            marker=dict(colors=["skyblue", "lightcoral", "lightgreen"]))])

fig.update_layout(title_text="1 = Clear/Partly Cloud  2 = Misty/Cloudy  3 = Light Rain/Snow",
                  title_x=0.5,
                  title_font_size=12,
                  width=800,
                  height=600)

st.plotly_chart(fig)

st.markdown("---")
st.subheader("How does time affect the amount of bike-sharing usage?")
st.markdown("---")
fig, ax = plt.subplots(figsize=(10, 6))

sns.barplot(x='hour',
            y="count",
            data=bike_sharing_hour_data,
            hue="hour",
            palette="coolwarm",
            ax=ax)

ax.set_title("Bike-sharing usage based on time")
ax.set_xlabel("Time")
ax.set_ylabel("Total users : (x1.000.0000)")
plt.xticks(rotation=45)
st.pyplot(fig)

st.markdown("---")
st.subheader("What is the correlation between humidity and wind speed with total bike rentals?")
st.markdown("---")
filtered_data['humidity_bin'] = pd.cut(filtered_data['humidity'], bins=3, labels=["Low", "Medium", "High"])
filtered_data['windspeed_bin'] = pd.cut(filtered_data['windspeed'], bins=3, labels=["Low", "Medium", "High"])

fig, axes = plt.subplots(1, 2, figsize=(14, 7))

sns.scatterplot(
    x="humidity",
    y="count",
    hue="humidity_bin",
    palette="viridis",
    data=filtered_data,
    alpha=0.8,
    ax=axes[0]
)
axes[0].set_title("Humidity vs Count (Clustered by Humidity Bins)")

sns.scatterplot(
    x="windspeed",
    y="count",
    hue="windspeed_bin",
    palette="viridis",
    data=filtered_data,
    alpha=0.8,
    ax=axes[1]
)
axes[1].set_title("Windspeed vs Count (Clustered by Windspeed Bins)")
plt.tight_layout()
st.pyplot(fig)
