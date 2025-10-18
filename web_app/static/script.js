document.addEventListener('DOMContentLoaded', () => {
    const degreeInput = document.getElementById('degree');
    const equationInputs = document.getElementById('equation-inputs');
    const initialConditions = document.getElementById('initial-conditions');
    const solverForm = document.getElementById('solver-form');
    const solutionText = document.getElementById('solution-text');
    const plainSolutionText = document.getElementById('plain-solution-text');
    const themeToggle = document.getElementById('theme-toggle');
    const body = document.body;
    const isNonhomogeneous = window.location.pathname === '/nonhomogeneous';

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

        const varDep = document.getElementById('var_dep').value || 'y';
        const varIndep = document.getElementById('var_indep').value || 't';

        equationInputs.innerHTML = '';
        initialConditions.innerHTML = '';

        // Generate equation inputs
        let equationHTML = '';
        for (let i = degree; i >= 0; i--) {
            let term = varDep;
            if (i === 1) term = `${varDep}'`;
            else if (i > 1) term = `${varDep}${"'".repeat(i)}`;

            equationHTML += `<span class="term">
                                <input type="text" name="coeff${i}" value="1" required> ${term}
                             </span>`;
            if (i > 0) equationHTML += ' + ';
        }
        const rhsPart = isNonhomogeneous ? ` = <input type="text" id="rhs" name="rhs" placeholder="f(${varIndep})" required>` : ' = 0';
        equationInputs.innerHTML = `<div class="form-group"><label>Equation:</label>${equationHTML}${rhsPart}</div>`;

        // Generate initial condition inputs
        for (let i = 0; i < degree; i++) {
            let term = `${varDep}(0)`;
            if (i === 1) term = `${varDep}'(0)`;
            else if (i > 1) term = `${varDep}${"'".repeat(i)}(0)`;

            initialConditions.innerHTML += `<div class="form-group ic-group">
                                                <span>${term} = </span>
                                                <input type="text" name="ic${i}" value="0" class="ic-input" required>
                                            </div>`;
        }
    }

    degreeInput.addEventListener('change', generateInputs);
    document.getElementById('var_dep').addEventListener('input', generateInputs);
    document.getElementById('var_indep').addEventListener('input', generateInputs);
    generateInputs();

    solverForm.addEventListener('submit', async (event) => {
        event.preventDefault();
        let dots = 0;
        const maxDots = 3;
        const startTime = Date.now();

        const interval = setInterval(() => {
            dots = (dots + 1) % (maxDots + 1);
            const dotString = '.'.repeat(dots);
            solutionText.textContent = `Solving${dotString}`;
        }, 500);

        plainSolutionText.textContent = "";

        const formData = new FormData(solverForm);
        const data = Object.fromEntries(formData.entries());

        const endpoint = isNonhomogeneous ? '/solve_nonhomogeneous' : '/solve';

        try {
            const response = await fetch(endpoint, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            });

            clearInterval(interval);

            const result = await response.json();

            if (result.error) {
                solutionText.textContent = "Error: " + result.error;
                plainSolutionText.textContent = result.error;
            } else {
                const displayStartTime = Date.now();
                const varDep = document.getElementById('var_dep').value || 'y';
                const varIndep = document.getElementById('var_indep').value || 't';
                solutionText.innerHTML = `\\( ${varDep}(${varIndep}) = ${result.latex} \\)`;
                plainSolutionText.textContent = `${varDep}(${varIndep}) = ${result.plain}`;

                if (typeof MathJax !== 'undefined') {
                    await MathJax.typesetPromise();
                }

                const displayElapsedTime = ((Date.now() - displayStartTime) / 1000).toFixed(2);

                // Display display time
                const timeElement = document.createElement('p');
                timeElement.textContent = `Displayed in ${displayElapsedTime} seconds`;
                timeElement.style.fontSize = '0.9rem';
                timeElement.style.color = '#7f8c8d';
                solutionText.parentElement.appendChild(timeElement);

                // Clear the time after a short delay
                setTimeout(() => {
                    if (timeElement.parentElement) {
                        timeElement.parentElement.removeChild(timeElement);
                    }
                }, 3000);
            }
        } catch (err) {
            clearInterval(interval);
            solutionText.textContent = "Error: Could not reach server.";
            console.error(err);
        }
    });
});
