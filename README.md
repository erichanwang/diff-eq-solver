# Differential Equation Solver

This project provides two user interfaces for solving homogeneous linear ordinary differential equations with constant coefficients: a web application and a Pygame application. The backend for both applications uses the `sympy` library to perform the symbolic calculations.

## Features

-   Solve homogeneous linear ODEs of up to the 4th degree.
-   Provide initial conditions to find the particular solution.
-   Two interfaces:
    -   A web-based UI built with Flask, HTML, CSS, and JavaScript.
    -   A desktop UI built with Pygame.

## Prerequisites

-   Python 3.x
-   pip

## Installation

1.  Clone the repository:
    ```bash
    git clone <repository-url>
    cd diff-eq-solver
    ```

2.  Install the required Python packages:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

### Web Application

To run the web-based solver, execute the following command from the project's root directory:

```bash
python web_app/app.py
```

Then, open your web browser and navigate to `http://127.0.0.1:5000`.

### Pygame Application

To run the desktop solver, execute the following command from the project's root directory:

```bash
python pygame_app/main.py
```

This will open a window with the graphical user interface.
