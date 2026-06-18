import streamlit as st
import pandas as pd

# ---------------------------------
# PAGE CONFIG
# ---------------------------------

st.set_page_config(
    page_title="AI Travel Planner",
    page_icon="🌍",
    layout="wide"
)

# ---------------------------------
# LOAD CSS
# ---------------------------------

with open("style.css") as f:
    st.markdown(
        f"<style>{f.read()}</style>",
        unsafe_allow_html=True
    )

# ---------------------------------
# LOAD DATASET
# ---------------------------------

df = pd.read_csv("travel_data.csv")

# ---------------------------------
# IMAGE MAPPING
# ---------------------------------

image_map = {
    "Goa": "images/goa.jpg",
    "Manali": "images/manali.jpg",
    "Ooty": "images/ooty.jpg",
    "Jaipur": "images/jaipur.jpg",
    "Coorg": "images/coorg.jpg",
    "Rishikesh": "images/rishikesh.jpg",
    "Munnar": "images/Munnar.jpg",
    "Darjeeling": "images/darjeeling.jpg",
    "Shimla": "images/shimla.jpg",
    "Alleppey": "images/alleppey.jpg",
    "Varanasi": "images/varanasi.jpg",
    "Amritsar": "images/amritsar.jpg",
    "Pondicherry": "images/pondicherry.jpg",
    "Leh": "images/leh.jpg",
    "Srinagar": "images/srinagar.jpg"
}

# ---------------------------------
# HEADER
# ---------------------------------

st.markdown(
    """
    <h1 class='main-title'>
    🌍 AI Travel Planner for Students
    </h1>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <p class='sub-title'>
    Find Budget-Friendly Trips Across India
    </p>
    """,
    unsafe_allow_html=True
)

# ---------------------------------
# HERO IMAGE
# ---------------------------------

st.image(
    "https://images.unsplash.com/photo-1501785888041-af3ef285b470",
    use_container_width=True
)

# ---------------------------------
# SIDEBAR
# ---------------------------------

st.sidebar.header("✈️ Trip Preferences")

budget = st.sidebar.slider(
    "Maximum Budget (₹)",
    3000,
    20000,
    8000
)

category = st.sidebar.selectbox(
    "Travel Interest",
    sorted(df["Category"].unique())
)

state = st.sidebar.selectbox(
    "State",
    ["All"] + sorted(df["State"].unique())
)

days = st.sidebar.slider(
    "Trip Duration (Days)",
    1,
    15,
    3
)

# ---------------------------------
# FILTER DATA
# ---------------------------------

filtered = df[
    (df["Budget"] <= budget)
    &
    (df["Category"] == category)
]

if state != "All":
    filtered = filtered[
        filtered["State"] == state
    ]

# ---------------------------------
# DASHBOARD
# ---------------------------------

st.subheader("📊 Travel Statistics")

col1, col2, col3 = st.columns(3)

col1.metric(
    "Destinations Found",
    len(filtered)
)

col2.metric(
    "Budget",
    f"₹{budget}"
)

col3.metric(
    "Trip Days",
    days
)

# ---------------------------------
# RECOMMENDATIONS
# ---------------------------------

st.subheader("🏖️ Recommended Destinations")

if not filtered.empty:

    for _, row in filtered.iterrows():

        col1, col2 = st.columns([1, 2])

        with col1:

            if row["Destination"] in image_map:

                st.image(
                    image_map[row["Destination"]],
                    use_container_width=True
                )

        with col2:

            st.markdown(
                f"""
                <div class='card'>
                <h2>{row['Destination']}</h2>

                <b>State:</b> {row['State']} <br><br>

                <b>Category:</b> {row['Category']} <br><br>

                <b>Budget:</b> ₹{row['Budget']} <br><br>

                <b>Rating:</b> ⭐ {row['Rating']} <br><br>

                <b>Best Season:</b> {row['Best_Season']}
                </div>
                """,
                unsafe_allow_html=True
            )

else:

    st.warning(
        "No destinations found for selected filters."
    )

# ---------------------------------
# DESTINATION SELECTION
# ---------------------------------

st.divider()

if not filtered.empty:

    destination = st.selectbox(
        "📍 Select Destination",
        filtered["Destination"]
    )

    selected = filtered[
        filtered["Destination"] == destination
    ].iloc[0]

    st.success(
        f"You selected {destination}"
    )

    st.subheader("🧳 Trip Summary")

    c1, c2 = st.columns(2)

    with c1:

        st.metric(
            "Budget",
            f"₹{selected['Budget']}"
        )

        st.metric(
            "Rating",
            f"⭐ {selected['Rating']}"
        )

    with c2:

        st.metric(
            "Duration",
            f"{days} Days"
        )

        st.metric(
            "Best Season",
            selected["Best_Season"]
        )

    st.subheader("📅 Suggested Plan")

    for day in range(1, days + 1):

        st.write(
            f"Day {day}: Explore {destination} and nearby attractions."
        )

    st.subheader("📍 Google Maps")

    st.markdown(
        f"[Open {destination} in Google Maps](https://www.google.com/maps/search/{destination})"
    )