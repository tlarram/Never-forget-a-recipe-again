# Never-forget-a-recipe-again
## Welcome to My Cookbook! 

I created a web application to store recipes since my family loves to cook.  The first sprint includes creating a user based recipe database.  I also used the Spoonacular API to create recipes from items you have at home and can use in the recipe.  The API can also generate recipes if no food is provided so the user can see up to 5 recipes they may be interested in.  Who isn't looking for new things to try?

I like jokes, so there is a random food related joke each time that page loads.  

- Users can view, post, and add recipies to the database
- Create recipes based on items in the fridge or pantry
- Generate random recipes
- View a joke 
- Full CRUD for reciepes including AJAX to show changes without reloading the page
- View all users recipes

## Table of Contents

- [Installation](#installation)
- [License](#license)

## Installation

Feel free to clone the project to implement your own virtual cookbook. 
Clone the project

Create a directory for your files.
You will use pipenv to install flask.
Make sure you are in the file containing your server.py
Use your command promp:
pipenv install flask
pipenv shell
python server.py

THis should get the server up and running at local host 5000.

Contol + Z will exit, and you can type exit to leave the shell.




## License

MIT License

Copyright (c) [2022] [Timothy Larramore]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

---

## Features

- Spoonacular API
- AJAX for adding and updating recipes without refresh
- Recipe Database created by users

# Check out the real-time features!
![Demo of My Virtual Cookbook](/myCookbook.gif)
