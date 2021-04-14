from setuptools import setup, find_packages


setup(
    name='xmlinjector',
    version='0.1',
    author='Darren Smith',
    author_email='darren.smith@sparkpost.com',
    packages=find_packages(),
    url='https://github.com/darrensmith223/XML_Injector',
    license='Apache 2.0',
    description='Configure Intermediary DKIM Domain with SparkPost',
    install_requires=['requests>=2.20.1']
)