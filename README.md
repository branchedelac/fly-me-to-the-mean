# Fly Me To the Mean<sup>1</sup>
## Multi-origin destination and flight search
![alt text](static/image.png)

The possibility to travel, work remotely, and develop meaningful connections with people all over the world, creates new challenges for whoever tries to organize a meetup of friends or colleagues in the physical world. Where should you meet? How can you make it as easy and economically feasible for everyone of you to get there?

This is where Fly Me To the Mean comes in. Given a set of departure cities and a date range, this service helps you find the destination with the cheapest *total* ticket price, or the cheapest average price per flight/person.

The service is built using free versions of the Kiwi Tequila API for flights ✈️, and the Carbon Interface estimates API for CO2 emission estimates 🍃. If the Carbon Interface limit of 200 calls per month has been reached, CO2 estimates are omitted. The web interface is built using Streamlit.

## Some next steps
- Improve error handling, including user-facing error messages
- Make CO2 emission estimate, as well as price, a possible selection criterium 🍃
- Add support for multiple passngers per departure
- Add support for roundtrips / understand if the API really differentiates these
- Add support for searching for train rather than plane trips 🚂🍃
- Without cluttering the UI, isplay ticket information for more than one destination

----
<sup><sup>1</sup> "mean" as in "average", it's a working title... 🙂</sup>