# hathitrust book export

*Convenience utility to export books page-by-page from hathitrust, and convert to pdf for printing*

## Installation / Setup

This is intended for macOS only, although it might work on linux too. You need python 3.x and a few libraries.

If you don't have those libraries, you'll need to install the missing ones using pip, e.g.,  `pip install fire`. Follow the prompts.

## Usage

First, set the `SAVE_PATH` variable in `book.py` to the folder where you want to save the files. The script will create new folders inside this folder, for any book you export. It should be the absolute path, e.g,. `/Users/my_username/Desktop`, **not** `/Desktop`.

You may also need to modify the `SSO_INTRO_URL` for your particular instituation / login. This should not be the page that has the login form, but rather a page that requires a login and will redirect you to the login page itself. It could be a list view, or a book detail view.

To run the tool in Terminal, move to the directory where the script is saved (e.g., `cd /path/to/book.py`):
```
python book.py run book_id start_page end_page
```
For example, to get pages 1 - 10 of book mdp.39015073873914, run... `python book.py run mdp.39015073873914 1 10`.

You can find the book_id for a given book by looking in the URL on hathitrust. For example, if the url is `https://babel.hathitrust.org/cgi/pt?id=mdp.39015073873914&view=1up&seq=3`, then the book_id is `mdp.39015073873914`.

The command above will open a chromedriver window (looks like chrome browser). It's important to keep this same chromedriver window open throughout the whole process, since it is used in multiple steps.

Log in with SSO (with 2-factor if needed) in the chromedriver windw, and then go back to the command prompt to continue. You can press any key when you're logged in. You will also need to "Check out" the book in Hathitrust to be able to export pages, by navigating in chromedriver to the book and clicking "Check out" (yellow button). 

The script will then try to export pages. After the first try, it will prompt to ask if the export worked. You can verify this by checking the folder named `path/to/<SAVE_PATH>/<book_id>`. If it did, type *yes* (case sensitive) to move to next step. Otherwise, type anything else.

If it's not working, sometimes you need to load the page in the chromedriver window manually, or re-check out the book, and then rerun (by typing something other than *yes*). Don't worry - it's not abnormal to take a few tries. The site and export is a pretty flaky process.

Once pages are successfully exported, the next step is to convert the indidividual pngs to pdf and combine.

To combine / convert the individual pages to a single pdf:
```
python book.py combine <book_id>
```

The final output should be a single pdf file with the book_id name, e.g., `mdp.39015073873914.pdf`.

## Debugging

* Are all the dependencies installed?
* Don't change chromedriver browser window from the default size! Pixel math will be messed up.
* The dimensions of your screen may be different, so you may have to play with the left/right values in `_save_image` for correct cropping
* Chromedriver must have same (major) version as chrome. You can confirm this by running `chromedriver -v` and `chrome - v`. If they are different, upgrade one of them!
* Restart your computer? lol

## Note

This is simply meant as a convenience tool for users to download content they already have access to. 

It is not meant to facilitate unauthorized or illegal access, and you take on all responsibility by using this tool. 

You can modify and redistribute it however you'd like.

