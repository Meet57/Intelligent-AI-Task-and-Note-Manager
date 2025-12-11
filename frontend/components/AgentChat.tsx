"use client";

import React, { useState } from "react";
import { agentService } from "../utils/api";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

interface Message {
  type: "human" | "ai" | "tool" | "system";
  content: string;
  name?: string;
  tool_calls?: any[];
}

interface AgentChatProps {
  onMessage?: (message: string, messages: Message[]) => void;
}

export default function AgentChat({ onMessage }: AgentChatProps) {
  const [message, setMessage] = useState("");
  const [messages, setMessages] = useState<Message[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSend = async () => {
    if (!message.trim()) {
      setError("Please enter a message");
      return;
    }

    setLoading(true);
    setError("");

    const userMsg: Message = { type: "human", content: message };

    // Add user message locally
    setMessages((prev) => [...prev, userMsg]);

    try {
      const result = await agentService.send(message);

      // Append ONLY new messages returned from backend
      const newMessages = result.messages.filter(
        (msg: Message) => !(msg.type === "human" && msg.content === message)
      );

      setMessages((prev) => [...prev, ...newMessages]);

      if (onMessage) {
        onMessage(message, result.messages);
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : "Something went wrong");
    } finally {
      setLoading(false);
      setMessage("");
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const bubbleColor = {
    human: "bg-blue-600 text-white",
    ai: "bg-gray-200 text-black",
    tool: "bg-yellow-100 text-black border border-yellow-300",
    system: "bg-purple-100 text-black border border-purple-300",
  };

  return (
    <div className="space-y-4 text-black">
      <div className="p-6 rounded-md flex flex-col h-[600px] text-black">
        {/* Messages */}
        <div className="grow overflow-y-auto space-y-4 pr-2">
          {messages.map((msg, idx) => (
            <div
              key={idx}
              className={`flex ${
                msg.type === "human" ? "justify-end" : "justify-start"
              }`}
            >
              <div className="text-black">
                <div className="text-xs text-black mb-1 ml-1 font-medium">
                  {msg.type === "human" && "You"}
                  {msg.type === "ai" && "AI Assistant"}
                  {msg.type === "tool" && `Tool: ${msg.name}`}
                  {msg.type === "system" && "System"}
                </div>

                {/* Message bubble */}
                <div
                  className={`max-w-xs md:max-w-md lg:max-w-lg px-3 py-2 rounded-2xl overflow-x-auto shadow-sm text-black ${
                    bubbleColor[msg.type]
                  }`}
                >
                  {msg.tool_calls &&
                    msg.tool_calls.map((call, i) => (
                      <div key={i} className="font-medium">
                        🛠️ {call.name}
                      </div>
                    ))}

                  {msg.type === "tool" ? (
                    <pre className="p-2 rounded text-sm overflow-x-auto">{msg.content}</pre>
                  ) : (
                    <ReactMarkdown remarkPlugins={[remarkGfm]}>
                      {msg.content}
                    </ReactMarkdown>
                  )}
                </div>

                {/* Debug */}
                <details className="mt-1 text-xs text-black">
                  <summary className="cursor-pointer text-gray-600">
                    debug
                  </summary>
                  <pre className="text-[10px] bg-gray-50 border p-2 rounded">
                    {JSON.stringify(msg, null, 2)}
                  </pre>
                </details>
              </div>
            </div>
          ))}

          {loading && (
            <div className="flex justify-start">
              <div className="bg-gray-200 px-4 py-2 rounded-2xl animate-pulse">
                Thinking…
              </div>
            </div>
          )}
        </div>

        {/* Input Bar */}
        <div className="mt-4">
          <textarea
            id="message"
            value={message}
            disabled={loading}
            onChange={(e) => setMessage(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Type your message..."
            rows={2}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500"
          />

          <button
            onClick={handleSend}
            disabled={loading || !message.trim()}
            className="w-full mt-2 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-300 text-white px-4 py-2 rounded-md font-medium transition"
          >
            {loading ? "Thinking..." : "Send"}
          </button>
        </div>

        {error && (
          <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-2 rounded mt-3">
            {error}
          </div>
        )}
      </div>
    </div>
  );
}
