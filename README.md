# Dash Image Processing App


[![GitHub license](https://img.shields.io/github/license/plotly/dash-image-processing.svg)](https://github.com/plotly/dash-image-processing/blob/master/LICENSE.md)
[![GitHub issues](https://img.shields.io/github/issues/plotly/dash-image-processing.svg)](https://github.com/plotly/dash-image-processing/issues)
[![GitHub forks](https://img.shields.io/github/forks/plotly/dash-image-processing.svg)](https://github.com/plotly/dash-image-processing/network)
[![GitHub stars](https://img.shields.io/github/stars/plotly/dash-image-processing.svg)](https://github.com/plotly/dash-image-processing/stargazers)

This is a demo of the Dash interactive Python framework developed by [Plotly](https://plot.ly/).

Dash abstracts away all of the technologies and protocols required to build an interactive web-based application and is a simple and effective way to bind a user interface around your Python code. To learn more check out our [documentation](https://plot.ly/dash).

Try out the [demo app here](https://dash-image-processing.plot.ly/).

![animated1](images/animated1.gif)


## Getting Started
### Using the demo
This demo lets you interactive explore Support Vector Machine (SVM). 

It includes a few artificially generated datasets that you can choose from the dropdown, and that you can modify by changing the sample size and the noise level of those datasets.

The other dropdowns and sliders lets you change the parameters of your classifier, such that it could increase or decrease its accuracy.

### Running the app locally

First create a virtual environment with conda or venv inside a temp folder, then activate it.

```
virtualenv dash-image-processing-venv

# Windows
dash-image-processing-venv\Scripts\activate
# Or Linux
source venv/bin/activate
```

Clone the git repo, then install the requirements with pip
```
git clone https://github.com/plotly/dash-image-processing.git
cd dash-image-processing
pip install -r requirements.txt
```

Run the app
```
python app.py
```

## About the app
This app wraps Pillow, a powerful image processing library in Python, and abstracts all the operations through an easy-to-use GUI. All the computation is done on the back-end through Dash, and image transfer is optimized through session-based Redis caching and S3 storage.

### Motivation
Recently, while we were experimenting with ImageJ, an image processing app in Java, we wondered if it was possible to bring two changes: port the app into a browser interface, and shift the computation to the backend (so that extremely large images can also be processed).

This is how we thought about making a Dash app that would wrap Pillow, the modern version of the Python Imaging Library. This was the natural thing to do because Dash itself is already based on Flask, and Plotly already has the graph objects for manipulating images. Adding S3 storage to keep the uploaded file and caching the operations with Redis were absolutely painless because of the easy integration with Python.

## Built With
* [Dash](https://dash.plot.ly/) - Main server and interactive components
* [Plotly Python](https://plot.ly/python/) - Used to create the interactive plots
* [Pillow](http://scikit-learn.org/stable/documentation.html) - Apply operations to images
* [Boto S3](http://boto.cloudhackers.com/en/latest/ref/s3.html) - Store User inputted images
* [Redis](https://redis.io/documentation) - Cache the user input

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests to us. 
Although only a subset of Pillow is currently present, you are welcome to add any type of plugins, e.g. ML-based image processing. Just visit the project repo and make a PR with your addition: https://github.com/plotly/dash-image-processing

## Authors

* **Xing Han Lu** - *Initial Work* - [@xhlulu](https://github.com/xhlulu)
* **Chris** - *Code Review* - [@chriddyp](https://github.com/chriddyp)

See also the list of [contributors](https://github.com/plotly/dash-svm/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments


## Screenshots
![screenshot1](images/screenshot1.png)

![screenshot2](images/screenshot2.png)
