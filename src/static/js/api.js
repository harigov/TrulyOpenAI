const BASE_URL = '';
const API_URL = `${BASE_URL}/v1`;

// Fetch all chat sessions
const fetchChatSessions = () => {
    return $.get(`${API_URL}/sessions`);
};

// Create a new chat session
const createChatSession = () => {
    return $.ajax({
        url: `${API_URL}/sessions`,
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
        url: `${API_URL}/sessions/${sessionId}`,
        type: 'PUT',
        contentType: 'application/json',
        data: JSON.stringify({ is_archived: isArchived })
    });
};

// Delete an existing chat session
const deleteChatSession = (sessionId) => {
    return $.ajax({
        url: `${API_URL}/sessions/${sessionId}`,
        type: 'DELETE'
    });
};

// Fetch all chat messages for a specific chat session
const fetchChatMessages = (sessionId) => {
    return $.get(`${API_URL}/api/sessions/${sessionId}/messages`);
};

const sendChatMessage = (sessionId, message) => {
    console.log('Sending message: ' + message);
    return $.ajax({
        url: `${BASE_URL}/message`,
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({
            session_id: sessionId, content: message
        })
    });
};

// Fetch all chat sessions and create DOM elements for each session
const createChatSessionElements = async () => {
    console.log("Creating chat session elements");
    const sessions = await fetchChatSessions();
    const chatList = $('#chat-list-container:first');
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

const createChatMessageItem = (role, message, created_at) => {
    if (role == 'assistant') {
        return $(`
        <li class="clearfix">
            <div class="message-data">
                <span class="message-data-time">${created_at}</span> &nbsp; &nbsp;
                <span class="message-data-name">Sidekick</span> <i class="fa fa-circle me"></i>
            </div>
            <div class="message my-message">
                ${message}
            </div>
        </li>
        `);
    } else {
        return $(`
        <li class="clearfix">
            <div class="message-data align-right">
                <span class="message-data-time">${created_at}</span> &nbsp; &nbsp;
                <span class="message-data-name">You</span> <i class="fa fa-circle me"></i>
            </div>
            <div class="message other-message float-right">
                ${message}
            </div>
        </li>
        `);
    }
};

const createChatMessageElements = async (sessionId) => {
    const messages = await fetchChatMessages(sessionId);
    const messageContainer = $('#chat-messages-container:first');
    messageContainer.empty();
    messages.forEach((message) => {
        const messageItem = createChatMessageItem(message.role, message.message, message.created_at);
        messageContainer.append(messageItem);
    });
};

// Activate a chat session
const activateSession = async (event) => {
    const sessionId = $(event.currentTarget).data('session-id');
    const sessionName = $(event.currentTarget).find('.name').text();
    $('.chat').data('session-id', sessionId);
    $('.chat-about').text(sessionName);
    console.log(`Session ${sessionId} activated`);
};

const sendMessage = async (event) => {
    event.preventDefault();

    const message = $('#chat-input').val();
    const userMsgItem = createChatMessageItem('user', message, 'now');
    const msgContainer = $('.chat-messages-container:first');
    msgContainer.append(userMsgItem);
    $('#chat-input').val('');

    const sessionId = $('.chat').data('session-id');

    const response = await sendChatMessage(sessionId, message);
    console.log(response);
    const assistantMsgItem = createChatMessageItem('assistant', response['message'], 'now');
    msgContainer.append(assistantMsgItem);
    $('#chat-input').focus();
}

$(document).ready(() => {
    // Add click event listener to add button
    $('#addButton').on('click', async () => {
        await createChatSession();
        await createChatSessionElements();
    });

    $('#sendButton').on('click', sendMessage);

    // Create chat session elements on page load
    createChatSessionElements();
    $('#chat-input').focus();
});