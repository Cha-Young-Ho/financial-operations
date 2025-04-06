from setuptools import setup, find_packages

setup(
    name="aws-finops-tools",
    version="0.1.4",
    description="AWS 리소스 비용 최적화를 위한 도구",
    author="YoungHo Cha",
    packages=find_packages(),
    install_requires=[
        "aioboto3>=9.0.0",
        "boto3>=1.18.0", 
        "pandas>=1.3.0",
    ],
    python_requires=">=3.7",
    entry_points={
        "console_scripts": [
            "finops=aws_finops_tools.main:main_cli",  # 경로 변경
        ],
    },
)