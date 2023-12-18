from setuptools import setup

setup(
    name='londontube',
    version='1.0.0',
    description='A tool for navigating the London Tube network.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Your Name',
    author_email='your.email@example.com',
    url='https://github.com/yourusername/londontube',
    packages=['londontube'],
    install_requires=[
        # List your package dependencies here
        'requests',
        'matplotlib',
        'pytest',
        'numpy',
        'timeit',
        'pandas',
        'urllib'
        # etc.
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        # etc.
    ],
    entry_points={
        'console_scripts': [
            'journey-planner=londontube.journey_planner:main'
        ]
    }

)
