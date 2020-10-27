Packaging with Poetry and Pipx!
###############################

:thumbnail:
:category: tutorial
:date: 2020-10-16
:tags: Linux, Scientific Python, Docker, Poetry, pipx, chemistry

Ask most Python devs the largest shortcoming of the language, and they'll most likely say one of two things: the lack of `mobile presence <https://talkpython.fm/episodes/show/245/python-packaging-landscape-in-2020>`_ or the difficulties with packaging. It's easy to be jealous of Go/Rust programmers' ability to package everything into a binary install, or C# devs putting their app into an exe. Python may not have this luxury, but that doesn't negate its ability to make clean, intuitive CLIs in a short period of time.

The versioning difficulties are compounded when you try to share your creation with a non-technical audience. It's unreasonable to expect your end-users to have modern Python installed, or to even know what that is in the first place. However, even scientists who have never coded in their life probably have experience with scripting via Excel, LabView, Origin, Igor, or many other macro-based apps. As I couldn't find a tutorial on this exact topic when packaging several tools I wrote for my graduate work, I decided to write one for future devs/scientists trying to do the same.

Two solutions
-------------
This can be solved by either a lightweight or more versatile heavyweight approach. The lightweight approach involves `pipx <https://pipxproject.github.io/pipx/>`__, a utility that isolates a CLI and its requirements in a venv and adds them to the `PATH` automatically. It's pretty great at what it does, and I've found it to be the most pain-free way to install things like Black or Poetry globally without breaking any dependencies or builds.

Speaking of `Poetry <https://python-poetry.org/>`__, it is actually vital to both of these solutions. For those unfamiliar, Poetry is an all-in-one dependency management, venv, and packaging utility. It uses the rather friendly TOML language to define versions in a fuzzy manner, and will basically refuse to install anything if there's a version mismatch, e.g. one app requires python 3.6.4+, but the project only requires 3.6.0+. These requirements are also locked in place, so people can add dependencies asynchronously without worrying about breaking the build, because poetry will throw a ton of errors your way. It also works very nicely with `pyenv <https://github.com/pyenv/pyenv>`__, and allows you to export your requirements to the classic `requirements.txt`.

The latter is important because of the heavyweight solution: Docker. Pipx installs dependencies via pip. If you have non-pip dependencies, Docker is likely the way to go. An example in my recent past is a project that required a LaTeX install, which can be `quite painful <https://dalwilliams.info/lessons-learned-from-writing-a-phd-dissertation-in-markdown.html>`__ and is prone to OS-dependent errors. So, I wrapped everything up in a `Docker container <https://github.com/dendrondal/phd_thesis_markdown>`__, and everything worked perfectly. However, this takes quite a bit more overhead on the end-users part, and requires more space to be used. Docker is complex enough that it would require another tutorial, but thankfully there are already many `good ones <https://pythonspeed.com/>`__ out there.

Packaging & Testing
---------------------
Now that we know our options, let's go through how to get this up and working. I'll be using the actual project that inspired this post, `instrumentools <https://github.com/dendrondal/instrumentools>`__, as an example, but this approach should be relatively agnostic. That is, whether you use `argparse <https://realpython.com/command-line-interfaces-python-argparse/>`__, `click <https://click.palletsprojects.com/en/7.x/>`__, or `typer <https://typer.tiangolo.com/>`__ to create your CLI, these steps should serve you regardless. Let's first go through a basic idea of how to structure this project:
::

    .
    |── poetry.lock
    |── pyproject.toml
    |── README.md
    |── instrumentools
    |   └── __init__.py
    |       CAC.py
    |       TEM.py
    |       thermal_analysis.py

The key factor is that each of your CLI components are stored in modules within the parent directory. This allows you to define them as entrypoints within your `pyproject.toml`:

.. code:: toml

    [tool.poetry.scripts]
    tem_analysis = "instrumentools.TEM:main"
    cac_analysis = "instrumentools.CAC:cac_graphing"
    thermal_analysis = "instrumentools.thermal_analysis:main"


This creates symlinks to Python executing the `main` function in the `cli.py` file of each module. To test whether this worked, you first need to run `poetry install` to set up the links, and run `poetry run FEATURE`, where feature could be tem_analysis, cac_analysis, or thermal_analysis in the case above. Alternatively, you could use click to allow multiple entrypoints via a `single command line script <https://click.palletsprojects.com/en/7.x/commands/>`__, which could be better in terms of namespace pollution. I'm sure there are also ways to do this with the other CLI software listed above.

.. block-primary::
        Ideally, it would make more sense to include each feature as a package rather than a module, making your project more modular and less cluttered. Unfortunately, I have not found a way to do this with Poetry's scripts command in a way that pipx understands.


As mentioned before, poetry makes packaging very easy. First, you should create an account on `test.pypi.org <https://test.pypi.org/>`__. Just to make things easier and safer, I would recommend going to account settings and getting an API key. Back on the command line, do this:

.. code:: bash

    $ poetry config respositories.testpypi.url https://test.pypi.org/legacy/
    $ poetry config pypi-token.testpypi <YOUR_API_KEY>
    $ poetry publish -r testpypi --build

As of Poetry 1.0, having the legacy prefix for testpypi is important. You can view your configuration settings using `poetry config --list`, but your api key will be hidden. After running the final command, your package should show up on your testpypi account. You will generate both zipped source code and a `wheel <https://realpython.com/python-wheels/>`__ in the newly created `dist` folder within your repository. There are multiple ways to test whether or not this worked. Note that pipx takes awhile to sync with your remote repository, so the local version may work better in this case:

.. code:: bash

   # Local installation
   pipx run --spec PATH_TO_YOUR_PROJECT/dist/VERSION.whl FEATURE

   # Remote install
   pipx run WHEEL_URL FEATURE

Here, your `WHEEL_URL` can be found under the link for the current release, in the releases page of your project on testpypi. Registering your project to PyPi goes through a very similar process to the test server, just with pypi.org instead, so you can effectively repeat the steps above once you're comfortable with the result. Then by running `pipx install instrumentools`, every command works as expected. As with any programming endeavor, make sure that your code is well-documented! It's important that the end-user doesn't need to memorize commands and can get a nice set of instructions by using `--help`:

.. code:: bash

        Usage: cac_analysis [OPTIONS]

        Graphs .csv output from Bruker UV-Vis software. Outputs stacked UV-vis
        spectra and wavelength (or wavelength raio, depending on dye) vs.
        log(concentration) spectra as .png files in the same directory as .csv
        file.

        Options:
          --path PATH      Full path to .csv file
          --wv_range TEXT  Range of wavelengths (i.e. max - min)
          --min_conc TEXT  Minimum concentration, in mg/mL
          --max_conc TEXT  Maximum concentration, in mg/mL
          --step TEXT      Total number of samples in csv
          --vb1 TEXT       Lambda max/first vibronic band
          --vb3 TEXT       If you are comparing the first and third vibronic band for
                           a dye, (i.e. pyrene), enter it here. Otherwise, just press
                           enter

          --help           Show this message and exit.

Closing Thoughts
----------------
I hope this is a useful tutorial for anyone trying to get a CLI to a broader audience. Though most scientists are primarily used to working with a GUI-based UX, it shouldn't take long to evangelize the advantages of using CLIs for particularly tedious graph creation or simple data analysis. These tools certainly exist in the form of Origin/VBA macros, but Python tends to lend itself to much cleaner code in my personal experience. Even better, having Pipx or Docker makes software that is less likely to break down the road or break system installations.
