from setuptools import setup


def readme():
    with open('README.md') as f:
        return f.read()


setup(
    name='diffenv',
    version='0.1.1',
    author='Stan James, Gabriel Pickard',
    author_email='wanderingstan@gmail.com, wergomat@gmail.com',
    url='http://github.com/error-central/diffenv',
    description='Compare development environments',
    long_description=readme(),
    long_description_content_type='text/markdown',
    scripts=['bin/diffenv', 'bin/diffenv-nopaging'],
    license='MIT',
    packages=['diffenv'],
    install_requires=[
        'colorama',
        'requests',
        'ruamel.yaml'
    ],
    zip_safe=False,

)
