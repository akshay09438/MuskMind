'use client'

import { useState, useRef, useEffect } from 'react'

// ── Types ────────────────────────────────────────────────────────────────────

type Msg = {
  id: string
  role: 'user' | 'assistant'
  content: string
}

type HistoryEntry = { role: string; content: string }

const BACKEND = process.env.NEXT_PUBLIC_BACKEND_URL ?? 'http://localhost:8000'

// ── SVG Icons ────────────────────────────────────────────────────────────────

function MindMuskMark({ size = 28 }: { size?: number }) {
  return (
    <svg width={size} height={size} viewBox="0 0 28 28" fill="none">
      <line x1="14" y1="3" x2="14" y2="25" stroke="#111" strokeWidth="2.2" strokeLinecap="round" />
      <line x1="3" y1="9" x2="25" y2="19" stroke="#111" strokeWidth="2.2" strokeLinecap="round" />
      <line x1="25" y1="9" x2="3" y2="19" stroke="#111" strokeWidth="2.2" strokeLinecap="round" />
    </svg>
  )
}

function CopyIcon() {
  return (
    <svg width="15" height="15" viewBox="0 0 15 15" fill="none">
      <rect x="4" y="4" width="9" height="9" rx="1.5" stroke="#bbb" strokeWidth="1.3" />
      <path d="M2 11V2h9" stroke="#bbb" strokeWidth="1.3" strokeLinecap="round" />
    </svg>
  )
}

function ThumbUpIcon() {
  return (
    <svg width="15" height="15" viewBox="0 0 15 15" fill="none">
      <path d="M5 7l1-4c.5-1 1.5-1 2 0V7h3c.5 0 1 .5.8 1l-1 4H4V7H2V4h3V7z" stroke="#bbb" strokeWidth="1.3" strokeLinejoin="round" />
    </svg>
  )
}

function ThumbDownIcon() {
  return (
    <svg width="15" height="15" viewBox="0 0 15 15" fill="none">
      <path d="M10 8l-1 4c-.5 1-1.5 1-2 0V8H4c-.5 0-1-.5-.8-1l1-4h6.8V8h2V11h-3V8z" stroke="#bbb" strokeWidth="1.3" strokeLinejoin="round" />
    </svg>
  )
}

function RefreshIcon() {
  return (
    <svg width="15" height="15" viewBox="0 0 15 15" fill="none">
      <path d="M2 7.5A5.5 5.5 0 0113 7.5M13 5v2.5H10.5" stroke="#bbb" strokeWidth="1.3" strokeLinecap="round" strokeLinejoin="round" />
    </svg>
  )
}

function FollowUpArrow() {
  return (
    <svg width="13" height="13" viewBox="0 0 13 13" fill="none" className="shrink-0">
      <path d="M3 4l4 4" stroke="#ccc" strokeWidth="1.3" strokeLinecap="round" />
      <path d="M3 8h4V4" stroke="#ccc" strokeWidth="1.3" strokeLinecap="round" strokeLinejoin="round" />
    </svg>
  )
}

function SendIcon() {
  return (
    <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
      <path d="M8 12V4M4 8l4-4 4 4" stroke="#fff" strokeWidth="1.6" strokeLinecap="round" strokeLinejoin="round" />
    </svg>
  )
}

// ── Sidebar ──────────────────────────────────────────────────────────────────

type SidebarProps = {
  onNewChat: () => void
  hasMessages: boolean
}

function Sidebar({ onNewChat, hasMessages }: SidebarProps) {
  const navItemClass =
    'flex items-center gap-[10px] px-3 py-[7px] rounded-[7px] cursor-pointer text-[#333] text-[14px] hover:bg-[#f2f2f2] transition-colors duration-100 select-none'

  return (
    <div
      style={{ width: 224, borderRight: '1px solid #ebebeb' }}
      className="flex flex-col shrink-0 px-2 py-[10px] h-full"
    >
      {/* Logo row */}
      <div className="flex items-center justify-between px-2 pb-[10px]">
        <MindMuskMark size={26} />
        <svg width="18" height="18" viewBox="0 0 18 18" fill="none" className="cursor-pointer">
          <path d="M11 5L7 9L11 13" stroke="#ccc" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" />
          <rect x="2" y="2" width="5" height="14" rx="2" stroke="#ccc" strokeWidth="1.3" />
        </svg>
      </div>

      {/* Nav items */}
      <div className={navItemClass}>
        <svg width="16" height="16" viewBox="0 0 16 16" fill="none" className="shrink-0 opacity-60">
          <circle cx="7" cy="7" r="5" stroke="#444" strokeWidth="1.4" />
          <path d="M11 11L14 14" stroke="#444" strokeWidth="1.4" strokeLinecap="round" />
        </svg>
        Search
      </div>

      <div className={navItemClass} onClick={onNewChat} role="button">
        <svg width="16" height="16" viewBox="0 0 16 16" fill="none" className="shrink-0 opacity-60">
          <path d="M2 3h12v8H9l-3 3V11H2V3z" stroke="#444" strokeWidth="1.4" strokeLinejoin="round" />
        </svg>
        New Chat
      </div>

      {/* History */}
      <div className="mt-[10px]">
        <div className={navItemClass + ' justify-between'}>
          <span>History</span>
          <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
            <path d="M3 5l4 4 4-4" stroke="#bbb" strokeWidth="1.4" strokeLinecap="round" />
          </svg>
        </div>
      </div>

      {hasMessages && (
        <>
          <div className="px-3 pt-[6px] pb-[2px] text-[12px] text-[#aaa]">Today</div>
          <div
            className="px-3 py-[6px] text-[13px] text-[#111] rounded-[7px] bg-[#f0f0f0] cursor-pointer truncate"
            title="Current conversation"
          >
            Current conversation
          </div>
        </>
      )}

      {!hasMessages && (
        <>
          <div className="px-3 pt-[6px] pb-[2px] text-[12px] text-[#aaa]">Earlier</div>
          {['How rockets get cheap', 'AI and consciousness', "Elon's hiring framework"].map(
            (title) => (
              <div
                key={title}
                className="px-3 py-[6px] text-[13px] text-[#555] rounded-[7px] cursor-pointer hover:bg-[#f2f2f2] truncate"
              >
                {title}
              </div>
            ),
          )}
          <div className="px-3 py-[6px]">
            <span className="text-[13px] text-[#aaa] cursor-pointer">See all</span>
          </div>
        </>
      )}

      <div className="flex-1" />

      {/* User profile */}
      <div
        style={{ borderTop: '1px solid #ebebeb' }}
        className="flex items-center gap-[9px] px-[10px] py-[10px] mt-1"
      >
        <div className="w-[30px] h-[30px] rounded-full bg-[#e85d00] flex items-center justify-center shrink-0">
          <span className="text-white text-[13px] font-semibold">A</span>
        </div>
        <div className="min-w-0">
          <div className="text-[#111] text-[13px] font-medium truncate">Akshay bansal</div>
          <div className="text-[#aaa] text-[11px] truncate">akshay.bansal987@gmail.com</div>
        </div>
      </div>
    </div>
  )
}

// ── Action Icon Button ───────────────────────────────────────────────────────

function IconBtn({ children, title, onClick }: { children: React.ReactNode; title?: string; onClick?: () => void }) {
  return (
    <button
      className="p-[5px] rounded-[5px] cursor-pointer hover:bg-[#f5f5f5] transition-colors"
      title={title}
      onClick={onClick}
    >
      {children}
    </button>
  )
}

// ── Minimal markdown renderer (bold + bullets, no library) ──────────────────

function renderInline(text: string, keyPrefix: string): React.ReactNode[] {
  const parts = text.split(/(\*\*[^*]+\*\*)/g).filter((p) => p !== '')
  return parts.map((part, i) =>
    part.startsWith('**') && part.endsWith('**') ? (
      <strong key={`${keyPrefix}-${i}`} className="font-semibold text-[#111]">
        {part.slice(2, -2)}
      </strong>
    ) : (
      <span key={`${keyPrefix}-${i}`}>{part}</span>
    ),
  )
}

type LineKind = 'h2' | 'h3' | 'bullet' | 'body'

function classifyLine(rawLine: string): { kind: LineKind; text: string } {
  const trimmed = rawLine.trim()
  if (trimmed.startsWith('## ')) return { kind: 'h2', text: trimmed.slice(3) }
  if (trimmed.startsWith('### ')) return { kind: 'h3', text: trimmed.slice(4) }
  if (trimmed.startsWith('- ') || trimmed.startsWith('• ')) return { kind: 'bullet', text: trimmed.slice(2) }
  return { kind: 'body', text: rawLine }
}

const LINE_STYLES: Record<LineKind, string> = {
  h2: 'text-[17px] font-semibold text-[#111] leading-[1.4] mb-[6px]',
  h3: 'text-[15.5px] font-semibold text-[#111] leading-[1.5] mb-[3px]',
  bullet: 'flex gap-2 text-[14.5px] text-[#333] leading-[1.6]',
  body: 'text-[14.5px] text-[#333] leading-[1.6]',
}

function MarkdownBlock({ text }: { text: string }) {
  const blocks = text.split('\n\n').filter(Boolean)

  return (
    <>
      {blocks.map((block, bi) => {
        const lines = block.split('\n').filter(Boolean)
        const classified = lines.map(classifyLine)
        // A block with exactly one plain body line gets extra breathing
        // room, reproducing the reference transcript's staccato pacing
        // for isolated one-line punch statements.
        const isPunchLine = classified.length === 1 && classified[0].kind === 'body'

        return (
          <div key={bi} className={isPunchLine ? 'mb-5 last:mb-0' : 'mb-4 last:mb-0'}>
            {classified.map(({ kind, text: lineText }, li) => {
              const isVeryFirstLine = bi === 0 && li === 0
              const topMargin = isVeryFirstLine
                ? ''
                : kind === 'h2'
                  ? 'mt-4'
                  : kind === 'h3'
                    ? 'mt-3'
                    : ''
              return (
                <div key={li} className={`${LINE_STYLES[kind]} ${topMargin}`}>
                  {kind === 'bullet' && <span className="text-[#bbb] shrink-0">•</span>}
                  <span>{renderInline(lineText, `${bi}-${li}`)}</span>
                </div>
              )
            })}
          </div>
        )
      })}
    </>
  )
}

// ── Message ──────────────────────────────────────────────────────────────────

function UserMessage({ content }: { content: string }) {
  return (
    <div className="flex justify-end">
      <div
        style={{ background: '#f0f0f0', borderRadius: 20, maxWidth: '60%' }}
        className="px-[18px] py-[10px] text-[15px] text-[#111]"
      >
        {content}
      </div>
    </div>
  )
}

function AssistantMessage({
  content,
  isStreaming,
  onCopy,
}: {
  content: string
  isStreaming: boolean
  onCopy: () => void
}) {
  return (
    <div className="flex flex-col gap-[10px]">
      {/* Response text */}
      <div className={`text-[15px] text-[#111] ${isStreaming && !content ? 'streaming-cursor' : ''}`}>
        {content ? (
          <>
            <MarkdownBlock text={content} />
            {isStreaming && <span className="streaming-cursor" />}
          </>
        ) : (
          isStreaming && <span className="streaming-cursor" />
        )}
      </div>

      {/* Action icons — shown when not streaming */}
      {!isStreaming && content && (
        <>
          <div className="flex items-center gap-1 mt-[2px]">
            <IconBtn title="Copy" onClick={onCopy}><CopyIcon /></IconBtn>
            <IconBtn title="Like"><ThumbUpIcon /></IconBtn>
            <IconBtn title="Dislike"><ThumbDownIcon /></IconBtn>
            <IconBtn title="Regenerate"><RefreshIcon /></IconBtn>
          </div>

          {/* Suggested follow-ups */}
          <div className="flex flex-col gap-[6px] mt-1">
            {['Dig deeper on this', 'Take it to first principles', 'What would you do?'].map(
              (q) => (
                <div key={q} className="flex items-center gap-2 cursor-pointer py-1 group">
                  <FollowUpArrow />
                  <span className="text-[13px] text-[#bbb] group-hover:text-[#888] transition-colors">
                    {q}
                  </span>
                </div>
              ),
            )}
          </div>
        </>
      )}
    </div>
  )
}

// ── Empty State ──────────────────────────────────────────────────────────────

function EmptyState() {
  return (
    <div className="flex flex-col items-center justify-center h-full gap-6 select-none">
      <MindMuskMark size={48} />
      <div className="text-[16px] text-[#aaa] text-center leading-relaxed">
        Ask Elon anything.<br />
        <span className="text-[13px] text-[#ccc]">First Principles Engine · 5 Layers Active</span>
      </div>
    </div>
  )
}

// ── Main Page ────────────────────────────────────────────────────────────────

export default function Home() {
  const [messages, setMessages] = useState<Msg[]>([])
  const [history, setHistory] = useState<HistoryEntry[]>([])
  const [input, setInput] = useState('')
  const [streaming, setStreaming] = useState(false)
  const [streamingId, setStreamingId] = useState<string | null>(null)
  const bottomRef = useRef<HTMLDivElement>(null)
  const inputRef = useRef<HTMLInputElement>(null)

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  function newChat() {
    setMessages([])
    setHistory([])
    setInput('')
    inputRef.current?.focus()
  }

  async function send() {
    const text = input.trim()
    if (!text || streaming) return

    const userId = crypto.randomUUID()
    const assistantId = crypto.randomUUID()

    setMessages((prev) => [
      ...prev,
      { id: userId, role: 'user', content: text },
      { id: assistantId, role: 'assistant', content: '' },
    ])
    setInput('')
    setStreamingId(assistantId)
    setStreaming(true)

    let fullContent = ''

    try {
      const res = await fetch(`${BACKEND}/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: text, history }),
      })

      if (!res.ok || !res.body) throw new Error(`HTTP ${res.status}`)

      const reader = res.body.getReader()
      const decoder = new TextDecoder()
      let buffer = ''

      while (true) {
        const { done, value } = await reader.read()
        if (done) break

        buffer += decoder.decode(value, { stream: true })
        const lines = buffer.split('\n')
        buffer = lines.pop() ?? ''

        for (const line of lines) {
          if (!line.startsWith('data: ')) continue
          const data = line.slice(6)
          if (data === '[DONE]') continue
          // Backend JSON-encodes each chunk so embedded newlines survive
          // SSE framing intact — decode it back to raw text here.
          let chunk: string
          try {
            chunk = JSON.parse(data)
          } catch {
            chunk = data
          }
          fullContent += chunk
          setMessages((prev) =>
            prev.map((m) => (m.id === assistantId ? { ...m, content: fullContent } : m)),
          )
        }
      }

      setHistory((prev) => [
        ...prev,
        { role: 'user', content: text },
        { role: 'assistant', content: fullContent },
      ])
    } catch (err) {
      const errMsg =
        err instanceof Error && err.message.includes('fetch')
          ? 'Cannot reach backend. Start the FastAPI server on port 8000.'
          : 'Something went wrong. Please try again.'
      setMessages((prev) =>
        prev.map((m) => (m.id === assistantId ? { ...m, content: errMsg } : m)),
      )
    } finally {
      setStreaming(false)
      setStreamingId(null)
    }
  }

  function copyMessage(content: string) {
    navigator.clipboard.writeText(content).catch(() => {})
  }

  return (
    <div className="flex h-screen overflow-hidden bg-white">
      {/* Sidebar */}
      <Sidebar onNewChat={newChat} hasMessages={messages.length > 0} />

      {/* Main */}
      <div className="flex-1 flex flex-col relative">
        {/* Top right controls */}
        <div className="absolute top-[14px] right-5 flex gap-3 items-center z-10">
          <svg width="18" height="18" viewBox="0 0 18 18" fill="none" className="cursor-pointer">
            <circle cx="4" cy="9" r="1.5" fill="#ddd" />
            <circle cx="9" cy="9" r="1.5" fill="#ddd" />
            <circle cx="14" cy="9" r="1.5" fill="#ddd" />
          </svg>
          <svg width="18" height="18" viewBox="0 0 18 18" fill="none" className="cursor-pointer">
            <path d="M5 13L13 5M13 5H8M13 5V10" stroke="#ddd" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" />
          </svg>
        </div>

        {/* Messages */}
        <div className="flex-1 overflow-y-auto pb-[160px] pt-10" style={{ scrollbarWidth: 'thin', scrollbarColor: '#eee transparent' }}>
          {messages.length === 0 ? (
            <EmptyState />
          ) : (
            <div className="flex flex-col gap-6 mx-auto px-6" style={{ maxWidth: 700 }}>
              {messages.map((m) =>
                m.role === 'user' ? (
                  <UserMessage key={m.id} content={m.content} />
                ) : (
                  <AssistantMessage
                    key={m.id}
                    content={m.content}
                    isStreaming={m.id === streamingId}
                    onCopy={() => copyMessage(m.content)}
                  />
                ),
              )}
              <div ref={bottomRef} />
            </div>
          )}
        </div>

        {/* Floating asterisk watermark */}
        <div className="absolute bottom-[100px] right-7 pointer-events-none opacity-[0.07]">
          <MindMuskMark size={40} />
        </div>

        {/* Input bar */}
        <div className="absolute bottom-0 left-0 right-0 px-6 pb-6 pt-4 flex justify-center">
          <div className="w-full" style={{ maxWidth: 700 }}>
            <div
              style={{ border: '1.5px solid #ddd', borderRadius: 999, boxShadow: '0 2px 12px rgba(0,0,0,.06)' }}
              className="flex items-center gap-[10px] px-4 py-3 bg-white"
            >
              {/* + button */}
              <svg width="16" height="16" viewBox="0 0 16 16" fill="none" className="shrink-0 cursor-pointer">
                <path d="M3 8h10M8 3v10" stroke="#ccc" strokeWidth="1.5" strokeLinecap="round" />
              </svg>

              <input
                ref={inputRef}
                type="text"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={(e) => {
                  if (e.key === 'Enter' && !e.shiftKey) {
                    e.preventDefault()
                    send()
                  }
                }}
                placeholder="Ask anything"
                className="flex-1 border-none outline-none text-[15px] text-[#111] bg-transparent placeholder:text-[#ccc]"
              />

              <div className="flex items-center gap-[10px] shrink-0">
                <span className="text-[13px] text-[#aaa] flex items-center gap-[3px] cursor-pointer select-none">
                  Fast
                  <svg width="12" height="12" viewBox="0 0 12 12" fill="none">
                    <path d="M3 4.5l3 3 3-3" stroke="#bbb" strokeWidth="1.3" strokeLinecap="round" />
                  </svg>
                </span>

                {/* Mic */}
                <svg width="18" height="18" viewBox="0 0 18 18" fill="none" className="cursor-pointer opacity-40">
                  <rect x="6" y="2" width="6" height="9" rx="3" stroke="#555" strokeWidth="1.3" />
                  <path d="M3 9a6 6 0 0012 0M9 15v2" stroke="#555" strokeWidth="1.3" strokeLinecap="round" />
                </svg>

                {/* Send */}
                <button
                  onClick={send}
                  disabled={!input.trim() || streaming}
                  className="w-8 h-8 rounded-full bg-[#111] flex items-center justify-center cursor-pointer disabled:opacity-30 transition-opacity hover:opacity-80"
                >
                  <SendIcon />
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
