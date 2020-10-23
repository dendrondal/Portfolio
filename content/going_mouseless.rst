Going Mouseless, or How I Learned to Stop Clicking and Love the Clack
#######################################################################

:thumbnail:
:category: tutorial
:date: 2020-07-25
:tags: Linux, Vim, Productivity

Jokes about googling aside, it's no secret that writing code involves some pretty heavy browser usage.
Like may people, I used to be one of those who opened so many tabs that I could no longer see the title on each.
Though there are browser extensions that help with this, I knew there had to be a better way.
This, in a very roundabout way, ended up being the starting point in the journey I'm going to outline in this post.

On my home home computer, I'm a bit spoiled.
I have a mechanical keyboard, two monitors (one horizontal & one vertical), and a gaming mouse with side buttons.
Because of this, I've always preferred doing any heavy-duty developing on my desktop, and saving minor edits/documentation/model training on AWS for my laptop.
However, for various reasons, I've needed to use my laptop more as of late.
I thus wanted to make my development environment as comfy and efficient as possible.
This was done in four ways:

1. **Tiling Window Management** Though this was the first part of my journey, it actually may be the least important, as it requires a decent amount of overhead to set up.
That being said, I definitely believe it was worth it.
Once you get more comfortable with workspace navigation, switching windows, and custom sizing/placement, it's kind of hard to go back.
But, be very warned that `ricing <https://rizonrice.club/Main_Page>__` your own custom workspace is both very fun and time consuming, so prepare to get sucked down that rabbit hole.
I started with the most popular and apparently easiest-to-use one, `i3 <https://i3wm.org>`__, though there are many more available.
AwesomeWM is apparently also beginner friendly, and there are some `absolutely gorgeous <https://github.com/elenapan/dotfiles/wiki/Gallery>`__ themes you can use for inspiration.
However, I found the documentation for i3 to be superior, which means it's certainly my reccomendation.

2. **Browser choices** I've used the Chromium-based Brave for quite awhile, and although I highly approve of their mission statement, I wanted something that was both easier to sync across multiple machines, and far more customizable.
This lead me to another Chromium-based browser called Vivaldi with a dizzying number of customizations.
This includes, very importantly, tab stacking and custom hotkeys.
Thus far, I've had consistently less ram usage and less crashes than Brave, though a similar number of compatibility issues.
The ability to add `web panels <https://vivaldi.
com/blog/5-web-panels-to-add-for-programmers/>`__ is also quite nice, though I've had issues with notification badges and ProtonMail staying logged in.
It turns out the hotkey customizations, while super nice, where mostly irrelevant due to a certain extension.

3. **Vimium** Not to sound clickbaity, but this is easily my all-time favorite browser extension (minus an ad-blocker, which is thankfully a default in Vivaldi). I had never used Vim before, but this seemed to be unanimously recommended for making the browser more keyboard-friendly. This gif illustrates my favorite of its features, accessed by simply pressing the `f` key (or `F` to open the link in a new tab):

|image0|

No more scrolling, no more moving the mouse around, just pure touch typing to search and navigate.
It's an absolute godsend.
There are also plenty of other keybindings, many of which are just more efficient versions of standard browser ones.
For example, instead of the standard `ctrl + pgup/pgdown` to navigate tabs, it's simply `J` and `K`, so your hands never have to leave the home keys.
Unsurprisingly, these are adopted straight from Vim, so you can Guess where this goes next...

4. **Vim (or vim bindings)** Yes, I've gone full tech hipster here, but hear me out.
If you're already familiar with the extensive key bindings thanks to Vimium, it actually steepens the learning curve for Vim (and yes, by "steepen", I mean make easier, as opposed to the colloquially common form of the phrase).
There are several very useful features that I wish were in other IDEs, such as `dw` to delete a word or `3b` to go back 5 words, or the ability to save markers.
There several great tutorials outside of the `vimtutor` that comes with vim, including `this one <https://danielmiessler.com/study/vim/>`__ and this really entertaining guy's `entire YouTube channel <https://www.youtube.com/channel/UC8ENHE5xdFSwx71u3fDH5Xw>`__.
I'm not suggesting going fully into Vim, because thankfully other IDEs such as VSCode have plugins for vim bindings.
The text editor part itself is almost secondary.
The modal nature of Vim is what makes it exceptional.
When writing/coding, think of how long is spent editing vs. how long is spent actually writing.
I'm sure you'll agree that editing takes up far more time.
Having a way to efficiently navigate and rewrite sections of text is more helpful than I can possibly articulate.
If you've ever seen a Vim veteran at work, you'll understand what I mean.
So far I'm absolutely loving it. It feels almost like I'm playing StarCraft again, trying to find the most efficient key combos to max my APM.
As a very important added bonus, I feel it's making me better at Linux as a whole, considering that the vi normal mode keybindings are the *lingua franca* of many Linux apps.

So there you have it.
How having too many tabs led me on a journey to Vim.
It definitely takes awhile to learn, but I think it's been worth it.
Did it make me more efficient, and a faster developer? Time will tell that, but I'll leave you with this very relevant XKCD on the subject.


|image1|


.. |image0| image:: https://sudipbhandari126.github.io/resources/links-vimium.gif
        :width: 100%
.. |image1| image:: https://imgs.xkcd.com/comics/is_it_worth_the_time.png
        :width: 100%
