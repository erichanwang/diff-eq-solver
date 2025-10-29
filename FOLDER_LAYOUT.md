# Folder Layout

This document describes the folder layout of the differential equation solver project.

- **`solver.py`**: This is the core of the project. It contains the logic for solving differential equations.

- **`problem.py`**: This file defines the differential equation problems that can be solved by `solver.py`.

- **`web_app/`**: This directory contains a Flask web application that provides a user interface for the differential equation solver.
    - **`app.py`**: The main Flask application file.
    - **`static/`**: Contains static assets like CSS, JavaScript, and images.
    - **`templates/`**: Contains the HTML templates for the web application.

- **`pygame_app/`**: This directory contains a Pygame application, likely for demonstrating or visualizing the solver.
    - **`main.py`**: The main file for the Pygame application.

- **`render.yaml`**: Configuration file for deploying the web application to Render.

- **`README.md`**: The main README file for the project.

- **`examples.txt`**: Contains examples of how to use the solver.
