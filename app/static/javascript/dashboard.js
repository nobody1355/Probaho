document.addEventListener("DOMContentLoaded", () => {
    console.log("Dashboard JavaScript loaded.");

    // Dropdown toggle for user menu
    const userImg = document.querySelector(".user-img");
    const dropdown = document.querySelector(".user-dropdown");

    userImg.addEventListener("click", () => {
        dropdown.style.display = dropdown.style.display === "block" ? "none" : "block";
    });

    // Fetch and update Monthly Sales Chart
    fetch("/dashboard/dashboard/chart/sales")
        .then(response => {
            console.log("Sales API response status:", response.status);
            return response.json();
        })
        .then(data => {
            console.log("Sales API data:", data);

            if (data.error) {
                console.error("Sales API Error:", data.error);
                return;
            }

            const labels = data.map(item => item.month);
            const values = data.map(item => item.total);

            const ctxSales = document.getElementById("salesChart").getContext("2d");
            new Chart(ctxSales, {
                type: "line",
                data: {
                    labels: labels,
                    datasets: [{
                        label: "Sales (Tk)",
                        data: values,
                        borderColor: "#007BFF",
                        backgroundColor: "rgba(0, 123, 255, 0.2)",
                        tension: 0.4,
                        fill: true,
                    }]
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: {
                            display: true,
                        },
                    },
                    scales: {
                        x: {
                            title: {
                                display: true,
                                text: "Months",
                            },
                        },
                        y: {
                            title: {
                                display: true,
                                text: "Sales (Tk)",
                            },
                        },
                    },
                },
            });
        })
        .catch(error => console.error("Error fetching sales data:", error));

    // Fetch and update Most Demanding Products Chart
    fetch("/dashboard/dashboard/chart/demanding-products")
        .then(response => {
            console.log("Demanding Products API response status:", response.status);
            return response.json();
        })
        .then(data => {
            console.log("Demanding Products API data:", data);

            if (data.error) {
                console.error("Demanding Products API Error:", data.error);
                return;
            }

            const labels = data.map(item => item.product);
            const values = data.map(item => item.demand);

            const ctxDemanding = document.getElementById("demandingChart").getContext("2d");
            new Chart(ctxDemanding, {
                type: "bar",
                data: {
                    labels: labels,
                    datasets: [{
                        label: "Demand",
                        data: values,
                        backgroundColor: "#007BFF",
                        borderColor: "rgba(0, 123, 255, 0.2)",
                        borderWidth: 1,
                    }]
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: {
                            display: false,
                        },
                    },
                    scales: {
                        y: {
                            beginAtZero: true,
                        },
                    },
                },
            });
        })
        .catch(error => console.error("Error fetching demanding products data:", error));

    // Update Date and Time every second
    function updateTime() {
        const now = new Date();
        const dateTimeElement = document.getElementById("date-time");
        if (dateTimeElement) {
            dateTimeElement.innerHTML = now.toLocaleString();
        }
    }

    setInterval(updateTime, 1000);
});
