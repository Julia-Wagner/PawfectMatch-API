# **Testing**

[Go back to the README](README.md)

## **Table of Contents**

<!-- TOC -->
* [**Testing**](#testing)
  * [**Table of Contents**](#table-of-contents)
  * [**Manual Testing**](#manual-testing)
  * [**Automated Testing**](#automated-testing)
<!-- TOC -->

## **Manual Testing**

I tested each app manually while creating the views in the DRF API interface.

## **Automated Testing**

I created and performed automated unit tests for each app. I structured my tests according to my views and tested each HTTP request and the applicable permissions. 

I installed *coverage* to check the testing coverage for my code. Using the *.html* report, I managed to find untested parts and add tests for these.

My total coverage for my unit tests is **98%**, with **100%** for all custom apps except for two. The medias serializer can not be fully tested automatically as it checks the uploaded size and file type for the image or video. And the posts view filter to check if a post has linked dogs was not tested automatically. I made sure to test these two apps again manually.

![test coverage](docs/screenshots/coverage.jpg)
*Unit test coverage*
