from distutils.core import setup
import setuptools

setup(
    name='instapy',
    version='1.0',
    author='Tellef',
    author_email='tellefos@uio.no',
    packages=setuptools.find_packages(),
    scripts=['bin/instapy']
)
