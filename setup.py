from setuptools import setup

setup(
    # Needed to silence warnings (and to be a worthwhile package)
    name='Conversion',
    url='https://github.com/Bribak/conversion',
    author='Daniel Bojar',
    author_email='daniel@bojar.net',
    # Needed to actually package something
    packages=['conversion'],
    # Needed for dependencies
    install_requires=['janitor','scikit-learn','pandas','numpy',
                      'scikit-learn','plotly'],
    # *strongly* suggested for sharing
    version='0.1',
    # The license can be anything you like
    license='CC0',
    description='Analyzing cocktail recipes',
    long_description=open('README.md').read(),
)
