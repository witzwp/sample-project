/**
 * WebChat Client
 * Handles Socket.IO connection and UI interactions
 */

// DOM Elements
const loginScreen = document.getElementById('login-screen');
const chatScreen = document.getElementById('chat-screen');
const loginForm = document.getElementById('login-form');
const usernameInput = document.getElementById('username-input');
const messageForm = document.getElementById('message-form');
const messageInput = document.getElementById('message-input');
const messagesContainer = document.getElementById('messages-container');
const messagesDiv = document.getElementById('messages');
const usersList = document.getElementById('users-list');
const userCount = document.getElementById('user-count');
const currentUserSpan = document.getElementById('current-user');
const leaveBtn = document.getElementById('leave-btn');
const typingIndicator = document.getElementById('typing-indicator');

// State
let socket = null;
let username = '';
let typingTimeout = null;

/**
 * Initialize Socket.IO connection
 */
function initSocket() {
    socket = io();

    // Connection events
    socket.on('connect', () => {
        console.log('Connected to server');
    });

    socket.on('disconnect', () => {
        console.log('Disconnected from server');
    });

    // Chat events
    socket.on('user_joined', (data) => {
        addSystemMessage(data.message);
        updateUsersList(data.users);
    });

    socket.on('user_left', (data) => {
        addSystemMessage(`${data.username} left the chat`);
        updateUsersList(data.users);
    });

    socket.on('new_message', (data) => {
        addMessage(data.username, data.message, data.timestamp, false);
    });

    socket.on('history', (data) => {
        loadHistory(data.messages);
    });

    socket.on('user_typing', (data) => {
        if (data.typing) {
            typingIndicator.textContent = `${data.username} is typing...`;
        } else {
            typingIndicator.textContent = '';
        }
    });
}

/**
 * Join the chat with a username
 */
function joinChat() {
    username = usernameInput.value.trim() || 'Anonymous';
    
    // Update UI
    currentUserSpan.textContent = username;
    loginScreen.classList.remove('active');
    chatScreen.classList.add('active');
    
    // Initialize socket and join
    initSocket();
    socket.emit('join', { username });
    
    // Focus on message input
    setTimeout(() => messageInput.focus(), 100);
}

/**
 * Leave the chat
 */
function leaveChat() {
    if (socket) {
        socket.disconnect();
    }
    
    // Reset state
    username = '';
    messagesDiv.innerHTML = '';
    usersList.innerHTML = '';
    userCount.textContent = '0';
    typingIndicator.textContent = '';
    
    // Switch screens
    chatScreen.classList.remove('active');
    loginScreen.classList.add('active');
    usernameInput.value = '';
}

/**
 * Send a message
 */
function sendMessage() {
    const message = messageInput.value.trim();
    
    if (!message || !socket) return;
    
    // Send to server
    socket.emit('message', { message });
    
    // Add to UI immediately (optimistic)
    const timestamp = new Date().toISOString();
    addMessage(username, message, timestamp, true);
    
    // Clear input
    messageInput.value = '';
    messageInput.focus();
    
    // Clear typing indicator
    socket.emit('typing', { typing: false });
}

/**
 * Add a message to the chat
 */
function addMessage(sender, text, timestamp, isOwn) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${isOwn ? 'own' : ''}`;
    
    const time = formatTime(timestamp);
    
    messageDiv.innerHTML = `
        <div class="message-header">
            <span class="message-username">${escapeHtml(sender)}</span>
            <span class="message-time">${time}</span>
        </div>
        <div class="message-content">${escapeHtml(text)}</div>
    `;
    
    messagesDiv.appendChild(messageDiv);
    scrollToBottom();
}

/**
 * Add a system message
 */
function addSystemMessage(text) {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message system';
    messageDiv.innerHTML = `<div class="message-content">${escapeHtml(text)}</div>`;
    messagesDiv.appendChild(messageDiv);
    scrollToBottom();
}

/**
 * Load message history
 */
function loadHistory(messages) {
    messages.forEach(msg => {
        const isOwn = msg.username === username;
        addMessage(msg.username, msg.message, msg.timestamp, isOwn);
    });
}

/**
 * Update the users list
 */
function updateUsersList(users) {
    usersList.innerHTML = '';
    userCount.textContent = users.length;
    
    users.forEach(user => {
        const li = document.createElement('li');
        li.textContent = user;
        if (user === username) {
            li.classList.add('current-user');
            li.textContent += ' (you)';
        }
        usersList.appendChild(li);
    });
}

/**
 * Scroll to the bottom of messages
 */
function scrollToBottom() {
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

/**
 * Format timestamp for display
 */
function formatTime(timestamp) {
    const date = new Date(timestamp);
    return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
}

/**
 * Escape HTML to prevent XSS
 */
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

/**
 * Handle typing indicator
 */
function handleTyping() {
    if (!socket) return;
    
    socket.emit('typing', { typing: true });
    
    // Clear existing timeout
    if (typingTimeout) {
        clearTimeout(typingTimeout);
    }
    
    // Set new timeout to clear typing indicator
    typingTimeout = setTimeout(() => {
        socket.emit('typing', { typing: false });
    }, 1000);
}

// Event Listeners
loginForm.addEventListener('submit', (e) => {
    e.preventDefault();
    joinChat();
});

messageForm.addEventListener('submit', (e) => {
    e.preventDefault();
    sendMessage();
});

messageInput.addEventListener('input', handleTyping);

leaveBtn.addEventListener('click', leaveChat);

// Handle enter key in username input
usernameInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        e.preventDefault();
        joinChat();
    }
});

// Auto-focus username input on load
usernameInput.focus();
