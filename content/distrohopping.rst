Should you switch to Manjaro Linux?
####################################

:summary: Probably not. Here's why:
:date: 2020-05-02
:category: blog
:tags: Linux, Bash, Docker, TensorFlow

Since I first decided I wanted to install GPU-enabled TensorFlow, I've mainly been working on Ubuntu 16.04. However, as of late, there have been several issues that prompted a switch. The first of which was that I could not for the life of me get Docker to install. Secondly, updating CUDA for my (now) rather old GTX 660 GPU so that I can use all of the newer TensorFlow features became significantly more difficult and less stable. Ubuntu 19.04, adorably named Disco Dingo, claimed to `fix some of the GPU compatibility issues <https://wiki.ubuntu.com/DiscoDingo/ReleaseNotes>`_, but since I was between OSes, and Ubuntu's parent company, Canonical, has been `known to participate in some sketchy business practices <https://ubuntu.com/legal/data-privacy>`_, I decided to experiment instead. Looking at both `DistroWatch <https://distrowatch.com/>`_ and the `Distro hopping subreddit <https://www.reddit.com/r/DistroHopping/>`_, Manjaro Linux seemed to be the most highly recommended and well reviewed, with a few caveats that we'll come back to. I decided to give it a try. Feel free to skip the next section if you're a nix veteran, but if you're relatively new to the non-Ubuntu Linux world, this may be good to know.

Distros & Desktops
-------------------
It's very important to note that all of the things I'm talking about run on the same Linux Kernel, so deep down under the hood, they all work the same. However, out of the absurd number of distros out there, they can be roughly grouped based on how they manage their software.

|image0| 

- **The Debian family** This is where Ubuntu, Mint, Kali, and Elementary OS fall. They primarily use ``apt`` as their package manager, with some of them using ``flatpak`` or ``snap``. The Debian archives are massive, but installation sometimes takes several steps due to dependency management. ``Snap`` tries to fix this, effectively trying to be the Linux version of the Apple store, but the tradeoff is that apps installed through here are often `significantly slower than their apt counterparts <https://askubuntu.com/questions/948861/why-would-i-want-to-install-a-snap-if-i-can-install-via-apt-instead>`_, and the selection isn't as broad. Also, with apt, in order to keep your software on the bleeding edge (if needed), you need to use a personal package archive (PPA). **These must be used very carefully**, as they have the potential to be a large security vulnerability. Make sure the source is trusted. 
- **The Red Hat family** These are the kings of the enterprise servers. Slow to update, but very stable in exchange. I haven't personally used Fedora or the like, so I can't really say much else here.
- **The Arch family** Arch itself is quite popular, and notoriously difficult to install. Manjaro sought to streamline this process for a better out of box experience. The Arch user repository (AUR) is used for software installation here, and is a major draw toward Manjaro. To use a Python analogy, ``apt`` seemed like using ``venv + pip`` for dependency management, whereas the AUR felt more like `Poetry <https://python-poetry.org/>`_ with how it handles dependency management. Unlike what we've talked about so far where the distros have versions, Arch and Manjaro both have rolling releases, meaning that you effectively always have the latest and greatest. This comes with the tradeoff of stability, and Manjaro actually runs slightly behind Arch so that pure Arch users can be used as a test audience.
- **The SUSE family** openSUSE lies somewhere in between Manjaro and Ubuntu, as it allows both versioned and rolling releases. I have little experience with this family, but out of all the families/distros, the computational chemists in my PhD program chose openSUSE, which speaks very highly of its reliability and flexibility.

I'm sure I missed a significant number here, but I believe these are the four biggest families. In addition to distros, there are also desktop environments (DEs). Ubuntu users know that it normally ships with GNOME desktop, but there are also versions such as Kubuntu and Xubuntu that look very different, with the first letter indicating the DE. GNOME tends to be the most resource-intensive DE, and XFCE/LXDE(LXQt) tend to be the lightest. In between these, we have KDE, Cinnamon, Budgie, and many others. Honestly, unless you're on an older computer, resource usage is kind of a moot point, as if you have a few tabs open in $YOUR_FAVORITE_BROWSER, you've already eaten up far more resources than any background DE process. KDE Plasma has the reputation of being the most customizable if you want to tinker, but otherwise, just spend some time on the boot disk OS and use what catches your eye (and is actively maintained, preferably).

If you want something even more minimalist, or would like more keyboard control, there's also an entire ecosystem of window managers (WMs). There's a great post on `the ubuntu forums <https://ubuntuforums.org/showthread.php?t=2415676&>`_ that covers comprehensively covers DEs/WMs.

"I use Arch, BTW"
------------------
Manjaro installation is equally as easy as Ubuntu, even having an option to install alongside another OS on the same drive. It's literally a point and click installer that can be easily put Manjaro alongside Windows. KDE is lives up to its reputation of being incredibly customizable, but has built-in global themes available to improve the look out of the box (normal Plasma is just ok looking, IMO). AUR is not enabled by default, which is understandable for security reasons. Much like PPAs with apt, one needs to be very careful to note who the package is coming from. The package manager, pacman, can install packages in a single line once they recieve enough upvotes in the AUR, but otherwise, you'll need to use ``makepkg`` first before using pacman. If you elect to do this, make sure you check the PKGBUILD and .install files for any suspicious requirements or scripts. Unless you need some very niche software, it is far more time-efficient to limit yourself to packages directly installable via pacman.

Now we get to the true test: installing GPU-enabled TensorFlow. This is where Manjaro really shines, due to its built in hardware detection and pacman. I've had issues with conda, pip, and the incredibly slow bazel for installation, and the official Docker container for some reason `runs on legacy python <https://hub.docker.com/r/tensorflow/tensorflow/tags/>`_. Thankfully, on Manjaro, all I needed was:

``sudo pacman -S cuda cudnn python-tensorflow114-opt-cuda``

.. warning:: This is no longer the most up-to-date version of TensorFlow. When I did this, the 1.14 didn't even need to be specified. More importantly, there is apparently a `bug in bazel <https://github.com/tensorflow/tensorflow/issues?q=is%3Aissue+is%3Aopen+bazel+runtime+exception>`_ preventing this install from working unless you downgrade it, so proceed with caution.

After happily using GPU-enabled TensorFlow for awhile, I eventually decided to restart my computer for one reason or another, and when I booted back into Manjaro, I received the dreaded blinking cursor on a blac k screen. I thought maybe I had somehow messed with my Grub loader, so I used my live disk to check it with ``fstab``, and everything appeared to be in order. I tried downgrading the Kernel, as apparently there were issues with the newest release, still nothing. Finally, I decided to uninstall my NVIDIA drivers, as they rarely play nice with Linux. This black screen didn't respond to any commands to bring up a command prompt, so after a couple painful days, I had to call this a loss. The issue was most likely due to the fact that I let pamac (the pacman gui) manage my updates for several packages for me, which caused some sort of `breaking change <https://www.youtube.com/watch?v=skMiDMaephc>`_. In other words, this was definitely my fault. 

It's important to learn that cutting-edge implies you can also cut yourself with it, as I did. Apparently Manjaro does `have a tendency to break  occasionally <https://forum.manjaro.org/t/the-how-often-does-an-update-break-something-survey/45702>`_ unless properly managed, which I suppose is true of any Linux distro, but is likely far more true with a rolling release. One side note is that I ended up messing around with Kubuntu rather than doing a reinstall, and had significant issues with the display, ranging from granularity in parts of my windows to full-stop freezes. Given that I know Ubuntu works on this machine, I now wonder if KDE Plasma was the issue rather than Manjaro, as it clearly just doesn't work on my machine.

Key Takeaways
-------------
Think about what you need from your OS. Most people reading this are probably some variant of a data scientist or developer, so we mainly need an environment conducive to programming in Python/R/Scala/JavaScript with all our required tooling. A stable OS is necessary for this, so unless you want to dive far deeper into the inner workings of nix, Manjaro probably isn't for you. In addition, it's important to remember that software is a popularity contest of sorts. I say this because the more people use a given OS/software/framework/language, the higher the chance that someone has had the same problem as you and possibly found a solution. 

For those curious, I ended up settling with Linux Mint on my desktop, and I don't see myself hopping to anything else anytime soon. Cinnamon is a gorgeous and highly customizable DE, and everything else just feels natural. On my laptop, I still use Ubuntu, but I also use I3 WM to minimize how much I need to use the trackpad and maximize efficiency. This definitely took some tinkering (along with some `shameless copying <https://www.reddit.com/r/unixporn/comments/b79cva/i3gapspolybarcyberpunk_theme_v2/>`_), but I'm very happy with the result:

|image1|

The **most important takeaway** is whatever you do, make sure your "dots" are put under version control. That is, your ``.bashrc, .zshrc, .config,`` or whatever other config files your particular flavor has. Atlassian has a `good guide <https://www.atlassian.com/git/tutorials/dotfiles>`_ on how to set this up. I also have a few `install scripts <https://github.com/dendrondal/dots>`_ in the same repository as my dots, so if I change machines, I can have a reproducible environment in no time!

.. |image0| image:: https://cdn-media-1.freecodecamp.org/images/1*7KP2aqaHVrCgJfF9mhE8hQ.png
    :alt: The Linux family tree. See, it's not so complicated! /s
    :width: 400px

.. |image1| image:: {static}/images/desktop_screenshot.png
    :width: 400px