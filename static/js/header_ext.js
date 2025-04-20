// Function to update breadcrumbs (Step 1: Change "Home" link and remove "Src")
function updateBreadcrumbs() {
  const breadcrumbs = document.querySelector(".breadcrumbs");

  if (breadcrumbs) {
    const srcLink = breadcrumbs.querySelector('a[href="/admin/src/"]');
    const srcTextNodes = breadcrumbs.childNodes;

    // Remove "Src" link if present
    if (srcLink) {
      srcLink.parentNode.removeChild(srcLink);
    } else {
      // Remove "Src" text node if present
      srcTextNodes.forEach((node) => {
        if (
          node.nodeType === Node.TEXT_NODE &&
          node.textContent.includes("Src")
        ) {
          node.parentNode.removeChild(node);
        }
      });
    }

    // Change "Home" link to "/admin/src/"
    const homeLink = breadcrumbs.querySelector('a[href="/admin/"]');
    if (homeLink) {
      homeLink.href = "/admin/src/";
      homeLink.innerHTML = "Home";
    }

    // Remove any extra "›" symbols
    const arrows = Array.from(breadcrumbs.childNodes).filter(
      (node) =>
        node.nodeType === Node.TEXT_NODE && node.textContent.trim() === "›"
    );

    if (arrows.length > 1) {
      arrows[0].parentNode.removeChild(arrows[0]); // Remove the first "›"
    }
  }
}

// Function to update the header with GingerDB, Welcome message, Logout, and Theme Toggle buttons
function updateHeader() {
  const breadcrumbs = document.querySelector(".breadcrumbs");

  if (breadcrumbs) {
    // Create and add GingerDB logo and text
    const gingerSpan = document.createElement("span");
    gingerSpan.classList.add("gingerdb-container");

    const gingerText = document.createTextNode("GingerDB ");
    const gingerImage = document.createElement("img");
    gingerImage.src =
      "https://dev-portal-staging.gingersociety.org/ginger-db.png";
    gingerImage.alt = "GingerDB";
    gingerImage.style.width = "20px";
    gingerImage.style.height = "20px";
    gingerImage.style.marginLeft = "5px";

    gingerSpan.appendChild(gingerText);
    gingerSpan.appendChild(gingerImage);
    breadcrumbs.insertBefore(gingerSpan, breadcrumbs.firstChild);

    // Create Logout button
    const logoutButton = document.createElement("button");
    logoutButton.innerText = "Logout";
    logoutButton.classList.add("logout-button");
    logoutButton.onclick = async function () {
      await fetch("/clear-session");
      window.location.href = "/?logout"; // Redirect to logout
    };

    breadcrumbs.appendChild(logoutButton);

    // Create and add Theme Toggle button
    const toggleThemeButton = document.createElement("button");
    toggleThemeButton.innerHTML = '<i class="fas fa-sun"></i>';
    toggleThemeButton.classList.add("theme-toggle-button");

    toggleThemeButton.onclick = function () {
      const htmlTag = document.documentElement;
      const currentTheme = htmlTag.getAttribute("data-theme");

      if (currentTheme === "dark") {
        htmlTag.setAttribute("data-theme", "light");
        toggleThemeButton.innerHTML = '<i class="fas fa-sun"></i>';
        localStorage.setItem("theme", "light");
      } else {
        htmlTag.setAttribute("data-theme", "dark");
        toggleThemeButton.innerHTML = '<i class="fas fa-moon"></i>';
        localStorage.setItem("theme", "dark");
      }
    };

    breadcrumbs.appendChild(toggleThemeButton);
  }
}

// Function to fetch email from /additional-info and add Welcome message
function addWelcomeMessage() {
  const breadcrumbs = document.querySelector(".breadcrumbs");
  let welcomeMessage = breadcrumbs.querySelector(".welcome-message");
  const logoutButton = breadcrumbs.querySelector(".logout-button");

  // Fetch the email from the server
  fetch("/additional-details")
    .then((response) => response.json())
    .then((data) => {
      const userEmail = data.email || null; // Default value if email is not available

      // Create and add Welcome message with user email
      
      if (!welcomeMessage) {
        welcomeMessage = document.createElement("span");
        welcomeMessage.classList.add("welcome-message");
        welcomeMessage.innerText = `Welcome, ${userEmail}`;
        welcomeMessage.style.marginRight = "10px";

        
        breadcrumbs.insertBefore(welcomeMessage, logoutButton);
      }
    })
    .catch((error) => {
      logoutButton.style.display = "none"; // Hide Logout button
      console.error("Error fetching additional info:", error);
    });
}

// Function to load the theme from localStorage and apply it
function loadThemeFromLocalStorage() {
  const savedTheme = localStorage.getItem("theme");

  if (savedTheme) {
    const htmlTag = document.documentElement;
    htmlTag.setAttribute("data-theme", savedTheme); // Apply the saved theme

    const toggleThemeButton = document.querySelector(".theme-toggle-button");
    if (savedTheme === "dark") {
      toggleThemeButton.innerHTML = '<i class="fas fa-moon"></i>'; // Set dark mode icon
    } else {
      toggleThemeButton.innerHTML = '<i class="fas fa-sun"></i>'; // Set light mode icon
    }
  }
}

// Call the functions when the DOM content is fully loaded
document.addEventListener("DOMContentLoaded", function () {
  updateBreadcrumbs();
  updateHeader();
  loadThemeFromLocalStorage(); // Load the saved theme on page load
  addWelcomeMessage(); // Fetch and add the welcome message
});

// Set up an interval to refresh token every 5 minutes
setInterval(() => {
  fetch("/refresh-token");
}, 300000);
