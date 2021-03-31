# pq2-smart-cookies

Danny Little, Bruce Tang, August Wadlington
CSCI 3725

Our first portion of this assignment involved making a CC system to generate cookie recipes. This was done in a manner similar to the previous assignment, with a few main changes. We weren't given any data to use, so we scraped some recipes from Allrecipes.
We also used a new concept in our recipe generation: core ingredients. If every single cookie recipe we scraped has, for example, eggs, flour, butter, and sugar, we probably would want our system to be more free to experiment with other, “extra" ingredients like chocolate chips, peanut butter, nuts, etc. than any of those four ingredients.

Our fitness functions evaluate the recipe from three angles: is it a cookie recipe, how creative is the recipe, and does it taste good. To determine if it is a cookie recipe, we look at the amount of core ingredients used compared to the ones in the input pool, because regardless of the extra ingredients, the core ones establish the base of the cookie. To determine the level of creativity, we compare the frequency of extra ingredients in all input recipes. And lastly, we experimented with flavor pairing to determine whether the extra ingredients would actually make a tasty cookie. 


The two metrics we focused on during our evaluation phase were novelty and value. We chose these two metrics, firstly novelty, as we wanted our generator to give us something unique, using flavor combinations that were more unorthodox and pulled from flavors used in a variety of different cookies, but we also focused on value, using both generation constructions like core ingredients, and then flavor pairings and “core fitness” in our evaluation phase to make sure we weren’t being overly risky and had some safety nets in place for our recipe generation. We especially made sure to focus on value in our fitness methods, in order to ensure we followed baking conventions such as including flour, eggs, etc. to ensure that while we had a “novel” cookie, we still generated a recipe resulting in something falling under the cookie classification.
