A Wild Async Appeared!
######################

:thumbnail:
:category: Blog
:summary: Part 3 of the Wild Python series, focusing on the Async/Await keywords
:date: 2020-11-08
:tags: wild python, web development

Background
-----------
I was recently refactoring the web scraper in my `Localvore`_ app to be applicable to a broader range of websites, but realized that the performance was severly lacking. I vaguely knew about Python's `async` capabilites, and that they are most applicable in i/o bound operations. Given that this was one of them, I swtiched to an asynchronous approach, giving me a nearly 100x speedup! This was even after limiting the number of coroutines, so that I could be a polite scraper and not overload my targets' servers. This was not a painless process, as the `async/await` approach effectively comprises a new programming paradigm.

So what is `async` and when should you use it? Imagine you have a VR bakery. There are several functions, `mix_ingredients`, `bake_cake`, `make_frosting`, and `frost_cake`. Let's say you have 100,000 cakes to make. With a normal, synchronous approach, you would have a single thread, or baker, for each cake, going through the entire process in order. With async, you can have a predetermined number of bakers (let's say 100 in this case) operating in a much more chaotic, but faster and more efficient manner. You'll have ones that see the `mix_ingredients` line is too long, and jump over to the `make_frosting` line. After executing the `bake_cake` operation, they'll jump to start another cake or frosting as soon as it's in the oven, `awaiting` the cake's completion. Effectively, any process that can get more done with multiple workers can _theoretically_ benefit from Python's `async` abilities. For a much more detailed example of how all of this works, I would reccomenned this `blog post`_, which also mentions some of the shorcomings of this approach.

Async in Action
----------------
One thing that the addition of these keywords to the standard library has done is create a wave of new web frameworks that are async-first. My personal favorite of these that I have seen is `FastAPI`_.
