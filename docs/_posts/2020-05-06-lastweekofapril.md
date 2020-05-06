---
title: "Last week of april. Working on exercise 6"
excerpt: "Finishong exercise 6 and looking into Github pages"


sidebar:
  nav: "docs"

classes: wide

categories:
- Main project. Second iteration

tags:


author: Ana Cuevas
pinned: false


---

# Week objectives

- Look into Github Pages
- Advance with textures in Ex5
- Continue translating Ex4
- Continue Ex6

# Advances

- Looked into jekyll and installing linux in a spare computer since it's easier to work on ubuntu as most of the documentation about jekyll is based on Ubuntu.

- Textures Exercise 5:
    - The filters used in the original excersise in matlab don't exist in OpenCV. Lookin at the code to see if it can be replicated in Python.
    - Found option for the Standard Deviation filter in [StackOverflow](https://stackoverflow.com/questions/7331105/stdfilt-in-opencv/40027378#40027378).
    - Implementing the filter in stdfilter.py. Here a comparison of the results in matlab and python.
    - Searching for information on the Entropy filter.
    - In matlab some of the code can't be seen.
    Found a way to calculate entropy of a one-dimensional array in python.
    - Trying to implement in entropyfilt.py, this consist og adding the padding to the image, calculating the entropy of 9X9 sized chunks of the image and building an answer from that.
    - Managed to get an image similar to the Matlab answer, trying to see where the mistakes are.

- Continue Exercise 6:
    - Use of morphological elements to get the edges of the seven chips
    - Finished copying the original text of the exercise
    - Finshed separating rectangles from squares using the information from the segmented image.
    - Exercise 6 complete without translation.
