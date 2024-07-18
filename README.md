# Jose Guzman's Capstone Project

## Setup Instructions

### Virtual Environment Setup

To ensure that your project dependencies are managed properly and to avoid conflicts with other projects, it is recommended to use a virtual environment. Below are the steps to create, activate, and install the required dependencies.

#### 1. Clone the Repository

First, clone the repository to your local machine:

```bash
git clone https://github.com/jg2012/Capstone_Project
cd your-repositor
```

#### 2. Create a Virtual Environment
Create a virtual environment in the project directory. You can use venv for this purpose.

For Windows:
```bash
python -m venv venv
```

For macOS and Linux:
```bash
python3 -m venv venv
```

#### 3. Activate the Virtual Environment
To activate the virtual environment, run the following command:
For Windows:
```bash
venv\Scripts\activate
```

For macOS and Linux:
```bash
source venv/bin/activate
```

#### 4. Install Dependencies
Once the virtual environment is activated, install the project dependencies using pip:
```bash
pip install -r requirements.txt
```

#### Deactivate the Virtual Environment
When you are done working in the virtual environment, you can deactivate it by simply running:
```bash
deactivate
```

#### Additional Information 
To add new packages to the project, use pip install package-name and then update the requirements.txt file with the new dependencies:
```bash
pip freeze > requirements.txt
```

