Packaging with Pipx!
#####################

:thumbnail:
:category: tutorial
:date: 2020-10-16
:tags: Linux, Scientific Python
:status: draft

Ask most Python devs the largest shortcoming of the language, and they'll most likely say one of two things: the lack of `mobile presence`_ or the difficulties with packaging. It's easy to be jealous of Go/Rust programmers' ability to package everything into a binary install, or C# devs putting their app into an exe. Python may not have this luxury, but that doesn't negate its ability to make clean, intuitive CLIs in a short period of time.

The versioning difficulties are compounded when you try to share your creation with a non-technical audience. It's unreasonable to expect your end-users to have modern Python installed, or to even know what that is in the first place. However, even scientists who have never coded in their life probably have experience with scripting via Excel, LabView, Origin, Igor, or many other CLI-adjacent apps.

Two solutions
-------------
This can be solved by either a lightweight or more versatile heavyweight approach. The lightweight approach involves `pipx`_, a utility that isolates a CLI and its requirements in a venv and adds them to the `PATH` automatically. It's pretty great at what it does, and I've found it to be the most pain-free way to install things like Black or Poetry globally without breaking any dependencies or builds.

Speaking of `Poetry`_, it is actually vital to both of these solutions. For those unfamiliar, Poetry is an all-in-one dependency management, venv, and packaging utility. It uses the rather friendly TOML language to define versions in a fuzzy manner, and will basically refuse to install anything if there's a version mismatch, e.g. one app requires python 3.6.4+, but the project only requires 3.6.0+. These requirements are also locked in place, so people can add dependencies asynchronously without worrying about breaking the build, because poetry will throw a ton of errors your way. It also works very nicely with `pyenv`_, and allows you to export your requirements to the classic `txt`.

The latter is important because of the heavyweight solution: Docker. Pipx installs dependencies via pip. If you have non-pip dependencies, Docker is likely the way to go. An example in my recent past is a project that required a LaTeX install, which can be `quite painful`_ and is prone to OS-dependent errors. So, I wrapped everything up in a `Docker container`_, and everything worked perfectly. However, this takes quite a bit more overhead on the end-users part, and requires more space to be used. Docker is complex enough that it would require another tutorial, but thankfully there are already many `good ones`_ out there.

Packaging & Testing
---------------------
Now that we know our options, let's go through how to get this
