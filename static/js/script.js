function saveNote(section) {
    const textarea = document.querySelector(`#note-input-${section}`);
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
  
    if (!textarea) {
      console.error(`Text Area Not Found for section: ${section}`);
      return;
    }
  
    const content = textarea.value.trim();
    if (!content) {
      alert("Please enter a note.");
      return;
    }
  
    const dkTopic = document.querySelector('#note-dkTopic').value;
    const topicTheme = document.querySelector('#note-topicTheme').value;
  
    fetch('/save-note/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrfToken,
      },
      body: JSON.stringify({
        noteTopic: dkTopic,
        noteTheme: topicTheme,
        noteContent: content,
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
    const topicId = document.querySelector('#note-dkTopic').value;
    const notesDisplay = document.querySelector(`#notes-display-${section}`);
  
    if (!notesDisplay) {
      console.error(`Notes display container not found for section: ${section}`);
      return;
    }
  
    fetch(`/get-notes/${topicId}/`)
      .then(response => response.json())
      .then(data => {
        if (data.status === 'success') {
          notesDisplay.innerHTML = '';
  
          data.notes.forEach(note => {
            const bubble = document.createElement('div');
            bubble.innerHTML = `
              <div>
                <strong>Post:</strong> ${note.relatedAdminPost}<br>
                <strong>Topic:</strong> ${note.topic}<br>
                <strong>Theme:</strong> ${note.theme}<br>
                <strong>Note:</strong> ${note.content}
              </div>
            `;
            bubble.style.cssText = `
              background-color: rgb(189, 189, 189);
              border-radius: 10px;
              padding: 10px;
              margin: 10px 0;
            `;
            notesDisplay.appendChild(bubble);
          });
        } else {
          notesDisplay.innerHTML = '<p>No notes for this section yet.</p>';
        }
      })
      .catch(error => console.error("Error fetching notes:", error));
  }
  
  document.addEventListener('DOMContentLoaded', () => {
    ['articles', 'videos', 'other'].forEach(fetchNotes);
  });
  
  
  document.querySelectorAll('.resources_boxes > div').forEach((box) => {
    const popoverContent = box.querySelector('[popover]').textContent; // Get popover content
    const previewText = popoverContent.slice(0, 200) + '...'; // Truncate to first 40 characters
    const previewElement = box.querySelector('p');
    if (previewElement) {
      previewElement.textContent = `${previewText}`;
    }
  });