document.addEventListener('DOMContentLoaded', () => {
    let lastEmployeeData = null;
    let lastTrainingModuleData = null;
    let lastDateCompleted = "{{ last_date_completed|escapejs }}";

    try {
        lastEmployeeData = JSON.parse('{{ last_employee_json|escapejs }}');
        lastTrainingModuleData = JSON.parse('{{ last_training_module_json|escapejs }}');
    } catch (e) {
        console.error("Error parsing JSON:", e);
    }

    const messageContainer = document.getElementById('last-input-message');
    if (lastEmployeeData && lastTrainingModuleData && lastDateCompleted) {
        const message = `
            <strong>Last Input:</strong><br>
            <p>Employee: <strong>${lastEmployeeData.name}</strong> (Staff Number: ${lastEmployeeData.staff_number})</p>
            <p>Training Module: <strong>${lastTrainingModuleData.name}</strong></p>
            <p>Date Completed: <strong>${lastDateCompleted}</strong></p>
        `;
        messageContainer.innerHTML = message;
        messageContainer.style.display = 'block';
    } else {
        console.log("Missing or invalid data.");
    }
});
