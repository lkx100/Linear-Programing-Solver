function validateDimension(input) {
    if (input.value <= 0) {
        alert("Dimension must be greater than 0");
        input.value = 1;
    }
}

function validateNumber(input) {
    if (input.value < 0) {
        alert("Values cannot be negative");
        input.value = "";
    }
}

function createMatrix() {
    const rows = parseInt(document.getElementById('rows').value);
    const cols = parseInt(document.getElementById('cols').value);
    
    // Create cost matrix
    let matrixHtml = '<table>';
    for(let i = 0; i < rows; i++) {
        matrixHtml += '<tr>';
        for(let j = 0; j < cols; j++) {
            matrixHtml += `<td><input type="number" step="0.01" name="cost_${i}_${j}" required onchange="validateNumber(this)"></td>`;
        }
        matrixHtml += '</tr>';
    }
    matrixHtml += '</table>';
    document.getElementById('cost-matrix').innerHTML = matrixHtml;
    
    // Create supply vector
    let supplyHtml = '<table><tr>';
    for(let i = 0; i < rows; i++) {
        supplyHtml += `<td><input type="number" step="0.01" min="0" name="supply_${i}" required onchange="validateNumber(this)"></td>`;
    }
    supplyHtml += '</tr></table>';
    document.getElementById('supply-vector').innerHTML = supplyHtml;
    
    // Create demand vector
    let demandHtml = '<table><tr>';
    for(let i = 0; i < cols; i++) {
        demandHtml += `<td><input type="number" step="0.01" min="0" name="demand_${i}" required onchange="validateNumber(this)"></td>`;
    }
    demandHtml += '</tr></table>';
    document.getElementById('demand-vector').innerHTML = demandHtml;

    // Add hidden inputs for dimensions
    const dimensionsHtml = `
        <input type="hidden" name="matrix_rows" value="${rows}">
        <input type="hidden" name="matrix_cols" value="${cols}">
    `;
    document.getElementById('matrix-container').insertAdjacentHTML('beforeend', dimensionsHtml);

    // Adjust container size
    adjustContainerSize();
}

// Adjust container size based on content
function adjustContainerSize() {
    const container = document.querySelector('.container');
    container.style.height = 'auto'; // Reset height
    const newHeight = container.scrollHeight;
    container.style.height = `${newHeight}px`;
}

// Create initial matrix on page load
createMatrix();

// Handle form submission with AJAX
document.getElementById('transportForm').addEventListener('submit', function(e) {
    e.preventDefault();
    
    const formData = new FormData(this);
    
    fetch('', {
        method: 'POST',
        body: formData,
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
    .then(response => response.json())
    .then(data => {
        const resultContainer = document.getElementById('result-container');
        
        if (data.error) {
            resultContainer.innerHTML = `
                <div class="error-message">${data.error}</div>
            `;
        } else {
            resultContainer.innerHTML = `
                <br><hr><br>
                <h3>Total Cost: ${data.total_cost}</h3>
                <p>Status: ${data.status}</p>
            `;
        }
    })
    .catch(error => {
        console.error('Error:', error);
        document.getElementById('result-container').innerHTML = `
            <div class="error-message">An error occurred while processing your request.</div>
        `;
    });
});