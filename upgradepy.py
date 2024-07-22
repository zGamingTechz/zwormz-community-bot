import os

# Run shell commands to upgrade Python using apt
os.system("apt update")
os.system("apt upgrade python3")

# Check the new Python version after the upgrade
os.system("python3 --version")