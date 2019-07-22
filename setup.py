from setuptools import setup, find_packages


setup(
    name='rn2483',
    version="0.1",
    license='Apache License, Version 2.0',
    description='rn2483 library',
    author='Alexandros Antoniades',
    author_email='alex.rogue.antoniades@gmail.com',
    url='https://github.com/alexantoniades/python-rn2483',
    packages=find_packages(),
    install_requires=['pyserial'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools', 
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ]
)
