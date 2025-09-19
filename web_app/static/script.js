document.addEventListener('DOMContentLoaded', () => {
    const degreeInput = document.getElementById('degree');
    const equationInputs = document.getElementById('equation-inputs');
    const initialConditions = document.getElementById('initial-conditions');
    const solverForm = document.getElementById('solver-form');
    const solutionText = document.getElementById('solution-text');
    const plainSolutionText = document.getElementById('plain-solution-text');

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
                                <input type="number" step="any" name="coeff${i}" value="1" required> ${term}
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
                                                <input type="number" step="any" name="ic${i}" value="0" class="ic-input" required>
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
                solutionText.innerHTML = `\\( y(x) = ${result.latex} \\)`;
                plainSolutionText.textContent = `y(x) = ${result.plain}`;

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
