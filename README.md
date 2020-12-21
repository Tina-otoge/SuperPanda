# SuperPanda

SuperPanda is a webclient to access SadPanda (e-hentai.org/exhentai.org).

It works by downloading the web pages then parsing them to extract the
information, and then outputs it in templates.

I made this because I was unhappy of the styling capabilities I had with custom
CSS, so I decided to rewrite entirely the HTML of the site.

## Main features

- Show tags in grid view by hovering the cover
- Stripped down titles, hover to show full title
- Keyboard shortcuts everywhere
- Theme system
- Responsive galleries list, use it on desktop, mobile or tablets
- Distraction free and always full size reader
- Turn pages using your left hand so you can keep your right hand free :eyes:
- Easy to read and understand HTML structure and classes, easy custom themes!
- Entirely exposed JSON API, write your own clients or tools using SuperPanda
- Open source (and welcoming pull requests!)

## Missing features

Those are planned but not done yet.

- Login to EH accounts (so your preferred categories, blocked tags, watched tags, etc can be used)
- Adding more settings other than theme, such as layout tweaks
- Support viewing popular, favorites and watched galleries
- Support viewing and posting comments

## Keyboard shortcuts reference

Key         | Page           | Action
------------|----------------|-------
f           | Everywhere     | Toggle fullscreen
z/w         | Everywhere     | Scroll up
s           | Everywhere     | scroll down
a/q/h/left  | Reader         | Go to previous page
d/l/right   | Reader         | Go to next page
g/backspace | Reader         | Go back to gallery
e/t         | Reader/Gallery | Go back to home
c           | Gallery        | Search galleries by first character
a           | Gallery        | Search galleries by first artist
g           | Gallery        | Search galleries by first group
p           | Gallery        | Search galleries by first parody
