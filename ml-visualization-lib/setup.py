from setuptools import setup, find_packages

setup(
    name='ml-visualization-lib',
    version='0.1.0',
    author='Your Name',
    author_email='your.email@example.com',
    description='A library for visualizing machine learning data and cost functions.',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'numpy',
        'matplotlib',
        'ipywidgets',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)