// Fetching the JSON data and populating the table
fetch('/fetchdata/customer_data')
  .then(response => response.json())
  .then(data => {
    const tableBody = document.getElementById('myTable').querySelector('tbody');
    data.forEach(item => {
      const row = document.createElement('tr');
      
      const customerIdCell = document.createElement('td');
      const recencyCell = document.createElement('td');
      const frequencyCell = document.createElement('td');
      const monetaryCell = document.createElement('td');
      const rfmScoreCell = document.createElement('td');
      const customerGroupCell = document.createElement('td');
      const clvCell = document.createElement('td');
      
      customerIdCell.textContent = item.customer_id;
      recencyCell.textContent = item.recency;
      frequencyCell.textContent = item.frequency;
      monetaryCell.textContent = item.monetary;
      rfmScoreCell.textContent = item.rfm_score;
      customerGroupCell.textContent = item.customer_group;
      clvCell.textContent = item.clv;

      row.appendChild(customerIdCell);
      row.appendChild(recencyCell);
      row.appendChild(frequencyCell);
      row.appendChild(monetaryCell);
      row.appendChild(rfmScoreCell);
      row.appendChild(customerGroupCell);
      row.appendChild(clvCell);

      tableBody.appendChild(row);
    });
  })
  .catch(error => {
    console.error('Error fetching data:', error);
  });

// Search functionality
const searchInput = document.getElementById('search-input');
searchInput.addEventListener('input', (event) => {
  const searchTerm = event.target.value.toLowerCase();
  const rows = document.querySelectorAll('#myTable tbody tr');
  rows.forEach(row => {
    const cells = row.querySelectorAll('td');
    let match = false;
    cells.forEach(cell => {
      if (cell.textContent.toLowerCase().includes(searchTerm)) {
        match = true;
      }
    });
    if (match) {
      row.style.display = '';
    } else {
      row.style.display = 'none';
    }
  });
});

// Back button functionality
const backButton = document.querySelector('.back-button');
backButton.addEventListener('click', () => {
  // Implement your back button logic here, e.g., redirect to the previous page
  window.history.back();
});
