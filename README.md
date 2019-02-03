#Introduction

This project aims to analyze and visualize the world flight routes data for different airlines.

The goal is to find interesting trends in how airlines use aircraft as part of their fleet. These trends could be useful
from a business intelligence perspective of either an airline vis-a-vis its fleet, an airline executive looking to gain insights into a competing airline, or for aircraft manufacturers  looking for "niche" routes to market their aircraft.

A web-app built using Dash/Plotly can make it easier to discover this data. A draft instance was deployed to heroku [FlyTheData](https://flythedata.herokuapp.com/).

As an example of interesting trends that can be extracted. The following graph figure shows that the 777 and 787, two of Boeing's best selling aircraft, are used slightly differently by airlines. The figure is a probability density plot of all scheduled flights by all airlines, with the distance (x-axis) normalized by the mean. It shows that while the 787 is flown often near its mean, the 777 has two distinct modes, with one at approximately 1.5 and the other at 0.5 of the mean. This indicates that the 777 is often used to fly much shorter routes than its maximum range.


![Range of 777 vs 787](https://www.dropbox.com/s/u53lz1d876203x7/Flight%20Ranges%20Distribution.png?dl=1)

It would be interesting for example for an aircraft manufacturer to dig deeper into this result to understand which airlines are using the 777 in this manner, and to potentially offer a different aircraft with better economics for these routes. Likewise, an airline executive could conclude that if a competitor airline is using a 777 on a short route, the route has a lot of passengers and is therefore a potential candidate for adding a new city pair.


Although the world view map is currently "static" in that only a subset of routes are plotted, I intend to improve this view as follows:
* link the routes displayed to the aircraft type and the airlines selected
* Use a clustering algorithm to minimize the number of lines being plotted and improve usability
* Make it possible to use the map to select a "region of interest" and only plot airlines/aircraft of that region.


In addition to these two graphs, I plan to add a 3rd graph showing the breakdown of the routes by airlines. This would allow the user to narrow down the analysis to specific airlines of interest. This graph would be cross-linked with both the world-view and the aircraft-range map.


Aside from these obvious three graphs, there are other potential ways to analyze and tease out meaning from this data by combining it with other data:
* One possibility is to use data about the capacity of each aircraft type (both in economy/business/first) which can be scraped from a site like [Seat Guru][http://seatguru.com]. This would make it possible to get a view into the seat-capacity of each airlines by region or city-pairs.
* Another possibility is 

#Limitations
Unfortunately, there are limitations to this data set.

First of all, it's an old one dating back to 2014. Any serious use of it would require an updated route. It could be helpful to find ways to scrape this data from amadeus or other airline scheduling tools. But that is not a trivial task and it's not clear if it's within the scope of this project.

Another limitation is that the data set does not contain any frequency information. This makes it difficult to get good approximations for seat capacity for example. Likewise, there is not time information. The latter would make it possible to see trends of growth accross regions, which could be helpful again for an aircraft manufacturer or airline looking for expansion opportunities.
