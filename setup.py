from setuptools import setup, find_packages
# Setting up
setup(
    name="bytop",
    python_requires='>=3.8',
    version="1.1.3",
    author="LBY_L",
    license='GNU General Public License 3.0 (GPL 3.0)',
    description="BYTop a cli dash to show up RAM and CPU stats 🚀",
    entry_points={
        'console_scripts': 'bytop = bytop.__init__:__main__'
    },
    packages=find_packages(),
    install_requires=['psutil'],
    keywords=['cli', 'tui'],
    classifiers=[
        "Development Status :: IDK bro im just developing",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Linux",
    ]
)
# Hmm... i think that AnotherPing is 🏳️‍🌈
