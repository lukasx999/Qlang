from setuptools import setup, find_packages

setup(
    name='qlang',
    version='0.0.1',
    description='a primitive programming lanuage',
    author='lukasx999',
    url='https://github.com/lukasx999/Qlang',
    # install_requires=[],
    # install_requires=REQUIREMENTS,
    packages=find_packages(
        where="src",  # "." by default
        include=["*"],  # * by default
    ),
    package_dir={"": "src"},
    entry_points={
        'console_scripts': [
            "qlang = qlang.main:main",
        ],
    },
)
