
// Real Estate Dashboard - Frontend JavaScript

// Global variables for charts
let priceChart = null
let cityChart = null

// Initialize dashboard on page load
document.addEventListener("DOMContentLoaded", () => {
  console.log("[v0] Initializing Real Estate Dashboard...")

  // Load analytics data
  loadAnalytics()

  // Setup form submission
  const form = document.getElementById("predictionForm")
  form.addEventListener("submit", handlePrediction)

  console.log("[v0] Dashboard initialized successfully")
})

// Load and display analytics data
function loadAnalytics() {
  console.log("[v0] Loading analytics data...")

  fetch("/api/analytics")
    .then((response) => {
      if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`)
      return response.json()
    })
    .then((data) => {
      console.log("[v0] Analytics data received:", data)

      // Update summary cards
      document.getElementById("totalListings").textContent = data.total_listings.toLocaleString()
      document.getElementById("avgPrice").textContent = "$" + Math.round(data.avg_price).toLocaleString()
      document.getElementById("minPrice").textContent = "$" + Math.round(data.min_price).toLocaleString()
      document.getElementById("maxPrice").textContent = "$" + Math.round(data.max_price).toLocaleString()

      // Initialize charts
      initPriceChart(data.price_trends)
      initCityChart(data.city_data)
    })
    .catch((error) => {
      console.error("[v0] Error loading analytics:", error)
      alert("Failed to load analytics data")
    })
}

// Initialize price trends line chart
function initPriceChart(trends) {
  console.log("[v0] Initializing price trend chart with", trends.length, "data points")

  const ctx = document.getElementById("priceChart").getContext("2d")

  // Destroy existing chart if it exists
  if (priceChart) priceChart.destroy()

  priceChart = new Chart(ctx, {
    type: "line",
    data: {
      labels: trends.map((t) => t.area + " sqft"),
      datasets: [
        {
          label: "Price ($)",
          data: trends.map((t) => t.price),
          borderColor: "#1e40af",
          backgroundColor: "rgba(30, 64, 175, 0.1)",
          tension: 0.4,
          fill: true,
          pointRadius: 3,
          pointBackgroundColor: "#1e40af",
          pointBorderColor: "#fff",
          pointBorderWidth: 2,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: true,
      plugins: {
        legend: {
          display: true,
          position: "top",
        },
      },
      scales: {
        y: {
          beginAtZero: false,
          title: {
            display: true,
            text: "Price ($)",
          },
          ticks: {
            callback: (value) => "$" + value.toLocaleString(),
          },
        },
        x: {
          title: {
            display: true,
            text: "Area (sqft)",
          },
        },
      },
    },
  })
}

// Initialize city distribution pie chart
function initCityChart(cityData) {
  console.log("[v0] Initializing city distribution chart with", cityData.length, "cities")

  const ctx = document.getElementById("cityChart").getContext("2d")

  // Destroy existing chart if it exists
  if (cityChart) cityChart.destroy()

  const colors = ["#1e40af", "#3b82f6", "#60a5fa", "#93c5fd", "#dbeafe"]

  cityChart = new Chart(ctx, {
    type: "pie",
    data: {
      labels: cityData.map((c) => c.city),
      datasets: [
        {
          data: cityData.map((c) => c.count),
          backgroundColor: colors.slice(0, cityData.length),
          borderColor: "#fff",
          borderWidth: 2,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: true,
      plugins: {
        legend: {
          display: true,
          position: "right",
        },
        tooltip: {
          callbacks: {
            label: (context) => {
              const label = context.label || ""
              const value = context.parsed || 0
              return label + ": " + value + " listings"
            },
          },
        },
      },
    },
  })
}

// Handle price prediction form submission
function handlePrediction(event) {
  event.preventDefault()
  console.log("[v0] Prediction form submitted")

  // Get form values
  const formData = new FormData(event.target)
  const data = {
    area: Number.parseFloat(formData.get("area")),
    bedrooms: Number.parseInt(formData.get("bedrooms")),
    bathrooms: Number.parseInt(formData.get("bathrooms")),
    city: formData.get("city"),
    property_type: formData.get("property_type"),
  }

  console.log("[v0] Sending prediction request:", data)

  // Disable button during request
  const button = event.target.querySelector('button[type="submit"]')
  button.disabled = true
  button.textContent = "Predicting..."

  // Send to Flask backend
  fetch("/api/predict", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  })
    .then((response) => {
      if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`)
      return response.json()
    })
    .then((result) => {
      console.log("[v0] Prediction result:", result)

      // Display result
      displayPredictionResult(result)
    })
    .catch((error) => {
      console.error("[v0] Prediction error:", error)
      alert("Error predicting price. Please check your input and try again.")
    })
    .finally(() => {
      // Re-enable button
      button.disabled = false
      button.textContent = "Predict Price"
    })
}

// Display prediction result on page
function displayPredictionResult(result) {
  console.log("[v0] Displaying prediction result")

  const resultContainer = document.getElementById("resultContainer")
  const predictedPrice = document.getElementById("predictedPrice")
  const resultDetails = document.getElementById("resultDetails")

  // Update predicted price
  predictedPrice.textContent =
    "$" +
    result.predicted_price.toLocaleString("en-US", {
      minimumFractionDigits: 2,
      maximumFractionDigits: 2,
    })

  // Update details
  const input = result.input_data
  resultDetails.innerHTML = `
        <div class="detail-item">
            <div class="detail-label">Area</div>
            <div class="detail-value">${input.area.toLocaleString()} sqft</div>
        </div>
        <div class="detail-item">
            <div class="detail-label">Bedrooms</div>
            <div class="detail-value">${input.bedrooms}</div>
        </div>
        <div class="detail-item">
            <div class="detail-label">Bathrooms</div>
            <div class="detail-value">${input.bathrooms}</div>
        </div>
        <div class="detail-item">
            <div class="detail-label">City</div>
            <div class="detail-value">${input.city}</div>
        </div>
        <div class="detail-item">
            <div class="detail-label">Property Type</div>
            <div class="detail-value">${input.property_type}</div>
        </div>
    `

  // Show result container
  resultContainer.classList.remove("hidden")

  // Scroll to result
  resultContainer.scrollIntoView({ behavior: "smooth", block: "nearest" })
}
