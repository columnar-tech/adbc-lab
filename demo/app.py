import os
import time
import pandas as pd
import pydeck as pdk
import streamlit as st

st.set_page_config(page_title="Citi Bike Explorer", layout="wide")

# --- Config ---
POSTGRES_URI = os.getenv("POSTGRES_URI", "postgresql://postgres:postgres@localhost:5432/postgres")

# --- Sidebar ---
question = st.sidebar.radio(
    "Question",
    options=[
        "Busiest stations",
        "Most popular routes",
        "Rebalancing needs",
    ],
)

num_trips = st.sidebar.select_slider(
    "Number of trips to fetch",
    options=[50_000, 100_000, 250_000, 500_000, 1_000_000],
    value=500_000,
    format_func=lambda x: f"{x:,}",
)

user_type = st.sidebar.radio(
    "User type",
    options=["All", "Subscriber", "Customer"],
    horizontal=True,
)

# --- Build query ---
where_clauses = []
if user_type != "All":
    where_clauses.append(f"usertype = '{user_type}'")

where_sql = f"WHERE {' AND '.join(where_clauses)}" if where_clauses else ""
query = f"SELECT * FROM trips {where_sql} ORDER BY starttime DESC LIMIT {num_trips}"

# --- Header ---
st.title("Citi Bike Explorer")
connector = st.toggle("Use ADBC (columnar)", value=False)
connector_label = "ADBC (columnar)" if connector else "psycopg2 (row-based)"

# --- Fetch data (timed) ---
query_start = time.perf_counter()

if not connector:
    import psycopg2
    conn = psycopg2.connect(POSTGRES_URI)
    cursor = conn.cursor()
    cursor.execute(query)
    columns = [desc[0] for desc in cursor.description]
    rows = cursor.fetchall()
    trips = pd.DataFrame(rows, columns=columns)
    cursor.close()
    conn.close()
else:
    from adbc_driver_manager import dbapi
    conn = dbapi.connect(driver="postgresql", db_kwargs={"uri": POSTGRES_URI})
    cursor = conn.cursor()
    cursor.execute(query)
    trips = cursor.fetch_arrow_table().to_pandas()
    cursor.close()
    conn.close()

load_time = time.perf_counter() - query_start

col_metric1, col_metric2 = st.columns(2)
col_metric1.metric("Connector", connector_label)
col_metric2.metric("Query time", f"{load_time:.3f}s", help=f"{len(trips):,} trips fetched")
st.divider()

# --- Results ---
if question == "Busiest stations":
    station_counts = (
        trips.groupby(["start_station_name", "start_station_latitude", "start_station_longitude"])
        .size()
        .reset_index(name="trip_count")
        .sort_values("trip_count", ascending=False)
    )

    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader("Top 20 Stations")
        st.dataframe(
            station_counts[["start_station_name", "trip_count"]].head(20),
            hide_index=True,
            width="stretch",
        )

    with col2:
        st.subheader("Station Map")
        max_count = station_counts["trip_count"].max()
        station_counts["radius"] = (station_counts["trip_count"] / max_count) * 500 + 50

        st.pydeck_chart(pdk.Deck(
            layers=[pdk.Layer(
                "ScatterplotLayer",
                data=station_counts,
                get_position="[start_station_longitude, start_station_latitude]",
                get_radius="radius",
                get_fill_color=[46, 196, 182, 180],
                pickable=True,
            )],
            initial_view_state=pdk.ViewState(
                latitude=station_counts["start_station_latitude"].mean(),
                longitude=station_counts["start_station_longitude"].mean(),
                zoom=11,
            ),
        ))

elif question == "Most popular routes":
    routes = (
        trips.groupby([
            "start_station_name", "start_station_latitude", "start_station_longitude",
            "end_station_name", "end_station_latitude", "end_station_longitude",
        ])
        .size()
        .reset_index(name="trip_count")
        .sort_values("trip_count", ascending=False)
    )

    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader("Top 20 Routes")
        display = routes[["start_station_name", "end_station_name", "trip_count"]].head(20)
        display.columns = ["From", "To", "Trips"]
        st.dataframe(display, hide_index=True, width="stretch")

    with col2:
        st.subheader("Route Map")
        top = routes.head(50)

        st.pydeck_chart(pdk.Deck(
            layers=[pdk.Layer(
                "ArcLayer",
                data=top,
                get_source_position="[start_station_longitude, start_station_latitude]",
                get_target_position="[end_station_longitude, end_station_latitude]",
                get_source_color=[46, 196, 182, 160],
                get_target_color=[220, 53, 69, 160],
                get_width=5,
                pickable=True,
            )],
            initial_view_state=pdk.ViewState(
                latitude=top["start_station_latitude"].mean(),
                longitude=top["start_station_longitude"].mean(),
                zoom=11,
            ),
        ))

elif question == "Rebalancing needs":
    deps = trips.groupby(["start_station_name", "start_station_latitude", "start_station_longitude"]).size()
    arrs = trips.groupby(["end_station_name", "end_station_latitude", "end_station_longitude"]).size()

    flow = pd.DataFrame({"departures": deps, "arrivals": arrs}).fillna(0)
    flow["net_flow"] = flow["arrivals"] - flow["departures"]
    flow = flow.reset_index()
    flow.columns = ["station_name", "lat", "lon", "departures", "arrivals", "net_flow"]

    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader("Biggest Imbalances")
        display = flow.reindex(flow["net_flow"].abs().sort_values(ascending=False).index)
        st.dataframe(display[["station_name", "net_flow"]].head(20), hide_index=True, width="stretch")
        st.caption("Positive = gaining bikes, Negative = losing bikes")

    with col2:
        st.subheader("Flow Map")
        st.caption("Green = gaining, Red = losing")

        max_abs = flow["net_flow"].abs().max()
        flow["color"] = flow["net_flow"].apply(lambda x: [220, 53, 69, 180] if x < 0 else [46, 196, 182, 180])
        flow["radius"] = (flow["net_flow"].abs() / max_abs) * 400 + 50

        st.pydeck_chart(pdk.Deck(
            layers=[pdk.Layer(
                "ScatterplotLayer",
                data=flow,
                get_position="[lon, lat]",
                get_radius="radius",
                get_fill_color="color",
                pickable=True,
            )],
            initial_view_state=pdk.ViewState(
                latitude=flow["lat"].mean(),
                longitude=flow["lon"].mean(),
                zoom=11,
            ),
        ))
