Installation
============

Prerequisites
-------------

Before installing Londontube, ensure you have Python 3.6 or later installed.

Computer Type
-------------

Different install process for macOS and Windows.

If you are using Windows:

Installing from Source
----------------------

To install from source, clone the repository and install using pip:

.. code-block:: bash

    git clone <SSH>
    # where <SSH> can be find in the GitHub repository: https://github.com/UCL-COMP0233-23-24/londontube-Working-Group-07
    cd londontube
    pip install .

If you are using Macbook:

Installing on macOS
-------------------

1. **Install Python**: Make sure you have Python installed. You can download it from `the official Python website <https://www.python.org/downloads/macos/>`_.

2. **Install Londontube**: Open the Terminal and run the following command:

.. code-block:: bash

    cd repository
    pip install .

   This will download and install Londontube and its dependencies.

3. **Verify Installation**: To verify that Londontube has been installed correctly, run:

   .. code-block:: bash

       python -c "import londontube; print(londontube.__version__)"

   This should print the version number of Londontube.


Installing on Windows
---------------------

1. **Install Python**: Download and install Python from the `official Python website <https://www.python.org/downloads/windows/>`_. During installation, ensure that you check the option to 'Add Python to PATH'.

2. **Install Londontube**: Open Command Prompt and run the following command:

.. code-block:: bash

    cd repository
    pip install .


   This will download and install Londontube and its dependencies.

3. **Verify Installation**: To check if Londontube was installed successfully, run:

   .. code-block:: bash

       python -c



