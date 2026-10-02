# Milestone 1 - Ciara Staveley-O'Carroll

## Description

For this project, I want to look at where people are birding in Chicago and what makes some parts of the city much more observed than others. eBird is interesting for this because the data capture both where birds are being found and where people are choosing to spend time looking for and documenting them. In that sense, the data show something about Chicago's birds, but also about how people interact with nature across the city.

The main question I want to explore is: **Which parts of Chicago receive less "citizen-science" (scientific data that is collected by regular citizens, a new term to me) attention than their available habitat would lead us to expect?**

I plan to map birding effort across Chicago and compare it with green space and neighborhood characteristics like income, race, age, and population. I am interested in whether two areas with similar amounts of park space can receive very different levels of birding activity, and what might explain that difference. On the other hand, I also want to identify unexpected birding hotspots: places that receive much more birding activity than their location, green space, or neighborhood characteristics might initially suggest.

If the historical eBird data allow for it (I have put the request in for the data, they said it should get the OK by Tuesday), I also want to look at how these patterns have changed over time. Like, has birding become more common across Chicago generally, or has growth remained concentrated in places that were already popular places to bird?

I am not treating eBird observations as a direct measure of bird abundance or assuming that the demographics of a neighborhood represent the demographics of the people birding there. Instead, I want to separate birding effort from bird observations as much as possible and use the project to explore where citizen-science data are being produced, where there may be gaps, and what those patterns tell us about access to and engagement with urban nature.

## Data Sources

### Data Source 1: eBird Basic Dataset and Sampling Event Data

URL: https://science.ebird.org/en/use-ebird-data/download-ebird-data-products

Size: Final requested dataset pending approval. The provided sample eBird Basic Dataset contains 4,863 rows and 52 columns. The accompanying Sampling Event Data sample contains 317 rows and 33 columns.

The eBird Basic Dataset contains individual bird observations, including species, date, latitude and longitude, locality, observer ID, and a checklist identifier. I submitted a request on October 1 for data covering Cook County and will limit the data to observations within Chicago once I receive it.

I have explored the sample data and metadata while waiting for the full download. I'm particularly interested in the Sampling Event Data because it has one row per checklist and includes measures of birding effort such as duration, distance traveled, and number of observers. The data also distinguish eBird hotspots from personal locations and include identifiers that can be used to account for shared checklists. This should let me measure where people are actually birding rather than simply mapping the total number of bird observations.

### Data Source 2: U.S. Census Bureau American Community Survey and Chicago Census Tracts

URL: https://api.census.gov/data/2024/acs/acs5.html

Size: Chicago census tracts as rows, with the final number of columns depending on the ACS variables selected.

I will use ACS 5-year estimates at the census-tract level for neighborhood characteristics including median household income, race and ethnicity, age, and population. Census tracts will also provide the common geography for comparing these characteristics with eBird activity across Chicago.

I have used this same tract-level Census setup in a previous Chicago project (CAPP122 CTA proj), including 2024 ACS data and Chicago tract boundaries joined using Census GEOIDs. I plan to reuse that geographic setup and add or change ACS variables based on what is useful for this project. I will assign eBird checklists to census tracts using their latitude and longitude.

### Data Source 3: Chicago Park District Park Boundaries

URL: https://data.cityofchicago.org/Parks-Recreation/Parks-Chicago-Park-District-Park-Boundaries-curren/ej32-qgdr

Size: Exact dimensions to be confirmed when downloaded.

This dataset contains the boundaries of Chicago Park District properties. I plan to use it as a measure of available green space and potential birding opportunity. I can calculate how much park space is available within or near different census tracts and compare that with the amount of eBird activity occurring there.

This is especially important for the main question of the project. A tract with little birding activity and little green space is different from a tract with substantial park space but surprisingly little birding activity. I want to use that difference to identify areas that appear under-observed, as well as places that have more birding activity than I might otherwise expect.

## Questions

1. Does it make sense to define an "under-observed" area as somewhere with substantially less eBird activity than we would expect given the amount of available green space? Are there other factors I should be considering when defining what we would "expect"?

2. Is census tract an appropriate level of geography for this comparison, or should I consider a larger unit given how people actually use parks and move around while birding?

3. My requested eBird dataset is still pending approval. Is using the provided sample to verify the available variables and structure OK for the proposal, with the full data incorporated once the request is approved? re: Reddit it seems like everyone gets approved but I know this can be frustrating. 