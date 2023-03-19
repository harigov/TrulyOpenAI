const BASE_URL = 'v1';

// Fetch all chat sessions
const fetchChatSessions = () => {
  return $.get(`${BASE_URL}/sessions`);
};

// Create a new chat session
const createChatSession = () => {
  return $.ajax({
    url: `${BASE_URL}/sessions`,
    type: 'POST',
    contentType: 'application/json',
    data: JSON.stringify({ 
        name: 'New Chat Session',
        is_archived: false 
    }),
  });
};

// Update an existing chat session
const updateChatSession = (sessionId, isArchived) => {
  return $.ajax({
    url: `${BASE_URL}/sessions/${sessionId}`,
    type: 'PUT',
    contentType: 'application/json',
    data: JSON.stringify({ is_archived: isArchived })
  });
};

// Delete an existing chat session
const deleteChatSession = (sessionId) => {
  return $.ajax({
    url: `${BASE_URL}/sessions/${sessionId}`,
    type: 'DELETE'
  });
};

// Fetch all chat messages for a specific chat session
const fetchChatMessages = (sessionId) => {
  return $.get(`${BASE_URL}/api/sessions/${sessionId}/messages`);
};

// Fetch all chat sessions and create DOM elements for each session
const createChatSessionElements = async () => {
  const sessions = await fetchChatSessions();
  const chatList = $('.chat-list');
  chatList.empty();
  sessions.forEach((session) => {
    const listItem = `
      <li class="clearfix session-item" data-session-id="${session.id}">
        <img src="https://bootdey.com/img/Content/avatar/avatar1.png" alt="avatar">
        <div class="about">
          <div class="name">${session.name}</div>
        </div>
      </li>
    `;
    chatList.append(listItem);
  });

  // Add click event listener to session items
  $('.session-item').on('click', activateSession);
};

// Activate a chat session
const activateSession = (event) => {
  const sessionId = $(event.currentTarget).data('session-id');
  console.log(`Session ${sessionId} activated`);
};

$(document).ready(() => {
  // Add click event listener to add button
  $('#addButton').on('click', async () => {
    await createChatSession();
    await createChatSessionElements();
  });

  // Create chat session elements on page load
  createChatSessionElements();
});