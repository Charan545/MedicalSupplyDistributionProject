function generateFields() {
    const numHospitals = parseInt(document.getElementById("num_hospitals").value);
    const numCenters = parseInt(document.getElementById("num_centers").value);

    const container = document.getElementById("dynamicFields");
    container.innerHTML = ""; // Clear previous

    // Supply Inputs
    const supplyHeader = document.createElement("h3");
    supplyHeader.innerText = "Supply from Centers";
    container.appendChild(supplyHeader);

    for (let i = 0; i < numCenters; i++) {
        const input = document.createElement("input");
        input.type = "number";
        input.name = "supply";
        input.placeholder = `Center ${i + 1} Supply`;
        input.required = true;
        container.appendChild(input);
    }

    // Demand Inputs
    const demandHeader = document.createElement("h3");
    demandHeader.innerText = "Demand at Hospitals";
    container.appendChild(demandHeader);

    for (let i = 0; i < numHospitals; i++) {
        const input = document.createElement("input");
        input.type = "number";
        input.name = "demand";
        input.placeholder = `Hospital ${i + 1} Demand`;
        input.required = true;
        container.appendChild(input);
    }

    // Cost Matrix
    const costHeader = document.createElement("h3");
    costHeader.innerText = "Cost Matrix";
    container.appendChild(costHeader);

    for (let i = 0; i < numCenters; i++) {
        for (let j = 0; j < numHospitals; j++) {
            const input = document.createElement("input");
            input.type = "number";
            input.name = "cost";
            input.placeholder = `Cost C${i + 1} to H${j + 1}`;
            input.required = true;
            container.appendChild(input);
        }
        container.appendChild(document.createElement("br"));
    }

    // Show submit button
    document.getElementById("submitBtn").style.display = "block";
}

document.getElementById("optimizationForm").addEventListener("submit", function (e) {
    e.preventDefault();

    const supply = Array.from(document.querySelectorAll("input[name='supply']")).map(i => parseInt(i.value));
    const demand = Array.from(document.querySelectorAll("input[name='demand']")).map(i => parseInt(i.value));
    const costInputs = Array.from(document.querySelectorAll("input[name='cost']")).map(i => parseInt(i.value));

    const numCenters = supply.length;
    const numHospitals = demand.length;
    const cost_matrix = [];

    for (let i = 0; i < numCenters; i++) {
        const row = [];
        for (let j = 0; j < numHospitals; j++) {
            row.push(costInputs[i * numHospitals + j]);
        }
        cost_matrix.push(row);
    }

    fetch("/optimize/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]").value
        },
        body: JSON.stringify({
            supply,
            demand,
            cost_matrix
        })
    })
    .then(res => res.json())
    .then(data => {
        const outputDiv = document.getElementById("optimizationResults");
        if (data.success) {
            const table = data.distribution.map(row => `<tr>${row.map(v => `<td>${v}</td>`).join('')}</tr>`).join('');
            outputDiv.innerHTML = `
                <h2>Optimized Distribution Matrix</h2>
                <table border="1"><tbody>${table}</tbody></table>
            `;
        } else {
            outputDiv.innerHTML = `<div class="alert alert-danger">${data.error}</div>`;
        }
    });
});
