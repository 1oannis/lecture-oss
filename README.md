# Open-Source Software Labs
>
> [!NOTE]
> Copyright 2024 - present [Ioannis Theodosiadis](mailto:ioannis@seoultech.ac.kr), SEOULTECH University
>
> This program is free software: you can redistribute it and/or modify
> it under the terms of the GNU General Public License as published by
> the Free Software Foundation, either version 3 of the License, or
> at your option any later version
>
> This program is distributed in the hope that it will be useful
> but WITHOUT ANY WARRANTY; without even the implied warranty of
> MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
> GNU General Public License for more details
>
> You should have received a copy of the GNU General Public License
> along with this program. If not, see <https://www.gnu.org/licenses/>

This repository holds the mandatory labs of the course Open-Source Software at SeoulTech University.

---

- [Lab-1](./lab-1/README.md) - Python Lab #1: Korean COVID-19 New Cases by Region
- [Lab-2](./lab-2/README.md) - Python Lab #2: Midterm and Final Exam Analysis
- [Lab-3](./lab-3/README.md) - Python Lab #3: Turtle Runaway
- [Lab-4](./lab-4/README.md) - Math Lab #1: Midterm and Final Exam Visualization
- [Lab-5](./lab-5/README.md) - Math Lab #2: Final Exam Score Prediction
- [Lab-6](./lab-6/README.md) - Math Lab #3: Multivariate Nonlinear Optimization
- [Lab-7](./lab-7/README.md) - ML Lab #1: Breast Cancer Classification
- [Lab-8](./lab-8/README.md) - ML Lab #2: Breast Cancer Classification with Cross-validation
- [Lab-9](./lab-9/README.md) - DL Lab #1: Object Detection using YOLO

## How to run the Labs

In order to be able to run the labs properly you might need some dependencies installed. So you will need to create a venv and install the requirements.

> [!IMPORTANT]
> The following steps require a local and executeable python installation.

1. First create a python virtual environment in the root directory:

    ```PowerShell
    python -m venv .venv
    ```

1. Activate the venv:

    - Windows:

        ```PowerShell
        .\venv\Script\activate
        ```

    - Mac / Linux:

        ```bash
        source myenv/bin/activate
        ```

1. Upgrade pip if necessary:

    ```PowerShell
    python -m pip install --upgrade pip
    ```

1. Install the required dependencies:

    ```PowerShell
    pip install -r requirements.txt
    ```

1. For lab-9 also install the pytorch dependenies:

    ```PowerShell
    pip install -r requirements_torch.txt
    ```
