A Wild Hypothesis Appeared!
###########################

:tags: wild python, testing, tutorials, functional programming
:category: Blog
:summary: Part 2 of the Wild Python series, focusing on property-based testing
:date: 2020-05-29

.. note-default:: This article presumes some familiarity with unit and functional testing, as well as pytest. Though there are many tutorials for these topics online, I found less on the Hypothesis library. Moreover, I wrote this article to gain some intuition as to *when* to use property-based tests rather than example-based tests.

What is property-based testing?
--------------------------------
Putting it rather coarsely, property-based testing (PBT) is a method of brute forcing your tests. Rather than the general workflow of asserting what a function should output with a given example, PBT runs the function multiple times with inputs sampled from a space of all possible examples. You may be thinking "why not just use ``pytest.mark.parameterize``?" The answer is edge cases and other unknown unknowns. In theory, this should catch bugs more quickly, and result in less code necessary for your test suite by not having to manually add pytest marks.

|image0|

The introduction to `Hypothesis <https://hypothesis.works/articles/getting-started-with-hypothesis/>`_, a PBT framework for Python, gives a quick rundown of what this might look like. Hypothesis is effectively the Python version of `QuickCheck <https://www.youtube.com/watch?v=hXnS_Xjwk2Y>`_, Haskell's PBT framework. Functional programming languages like Haskell lend themselves well to PBT, due to their heavily mathematical nature. Going through some `properties of mathematical funcitons <https://dev.to/jdsteinhauser/intro-to-property-based-testing-2cj8>`_, their Python equivalents would look something like this:

.. code:: python

    # Associative: a + (b + c) = (a + b) + c
    assert lst1.extend(lst2.extend(lst3)) == (lst1.extend(lst2)).extend(lst3)
    # Commutative: a + b = b + a
    assert max([2, 3]) == max([3, 2])
    # Distributive: a(b+c) = ab + ac
    assert 'asdf'.upper() + 'jkl;'.upper() == ('asdf' + 'jkl;').upper()
    # Idiompotent: f(x) = f(f(x))
    lst1 = lst.sort()
    lst2 = lst.sort().sort()
    assert lst1 == lst2
    # Identity: f(x, i) = x
    assert lst.extend([]) == lst
    # 'Bilbo' testing (there and back again)
    assert lst1[::-1][::-1] == lst
    # No surprise side effects
    assert len(lst) = len(lst[::-1])

These are contrived examples, but they should give you some sort of an idea of what the "property" in PBT implies. I originally referred to PBT as brute forcing your tests, but that's only partially true. A good framework, like Hypothesis, will change behavior once an assertion fails, and "shrink" the input it provides until it can provide a *minimum working example* of what will cause your program to break. This save a lot of guesswork in diagnosing the problem.

Hypothesis in Action
---------------------
At its core, Hypothesis builds its test suite around strategies (the ``st`` module from here on). These allow for random generation of data types within Python, and allow for parameterization (i.e. an ASCII string with a minimum length of 1). For more complex data types, ``st.composite`` can be used. Other important terms are ``given`` and ``assume``. The ``@given`` decorator is used to express which strategies and boundaries a function should be tested with, and ``assume`` removes test cases that we don't care about. The opposite of assume, ``@example``, tells hypothesis to try this test case every single time. A good place for this would be to include a SQL injection attack as an example when testing a Flask function that has a query string.

Before going into production use cases, let's take one of our contrived unit tests from the previous section and change it to a Hypothesis test. Let's say we're writing our own programming language, and want to make sure our version of Python's ``upper`` method work properly. This is an ideal use case for PBT, as we want to make sure this can handle any kind of text:

.. code:: python
        
    @given(data=st.text(min_size=1))
    def test_upper(data):
        # Idiompotency
        assert data.upper() == data.upper().upper()
        # Distributive (this assumes + is overloaded for string concatenation)
        assert data.upper() + data.upper() == (data + data).upper()
        # No side effects
        assert len(data.upper()) == len(data)

This is where hypothesis gets its name from, as we could write out the above test like a traditional hypothesis: "Given a string of length > 1, upper will be idiompotent, distributive, and will return a string with the same length as its input." Then we test it by trying to find a case that falsifies that hypothesis. If we were wanting to extend our new language's functionality by using the ``extend`` method (see what I did there?), we would need a more complex data type to test on. This is where composite strategies come in:

.. code:: python

    @st.composite
    def make_lists(draw):
        return draw(st.lists(st.lists(from_type(), min_size=1), min_size=3, max_size=3))

    @given(data=make_lists())
    def test_extend(data):
        assume(len(data) == 3)
        lst1, lst2, lst3 = data
        concat = lst1.extend(lst2.extend(lst3))
        # Associativity
        assert concat == (lst1.extend(lst2)).extend(lst3)
        # No side effects
        assert len(concat) == sum([len(lst) for lst in data])
    
Here we draw 3 lists full of arbitrary data types and lengths with ``make_lists``, and try to combine them. As a fail-safe, we assume that all three lists exist.Not to belabor the point, I will recommend the `documentation <https://hypothesis.readthedocs.io/en/latest/data.html>`_ for more examples, and move on to production use cases.
    
Hypothesis in the Wild
----------------------

The `APIFuzzer <https://github.com/KissPeter/APIFuzzer>`_ library uses Hypothesis to see if their API testing framework can handle arbitrary JSON. This is trivial to implement in Hypothesis:

.. code:: python

    @st.composite
    def dict_str(draw):
        return draw(st.dictionaries(st.text(min_size=1), st.text(min_size=1), min_size=1))

    @st.composite
    def list_of_dicts(draw):
        return draw(st.lists(dict_str()))

    @given(data=dict_str())
    def test_json_data_dict_valid(data):
        res = json_data(data)
        assert isinstance(res, dict)

    @given(data=list_of_dicts())
    def test_json_data_list_valid(data):
        res = json_data(data)
        assert isinstance(res, list)

Walking through this code, the composite used draws from strategies, producing nonzero sized dictionaries with string keys and values. It can then produce lists of these dicts by drawing from this strategy. It's then used to make sure their ``json_data`` function returns the proper type regardless of what is thrown at it. The Hypothesis documentation has an `even more robust <https://hypothesis.readthedocs.io/en/latest/data.html#recursive-data>`_ example of generating random JSON by using a recursive strategy. This method uses unbounded types, but we can also add boundary conditions based off of what input sizes/shapes we expect. Here's an example from `pyvista <https://github.com/pyvista/pyvista>`_, a 3D rendering library, where they want to make sure an error is raised when someone tries to use their ``grid.transform`` method is called on an improperly shaped array:

.. code:: python

    @given(array=arrays(dtype=np.float32, shape=array_shapes(max_dims=5, max_side=5)))
    def test_transform_should_fail_given_wrong_numpy_shape(array, grid):
        assume(array.shape != (4, 4))
        with pytest.raises(ValueError):
            grid.transform(array)

Let's move on to something that many data scientists will want to keep in mind, which is determining whether the output of a function is stochastic or deterministic. The `Axelrod <https://github.com/Axelrod-Python/Axelrod>`_ library, a game theory simulator in python, does just this with Hypothesis. Here, they test to see if either randomizing the choices of their players at the start by using a ``Random`` player or making the decision making of the players less consistent by adding noise.

.. code:: python

    @given(p=floats(min_value=0, max_value=1))
    def test_stochastic(self, p):

        assume(0 < p < 1)

        p1, p2 = axl.Cooperator(), axl.Cooperator()
        match = axl.Match((p1, p2), 5)
        self.assertFalse(match._stochastic)

        match = axl.Match((p1, p2), 5, noise=p)
        self.assertTrue(match._stochastic)

        p1 = axl.Random()
        match = axl.Match((p1, p2), 5)
        self.assertTrue(match._stochastic)

As you can imagine, this pattern would be ideal to test a bootstrapping or test-train splitting function. Hypothesis also lets you set the seed for the randomization, helping you ensure reproducibility.

Extensibility
-------------

Hypothesis also has built-in modules for Numpy (``hynp`` below) and Pandas compatibility. Here is a test within Numpy itself that makes sure array printing works with all possible unicode strings:

.. code:: python

    @given(hynp.from_dtype(np.dtype("U")))
    def test_any_text(self, text):
        # This test checks that, given any value that can be represented in an
        # array of dtype("U") (i.e. unicode string), ...
        a = np.array([text, text, text])
        # casting a list of them to an array does not e.g. truncate the value
        assert_equal(a[0], text)
        # and that np.array2string puts a newline in the expected location
        expected_repr = "[{0!r} {0!r}\n {0!r}]".format(text)
        result = np.array2string(a, max_line_width=len(repr(text)) * 2 + 3)
        assert_equal(result, expected_repr)

As for Pandas, I'll use an example from my `Localvore <https://github.com/dendrondal/Localvore>`_ project. I had a function, ``filter_predictions``, that was the core of an ETL pipeline. At a high level, it ingested a dataframe of JSON data of recipes (e.g. {'text': '1 cup flour'}) along with ids and matching model predicitons, and produced another dataframe with ids and ingredient lists (minus adjectives and units, e.g. 'flour'). Given that this was the major bottleneck in my ETL pipeline, I wanted to make sure any errors were caught early. Rather than using a mock DataFrame, I instead decided to let Hypothesis do the heavy lifting for me:

.. code:: python

    @given(
        data_frames(
            columns=[
                column(
                    name='_id',
                    elements=st.text(min_size=10, max_size=10,
                                    alphabet=string.ascii_lowercase)
                ),
                column(
                    name='raw_ingrs',
                    elements=st.lists(
                        st.dictionaries(keys=st.just('text'),
                                        values=st.text(min_size=3, max_size=12,
                                        alphabet=string.ascii_lowercase),
                                        min_size=1, max_size=1),
                        min_size=5, max_size=5),
                    dtype=list
                ),
                column(
                    name='valid',
                    elements=st.lists(st.booleans(), min_size=5, max_size=5),
                    dtype=list
                ),
            ]
        )
    )
    def test_filter_predictions(mock_df):
        assume(len(mock_df.columns) == 3)
        assume(len(mock_df) != 0)
        df = ETL_pipeline.filter_predictions(mock_df)
        assert len(df) > 0
        assert len(df.columns) == 2
        assert len(df['ingredients']) > 0)
        assert isinstance(df['ingredients'][0], str)

The ``data_frames`` utility can define a set of columns, with names and strategies for each column. I'm also making the assumptions that the dataframe is non-empty, and has the proper number of columns. Note the versatility of strategies available here: one can choose the alphabet to draw from, can create a list of booleans, and can fix a certain value, such as all dictionaries having the 'text' key. This may be a lot of code, but it allows me to be very confident in the code that I write. In addition, I could reuse this mock dataframe strategy by putting it in a function with the ``composite`` decorator.

When *Not* to use Hypothesis
-----------------------------

Some advice from the Hypothesis documentation gives some good starting wisdom: if you find that you need to parameterize a test extensively, that is a good sight PBT may be effective there. The primary reasons I have found not to use PBT is when either properties are very difficult to think of, or when they add too much overhead to your CI/CD pipeline (the default number of function calls for each Hypothesis test is 200). Between this increase in runtime, mental overhead, and code, PBT should not be your go-to method of testing, but instead a tool in your toolbox. The key factor in deciding what type of test to use isn't necessarily the complexity of your function, but *how many different types of input* are valid for said function. PBT can also be useful when approaching large legacy codebases. As a particular example, `this article <https://medium.com/criteo-labs/introduction-to-property-based-testing-f5236229d237>`_ about PBT in JavaScript managed to find a bug in a 1 million download/day package by treating a certain function as a black box, and making assumptions from there. 

I hope this introduction was helpful to all reading it. My challenge to you is to find a test you've written for a function with many possible input types, and try a property based test there. Let me know how it goes!


.. |image0| image:: https://1.bp.blogspot.com/-5n5lQoNvzNU/XAT3u9uu8SI/AAAAAAAAhUo/OMOOhkSYKNMAXaGeW0MfF07uudCWa-HZwCLcBGAs/s1600/everyone.png
    :width: 400px