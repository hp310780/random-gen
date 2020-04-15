import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
     name='random-gen',
     version='1.0.0',
     author="hp310780",
     description="Module to generate random numbers along a probability distribution",
     long_description=long_description,
     long_description_content_type='text/markdown',
     url="https://github.com/hp310780/random-gen",
     py_modules=['random_gen'],
     license='MIT License',
     classifiers=[
         "Programming Language :: Python :: 3"
     ],

 )