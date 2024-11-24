document.addEventListener('DOMContentLoaded', () => {
 
    function showMessage() {
        const contentContainer = document.getElementById('content-container');
        if (!contentContainer) {
            console.error("Content container not found!");
            return;
        }
        fetch('/add-completed-training/', {
            method: 'GET',
            headers: {
                'X-Requested-With': 'XMLHttpRequest' 
            }
        })
        .then(response => response.json())
        .then(data => {
            // Extract relevant data from the response
            const lastEmployeeData = data.last_employee;
            const lastTrainingModuleData = data.last_training_module;
            const lastDateCompleted = data.last_date_completed;

            // Check if we have the required data
            if (lastEmployeeData && lastTrainingModuleData && lastDateCompleted) {
                // Create the new content (alert message)
                const newContent = document.createElement('div');
                newContent.classList.add('new-item');
                
                newContent.innerHTML = `
                    <strong>Last Input:</strong><br>
                    <p>Employee: <strong>${lastEmployeeData.name}</strong> (Staff Number: ${lastEmployeeData.staff_number})</p>
                    <p>Training Module: <strong>${lastTrainingModuleData.name}</strong></p>
                    <p>Date Completed: <strong>${lastDateCompleted}</strong></p>
                    <button class="close-btn" onclick="this.parentElement.remove()">×</button>  <!-- Close button -->
                `;
                
                contentContainer.appendChild(newContent);

                contentContainer.classList.add('show');
            } else {
                console.log("Missing or invalid data.");
            }
        })
        .catch(error => {
            console.error("Error fetching data:", error);
        });
    }

    showMessage();
    const employeeIdElement = document.getElementById('employee-id');
    const employeeId = employeeIdElement ? employeeIdElement.getAttribute('data-employee-id') : null;
    console.log('Employee ID:', employeeId);

    // Function to update training progress
    function updateTrainingProgress(employeeId) {
        if (!employeeId) {
            console.error("Employee ID is not available.");
            return;
        }

        fetch(`/employee/${employeeId}/trainings/`)
            .then(response => response.json())
            .then(data => {
                const progressBar = document.querySelector('.progress-bar');
                const progressPercentage = data.progress_percentage;
                console.log("Training Progress:", progressPercentage);

                // Update progress bar width
                progressBar.style.width = progressPercentage + '%';
                progressBar.textContent = progressPercentage.toFixed(2) + '%';

                // Change color based on progress percentage
                if (progressPercentage >= 80) {
                    progressBar.style.backgroundColor = '#68fe04';
                } else if (progressPercentage >= 50) {
                    progressBar.style.backgroundColor = '#61d713'
                } else {
                    progressBar.style.backgroundColor = '#F44336';
                }
            })
            .catch(error => {
                console.error("Error fetching training progress:", error);
            });
    }

    if (employeeId) {
        updateTrainingProgress(employeeId);
    }
});