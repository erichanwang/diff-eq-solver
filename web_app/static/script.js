document.addEventListener('DOMContentLoaded', () => {
    const degreeInput = document.getElementById('degree');
    const equationInputs = document.getElementById('equation-inputs');
    const initialConditions = document.getElementById('initial-conditions');
    const solverForm = document.getElementById('solver-form');
    const solutionText = document.getElementById('solution-text');
    const plainSolutionText = document.getElementById('plain-solution-text');
    const themeToggle = document.getElementById('theme-toggle');
    const body = document.body;

    // Theme handling
    const themeIcon = document.getElementById('theme-icon');
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme === 'light-mode') {
        body.classList.remove('dark-mode');
        themeIcon.src = '/static/sun-74.png';
        themeIcon.alt = 'Sun Icon';
    } else {
        body.classList.add('dark-mode');
        themeIcon.src = '/static/moon-42.png';
        themeIcon.alt = 'Moon Icon';
    }

    themeToggle.addEventListener('click', () => {
        body.classList.toggle('dark-mode');
        if (body.classList.contains('dark-mode')) {
            localStorage.removeItem('theme');
            themeIcon.src = '/static/moon-42.png';
            themeIcon.alt = 'Moon Icon';
        } else {
            localStorage.setItem('theme', 'light-mode');
            themeIcon.src = '/static/sun-74.png';
            themeIcon.alt = 'Sun Icon';
        }
    });

    function generateInputs() {
        let degree = parseInt(degreeInput.value);
        if (isNaN(degree) || degree < 1) {
            degree = 2;
            degreeInput.value = degree;
        }

        equationInputs.innerHTML = '';
        initialConditions.innerHTML = '';

        // Generate equation inputs
        let equationHTML = '';
        for (let i = degree; i >= 0; i--) {
            let term = 'y';
            if (i === 1) term = "y'";
            else if (i > 1) term = `y${"'".repeat(i)}`;

            equationHTML += `<span class="term">
                                <input type="text" name="coeff${i}" value="1" required> ${term}
                             </span>`;
            if (i > 0) equationHTML += ' + ';
        }
        equationInputs.innerHTML = `<div class="form-group"><label>Equation:</label>${equationHTML} = 0</div>`;

        // Generate initial condition inputs
        for (let i = 0; i < degree; i++) {
            let term = 'y(0)';
            if (i === 1) term = "y'(0)";
            else if (i > 1) term = `y${"'".repeat(i)}(0)`;

            initialConditions.innerHTML += `<div class="form-group ic-group">
                                                <span>${term} = </span>
                                                <input type="text" name="ic${i}" value="0" class="ic-input" required>
                                            </div>`;
        }
    }

    degreeInput.addEventListener('change', generateInputs);
    generateInputs();

    solverForm.addEventListener('submit', async (event) => {
        event.preventDefault();
        solutionText.textContent = "Solving...";
        plainSolutionText.textContent = "";

        const formData = new FormData(solverForm);
        const data = Object.fromEntries(formData.entries());

        try {
            const response = await fetch('/solve', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            });

            const result = await response.json();

            if (result.error) {
                solutionText.textContent = "Error: " + result.error;
                plainSolutionText.textContent = result.error;
            } else {
                solutionText.innerHTML = `\\( y(t) = ${result.latex} \\)`;
                plainSolutionText.textContent = `y(t) = ${result.plain}`;

                if (typeof MathJax !== 'undefined') {
                    MathJax.typesetPromise();
                }
            }
        } catch (err) {
            solutionText.textContent = "Error: Could not reach server.";
            console.error(err);
        }
    });
});
