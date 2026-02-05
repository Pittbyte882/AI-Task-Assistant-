"use client"

import { useState } from "react"
import { Send, Loader2, CheckCircle } from "lucide-react"

interface Message {
  role: "user" | "assistant"
  content: string
  actions?: string[]
}

export default function Home() {
  const [messages, setMessages] = useState<Message[]>([])
  const [input, setInput] = useState("")
  const [loading, setLoading] = useState(false)
  const [conversationId, setConversationId] = useState<string | null>(null)

  const sendMessage = async () => {
    if (!input.trim() || loading) return

    const userMessage: Message = { role: "user", content: input }
    setMessages(prev => [...prev, userMessage])
    setInput("")
    setLoading(true)

    try {
      const response = await fetch("ai-task-assistant-production-3c00.up.railway.app", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          message: input,
          user_id: "demo-user",
          conversation_id: conversationId
        })
      })

      const data = await response.json()
      
      if (!conversationId) {
        setConversationId(data.conversation_id)
      }

      const assistantMessage: Message = {
        role: "assistant",
        content: data.response,
        actions: data.actions_taken
      }
      
      setMessages(prev => [...prev, assistantMessage])
    } catch (error) {
      console.error("Error:", error)
      setMessages(prev => [...prev, {
        role: "assistant",
        content: "Sorry, there was an error processing your request."
      }])
    } finally {
      setLoading(false)
    }
  }

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault()
      sendMessage()
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-950 via-slate-900 to-slate-950 flex items-center justify-center p-4">
      <div className="w-full max-w-4xl h-[800px] bg-slate-900/50 backdrop-blur-sm border border-cyan-500/20 rounded-2xl shadow-2xl flex flex-col">
        
        {/* Header */}
        <div className="p-6 border-b border-cyan-500/20">
          <h1 className="text-2xl font-bold bg-gradient-to-r from-cyan-400 to-blue-500 bg-clip-text text-transparent">
            AI Task Assistant
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            Your intelligent task management companion
          </p>
        </div>

        {/* Messages Area */}
        <div className="flex-1 overflow-y-auto p-6 space-y-4">
          {messages.length === 0 && (
            <div className="text-center text-slate-400 mt-20">
              <div className="text-6xl mb-4">🤖</div>
              <h2 className="text-xl font-semibold mb-2">Welcome to AI Task Assistant</h2>
              <p className="text-sm">Try saying:</p>
              <div className="mt-4 space-y-2">
                <div className="text-cyan-400">"Create a task to buy groceries"</div>
                <div className="text-cyan-400">"Show me my tasks"</div>
                <div className="text-cyan-400">"Mark task as complete"</div>
              </div>
            </div>
          )}

          {messages.map((message, index) => (
            <div
              key={index}
              className={`flex ${message.role === "user" ? "justify-end" : "justify-start"}`}
            >
              <div
                className={`max-w-[80%] rounded-2xl p-4 ${
                  message.role === "user"
                    ? "bg-gradient-to-r from-cyan-500 to-blue-500 text-white"
                    : "bg-slate-800 text-slate-100 border border-cyan-500/20"
                }`}
              >
                <p className="whitespace-pre-wrap">{message.content}</p>
                
                {message.actions && message.actions.length > 0 && (
                  <div className="mt-3 pt-3 border-t border-cyan-500/20">
                    <p className="text-xs text-cyan-400 font-semibold mb-2">Actions Taken:</p>
                    {message.actions.map((action, i) => (
                      <div key={i} className="flex items-center gap-2 text-xs text-slate-300">
                        <CheckCircle className="h-3 w-3 text-green-400" />
                        {action}
                      </div>
                    ))}
                  </div>
                )}
              </div>
            </div>
          ))}

          {loading && (
            <div className="flex justify-start">
              <div className="bg-slate-800 border border-cyan-500/20 rounded-2xl p-4">
                <Loader2 className="h-5 w-5 text-cyan-400 animate-spin" />
              </div>
            </div>
          )}
        </div>

        {/* Input Area */}
        <div className="p-6 border-t border-cyan-500/20">
          <div className="flex gap-3">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Type your message..."
              className="flex-1 bg-slate-800 border border-cyan-500/20 rounded-xl px-4 py-3 text-white placeholder-slate-400 focus:outline-none focus:border-cyan-500 transition-colors"
              disabled={loading}
            />
            <button
              onClick={sendMessage}
              disabled={loading || !input.trim()}
              className="px-6 py-3 bg-gradient-to-r from-cyan-500 to-blue-500 text-white rounded-xl font-semibold hover:shadow-lg hover:shadow-cyan-500/50 transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
            >
              {loading ? (
                <Loader2 className="h-5 w-5 animate-spin" />
              ) : (
                <>
                  <Send className="h-5 w-5" />
                  Send
                </>
              )}
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}