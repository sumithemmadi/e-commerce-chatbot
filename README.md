# Real Time E-commerce Question and Answering System

Creating a virtual environment (venv) in Windows.

1. **Install Python 3**:
   Make sure you have Python 3 installed on your system. You can download it from the official [Python website](https://www.python.org/downloads/).

2. **Open Command Prompt**:
   Open the Command Prompt. You can do this by pressing `Win + R`, typing `cmd`, and pressing Enter.

3. **Navigate to Your Project Directory**:
   Use the `cd` command to navigate to the directory where you want to create your virtual environment. For example:

   ```sh
    cd C:\Users\sumith\projects\e-commerce-chatbot
   ```

4. **Create the Virtual Environment**:
   Use the following command to create a virtual environment:

   ```sh
   python -m venv venv
   ```

   Here, `venv` is the name of your virtual environment. You can choose any name you prefer.

5. **Activate the Virtual Environment**:
   To activate the virtual environment, run:

   ```sh
   .\venv\Scripts\activate
   ```

   After activation, your command prompt should show the name of the virtual environment at the beginning of the line, indicating that the environment is active.

### Installing Dependencies

- **Installing Packages**: After activating your virtual environment, you can install packages using `pip`. For example:
  ```sh
  pip install requests scikit-learn torch  nltk transformers flask beautifulsoup4
  ```
