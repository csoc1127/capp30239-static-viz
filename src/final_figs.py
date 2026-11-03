from pathlib import Path

import altair as alt
import pandas as pd
import geopandas as gpd

from bird_colors import MAP_PALETTES, OBSERVER_COLORS

ROOT = Path(__file__).resolve().parents[1]

community = gpd.read_file(
    ROOT / "data/processed/community_summary.geojson"
)

print(community[
    ["community", "checklists", "birds_reported", "distinct_species"]
].head())


print(community.columns.tolist())
print(community.shape)


### Matching chart titles

def chart_title(main_title, subtitle="Chicago neighborhoods, 2020–2024"):
    return alt.TitleParams(
        text=main_title,
        subtitle=subtitle
    )

# map checklist activity across chicago
# map checklist activity across chicago
# map checklist activity across chicago neighborhoods
checklist_map = alt.Chart(
    alt.Data(values=community.to_crs("EPSG:4326").__geo_interface__["features"])
).mark_geoshape(
    stroke="white",
    strokeWidth=0.5
).encode(
    color=alt.Color(
        "properties.checklists:Q",
        title="Checklists submitted",
        scale=alt.Scale(
            type="sqrt",
            range=MAP_PALETTES["checklists"]
        )
    ),
    tooltip=[
        alt.Tooltip("properties.community:N", title="Neighborhood"),
        alt.Tooltip("properties.checklists:Q", title="Checklists", format=",")
    ]
).project(
    type="mercator"
).properties(
    title=chart_title("Birdwatching reports cluster on the North Side"),
    width=450,
    height=550
)

checklist_map.save("../static-viz/figures/checklists_map.svg")

### SPECIES RICHNESS MAP
# species richness across chicago
# map the number of different bird species reported across chicago neighborhoods
species_richness_map = alt.Chart(
    alt.Data(values=community.to_crs("EPSG:4326").__geo_interface__["features"])
).mark_geoshape(
    stroke="white",
    strokeWidth=0.5
).encode(
    color=alt.Color(
        "properties.distinct_species:Q",
        title="Different species reported",
        scale=alt.Scale(
            type="sqrt",
            range=MAP_PALETTES["species_richness"]
        )
    ),
    tooltip=[
        alt.Tooltip("properties.community:N", title="Neighborhood"),
        alt.Tooltip("properties.distinct_species:Q", title="Species", format=",")
    ]
).project(
    type="mercator"
).properties(
    title=chart_title("Bird species richness is highest along the lakefront and on the North Side"),
    width=450,
    height=550
)

species_richness_map.save("../static-viz/figures/species_richness_map.svg")

### bird count map

# map total birds reported across chicago
bird_count_map = species_richness_map.encode(
    color=alt.Color(
        "properties.birds_reported:Q",
        title="Birds reported",
        scale=alt.Scale(
            type="sqrt",
            range=MAP_PALETTES["birds_reported"]
        )
    ),
    tooltip=[
        alt.Tooltip("properties.community:N", title="Neighborhood"),
        alt.Tooltip("properties.birds_reported:Q", title="Birds reported", format=",")
    ]
).properties(
    title=chart_title("Nearly one-third of reported birds were counted in Uptown")
)

bird_count_map.save("../static-viz/figures/bird_count_map.svg")

### monthly activity map

# birdwatching activity by month and year
monthly = pd.read_csv("../data/processed/monthly_activity.csv")

month_names = [
    "Jan", "Feb", "Mar", "Apr", "May", "Jun",
    "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
]

monthly["month_name"] = monthly["month"].map(
    dict(enumerate(month_names, 1))
)

monthly_chart = alt.Chart(monthly).mark_rect(
    stroke="white",
    strokeWidth=2
).encode(
    x=alt.X("month_name:O", sort=month_names, title="Month"),
    y=alt.Y("year:O", title="Year", sort="ascending"),
    color=alt.Color(
        "checklists:Q",
        title="Checklists submitted",
        scale=alt.Scale(
            type="sqrt",
            range=MAP_PALETTES["monthly_activity"]
        )
    )
).properties(
    title=chart_title(
        "Chicago's birdwatching reports peak in May",
        "Monthly checklists, 2020–2024"
    ),
    width=650,
    height=260
)

monthly_chart.save("../static-viz/figures/monthly_heatmap.svg")

### Special observer map

# observer contribution across chicago and edgewater
# compare the top observer with everyone else
edgewater = community[community["community"] == "EDGEWATER"].iloc[0]

observer_data = pd.DataFrame({
    "place": ["Chicago", "Chicago", "Edgewater", "Edgewater"],
    "group": ["Top observer", "Everyone else"] * 2,
    "checklists": [
        community["top_observer_checklists"].sum(),
        community["other_checklists"].sum(),
        edgewater["top_observer_checklists"],
        edgewater["other_checklists"]
    ]
})
chicago_data = observer_data[observer_data["place"] == "Chicago"]
edgewater_data = observer_data[observer_data["place"] == "Edgewater"]

observer_colors = alt.Scale(
    domain=["Top observer", "Everyone else"],
    range=[
        OBSERVER_COLORS["Top observer"],
        OBSERVER_COLORS["Everyone else"]
    ]
)

# chicago
chicago_donut = alt.Chart(chicago_data).mark_arc(
    innerRadius=65,
    outerRadius=105
).encode(
    theta="checklists:Q",
    color=alt.Color(
        "group:N",
        scale=observer_colors,
        title=None
    )
).properties(
    title=chart_title(
        "One observer submitted 5.7% of Chicago's checklists",
        "Chicago, 2020–2024"
    ),
    width=250,
    height=250
)

chicago_donut.save("../static-viz/figures/chicago_observer.svg")


# edgewater
edgewater_donut = alt.Chart(edgewater_data).mark_arc(
    innerRadius=65,
    outerRadius=105
).encode(
    theta="checklists:Q",
    color=alt.Color(
        "group:N",
        scale=observer_colors,
        title=None
    )
).properties(
    title=chart_title(
        "One observer submitted 71.1% of Edgewater's checklists",
        "Edgewater, 2020–2024"
    ),
    width=250,
    height=250
)

edgewater_donut.save("../static-viz/figures/edgewater_observer.svg")

# map the top observer's share of neighborhood checklists
observer_map = checklist_map.encode(
    color=alt.Color(
        "properties.top_observer_share_pct:Q",
        title="Share of checklists (%)",
        scale=alt.Scale(
            type="sqrt",
            range=MAP_PALETTES["observer_share"]
        )
    ),
    tooltip=[
        alt.Tooltip("properties.community:N", title="Neighborhood"),
        alt.Tooltip("properties.top_observer_checklists:Q", title="Top observer", format=","),
        alt.Tooltip("properties.other_checklists:Q", title="Everyone else", format=","),
        alt.Tooltip("properties.top_observer_share_pct:Q", title="Share (%)", format=".1f")
    ]
).properties(
    title=chart_title(
        "One birdwatcher submitted 71% of Edgewater's checklists"
    )
)

observer_map.save("../static-viz/figures/observer_share_map.svg")

#### HOTSPOTS
# compare birdwatching activity and species variety at hotspots
hotspots = pd.read_csv("../data/processed/hotspot_summary.csv")

hotspot_chart = alt.Chart(hotspots).mark_circle(
    size=65,
    opacity=0.7,
    color="#3E7C6B"
).encode(
    x=alt.X(
        "checklists:Q",
        title="Birdwatching checklists",
        scale=alt.Scale(type="sqrt")
    ),
    y=alt.Y(
        "distinct_species:Q",
        title="Different species reported"
    ),
    tooltip=[
        "LOCALITY:N",
        "checklists:Q",
        "distinct_species:Q",
        "observers:Q"
    ]
).properties(
    title=chart_title(
        "Do busier birdwatching hotspots record more species?",
        "Chicago eBird hotspots, 2020–2024"
    ),
    width=650,
    height=400
)

hotspot_chart.save("../static-viz/figures/hotspot_scatter.svg")