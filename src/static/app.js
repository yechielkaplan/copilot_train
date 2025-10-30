document.addEventListener("DOMContentLoaded", () => {
  const activitiesList = document.getElementById("activities-list");
  const activitySelect = document.getElementById("activity");
  const signupForm = document.getElementById("signup-form");
  const messageDiv = document.getElementById("message");

  // --- new helper: escape HTML to avoid XSS when rendering participant names ---
  function escapeHtml(str) {
    return String(str)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#039;");
  }

  // Function to fetch activities from API
  async function fetchActivities() {
    try {
      const response = await fetch("/activities");
      const activities = await response.json();

  // Clear loading message and reset activity select to avoid duplicate options
  activitiesList.innerHTML = "";
  activitySelect.innerHTML = `<option value="">-- Select an activity --</option>`;

      // Populate activities list
      Object.entries(activities).forEach(([name, details]) => {
        const activityCard = document.createElement("div");
        activityCard.className = "activity-card";

        const spotsLeft = details.max_participants - details.participants.length;

        // --- replaced block: include participants section (bulleted list) ---
        const participants = Array.isArray(details.participants) ? details.participants : [];
        const participantsHtml =
          participants.length > 0
            ? `<div class="participants-container">
                 <h5 class="participants-title">Participants</h5>
                 <ul class="participants">
                   ${participants
                     .map(
                       (p) =>
                         `<li><span class="participant-email">${escapeHtml(p)}</span> <button class="delete-participant" aria-label="Remove participant" data-activity="${escapeHtml(
                           name
                         )}" data-email="${escapeHtml(p)}">🗑️</button></li>`
                     )
                     .join("")}
                 </ul>
               </div>`
            : `<p class="info">No participants yet.</p>`;

        activityCard.innerHTML = `
          <h4>${escapeHtml(name)}</h4>
          <p>${escapeHtml(details.description)}</p>
          <p><strong>Schedule:</strong> ${escapeHtml(details.schedule)}</p>
          <p><strong>Availability:</strong> ${spotsLeft} spots left</p>
          ${participantsHtml}
        `;
        // --- end replaced block ---

        activitiesList.appendChild(activityCard);

        // Add option to select dropdown
        const option = document.createElement("option");
        option.value = name;
        option.textContent = name;
        activitySelect.appendChild(option);
      });
    } catch (error) {
      activitiesList.innerHTML = "<p>Failed to load activities. Please try again later.</p>";
      console.error("Error fetching activities:", error);
    }
  }

  // Handle form submission
  signupForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const email = document.getElementById("email").value;
    const activity = document.getElementById("activity").value;

    try {
      const response = await fetch(
        `/activities/${encodeURIComponent(activity)}/signup?email=${encodeURIComponent(email)}`,
        {
          method: "POST",
        }
      );

      const result = await response.json();

      if (response.ok) {
        messageDiv.textContent = result.message;
        messageDiv.className = "message success";
        signupForm.reset();

        // Refresh activities so the new participant shows up immediately
        fetchActivities();
      } else {
        messageDiv.textContent = result.detail || "An error occurred";
        messageDiv.className = "message error";
      }

      // Ensure message is visible
      messageDiv.classList.remove("hidden");

      // Hide message after 5 seconds
      setTimeout(() => {
        messageDiv.classList.add("hidden");
      }, 5000);
    } catch (error) {
      messageDiv.textContent = "Failed to sign up. Please try again.";
      messageDiv.className = "error";
      messageDiv.classList.remove("hidden");
      console.error("Error signing up:", error);
    }
  });

  // Initialize app
  fetchActivities();
  
    // Event delegation: handle clicks on delete buttons to unregister participants
    activitiesList.addEventListener("click", async (event) => {
      const btn = event.target.closest(".delete-participant");
      if (!btn) return;
    
      const email = btn.dataset.email;
      const activity = btn.dataset.activity;
      if (!email || !activity) return;
    
      if (!confirm(`Remove ${email} from ${activity}?`)) return;
    
      try {
        const resp = await fetch(
          `/activities/${encodeURIComponent(activity)}/unregister?email=${encodeURIComponent(email)}`,
          { method: "POST" }
        );
        const result = await resp.json();
        if (resp.ok) {
          // Remove the participant's list item from the DOM
          const li = btn.closest("li");
          if (li) li.remove();
        
          // Refresh activities to update availability counts
          fetchActivities();
        } else {
          alert(result.detail || "Failed to remove participant");
        }
      } catch (err) {
        console.error("Error unregistering participant:", err);
        alert("Failed to remove participant. Please try again.");
      }
    });
});
