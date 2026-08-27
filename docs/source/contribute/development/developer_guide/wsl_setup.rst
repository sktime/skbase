.. _wsl_setup:

=========
WSL Setup
=========

If you are a Windows user and prefer developing in a Linux environment,
you can use the Windows Subsystem for Linux (WSL). This guide will help
you set up ``skbase`` for development in Ubuntu WSL.

Prerequisites
-------------

1.  **Install WSL**: Ensure you have WSL and the Ubuntu distribution
    installed on your Windows machine. If not, you can install it by
    running the following command in PowerShell as administrator:

    .. code-block:: powershell

        wsl --install

2.  **Clone the Repository**: Clone the ``skbase`` repository to your
    Windows filesystem (e.g., ``C:\code\skbase``). WSL can access your
    Windows files via ``/mnt/c/``.

    Alternatively, you can clone it directly inside the WSL filesystem
    for better performance:

    .. code-block:: bash

        git clone https://github.com/sktime/skbase.git
        cd skbase

Automated Setup
---------------

We provide a script to automate the setup of your development
environment in Ubuntu WSL.

1.  Open your Ubuntu terminal.
2.  Navigate to the root directory of the cloned ``skbase`` repository.
3.  Run the setup script:

    .. code-block:: bash

        bash scripts/setup_wsl.sh

This script will:

- Update your package lists.
- Install ``python3-venv`` and ``python3-pip``.
- Create a virtual environment named ``.venv_wsl``.
- Install ``skbase`` in editable mode with development
  and test dependencies.

Manual Activation
-----------------

After the setup is complete, you can activate the environment whenever
you open a new terminal:

.. code-block:: bash

    source .venv_wsl/bin/activate

Verifying the Installation
--------------------------

To verify that everything is set up correctly, you can run the tests:

.. code-block:: bash

    pytest
