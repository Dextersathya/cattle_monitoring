document.addEventListener("DOMContentLoaded", function () {
  let recentStrings = []; // Array to store recent non-empty strings

  function fetchDataAndUpdateCount() {
    fetch("http://localhost:3000/api/get")
      .then((response) => response.json())
      .then((data) => {
        const count = data.COUNT;
        const connectedDevicesElement = document.getElementById("countValue");
        connectedDevicesElement.textContent = count;

        // Add non-empty keyString to recentStrings array
        const keyString = data.string || ""; // Default to empty string if keyString is not provided
        if (keyString !== "") {
          recentStrings.push(keyString);
          if (recentStrings.length > 4) {
            recentStrings.shift(); // Remove the first element if array length exceeds 4
          }
        }

        // Map recent strings to HTML
        const recentStringsElement = document.getElementById("recentStrings");
        recentStringsElement.innerHTML = ""; // Clear previous content
        recentStrings.forEach((string) => {
          const stringItem = document.createElement("div");
          stringItem.textContent = "$ " + string;
          recentStringsElement.appendChild(stringItem);
        });
      })
      .catch((error) => console.error("Error fetching count:", error));
  }

  fetchDataAndUpdateCount(); // Initial fetch
  setInterval(fetchDataAndUpdateCount, 3000);
});
