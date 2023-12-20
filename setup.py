from setuptools import setup, find_packages
# Setting up
setup(
    name="bytop",
    version="1.0",
    author="LBY_L",
    license='GNU General Public License',
    description="BYTop a cli dash to show up ram and cpu stats 🚀",
    long_description_content_type="cli/tui",
    long_description="",
    entry_points={
        'console_scripts': 'bytop = BYTop.bytop:main'
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