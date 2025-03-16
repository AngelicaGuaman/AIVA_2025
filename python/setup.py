from setuptools import setup, find_packages

setup(
    name="patrolscan",
    version="0.1.0a1",
    package_dir={"": "src"},
    packages=find_packages(where="src"), 
    description="PatrolScan Python Library",
    author="Angélica Guaman y Lorenzo Costábile",
    install_requires=[
        'numpy',
        'pillow'
    ],
    extras_require={
        'dev': [
            'pytest',
        ],
    },
    python_requires='>=3.12', 
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.12',
    ],
) 