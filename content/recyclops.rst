Recyclops, pt. 1
#################

:thumbnail:
:category: projects
:date: 2020-08-12
:tags: Computer Vision, PyTorch, Keras, Linux, AWS, Docker


Back in March, I completed a fellowship with `Insight Data Science <https://insightfellows.com/data-science>`__.
For those unfamiliar, Insight has a capstone project, which consists of a data-based product.
Unsurprisingly, the process of ideating a data product is incredibly difficult, between the general popularity of data science, the large number of alumni Insight has now produced, and the grueling 2 week timeline for an MVP with a team of 1.
After having many ideas shot down, I finally settled on a problem near and dear to me: recycling.
There exist several "smart" recycling bins `on the market <https://www.smithsonianmag.com/innovation/smart-recycling-bin-could-sort-your-waste-you-180964848/>`__, which have a computer vision component telling you which bin to put your item in.
However, these bins have fixed guidelines, which does not reflect the large variance in recycling center requirements.
In fact, this represents a `major issue <https://fivethirtyeight.com/features/the-era-of-easy-recycling-may-be-coming-to-an-end/>`__ in recycling centers, resulting in most recycling centers operating at a loss.
This project seeks to solve the computer vision component of smart recycling.

Rather than reinvent the wheel, specific pain points were targeted with this project.
As an example, recycling centers are already highly efficient at `separating different kinds of plastic <https://medium.com/cleantech-rising/heres-your-guide-to-how-recycling-actually-works-1f3d97b37904>`__, but struggle with differentiating between clean and dirty plastic.
Today I wanted to walk through my journey on this project, including some of the unique challenges faced and how certain decisions were made.
In part 1, I want to talk about the background and motivations behind this project, as well as the MVP presented in `this post <https://dalwilliams.info/insight-project-demo.html>`__.
Hopefully, this will help someone who's struggling to bring their app to production.

Getting the MVP
---------------

As alluded to earlier, the ideation phase was in my opinion the most difficult part of this.
It's one of the worst cases of option paralysis I think I've ever had.
In addition to that, I experience the ever-present problem of "scope creep".
This resulted in me refining my MVP to building two proof-of-concept models: one based off of the University of Tennessee (UTK) recycling guidelines, and one based off of Penn State's guidelines.
The reason for this targeting is threefold:

   1. Both universities had well-defined guidelines
   2. College students tend to be more eco-concious
   3. College campuses give the opportunity of testing these models with appropriate hardware in a controlled, reasonable environment.

As to the last point, the idea with these was to do an IoT type deployment, with an ideal deployment being edge inference on a Raspberry Pi with a cheap camera.
In the case of insufficient computational power, the Pi can send images through intranet to a central hub to do the heavy lifting, which then sends the prediction back.
So now that I had the idea, it was time for the technical implementation.
I tried to implement a test-driven development approach, but that ended up biting me later on.

Data Gathering & Cleaning
~~~~~~~~~~~~~~~~~~~~~~~~~~~

I ended up copying the recycling guidelines of the respective universities as nested python dictionaries, which is easiest to understand by looking at the code `here <https://github.com/dendrondal/Recyclops/blob/master/cif3r/data/recycling_guidelines.py>`__.
Next, I built a web scraper with Selenium to download the images. The filepaths to these images were stored in a SQLite3 database along with relevant metadata.
The advantage to this approach is that I could operate off of one central table, adding new tables as needed with guidelines for new universities, joining on their subcategories.
Using SQLite3 had the advantage of bundiling my database with my app, simplifying the prospect of edge computation.
It's important to note that false positives (i.e. dirty items placed in recycling bins) hurt worse than false negatives, so unless a recyclable category is explicitly defined in university guidelines, it's instead labeled as trash.
Re-stating that in SQL code:

.. code:: sql

    SELECT
        hash,
        CASE
            WHEN(recyclable = 'O') THEN 'trash'
            WHEN(recyclable = 'R') THEN stream
        END
    FROM %

Here, stream is the major overlying category (paper, plastic, etc) and the wildcard is the university.
I adapted nomenclature from a `previous approach <https://www.kaggle.com/twhitehurst3/fastai-v1-waste-classification>`__, which used 'O', or organic, for trash.
The images were hand-validated, which was about as tedious as you might expect.
This ended up being a massive waste of time, but hindsight is 20:20.

Model Training
~~~~~~~~~~~~~~~~
My original idea was to use a pre-trained model with a small size, to evaluate my ability to do edge computation. I used `Mobile Net V2 <https://arxiv.org/abs/1801.04381>`__ a ResNet architecture that has a built-in pretrained model in Keras. I added a few trainable layers to the end of the pretrained model, and used several image augmentation steps (rotation, shearing, and zoom) to increase the generalizability of the model. Also, I class imbalances in my training data, so undersampling was applied on the majority class (paper in all cases). An F1 score and a confusion matrix was used to evaluate the model. The results were less than ideal, with an F1 score of ~0.6 for both universities.

Deployment
~~~~~~~~~~~
All of my model training was done on an AWS P2 instance, while I served the model on a far less expensive C5 instance. I wrote a Bootstrap frontend to allow for university selection, and used video capture with OpenCV to allow for inference on a single frame. This prediction was quite sluggish, even on my laptop. Also, getting OpenCV working behind NGINX and Gunicorn presents its own problems.

The Next Steps & Lessons Learned
-------------------------------------
In order to create an MVP, I decided to use tried-and-true methods over more experimental ones. It turns out, in retrospect, that this was a mistake. The amount of data required to have a functional MobileNetV2, even with transfer learning, was prohibitive for a single data cleaner, in addition to being painful. A few-shot learning approach would have been a far more productive route, which I'll go into in part 2. In addition, the approach used for deployment was quite painful. If I'd taken a step back and Dockerized my application rather than having to get all of my installation working over SSH, I would have saved a great deal of time. And finally, rather than the traditional Flask+Gunicorn+Nginx setup, I could have (maybe) used `Streamlit <https://www.streamlit.io/>`__, but to be honest, I wasn't aware of its existence at the time.
