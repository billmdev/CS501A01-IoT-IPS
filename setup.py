from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='IPS',
    packages=['IPS'],
    version='',
    description='A little tshark wrapper to count the number of cellphones in a particular limited area.',
    author='ghostbill',
    url='https://github.com/ghostbill/CS501A01-IoT-IPS',
    author_email='billmorrissonjr@gmail.com',
    keywords=['tshark', 'wifi', 'location'],
    install_requires=[
        "click",
        "netifaces",
        "pick",
    ],
    setup_requires=[],
    tests_require=[],
    entry_points={'console_scripts': [
        'IPS = IPS.__main__:main',
    ], },
)