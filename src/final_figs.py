from pathlib import Path

import altair as alt
import pandas as pd
import geopandas as gpd

from bird_colors import BIRD_COLORS, MAP_PALETTES, OBSERVER_COLORS, SCATTER_COLORS

ROOT = Path(__file__).resolve().parents[1]

community = gpd.read_file(
    ROOT / "data/processed/community_summary.geojson"
)

# compare checklists and birds counted by observer
checklists = pd.read_csv("../data/processed/checklist_summary.csv.gz")

observer_summary = (
    checklists.groupby("OBSERVER ID")
    .agg(
        checklists=("SAMPLING EVENT IDENTIFIER", "nunique"),
        birds_reported=("birds_reported", "sum")
    )
    .reset_index()
)

# chart titles

def chart_title(main_title, subtitle="Chicago neighborhoods, 2020–2024"):
    return alt.TitleParams(
        text=main_title,
        subtitle=subtitle
    )

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

# map different bird species across chicago neighborhoods
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

# map total birds counted across chicago
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

# compare checklists submitted with birds counted by observer
observer_plot = pd.concat([
    observer_summary.nlargest(100, "checklists"),
    observer_summary.nlargest(100, "birds_reported")
]).drop_duplicates("OBSERVER ID")

top_checklists = observer_plot.nlargest(1, "checklists")
top_birds = observer_plot.nlargest(1, "birds_reported")

base = alt.Chart(observer_plot).encode(
    x=alt.X(
        "checklists:Q",
        title="Checklists submitted",
        scale=alt.Scale(type="sqrt", zero=True),
        axis=alt.Axis(grid=False, tickCount=6, format="~s")
    ),
    y=alt.Y(
        "birds_reported:Q",
        title="Birds counted across checklists",
        scale=alt.Scale(type="sqrt", zero=True),
        axis=alt.Axis(grid=False, tickCount=6, format="~s")
    )
)

# other active observer accounts
dots = base.mark_circle(
    size=75,
    color=SCATTER_COLORS["others"],
    opacity=0.7,
    stroke="white",
    strokeWidth=0.7
)

# account with the most checklists
checklist_point = alt.Chart(top_checklists).mark_circle(
    size=220,
    color=SCATTER_COLORS["most_checklists"],
    stroke="white",
    strokeWidth=1.5
).encode(
    x="checklists:Q",
    y="birds_reported:Q"
)

checklist_label = alt.Chart(top_checklists).mark_text(
    align="right",
    dx=-10,
    dy=-12,
    fontSize=12,
    fontWeight="bold",
    color=SCATTER_COLORS["most_checklists"]
).encode(
    x="checklists:Q",
    y="birds_reported:Q",
    text=alt.value("Most checklists")
)

# account reporting the most birds
bird_point = alt.Chart(top_birds).mark_circle(
    size=220,
    color=SCATTER_COLORS["most_birds"],
    stroke="white",
    strokeWidth=1.5
).encode(
    x="checklists:Q",
    y="birds_reported:Q"
)

bird_label = alt.Chart(top_birds).mark_text(
    align="left",
    dx=12,
    dy=12,
    fontSize=12,
    fontWeight="bold",
    color=SCATTER_COLORS["most_birds"]
).encode(
    x="checklists:Q",
    y="birds_reported:Q",
    text=alt.value("Most birds counted")
)

observer_scatter = (
    dots + checklist_point + checklist_label + bird_point + bird_label
).properties(
    title=chart_title(
        "Chicago's busiest birder isn't the one counting the most birds",
        "Top 100 accounts by either measure, 2020–2024"
    ),
    width=650,
    height=400
).configure_view(stroke=None)

observer_scatter.save("../static-viz/figures/observer_scatter.svg")

# the birds most often reported in chicago

species = pd.read_csv("../data/processed/species_summary.csv")
top_species = species.nlargest(8, "checklists")

species_chart = alt.Chart(top_species).mark_bar(
    cornerRadiusEnd=3
).encode(
    y=alt.Y("COMMON NAME:N", sort="-x", title=None),
    x=alt.X(
        "checklists:Q",
        title="Checklists reporting this bird",
        axis=alt.Axis(grid=False, format="~s")
    ),
    color=alt.Color(
        "COMMON NAME:N",
        legend=None,
        scale=alt.Scale(
            domain=top_species["COMMON NAME"].tolist(),
            range=[
                BIRD_COLORS.get(bird, "#C8602B")
                for bird in top_species["COMMON NAME"]
            ]
        )
    )
).properties(
    title=chart_title(
        "Which birds appear most often in Chicago's birdwatching reports?",
        "Eight most frequently reported species, 2020–2024"
    ),
    width=540,
    height=320
)

species_chart.save("../static-viz/figures/top_species.svg")

# rank species by how many checklists they appear on
species_distribution = (
    species[["COMMON NAME", "checklists"]]
    .sort_values("checklists", ascending=False)
    .reset_index(drop=True)
    .assign(rank=lambda df: df.index + 1)
)

# label the top 10 species
top_species_labels = species_distribution.head(10)

species_line = alt.Chart(species_distribution).mark_line(
    color="#B9B1A5",
    strokeWidth=2
).encode(
    x=alt.X(
        "rank:Q",
        title="Species rank",
        axis=alt.Axis(tickCount=8)
    ),
    y=alt.Y(
        "checklists:Q",
        title="Checklists containing species",
        scale=alt.Scale(type="log"),
        axis=alt.Axis(format="~s", tickCount=6)
    )
)

species_dots = alt.Chart(species_distribution).mark_circle(
    color="#387753",
    size=45,
    opacity=0.85
).encode(
    x="rank:Q",
    y="checklists:Q",
    tooltip=[
        alt.Tooltip("rank:Q", title="Rank"),
        alt.Tooltip("COMMON NAME:N", title="Species"),
        alt.Tooltip("checklists:Q", title="Checklists", format=",")
    ]
)

species_labels = alt.Chart(top_species_labels).mark_text(
    dx=8,
    dy=-6,
    align="left",
    fontSize=11,
    color="#1F2A2E"
).encode(
    x="rank:Q",
    y="checklists:Q",
    text="COMMON NAME:N"
)

species_distribution_chart = (
    species_line + species_dots + species_labels
).properties(
    title=chart_title(
        "A small group of birds dominates Chicago's eBird record",
        "335 species ranked by checklist frequency, 2020–2024"
    ),
    width=650,
    height=400
)

species_distribution_chart.save("../static-viz/figures/species_distribution.svg")
print("total species:", len(species_distribution))
print("top species:", species_distribution.iloc[0]["COMMON NAME"])
print("top species checklists:", species_distribution.iloc[0]["checklists"])
print(
    "species appearing on fewer than 100 checklists:",
    (species_distribution["checklists"] < 100).sum()
)
print(
    "species appearing on fewer than 10 checklists:",
    (species_distribution["checklists"] < 10).sum()
)
print(species["checklists"].describe())

print("\nleast frequently reported species:")
print(
    species.nsmallest(15, "checklists")[
        ["COMMON NAME", "checklists"]
    ].to_string(index=False)
)

print("\nspecies on fewer than 100 checklists:")
print((species["checklists"] < 100).sum())


# investigate unexpected visitors
observations = pd.read_csv(
    "../data/processed/chicago_bird_observations_2020_2024.csv.gz"
)

print("\nobservation columns:")
print(observations.columns.tolist())


# examine reports of unusual bird species
unusual_birds = [
    "Short-tailed Shearwater",
    "Ferruginous Hawk",
    "Gull-billed Tern",
    "Pacific Loon",
    "White-faced Ibis"
]

unusual_sightings = observations[
    (observations["CATEGORY"] == "species") &
    (observations["COMMON NAME"].isin(unusual_birds))
].copy()

unusual_sightings = unusual_sightings.sort_values(
    ["COMMON NAME", "OBSERVATION DATE"]
)

print("\nunexpected visitor sightings:")
print(
    unusual_sightings[[
        "COMMON NAME",
        "OBSERVATION DATE",
        "community",
        "OBSERVER ID",
        "SAMPLING EVENT IDENTIFIER",
        "OBSERVATION COUNT"
    ]].to_string(index=False)
)


# timeline of five documented unexpected visitors
visitors = [
    "White-faced Ibis",
    "Gull-billed Tern",
    "Ferruginous Hawk",
    "Pacific Loon",
    "Short-tailed Shearwater"
]

visitor_dates = (
    observations[
        (observations["CATEGORY"] == "species") &
        (observations["COMMON NAME"].isin(visitors))
    ]
    .groupby("COMMON NAME")
    .agg(
        first_seen=("OBSERVATION DATE", "min"),
        checklists=("SAMPLING EVENT IDENTIFIER", "nunique")
    )
    .reset_index()
)

visitor_dates["first_seen"] = pd.to_datetime(
    visitor_dates["first_seen"]
)
visitor_dates["date_label"] = (
    visitor_dates["first_seen"].dt.strftime("%b %d, %Y")
)

base = alt.Chart(visitor_dates).encode(
    x=alt.X("first_seen:T", title="Date reported"),
    y=alt.Y("COMMON NAME:N", sort=visitors, title=None)
)

visitor_points = base.mark_circle(
    size=180,
    color="#7A2137"
)

visitor_labels = base.mark_text(
    align="left",
    dx=12,
    fontSize=12,
    color="#1F2A2E"
).encode(
    text="date_label:N"
)

visitor_chart = (
    visitor_points + visitor_labels
).properties(
    title=chart_title(
        "Unexpected visitors in Chicago",
        "Five unusual species recorded between 2020 and 2024"
    ),
    width=650,
    height=260
)

visitor_chart.save(
    "../static-viz/figures/unexpected_visitors.svg"
)
