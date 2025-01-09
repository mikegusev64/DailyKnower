function saveNote(section) {
    const textarea = document.querySelector(`#note-input-${section}`);
    const topicIdInput = document.querySelector(`#note-dkTopic-${section}`);
    const themeIdInput = document.querySelector('#note-topicTheme'); 
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
  

    console.log("Textarea:", textarea);
    console.log("Topic ID Input:", topicIdInput);

    if (!textarea) {
      console.error(`Text Area Not Found for section: ${section}`);
      return;
    }

    if (!topicIdInput) {
        console.error(`Topic ID input not found for section: ${section}`);
        return;
    }

    if (!themeIdInput) {
        console.error("Theme ID input not found.");
        return;
    }
  
    const content = textarea.value.trim();
    if (!content) {
      alert("Please enter a note.");
      return;
    }
  

    const topicId = topicIdInput.value;
    const themeId = themeIdInput.value;

    console.log("Saving Note:");
    console.log({
        noteTopic: topicId,
        noteTheme: themeId,
        noteContent: content,
    });



    fetch('/save-note/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrfToken,
      },
      body: JSON.stringify({
        noteTopic: topicId,
        noteContent: content,
        noteTheme: themeId,
      }),
    })
      .then(response => response.json())
      .then(data => {
        if (data.status === 'success') {
          alert("Note saved successfully!");
          textarea.value = ''; // Clear textarea
          fetchNotes(section); // Refresh displayed notes
        } else {
          alert("Error saving note: " + data.message);
        }
      })
      .catch(error => console.error("Error:", error));
  }
  
  function fetchNotes(section) {
    const topicIdInput = document.querySelector(`#note-dkTopic-${section}`);
    if (!topicIdInput) {
        console.error(`Topic ID input not found for section: ${section}`);
        return;
    }

    const topicId = topicIdInput.value;
    const notesDisplay = document.querySelector(`#notes-display-${section}`);

    if (!notesDisplay) {
        console.error(`Notes display container not found for section: ${section}`);
        return;
    }

    console.log(`Fetching notes for section: ${section}, Topic ID: ${topicId}`);

    notesDisplay.innerHTML = "";
  
    fetch(`/get-notes/${topicId}/`)
      .then(response => response.json())
      .then(data => {
        console.log("Fetched data:", data);
        if (data.status === 'success') {
          notesDisplay.innerHTML = '';
  
          data.notes.forEach(note => {
            console.log("Rendering note:", note);
            const bubble = document.createElement('div');
            bubble.textContent=note.content;
            bubble.style.cssText = `
              background-color: rgb(246,238,175);
              border-radius: 10px;
              padding: 10px;
              margin: 10px 0;
              box-shadow: 2px 2px 7px grey;
            `;
            notesDisplay.appendChild(bubble);
          });
        } else {
            console.error("Failed to fetch notes:", data.message);
          notesDisplay.innerHTML = '<p>No notes for this section yet.</p>';
        }
      })
      .catch(error => console.error("Error fetching notes:", error));
  }
  
  document.addEventListener('DOMContentLoaded', () => {
    console.log("DOM fully loaded and parsed.");
    console.log("Starting to fetch notes for sections: articles, videos, other");

    ['articles', 'videos', 'other'].forEach(section => {
        console.log(`Fetching notes for section: ${section}`);
        fetchNotes(section); 
    });
  });
  
  
  document.querySelectorAll('.resources_boxes > div').forEach((box) => {
    const popoverContent = box.querySelector('[popover]').textContent; // Get popover content
    const previewText = popoverContent.slice(0, 100) + '...'; // Truncate to first 40 characters
    const previewElement = box.querySelector('p');
    if (previewElement) {
      previewElement.textContent = `${previewText}`;
    }
  });