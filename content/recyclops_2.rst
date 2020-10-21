Recyclops, pt. 2
----------------

:status: draft

In `part one`_, I covered the background behind recyclops up until the point of `this presentation`_.In this part, I'm going to focus on how my product was improved from this MVP.

Few(er) shot learning
----------------------
My goal was to get to the point where models could be tailored to university guidelines. I originally had in mind to train a model for each university, and store it for inference. However, my hypothesis was that transfer learning from one set of university guidelines to another would speed up training. This did not prove to be true. In addition, even though MobileNet V2 has a small footprint, storing many of these models with the relevant data is very space inefficient. This application seems to be a great for `few-shot learning`_. I adopted the approach of establishing a new `git` branch for each type of model I was testing, so that I could "move fast and break stuff". This is the progression that I ended up following:

Scaling Down
~~~~~~~~~~~~
Given that the necessary data for few-shot learning is only ~5 examples per class, I ended up taking the first 24 high-quality examples from each subclass (e.g. plastic bottles, cardboard, soda cans). This is highly advantageous, as adding a new subclass is now far less intense than scraping several hundred examples as per the MobileNet approach. Once I had my "new" data, it was time to find a suitable model.

Siamese Networks
~~~~~~~~~~~~~~~~
`Siamese networks <https://www.cs.cmu.edu/~rsalakhu/papers/oneshot1.pdf>`__ were one of the first examples of few-shot learning. Rather than learning to classify images directly, these work using "twin"CNNs connected to a distance layer. The twins are fed different images, which belong to either the same or different class. This layer measures the L1 distance between the learned feature vectors, with a final sigmoidal function declaring whether or not the images are from the same class. This results in a combinatorial explosion of training data, especially when paired with image augmentation. Siamese networks are a task-invariant learning method.

ProtoNet
~~~~~~~~
ProtoNet, or prototypical networks, work similarly to siamese networks in that they both represent task-invariant learning methods, but differ in the way in which they compare sample embeddings. Rather than directly compare the L1 distances between embeddings of image pairs, they instead create "prototypical" vectors for each class, and compare the L2-squared distance between the training image and the prototypical vectors. This implementation is empirically more stable and computationally efficient than the Siamese network approach.

Evaluating performance
------------------------

Deployment
----------
One of my favorite tech blogs is Vicki Boikis' `normcore tech`_, and one of her recent posts inspired this workflow. First off, this was an excuse to work with the phenomenal `streamlit`_ library, which I found to be a much more efficient way of getting my product out the door. Second, to avoid having to do all of my work in an EC2 container rather than on my local machine, I adopted an infrastructure-as-code approach. This was surprisingly easy, as all I really needed to do was write a Dockerfile which installed my `requirements.txt` and open up Streamlit's port when running the container.
