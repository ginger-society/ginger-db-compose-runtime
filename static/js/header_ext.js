function updateBreadcrumbs() {
  // Find the breadcrumbs container
  const breadcrumbs = document.querySelector(".breadcrumbs");

  if (breadcrumbs) {
    // Step 2: Remove the "Src" link or text, if present
    const srcLink = breadcrumbs.querySelector('a[href="/admin/src/"]');
    const srcTextNodes = breadcrumbs.childNodes;

    if (srcLink) {
      // If there's a link for "Src", remove it
      srcLink.parentNode.removeChild(srcLink);
    } else {
      // If there is a "› Src" text (without a link), remove the text node
      srcTextNodes.forEach((node) => {
        if (
          node.nodeType === Node.TEXT_NODE &&
          node.textContent.includes("Src")
        ) {
          node.parentNode.removeChild(node); // Remove the text node
        }
      });
    }
    // Step 1: Change "Home" link to "/admin/src/"
    const homeLink = breadcrumbs.querySelector('a[href="/admin/"]');
    if (homeLink) {
      homeLink.href = "/admin/src/";
      homeLink.innerHTML = "Home";
    }

    // Step 3: Ensure there are no extra "›" symbols
    const arrows = Array.from(breadcrumbs.childNodes).filter(
      (node) =>
        node.nodeType === Node.TEXT_NODE && node.textContent.trim() === "›"
    );

    // Remove any extra › characters at the beginning
    if (arrows.length > 1) {
      arrows[0].parentNode.removeChild(arrows[0]); // Remove the first ›
    }
  }
}

function updateHeader() {
  // Find the breadcrumbs element
  const breadcrumbs = document.querySelector(".breadcrumbs");

  if (breadcrumbs) {
    // Create a new span element for GingerDB
    const gingerSpan = document.createElement("span");
    gingerSpan.classList.add("gingerdb-container"); // Add a class for styling

    // Create the text node "GingerDB"
    const gingerText = document.createTextNode("GingerDB ");

    // Create an image element
    const gingerImage = document.createElement("img");
    gingerImage.src =
      "https://dev-portal-staging.gingersociety.org/ginger-db.png";
    gingerImage.alt = "GingerDB";
    gingerImage.style.width = "20px"; // Set image width, adjust as needed
    gingerImage.style.height = "20px"; // Set image height, adjust as needed
    gingerImage.style.marginLeft = "5px"; // Add space between the text and image

    // Append text and image to the span
    gingerSpan.appendChild(gingerText);
    gingerSpan.appendChild(gingerImage);

    // Add the span as the first child of the breadcrumbs element
    breadcrumbs.insertBefore(gingerSpan, breadcrumbs.firstChild);

    // Create a Welcome message with the user email
    const userEmail = "hello@gingersociety.org"; // Replace with dynamic user email if needed
    let welcomeMessage = breadcrumbs.querySelector(".welcome-message");
    if (!welcomeMessage) {
      welcomeMessage = document.createElement("span");
      welcomeMessage.classList.add("welcome-message");
      welcomeMessage.innerText = `Welcome, ${userEmail}`;
      welcomeMessage.style.marginRight = "10px"; // Add some spacing before the logout button
    }

    // Create a Logout button
    const logoutButton = document.createElement("button");
    logoutButton.innerText = "Logout";
    logoutButton.classList.add("logout-button"); // Add a class for styling
    logoutButton.onclick = async function () {
      await fetch("/clear-session");
      window.location.href = "/"; // Navigate to /logout route
    };

    // Append the Logout button as the last child of the breadcrumbs element
    breadcrumbs.appendChild(logoutButton);
    breadcrumbs.appendChild(welcomeMessage);

    // Create a dark mode/light mode toggle
    const toggleThemeButton = document.createElement("button");
    toggleThemeButton.innerHTML = '<i class="fas fa-sun"></i>'; // Light mode icon initially
    toggleThemeButton.classList.add("theme-toggle-button"); // Add a class for styling

    // Add click event for toggling the theme
    toggleThemeButton.onclick = function () {
      const htmlTag = document.documentElement; // Get the <html> element
      const currentTheme = htmlTag.getAttribute("data-theme");

      if (currentTheme === "dark") {
        htmlTag.setAttribute("data-theme", "light");
        toggleThemeButton.innerHTML = '<i class="fas fa-sun"></i>'; // Switch to light mode icon
        localStorage.setItem("theme", "light"); // Save the theme to localStorage
      } else {
        htmlTag.setAttribute("data-theme", "dark");
        toggleThemeButton.innerHTML = '<i class="fas fa-moon"></i>'; // Switch to dark mode icon
        localStorage.setItem("theme", "dark"); // Save the theme to localStorage
      }
    };

    // Append the theme toggle button next to Logout button
    breadcrumbs.appendChild(toggleThemeButton);
  }
}

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

// Call the function when the DOM content is fully loaded
document.addEventListener("DOMContentLoaded", function () {
  updateBreadcrumbs();
  updateHeader();
  loadThemeFromLocalStorage(); // Load the saved theme on page load
});

// Set up an interval to refresh token every 5 minutes
setInterval(() => {
  fetch("/refresh-token");
}, 300000);
