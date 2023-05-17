
  const my_bar = document.getElementById('myBar');
  const my_pie = document.getElementById("myPie");
  const my_line = document.getElementById("myLine");
const my_dot = document.getElementById("myDot");

  new Chart(my_bar, {
    type: 'bar',
    data: {
      labels: ['Jean', 'Directeur', 'Katerin', 'Kodom'],
      datasets: [{
        label: 'Nombre de visiteurs',
        backgroundColor: ['Red', 'Blue', 'Green', 'Orange'],
        data: [12, 19, 3, 5],
        borderWidth: 1
      }]
    },
    options: {
      scales: {
        y: {
          beginAtZero: true
        }
      }
    }
  });

  new Chart(my_pie, {
    type: "doughnut",
    data: {
      labels: ["Hommes", "Femmes"],
      datasets: [
        {
          label: "Genre de Visiteurs",
          backgroundColor: [
            "Blue",
            "Pink",
          ],
          data: [12, 19],
          borderWidth: 1,
        },
      ],
    },
    options: {
      scales: {
        y: {
          beginAtZero: true,
        },
      },
    },
  });
