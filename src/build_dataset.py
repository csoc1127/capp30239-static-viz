"""
Prep reusable Chicago eBird datasets--

run from the project root:
    uv run python src/build_datasets.py

The large raw Cook County files were already filtered in the exploration notebooks.
This script uses those existing Chicago-only processed files; not supposed to rescan raw data.

"""

from pathlib import Path
import geopandas as gpd
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
PROCESSED = ROOT / "data" / "processed"
TOP_OBSERVER = "obsr4476574"


def load_data():
    """Load the three existing sources once, w stable paths."""
    checklists = pd.read_csv(
        PROCESSED / "chicago_checklists_2020_2024.csv",
        parse_dates=["OBSERVATION DATE"],
        low_memory=False,
    )
    birds = pd.read_csv(
        PROCESSED / "chicago_bird_observations_2020_2024.csv.gz",
        low_memory=False,
    )
    areas = gpd.read_file(PROCESSED / "community_areas.geojson")

    # Each checklist must have a single ID before aggregating its observations.
    assert checklists["SAMPLING EVENT IDENTIFIER"].is_unique
    return {"checklists": checklists, "birds": birds, "areas": areas}


def build_datasets(data):
    """make chart-ready tables from the already processed Chicago data."""
    checklists = data["checklists"]
    birds = data["birds"]

    species = birds.loc[birds["CATEGORY"].eq("species")].copy()
    species["bird_count"] = pd.to_numeric(
        species["OBSERVATION COUNT"], errors="coerce"
    )

    # 1 row per checklist, including checklists with no species-level records.
    per_checklist = (
        species.groupby("SAMPLING EVENT IDENTIFIER")
        .agg(
            birds_reported=("bird_count", "sum"),
            species_reported=("SCIENTIFIC NAME", "nunique"),
        )
        .reset_index()
    )
    checklist_summary = checklists[[
        "SAMPLING EVENT IDENTIFIER", "OBSERVER ID", "OBSERVATION DATE",
        "community", "LOCALITY ID", "LOCALITY", "LOCALITY TYPE",
        "LATITUDE", "LONGITUDE",
    ]].merge(per_checklist, on="SAMPLING EVENT IDENTIFIER", how="left", validate="one_to_one")
    checklist_summary[["birds_reported", "species_reported"]] = (
        checklist_summary[["birds_reported", "species_reported"]].fillna(0)
    )

    # Community-area measures: checklist volume, contributor count, reported birds,
    # species richness, and the share associated with the most active account.
    community = (
        checklist_summary.groupby("community")
        .agg(
            checklists=("SAMPLING EVENT IDENTIFIER", "nunique"),
            observers=("OBSERVER ID", "nunique"),
            birds_reported=("birds_reported", "sum"),
        )
    )
    richness = species.groupby("community")["SCIENTIFIC NAME"].nunique()
    top_counts = (
        checklist_summary.loc[checklist_summary["OBSERVER ID"].eq(TOP_OBSERVER)]
        .groupby("community").size()
    )
    community["distinct_species"] = richness
    community["top_observer_checklists"] = top_counts
    community = community.fillna(0).reset_index()
    community["other_checklists"] = (
        community["checklists"] - community["top_observer_checklists"]
    )
    community["top_observer_share_pct"] = (
        100 * community["top_observer_checklists"] / community["checklists"]
    )

    community_map = data["areas"].merge(
        community, on="community", how="left", validate="one_to_one"
    )

    # Common and scientific names together avoid ambiguous species labels.
    species_summary = (
        species.groupby(["COMMON NAME", "SCIENTIFIC NAME"], dropna=False)
        .agg(
            checklists=("SAMPLING EVENT IDENTIFIER", "nunique"),
            birds_reported=("bird_count", "sum"),
        )
        .reset_index()
    )

    # calendar-month reporting, keeping individual years separate.
    checklist_summary["year"] = checklist_summary["OBSERVATION DATE"].dt.year
    checklist_summary["month"] = checklist_summary["OBSERVATION DATE"].dt.month
    monthly = (
        checklist_summary.groupby(["year", "month"])
        .agg(
            checklists=("SAMPLING EVENT IDENTIFIER", "nunique"),
            observers=("OBSERVER ID", "nunique"),
            birds_reported=("birds_reported", "sum"),
        )
        .reset_index()
    )

    # Designated eBird hotspots only EXPLAIN LATER? (LOCALITY TYPE == 'H').
    hotspot_checklists = checklist_summary.loc[
        checklist_summary["LOCALITY TYPE"].eq("H")
    ]
    hotspots = (
        hotspot_checklists.groupby(["LOCALITY ID", "LOCALITY", "community"], dropna=False)
        .agg(
            checklists=("SAMPLING EVENT IDENTIFIER", "nunique"),
            observers=("OBSERVER ID", "nunique"),
            birds_reported=("birds_reported", "sum"),
            latitude=("LATITUDE", "median"),
            longitude=("LONGITUDE", "median"),
        )
        .reset_index()
    )
    hotspot_species = species.merge(
        hotspot_checklists[["SAMPLING EVENT IDENTIFIER", "LOCALITY ID"]],
        on="SAMPLING EVENT IDENTIFIER", how="inner", validate="many_to_one"
    )
    hotspot_richness = (
        hotspot_species.groupby("LOCALITY ID")["SCIENTIFIC NAME"]
        .nunique().rename("distinct_species")
    )
    hotspots = hotspots.join(hotspot_richness, on="LOCALITY ID")
    hotspots["distinct_species"] = hotspots["distinct_species"].fillna(0)

    # One row per community and observer group for paired-map comparisons.
    checklist_summary["observer_group"] = checklist_summary["OBSERVER ID"].eq(
        TOP_OBSERVER
    ).map({True: "Top account", False: "Everyone else"})
    observer_comparison = (
        checklist_summary.groupby(["community", "observer_group"])
        .agg(
            checklists=("SAMPLING EVENT IDENTIFIER", "nunique"),
            observers=("OBSERVER ID", "nunique"),
            birds_reported=("birds_reported", "sum"),
        )
        .reset_index()
    )

    # complete calendar ensures zero-submission days are visible.
    calendar_2024 = pd.date_range("2024-01-01", "2024-12-31", freq="D")
    top_2024 = checklist_summary.loc[
        checklist_summary["OBSERVER ID"].eq(TOP_OBSERVER)
        & checklist_summary["year"].eq(2024)
    ]
    daily = (
        top_2024.groupby("OBSERVATION DATE").size()
        .reindex(calendar_2024, fill_value=0)
        .rename_axis("date")
        .reset_index(name="checklists")
    )
    daily["weekday"] = daily["date"].dt.day_name()

    return {
        "checklists": checklists,
        "birds": birds,
        "species": species,
        "checklist_summary": checklist_summary,
        "community_summary": community,
        "community_map": community_map,
        "species_summary": species_summary,
        "monthly_activity": monthly,
        "hotspot_summary": hotspots,
        "observer_comparison": observer_comparison,
        "top_observer_daily_2024": daily,
    }


def save_datasets(tables):
    """Write compact chart-ready tables; never duplicate the large source files."""
    outputs = {
        "checklist_summary": "checklist_summary.csv.gz",
        "community_summary": "community_summary.csv",
        "species_summary": "species_summary.csv",
        "monthly_activity": "monthly_activity.csv",
        "hotspot_summary": "hotspot_summary.csv",
        "observer_comparison": "observer_comparison.csv",
        "top_observer_daily_2024": "top_observer_daily_2024.csv",
    }
    PROCESSED.mkdir(parents=True, exist_ok=True)
    for table_name, filename in outputs.items():
        tables[table_name].to_csv(PROCESSED / filename, index=False)
        print(f"Saved data/processed/{filename}")
    tables["community_map"].to_file(
        PROCESSED / "community_summary.geojson", driver="GeoJSON"
    )
    print("Saved data/processed/community_summary.geojson")


def main():
    tables = build_datasets(load_data())
    save_datasets(tables)
    dates = tables["top_observer_daily_2024"]
    missed = dates.loc[dates["checklists"].eq(0), "date"].dt.strftime("%B %d, %Y")
    print(f"Chicago checklists: {len(tables['checklists']):,}")
    print(f"Species-level birds counted: {tables['species']['bird_count'].sum():,.0f}")
    print(f"Distinct species: {tables['species']['SCIENTIFIC NAME'].nunique():,}")
    print("Top observer's 2024 dates without a Chicago checklist:")
    print("\n".join(missed) if not missed.empty else "None")


if __name__ == "__main__":
    main()
