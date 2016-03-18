# pymdb-analyse
A simple python script that generates graphs about imdb viewing habits.
This script has not been under version control(till now!)
To use this script, ensure that you have the pygal library.
Get the csv of your imdb ratings (It should be at the bottom of your ratings page)
The csv should be present in the same directory as the script.
On running the script, svg images are generated, with a graphical representation
of a bunch of movies you've watched. These svg images can be viewed with any (preferably modern) browser.

For reference, I've included the csv from my ratings, as well as svg files that were generated from my data.

TODO:
- Handle Unicode data better
- Include functionality to automatically get your public ratings data, given the user URL
