const dropzone = document.getElementById('dropzone')
const fileInput = document.getElementById('file-input')
const uploadBtn = document.getElementById('upload-btn')
const resultEl = document.getElementById('result')

const pasteForm = document.getElementById('paste-form')
const pasteContent = document.getElementById('paste-content')
const pasteLang = document.getElementById('paste-lang')

// Combined-zone view elements (exist only in the combined template version)
const dzView = document.getElementById('dz-view')
const textView = document.getElementById('text-view')
const cancelTextBtn = document.getElementById('cancel-text-btn')

let pendingFiles = []
let inTextMode = false

// ---------- UI helpers ----------
function setResult (obj) {
  resultEl.textContent =
    typeof obj === 'string' ? obj : JSON.stringify(obj, null, 2)
}

function setDragover (isOver) {
  dropzone.classList.toggle('dragover', isOver)
}

function enterTextMode (opts) {
  if (inTextMode) return
  if (!dzView || !textView || !pasteContent) return

  inTextMode = true
  dzView.style.display = 'none'
  textView.style.display = 'block'

  const seedText = opts?.seedText || ''
  if (seedText) pasteContent.value = seedText

  pasteContent.focus()
  const end = pasteContent.value.length
  pasteContent.selectionStart = end
  pasteContent.selectionEnd = end
}

function exitTextMode () {
  if (!inTextMode) return
  if (!dzView || !textView) return

  inTextMode = false
  textView.style.display = 'none'
  dzView.style.display = 'block'
  if (dropzone) dropzone.focus()
}

// ---------- Network helpers ----------
async function postForm (url, form) {
  const res = await fetch(url, { method: 'POST', body: form })

  // jscpd-friendly: one shared fetch+json+error path
  let data
  try {
    data = await res.json()
  } catch {
    data = { ok: false, error: 'Invalid JSON response' }
  }

  if (!res.ok) {
    setResult({ ok: false, status: res.status, data })
    return null
  }

  return data
}

function renderSavedLinks (data) {
  if (data?.saved?.length) {
    const lines = data.saved.map((s) => `${s.original_name} -> ${s.view_url}`)
    setResult(lines.join('\n'))
    return true
  }
  return false
}

// ---------- File queue helpers ----------
function addFiles (fileList) {
  const files = Array.from(fileList || [])
  if (!files.length) return

  pendingFiles.push(...files)
  setResult(
    `Queued ${pendingFiles.length} file(s). Click "Upload selected" or drop/paste more.`
  )
}

async function uploadFiles (files) {
  const list = Array.from(files || [])
  if (!list.length) return setResult('No files queued.')

  const form = new FormData()
  for (const f of list) form.append('files', f)

  setResult('Uploading...')
  const data = await postForm('/upload', form)
  if (!data) return

  if (!renderSavedLinks(data)) setResult(data)

  pendingFiles = []
  if (fileInput) fileInput.value = ''
}

// ---------- Clipboard helpers ----------
function filesFromClipboardItems (items) {
  const files = []
  for (const item of items) {
    if (item.kind === 'file') {
      const f = item.getAsFile()
      if (f) files.push(f)
    }
  }
  return files
}

function textFromClipboardItems (items) {
  const textItems = []
  for (const item of items) {
    if (item.kind === 'string') {
      textItems.push(
        new Promise((resolve) => item.getAsString((str) => resolve(str || '')))
      )
    }
  }
  return Promise.all(textItems).then((parts) => parts.join(''))
}

async function handlePaste (e) {
  const items = e.clipboardData?.items
  if (!items) return

  const files = filesFromClipboardItems(items)

  // If files exist, treat it as file paste
  if (files.length) {
    addFiles(files)
    return
  }

  // Otherwise, try text paste
  const text = await textFromClipboardItems(items)
  if (text.trim() && pasteContent) {
    // If you are using the combined zone, switch into text mode automatically
    if (dzView && textView && !inTextMode) enterTextMode()
    pasteContent.value = text
    setResult('Pasted text into the textarea. Submit to create a link.')
  }
}

// ---------- Event wiring ----------

// File picker + button
if (fileInput) {
  fileInput.addEventListener('change', (e) => addFiles(e.target.files))
}
if (uploadBtn) uploadBtn.addEventListener('click', () => uploadFiles(pendingFiles))

// Combined-zone behavior: double click or typing switches to textarea
if (dropzone && dzView && textView && pasteContent) {
  dropzone.addEventListener('dblclick', () => enterTextMode())

  // Key typing on the dropzone switches to textarea (but NOT Cmd/Ctrl+V)
  dropzone.addEventListener('keydown', (e) => {
    if (inTextMode) {
      if (e.key === 'Escape') {
        e.preventDefault()
        exitTextMode()
      }
      return
    }

    const isPaste = (e.ctrlKey || e.metaKey) && (e.key === 'v' || e.key === 'V')
    if (isPaste) return

    // ignore navigation/modifier keys
    if (
      e.key === 'Shift' ||
      e.key === 'Control' ||
      e.key === 'Alt' ||
      e.key === 'Meta' ||
      e.key === 'Tab' ||
      e.key === 'Enter' ||
      e.key.startsWith('Arrow')
    ) {
      return
    }

    // printable char => enter text mode and seed that character
    if (e.key.length === 1) {
      e.preventDefault()
      enterTextMode({ seedText: e.key })
    }
  })

  // Esc inside textarea returns to dropzone mode
  pasteContent.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
      e.preventDefault()
      exitTextMode()
    }
  })

  if (cancelTextBtn) cancelTextBtn.addEventListener('click', exitTextMode)
}

// Drag & drop + paste (keep existing behavior)
if (dropzone) {
  dropzone.addEventListener('dragover', (e) => {
    e.preventDefault()
    setDragover(true)
  })
  dropzone.addEventListener('dragleave', () => setDragover(false))
  dropzone.addEventListener('drop', (e) => {
    e.preventDefault()
    setDragover(false)
    if (e.dataTransfer?.files?.length) addFiles(e.dataTransfer.files)
  })

  dropzone.addEventListener('paste', (e) => {
    // paste event doesn’t need preventDefault unless you want to suppress default behavior
    handlePaste(e)
  })
}

// Paste form submit
if (pasteForm) {
  pasteForm.addEventListener('submit', async (e) => {
    e.preventDefault()

    const content = (pasteContent?.value || '').trim()
    if (!content) return setResult('Paste is empty.')

    const form = new FormData()
    form.append('content', content)
    form.append('language', pasteLang?.value || 'plaintext')

    setResult('Creating paste link...')
    const data = await postForm('/paste', form)
    if (!data) return

    setResult(`Paste created:\n${data.view_url}`)
    if (pasteContent) pasteContent.value = ''

    // If you're using the combined-zone UI, pop back to drop mode after submit
    if (dzView && textView) exitTextMode()
  })
}
