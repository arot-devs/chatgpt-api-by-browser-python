// ==UserScript==
// @name         ChatGPT API By Browser Script with Python Backend Reverse Control
// @namespace    http://tampermonkey.net/
// @version      2.0
// @match        https://chatgpt.com/*
// @icon         https://www.google.com/s2/favicons?sz=64&domain=openai.com
// @grant        none
// @license      MIT
// ==/UserScript==

(function () {
  'use strict';

  const log = (...args) => console.log('[ChatGPT-API-Script]', ...args);
  const WS_URL = 'ws://localhost:8765';

  class ChatScript {
    constructor() {
      this.socket = null;
      this.textInput = null;
      this.lastText = null;
      this.observer = null;
    }

    connectSocket() {
      this.socket = new WebSocket(WS_URL);

      this.socket.onopen = () => {
        log('Connected to backend.');
      };

      this.socket.onmessage = (event) => {
        const data = JSON.parse(event.data);
        log('Message received from backend:', data);

        if (data.type === 'message') {
          this.sendMessage(data.text);
        }
      };

      this.socket.onclose = () => {
        log('Disconnected from backend. Retrying...');
        setTimeout(() => this.connectSocket(), 2000);
      };

      this.socket.onerror = (err) => {
        log('WebSocket error:', err);
      };
    }

    sendMessageToBackend(message) {
      if (this.socket && this.socket.readyState === WebSocket.OPEN) {
        this.socket.send(JSON.stringify({ type: 'response', content: message }));
        log('Response sent to backend:', message);
      } else {
        log('WebSocket is not open. Response not sent.');
      }
    }

    sendMessage(text) {
      log('Sending message:', text);
      const promptTextarea = document.querySelector('#prompt-textarea');
      if (!promptTextarea) {
        log('Error: Unable to find the input box.');
        return;
      }

      promptTextarea.innerHTML = `<p>${text}</p>`;
      promptTextarea.dispatchEvent(new Event('input', { bubbles: true }));

      setTimeout(() => {
        const enterEvent = new KeyboardEvent('keydown', {
          key: 'Enter',
          code: 'Enter',
          bubbles: true,
          cancelable: true,
        });
        promptTextarea.dispatchEvent(enterEvent);
        log('Message submitted.');

        this.observeResponse();
      }, 50);
    }

    observeResponse() {
      if (this.observer) this.observer.disconnect();

      this.observer = new MutationObserver(() => {
        const messages = [...document.querySelectorAll('div.agent-turn')];
        const lastMessage = messages[messages.length - 1];
        if (!lastMessage) return;

        const assistantText = this.getTextFromNode(
          lastMessage.querySelector('div[data-message-author-role="assistant"]')
        );

        if (assistantText && assistantText !== this.lastText) {
          this.lastText = assistantText;
          log('Assistant response:', assistantText);

          // Send response to backend
          this.sendMessageToBackend(assistantText);
        }
      });

      this.observer.observe(document.body, {
        childList: true,
        subtree: true,
        characterData: true,
      });
    }

    getTextFromNode(node) {
      if (!node) return '';
      return [...node.childNodes].map((child) => child.textContent).join('');
    }

    init() {
      this.connectSocket();
    }
  }

  const app = new ChatScript();
  app.init();
})();
