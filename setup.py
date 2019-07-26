from setuptools import setup


def readme():
    with open('README.md') as f:
        return f.read()
setup(
  name='diffenv',
  version='0.1',
  url='http://github.com/error-central/diffenv',
  description='Compare development environments',
  long_description=readme(),
  scripts=['bin/diffenv'],
  license='MIT',
  packages=['diffenv'],
  install_requires=[
    'colorama',
  ],
  zip_safe=False,
  
)
