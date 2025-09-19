document.addEventListener('DOMContentLoaded', () => {
    const degreeInput = document.getElementById('degree');
    const equationInputs = document.getElementById('equation-inputs');
    const initialConditions = document.getElementById('initial-conditions');
    const solverForm = document.getElementById('solver-form');
    const solutionText = document.getElementById('solution-text');

    function generateInputs() {
        const degree = parseInt(degreeInput.value);
        equationInputs.innerHTML = '';
        initialConditions.innerHTML = '';

        let equationHTML = '';
        for (let i = degree; i >= 0; i--) {
            let term = `y${"'".repeat(i)}`;
            if (i === 0) term = 'y';
            if (i === 1) term = "y'";

            equationHTML += `<input type="number" name="coeff${i}" required> ${term}`;
            if (i > 0) {
                equationHTML += ' + ';
            }
        }
        equationInputs.innerHTML = `<div class="form-group"><label>Equation:</label>${equationHTML} = 0</div>`;

        for (let i = 0; i < degree; i++) {
            let term = `y${"'".repeat(i)}(0)`;
            if (i === 0) term = 'y(0)';
            if (i === 1) term = "y'(0)";
            initialConditions.innerHTML += `<div class="form-group"><label>${term}:</label><input type="number" name="ic${i}" required></div>`;
        }
    }

    degreeInput.addEventListener('change', generateInputs);
    generateInputs();

    solverForm.addEventListener('submit', async (event) => {
        event.preventDefault();
        const formData = new FormData(solverForm);
        const data = Object.fromEntries(formData.entries());

        const response = await fetch('/solve', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });

        const result = await response.json();
        solutionText.textContent = `y(x) = ${result.solution}`;
    });
});
