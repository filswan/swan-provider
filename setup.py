import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
     name='filswan_miner',
     version='0.2',
     author="nbfs",
     author_email="account@nbai.io",
     description="Swan Miner tool",
     long_description=long_description,
     long_description_content_type="text/markdown",
     url="https://github.com/nebulaai/swan-miner",
     packages=setuptools.find_packages(),
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
 )