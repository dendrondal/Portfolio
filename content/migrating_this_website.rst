Website Redesign
#################

:date: 2020-05-10
:category: Blog
:summary: Migrating to GitHub pages and simplifying everything
:tags: Markdown, rST, Make, Git, CI/CD, Pelican, Flask, Jinja, CSS

If you've ever been to my website previously, you've surely noticed a complete overhaul of the appearance. True, it's no longer nearly as fancy, but it's now far less bloated and easier to maintain. Considering I'm not trying to showcase my talents as a frontend engineer, that's a tradeoff I'm more than willing to make. If you read `my previous post <https://dalwilliams.info/making-this-website.html>`_ regarding the creation of this website, particularly the part about making it static, you probably thought to yourself "isn't this just a rough version of `Pelican? <blog.getpelican.com>`_" And yes, that's exactly the case. But it made for a great teaching experience! It got me thinking more about API design, gave me my first exposure to AWS, and gave me my first experience writing Travis CI. But, once I decided to start adding even simple features, like tags to my posts, or changing the appearance of the posts themselves I started to realize the amount of CSS I had was slowing me down significantly.

Slimming down
--------------
For anyone who has previously used Flask, Pelican is a pretty smooth transition, as it uses Jinja2 as its templating engine. There are quite a few external themes and plugins available to alter the appearance, depending on personal taste or how much customizability you need. Out of all the Pelican themes out there, one that particlularly caught my eye was `m.css <https://mcss.mosra.cz/why/>`_. It's very minimalistic, and doesn't include a single line of JavaScript, while still being responsive and looking clean. This actually got the load time of my page down from 771 to 283ms. Keeping with the ease-of-use of Pelican, adding variables to your ``pelicanconf.py`` file can be used to edit quite a bit of website styling. Also, if you look at the ``master`` vs. ``pelican_migration`` branches of `my portfolio repository <https://github.com/dendrondal/Portfolio>`_, you'll see just how much simpler the file structure is.

Learning a new language
---------------------------
Though I definitely like Markdown, having even `writing an entire PhD dissertation in it, <https://dalwilliams.info/lessons-learned-from-writing-a-phd-dissertation-in-markdown.html>`_ both Pelican, m.CSS, and `Read the Docs <https://readthedocs.org/>`_ reccomended rST as the writing languange, for reasons that are best outlined `here <https://www.ericholscher.com/blog/2016/mar/15/dont-use-markdown-for-technical-docs/>`_. In short, there are many flavors of Markdown, which leads to ambiguity and migration issues. In addition, rST is the native language for Sphinx documentation, which makes it a very useful skill to have for any software developer. It's surprisingly intuitive, and gives you far more control over styling than Markdown.

Changing platforms
------------------
Though learning to use S3 was an incredibly valuable skill, my AWS free tier subscription expired, making me look for other options. GitHub pages natively supports the Ruby framework Jekyll for creating blogs, but there are plenty of ways to host Python blogs there too. I used the cleverly named `Elsa <https://github.com/pyvec/elsa>`_ to integrate a TravisCI based deployment of my Flask frozen website. Of course, by using the ``ghp-import`` library, an analogous Pelican deployment is as easy as ``make github``! Given that pretty much every  developer has Git experience already, GitHub pages is a natural integration for most workflows, and I would highly reccomended it for a developer blog.

Final thoughts
--------------
So the million dollar question is, what would I do differently if I did all of this again? Honestly, the answer is not much. Yes, I ended up effectively throwing a lot of code away, but the lessons I learned as a part of the process more than made up for it. If you're familiar with AWS and Flask, then you should probably just be using Pelican. My advice is to think about how you want to present yourself to potential employers, as well as the rest of the programming world. If you want to be a full stack developer or want to specialize in creating beautiful dashboards as a data scientist, you'd probably benefit in buiding all of the CSS/templates (and possibly JS) from the ground up. If you're on the back end of things as an ML/Data engineer, just go with something like m.CSS and start writing. However, there's really no wrong answer so long as you keep a lifelong learnign mindset! 
