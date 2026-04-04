const dropzone = document.getElementById("dropzone");
const fileInput = document.getElementById("fileInput");
const uploadBtn  = document.getElementById("uploadBtn");
const resultEl   = document.getElementById("result");

let pendingFiles = []; // accumulate files from all sources

function setResult(obj) {
  resultEl.textContent = typeof obj === "string" ? obj : JSON.stringify(obj, null, 2);
}

function addFiles(files) {
  for (const f of files) pendingFiles.push(f);
  setResult(`Queued ${pendingFiles.length} file(s). Click "Upload selected" or drop/paste more.`);
}

async function uploadFiles(files) {
  if (!files.length) return setResult("No files queued.");

  const form = new FormData();
  for (const f of files) form.append("files", f);

  setResult("Uploading...");

  const res = await fetch("/upload", { method: "POST", body: form });
  const data = await res.json();

  if (!res.ok) {
    setResult({ ok: false, status: res.status, data });
    return;
  }

  // v1: setResult(data);
  if (data?.saved?.length) {
    const lines = data.saved.map(s => `${s.original_name} -> ${s.view_url}`);
    setResult(lines.join("\n"));
  } else {
    setResult(data);
  }

  pendingFiles = [];
  fileInput.value = "";
}

// File picker
fileInput.addEventListener("change", (e) => addFiles(e.target.files));
uploadBtn.addEventListener("click", () => uploadFiles(pendingFiles));

// Drag & drop
dropzone.addEventListener("dragover", (e) => {
  e.preventDefault();
  dropzone.classList.add("dragover");
});
dropzone.addEventListener("dragleave", () => dropzone.classList.remove("dragover"));
dropzone.addEventListener("drop", (e) => {
  e.preventDefault();
  dropzone.classList.remove("dragover");
  if (e.dataTransfer?.files?.length) addFiles(e.dataTransfer.files);
});

// // Paste from clipboard
// dropzone.addEventListener("paste", (e) => {
//   const items = e.clipboardData?.items;
//   if (!items) return;
//
//   const files = [];
//   for (const item of items) {
//     // Files and images often appear here
//     if (item.kind === "file") {
//       const f = item.getAsFile();
//       if (f) files.push(f);
//     }
//   }
//
//   if (files.length) addFiles(files);
// });

// Paste from clipboard
dropzone.addEventListener("paste", (e) => {
  const items = e.clipboardData?.items;
  if (!items) return;

  const files = [];
  let textContent = "";

  for (const item of items) {
    if (item.kind === "file") {
      // Handle file items
      const f = item.getAsFile();
      if (f) files.push(f);
    } else if (item.kind === "string") {
      alert("Paste string!!!");
      // Handle string items
   item.getAsString((str) => {
        textContent += str;
        document.getElementById("foo").value = textContent;
      });
    } else {
      alert("Unknown paste");
    }
  }

  if (files.length) {
    addFiles(files);
  } else if (textContent) {
    document.getElementById("foo").value = textContent;
  }
});


const pasteForm = document.getElementById("pasteForm");
const pasteContent = document.getElementById("pasteContent");
const pasteLang = document.getElementById("pasteLang");

if (pasteForm) {
  pasteForm.addEventListener("submit", async (e) => {
    e.preventDefault();

    const content = pasteContent.value || "";
    if (!content.trim()) {
      setResult("Paste is empty.");
      return;
    }

    const form = new FormData();
    form.append("content", content);
    form.append("language", pasteLang?.value || "plaintext");

    setResult("Creating paste link...");

    const res = await fetch("/paste", { method: "POST", body: form });
    const data = await res.json();

    if (!res.ok) {
      setResult({ ok: false, status: res.status, data });
      return;
    }

    // Show link + clear textarea
    setResult(`Paste created:\n${data.view_url}`);
    pasteContent.value = "";
  });
}

