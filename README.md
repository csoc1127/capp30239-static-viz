# Chicago's Birders and Birds

Ciara Staveley-O'Carroll  
CAPP 30239 — Data Visualization for Policy Analysis

## Description
My goal was to understand how birdwatching activity varies across Chicago and how the people collecting observations shape the city's bird records. Using eBird data from 2020 to 2024, I explored who was reporting birds, which species they documented and where and when those observations were concentrated. I started this project wanting to understand where Chicagoans go birding and why some parts of the city receive more attention than others. My original proposal included park space and neighborhood demographics. Once I started working with the eBird data, I became more interested in the records themselves: who submits them, which birds get reported and where and when people are looking.

The final article uses 218,781 eBird checklists from Chicago between 2020 and 2024. Those checklists document 335 species. I wanted to see what the data could tell me about Chicago's birds while keeping the people collecting the observations in view.
The birders. One observer account submitted 5.7% of Chicago's checklists and 71.1% of Edgewater's. Most of that account's activity took place in 2023 and 2024. I also found that the account submitting the most checklists was different from the one reporting the most birds.

## Final article

[Open the article](static-viz/final.html)

![Screenshot](static-viz/chicago_birders_full_article.png)



## Data sources
- [eBird Basic Dataset] https://science.ebird.org/en/use-ebird-data/download-ebird-data-products
- [Cornell Lab of Ornithology, eBird Basic Dataset and sampling-event data](https://science.ebird.org/en/use-ebird-data/download-ebird-data-products): August 2026 release, filtered to Chicago observations from 2020–2024.
- [City of Chicago community-area boundaries](https://data.cityofchicago.org/d/igwz-8jzy): used to map and summarize records across 77 community areas.
- [National Weather Service climate records](https://www.weather.gov/lot/ord_rfd_monthly_yearly_normals): background on Chicago winter temperatures.
- Chicago Ornithological Society and Illinois Ornithological Records Committee: background and verification for the unusual bird sightings. The article links to the relevant accounts.

[City of Chicago Community Area Boundaries] https://data.cityofchicago.org/d/igwz-8jzy

Used to map birdwatching activity across Chicago's 77 community areas. Additional sources for unusual bird sightings and Chicago weather are cited in the final article. To regenerate the charts, run cd src followed by uv run python final_figs.py.

## Code and files

The charts were made with Python and Altair using the prepared data in `data/processed/`. The plotting code is in `src/final_figs.py`, with colors in `src/bird_colors.py`. I used inkscape to build the 3 map collage and the donuts. I struggled presenting the three maps. 

To regenerate the chart SVGs, open a terminal in the project folder and run:

```bash
cd src
uv run python final_figs.py
```

The SVGs are saved in `static-viz/figures/`. I arranged the two doughnut charts and the three community-area maps into composite SVGs in Inkscape. Those final composites are saved beside `static-viz/final.html`.
