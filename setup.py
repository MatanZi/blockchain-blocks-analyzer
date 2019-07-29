import setuptools


setuptools.setup(
    name='blockchain_block_analyzer',
    version='1.0',
    author='MatufA, MatanZi, Saimon9852',
    packages=setuptools.find_packages(),
    url='https://github.com/MatufA/blockchain-blocks-analyzer',
    description='a blocks analyzer.',
    long_description=open('README.md').read(),
    install_requires=open('requirements.txt').readlines(),
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'btc-analyzer=blockchain_blocks_analyzer.__main__:btc_analyzer_cli'
        ],
    }
)
