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

## How to run the Labs

In order to be able to run the labs properly you might need some dependencies installed. So you will need to create a venv and install the requirements.

> [!IMPORTANT]
> The following steps require a local and executeable python installation.

```PowerShell
python -m venv .venv
```

Activate the virtual environment.

- Windows:

    ```PowerShell
    .\.venv\Scripts\activate
    ```

- Linux:

    ```bash
    source ./.venv/bin/activate
    ```

Now install the dependecies.

```PowerShell
pip install -r requirements.txt
```
