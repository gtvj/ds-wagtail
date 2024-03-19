
    const queryString = window.location.search;
    const urlParams = new URLSearchParams(queryString);
    //const startDate = urlParams.get('startDate');
    const startDateString = urlParams.get("startDate");
    


    // Convert startDateString to a number
    const startDateNumber = Number(startDateString); // Using Number() function

    const endDate = startDateNumber + 99;

    console.log(startDateNumber); // Output: 2000
    console.log(endDate); // Output: 2010
    const firstDecade = Math.floor(startDateNumber / 10) * 10;




    // Fetch the JSON data from a URL
    fetch('data/data.json')
      .then(response => response.json())
      .then(data => {
        // Assign the data to a variable
        const jsonData = data;

        // Process and filter data before creating the chart
        const chartData = processData(jsonData);

        function processData(data) {
          const decadeCounts = {};
          for (const item of data.data) {
            const creationFrom = parseInt(item["@template"].details.creationDateFrom, 10);
            const decade = Math.floor(creationFrom / 10) * 10;

            // Skip entries with invalid creation dates or missing data
            if (isNaN(creationFrom) || !decade) {
              continue;
            }

            // Filter for records between 1800 and 1900 (inclusive)
            if (decade >= startDateNumber && decade <= endDate) {
              decadeCounts[decade] = (decadeCounts[decade] || 0) + 1;
            }
          }

          // Remove any decades with zero count (no records)
          return Object.fromEntries(
            Object.entries(decadeCounts).filter(([key, value]) => value > 0)
          );
          
        }

        const decadeCounts = chartData;
        const yearLabels = [];

        for (let i = 0; i < 10; i++) {
            const decade = firstDecade + i * 10;
            yearLabels.push(decade.toString());
        }

        // Get the canvas element for the chart
        const ctx = document.getElementById("decade-counts-chart").getContext("2d");

        // Create a new bar chart with click event handling
        const chart = new Chart(ctx, {
          type: "bar",
          data: {
            labels: yearLabels,
            datasets: [
              {
                label: "Record Count",
                data: Object.values(decadeCounts),
                backgroundColor: "rgba(219, 98, 91, 1)",
                borderColor: "rgba(255, 99, 132, 1)",
                borderWidth: 1,
              },
            ],
          },
          options: {
            onHover: (event, chartElement) =>{
              event.native.target.style.cursor = chartElement [0] ? 'pointer' : 'default';
            },
            scales: {
              y:{ grid: {
                  drawOnChartArea: false,
                  color: "rgba(217 217, 214, 1)"
              },
              
              ticks: {
                display:false
              },
              
            },
            x: {
                position: 'top',
                grid: {
                drawBorder: false
             }
              },
          },
            // Adjust chart options as needed (e.g., scales, title)
            plugins: {
            legend: {
              display: false,  // This line hides the legend
              }
            },
          }
        });

        // Add click event listener to the chart
        chart.canvas.onclick = function(evt) {
            const activePoints = chart.getElementsAtEventForMode(evt, 'nearest', false); // Use getElementsAtEventForMode

          if (activePoints.length > 0) {
            // Get the clicked bar index
            const clickedIndex = activePoints[0].index;

            // Access the corresponding decade label and data
            const clickedDecade = chart.data.labels[clickedIndex];
            const recordCount = chart.data.datasets[0].data[clickedIndex];

            // Handle click event (e.g., display a message)
            //alert(`You clicked on the decade ${clickedDecade} with ${recordCount} records.`);
            window.location = `single-decade.html?startDate=${clickedDecade}`;
          }
        };
      });
