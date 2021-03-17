# pq2-smart-cookies

Danny Little, Bruce Tang, August Wadlington
CSCI 3725

## Generation Day
So far, our first portion of this assignment involved making a CC system to generate cookie recipes. This was done in a manner similar to the previous assignment, with a few main changes. We weren't given any data to use, so we scraped some recipes from [Allrecipes](https://www.allrecipes.com/recipes/362/desserts/cookies/). 

We also used a new concept in our recipe generation: base ingredients. If every single cookie recipe we scraped has, for example, eggs, flour, butter, and sugar, we probably would want our system to be more free to experiment with other, "add-on" ingredients like chocolate chips, peanut butter, nuts, etc. than any of those four ingredients. 