# flask-db-app
This is a web application deploying poetry generation from images. 

The model is from [here](https://github.com/researchmm/img2poem) . This model is a deep neural network that learns how to generate poems from images. You can just input your image to this web app,and it will show you the poem it generated. Also, It use database to save last three records for all users.

I used flask+SQLite to build this web , and to simplify database operations, we use a third party extension named "Flask-SQLAlchemy".

Because this neural network model is too huge, I can't deploy it in server end, so here is just a demo on my local computer.

![Demo](gif_demo.gif)

you can also check the whole vedio in this files.


Thanks for the turtorial about flask [here](https://read.helloflask.com/)

