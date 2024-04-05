from setuptools import setup, find_packages

setup(
    name='Telethon-channel-alerter',
    version='0.1',
    author='Arbab',
    packages=find_packages(),  # Automatically find and include all packages
    install_requires=[  # List of dependencies
        'twilio',  # Example dependency
        'loguru',
        'telethon'
    ],
    classifiers=[  # Classifiers help categorize the package
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',  # Minimum version requirement of the package
)