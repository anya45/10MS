import os
import subprocess
from flask import Flask, request, jsonify

app = Flask(__name__)

HTML_PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>10MS Class Merger &amp; Downloader</title>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@tabler/icons-webfont@3.19.0/tabler-icons.min.css">
<style>
  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
  :root {
    --bg: #f5f5f3; --surface: #ffffff; --surface-1: #f9f9f8; --surface-0: #f0efec;
    --border: rgba(0,0,0,0.10); --border-strong: rgba(0,0,0,0.18); --border-stronger: rgba(0,0,0,0.28);
    --text-primary: #1a1a18; --text-secondary: #4a4a46; --text-muted: #888782;
    --text-accent: #185fa5; --text-success: #3b6d11; --text-danger: #a32d2d;
    --bg-accent: #e6f1fb; --bg-success: #eaf3de; --bg-danger: #fcebeb;
    --border-accent: #85b7eb; --border-success: #97c459; --border-danger: #f09595;
    --fill-accent: #378add; --on-accent: #ffffff; --radius: 8px;
    --font-sans: -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif;
  }
  @media (prefers-color-scheme: dark) {
    :root {
      --bg: #1a1a18; --surface: #242421; --surface-1: #2c2c29; --surface-0: #1e1e1c;
      --border: rgba(255,255,255,0.10); --border-strong: rgba(255,255,255,0.18); --border-stronger: rgba(255,255,255,0.28);
      --text-primary: #f0efec; --text-secondary: #b4b2a9; --text-muted: #6b6a65;
      --text-accent: #85b7eb; --text-success: #97c459; --text-danger: #f09595;
      --bg-accent: #042c53; --bg-success: #173404; --bg-danger: #501313;
      --border-accent: #185fa5; --border-success: #3b6d11; --border-danger: #a32d2d;
      --fill-accent: #378add;
    }
  }
  body { font-family: var(--font-sans); background: var(--bg); color: var(--text-primary); min-height: 100vh; display: flex; align-items: flex-start; justify-content: center; padding: 2rem 1rem; }
  .container { width: 100%; max-width: 600px; }
  .header { margin-bottom: 2rem; }
  .header-title { display: flex; align-items: center; gap: 10px; font-size: 20px; font-weight: 500; color: var(--text-primary); margin-bottom: 4px; }
  .header-title i { font-size: 22px; color: var(--fill-accent); }
  .header-sub { font-size: 13px; color: var(--text-muted); margin-left: 32px; }
  .card { background: var(--surface); border: 0.5px solid var(--border); border-radius: 16px; overflow: hidden; }
  .tabs { display: flex; border-bottom: 0.5px solid var(--border); background: var(--surface-1); }
  .tab-btn { flex: 1; padding: 12px 16px; background: none; border: none; border-bottom: 2px solid transparent; font-size: 13px; font-weight: 500; cursor: pointer; color: var(--text-muted); transition: color 0.15s, border-color 0.15s; display: flex; align-items: center; justify-content: center; gap: 6px; }
  .tab-btn.active { color: var(--text-accent); border-bottom-color: var(--fill-accent); background: var(--surface); }
  .tab-btn i { font-size: 15px; }
  .panel { padding: 1.25rem; }
  .drop-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-bottom: 1rem; }
  .drop-zone { border: 1.5px dashed var(--border-stronger); border-radius: 12px; padding: 24px 12px; text-align: center; cursor: pointer; background: var(--surface-1); transition: background 0.15s, border-color 0.15s; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 5px; min-height: 110px; }
  .drop-zone:hover { background: var(--bg-accent); border-color: var(--border-accent); }
  .drop-zone i { font-size: 28px; color: var(--text-muted); }
  .drop-zone .zone-label { font-size: 13px; font-weight: 500; color: var(--text-secondary); }
  .drop-zone .zone-sub { font-size: 11px; color: var(--text-muted); }
  .drop-zone .zone-file { font-size: 11px; color: var(--text-accent); max-width: 100%; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; padding: 0 4px; }
  .drop-zone.active { background: var(--bg-accent); border-color: var(--border-accent); border-style: solid; }
  .drop-zone.active i, .drop-zone.active .zone-label { color: var(--text-accent); }

  .name-row { display: flex; gap: 8px; align-items: center; margin-bottom: 1rem; }
  .name-row input { flex: 1; height: 38px; border-radius: var(--radius); border: 0.5px solid var(--border-strong); background: var(--surface-1); color: var(--text-primary); padding: 0 12px; font-size: 13px; outline: none; transition: border-color 0.15s; }
  .name-row input:focus { border-color: var(--fill-accent); }
  .name-row input::placeholder { color: var(--text-muted); }
  .ext-badge { font-size: 12px; font-weight: 500; color: var(--text-accent); background: var(--bg-accent); border: 0.5px solid var(--border-accent); border-radius: var(--radius); padding: 0 10px; height: 38px; display: flex; align-items: center; }

  .primary-btn { width: 100%; height: 44px; border-radius: var(--radius); background: var(--fill-accent); color: var(--on-accent); border: none; font-size: 15px; font-weight: 500; cursor: not-allowed; opacity: 0.4; display: flex; align-items: center; justify-content: center; gap: 8px; transition: opacity 0.15s, transform 0.1s; }
  .primary-btn:not(:disabled) { cursor: pointer; opacity: 1; }
  .primary-btn:not(:disabled):hover { opacity: 0.9; }
  .primary-btn:not(:disabled):active { transform: scale(0.99); }

  .progress-wrap { margin-top: 10px; height: 4px; background: var(--surface-0); border-radius: 99px; overflow: hidden; display: none; }
  .progress-bar { height: 100%; background: var(--fill-accent); width: 0%; transition: width 0.3s; }
  .status-box { display: none; margin-top: 12px; padding: 10px 14px; border-radius: var(--radius); font-size: 13px; line-height: 1.5; }
  .hint { font-size: 12px; color: var(--text-muted); margin-top: 10px; line-height: 1.6; display: flex; align-items: flex-start; gap: 5px; }
  .hint i { font-size: 13px; flex-shrink: 0; margin-top: 1px; }
  .link-input-box { display: flex; flex-direction: column; gap: 6px; }
  .link-box-label { font-size: 12px; font-weight: 500; color: var(--text-secondary); display: flex; align-items: center; gap: 5px; }
  .link-box-label i { font-size: 13px; color: var(--fill-accent); }
  .link-input-box input { width: 100%; height: 38px; border-radius: var(--radius); border: 0.5px solid var(--border-strong); background: var(--surface-1); color: var(--text-primary); padding: 0 12px; font-size: 12px; outline: none; transition: border-color 0.15s; }
  .link-input-box input:focus { border-color: var(--fill-accent); }
  .link-input-box input::placeholder { color: var(--text-muted); font-size: 11px; }
  .cv-select { flex: 1; height: 38px; border-radius: var(--radius); border: 0.5px solid var(--border-strong); background: var(--surface-1); color: var(--text-primary); padding: 0 10px; font-size: 13px; font-family: var(--font-sans); outline: none; cursor: pointer; transition: border-color 0.15s; }
  .cv-select:focus { border-color: var(--fill-accent); }
</style>
</head>
<body>
<div class="container">
  <div class="header">
    <div class="header-title"><i class="ti ti-device-desktop-down"></i>10MS Class Merger &amp; Downloader</div>
    <div class="header-sub">Merge video and audio, download from an m3u8 link, or convert a video file.</div>
  </div>
  <div class="card">
    <div class="tabs">
      <button id="tab-merge-btn" class="tab-btn active" onclick="switchTab('merge')"><i class="ti ti-arrows-join"></i> Drop &amp; Merge</button>
      <button id="tab-dl-btn" class="tab-btn" onclick="switchTab('dl')"><i class="ti ti-cloud-download"></i> Link Download</button>
      <button id="tab-lm-btn" class="tab-btn" onclick="switchTab('lm')"><i class="ti ti-link"></i> Link Merge</button>
      <button id="tab-cv-btn" class="tab-btn" onclick="switchTab('cv')"><i class="ti ti-refresh"></i> Convert</button>
    </div>

    <!-- Drop & Merge Panel -->
    <div id="panel-merge" class="panel">
      <div class="drop-grid">
        <div id="zone-v" class="drop-zone" onclick="document.getElementById('inp-v').click()" ondragover="ev(event,'v')" ondragleave="el('v')" ondrop="ed(event,'v')">
          <input id="inp-v" type="file" accept="video/*,.mp4" onchange="fi(event,'v')" style="display:none;">
          <i id="icon-v" class="ti ti-video"></i>
          <div id="lbl-v" class="zone-label">Video file</div>
          <div id="sub-v" class="zone-sub">Drop a video file here, such as 720p.mp4</div>
          <div id="fn-v" class="zone-file"></div>
        </div>
        <div id="zone-a" class="drop-zone" onclick="document.getElementById('inp-a').click()" ondragover="ev(event,'a')" ondragleave="el('a')" ondrop="ed(event,'a')">
          <input id="inp-a" type="file" accept="audio/*,video/*,.mp4,.mp3,.m4a" onchange="fi(event,'a')" style="display:none;">
          <i id="icon-a" class="ti ti-music"></i>
          <div id="lbl-a" class="zone-label">Audio file</div>
          <div id="sub-a" class="zone-sub">Drop an audio file here, such as 128k.mp4 or .mp3</div>
          <div id="fn-a" class="zone-file"></div>
        </div>
      </div>
      <div class="name-row">
        <input id="out-name" type="text" placeholder="Output filename (for example, CH02-Class01)">
        <div class="ext-badge">.mp4</div>
      </div>
      <button id="merge-btn" class="primary-btn" onclick="doMerge()" disabled>
        <i class="ti ti-arrows-join"></i> Merge Files
      </button>
      <div class="progress-wrap" id="prog-wrap-merge"><div class="progress-bar" id="prog-bar-merge"></div></div>
      <div class="status-box" id="status-merge"></div>
    </div>

    <!-- Link Download Panel -->
    <div id="panel-dl" class="panel" style="display:none;">
      <div class="name-row">
        <input id="dl-url" type="text" placeholder="Paste an .m3u8 URL (for example, https://.../720_out.m3u8?...)" oninput="checkDlReady()">
      </div>
      <div class="name-row">
        <input id="dl-name" type="text" placeholder="Output filename (for example, CH02-Class01)" oninput="checkDlReady()">
        <div class="ext-badge">.mp4</div>
      </div>
      <button id="dl-btn" class="primary-btn" onclick="doDownload()" disabled>
        <i class="ti ti-download"></i> Download Video
      </button>
      <div class="progress-wrap" id="prog-wrap-dl"><div class="progress-bar" id="prog-bar-dl"></div></div>
      <div class="status-box" id="status-dl"></div>
      <div class="hint">
        <i class="ti ti-info-circle"></i> Some media links expire quickly. Start the download soon after copying the URL from your browser's Network tab.
      </div>
    </div>

    <!-- Link Merge Panel -->
    <div id="panel-lm" class="panel" style="display:none;">
      <div class="drop-grid">
        <div class="link-input-box">
          <div class="link-box-label"><i class="ti ti-video"></i> Video Link</div>
          <input id="lm-vurl" type="text" placeholder="Paste the video URL, such as 1080p.mp4?md5=...&amp;expires=..." oninput="checkLmReady()">
        </div>
        <div class="link-input-box">
          <div class="link-box-label"><i class="ti ti-music"></i> Audio Link</div>
          <input id="lm-aurl" type="text" placeholder="Paste the audio URL, such as 192k.mp4?md5=...&amp;expires=..." oninput="checkLmReady()">
        </div>
      </div>
      <div class="name-row">
        <input id="lm-name" type="text" placeholder="Output filename (for example, CH02-Class01)" oninput="checkLmReady()">
        <div class="ext-badge">.mp4</div>
      </div>
      <button id="lm-btn" class="primary-btn" onclick="doLinkMerge()" disabled>
        <i class="ti ti-arrows-join-2"></i> Download &amp; Merge
      </button>
      <div class="progress-wrap" id="prog-wrap-lm"><div class="progress-bar" id="prog-bar-lm"></div></div>
      <div class="status-box" id="status-lm"></div>
      <div class="hint">
        <i class="ti ti-info-circle"></i> Both media links may expire quickly. Start the merge soon after copying them from your browser's Network tab.
      </div>
    </div>

    <!-- Convert Panel -->
    <div id="panel-cv" class="panel" style="display:none;">
      <div id="zone-c" class="drop-zone" style="margin-bottom:1rem;" onclick="document.getElementById('inp-c').click()" ondragover="cvOver(event)" ondragleave="cvLeave()" ondrop="cvDrop(event)">
        <input id="inp-c" type="file" accept="video/*,.webm,.mkv,.avi,.mov,.flv,.ts,.wmv" onchange="cvPick(event)" style="display:none;">
        <i id="icon-c" class="ti ti-file-unknown"></i>
        <div id="lbl-c" class="zone-label">Source video</div>
        <div id="sub-c" class="zone-sub">Drop a video file, such as .webm, .mkv, .avi, or .mov</div>
        <div id="fn-c" class="zone-file"></div>
      </div>
      <div class="name-row">
        <select id="cv-quality" class="cv-select">
          <option value="23">Standard quality (CRF 23) — balanced size and quality</option>
          <option value="18">High quality (CRF 18) — larger file, better quality</option>
          <option value="28">Smaller file (CRF 28) — lower quality, less storage</option>
          <option value="copy">Remux only — no re-encoding (may not support every codec)</option>
        </select>
      </div>
      <div class="name-row">
        <input id="cv-name" type="text" placeholder="Output filename (leave blank to use the source filename)">
        <div class="ext-badge">.mp4</div>
      </div>
      <button id="cv-btn" class="primary-btn" onclick="doConvert()" disabled>
        <i class="ti ti-refresh"></i> Convert Video
      </button>
      <div class="progress-wrap" id="prog-wrap-cv"><div class="progress-bar" id="prog-bar-cv"></div></div>
      <div class="status-box" id="status-cv"></div>
      <div class="hint">
        <i class="ti ti-info-circle"></i> Place the source file in the same folder as app.py. Re-encoding can take several minutes for large videos; unlike merging, it is not instant.
      </div>
    </div>

  </div>
</div>

<script>
function switchTab(tab) {
  document.getElementById('panel-merge').style.display = (tab === 'merge') ? 'block' : 'none';
  document.getElementById('panel-dl').style.display   = (tab === 'dl')    ? 'block' : 'none';
  document.getElementById('panel-lm').style.display   = (tab === 'lm')    ? 'block' : 'none';
  document.getElementById('panel-cv').style.display   = (tab === 'cv')    ? 'block' : 'none';
  document.getElementById('tab-merge-btn').classList.toggle('active', tab === 'merge');
  document.getElementById('tab-dl-btn').classList.toggle('active',    tab === 'dl');
  document.getElementById('tab-lm-btn').classList.toggle('active',    tab === 'lm');
  document.getElementById('tab-cv-btn').classList.toggle('active',    tab === 'cv');
}

function showStatus(panel, msg, type) {
  var el = document.getElementById('status-' + panel);
  el.style.display = 'block';
  el.textContent = msg;
  var map = {
    info: ['var(--bg-accent)', 'var(--text-accent)', 'var(--border-accent)'],
    success: ['var(--bg-success)', 'var(--text-success)', 'var(--border-success)'],
    error: ['var(--bg-danger)', 'var(--text-danger)', 'var(--border-danger)']
  };
  var c = map[type] || map.info;
  el.style.background = c[0];
  el.style.color = c[1];
  el.style.border = '0.5px solid ' + c[2];
}

function setProgress(panel, pct) {
  document.getElementById('prog-wrap-' + panel).style.display = 'block';
  document.getElementById('prog-bar-' + panel).style.width = pct + '%';
}

var files = {v: null, a: null};
function ev(e, t) { e.preventDefault(); hoverZone(t, true); }
function el(t) { if(!files[t]) hoverZone(t, false); }
function ed(e, t) { e.preventDefault(); hoverZone(t, false); var f = e.dataTransfer.files[0]; if(f) setF(t, f); }
function fi(e, t) { var f = e.target.files[0]; if(f) setF(t, f); }
function hoverZone(t, on) {
  document.getElementById('zone-'+t).style.background = on ? 'var(--bg-accent)' : '';
  document.getElementById('zone-'+t).style.borderColor = on ? 'var(--border-accent)' : '';
}
function setF(t, f) {
  files[t] = f;
  var z = document.getElementById('zone-'+t);
  z.classList.add('active');
  document.getElementById('icon-'+t).style.color = 'var(--text-accent)';
  document.getElementById('lbl-'+t).style.color = 'var(--text-accent)';
  document.getElementById('sub-'+t).style.display = 'none';
  document.getElementById('fn-'+t).textContent = '✓ ' + (f.name.length > 26 ? f.name.substring(0,23)+'...' : f.name);
  document.getElementById('merge-btn').disabled = !(files.v && files.a);
}

async function doMerge() {
  var name = document.getElementById('out-name').value.trim() || 'merged_class';
  var outName = name.endsWith('.mp4') ? name : name + '.mp4';
  var btn = document.getElementById('merge-btn');
  
  btn.disabled = true; btn.style.cursor = 'not-allowed';
  btn.innerHTML = '<i class="ti ti-loader"></i>&nbsp;Merging files...';
  setProgress('merge', 50);
  showStatus('merge', 'Merging the video and audio. Please wait...', 'info');

  try {
    let formData = new FormData();
    formData.append('video', files.v.name);
    formData.append('audio', files.a.name);
    formData.append('output', outName);

    let response = await fetch('/run-merge', { method: 'POST', body: formData });
    let result = await response.json();

    if (result.success) {
      setProgress('merge', 100);
      showStatus('merge', '"' + outName + '" was saved successfully.', 'success');
    } else {
      throw new Error(result.error);
    }
  } catch(e) {
    showStatus('merge', 'Error: ' + e.message, 'error');
  }
  
  btn.disabled = false; btn.style.cursor = 'pointer';
  btn.innerHTML = '<i class="ti ti-arrows-join"></i>&nbsp;Merge Files';
}

function checkDlReady() {
  var url = document.getElementById('dl-url').value.trim();
  var name = document.getElementById('dl-name').value.trim();
  document.getElementById('dl-btn').disabled = !(url && name);
}

async function doDownload() {
  var url = document.getElementById('dl-url').value.trim();
  var name = document.getElementById('dl-name').value.trim();
  var outName = name.endsWith('.mp4') ? name : name + '.mp4';
  var btn = document.getElementById('dl-btn');
  
  btn.disabled = true; btn.style.cursor = 'not-allowed';
  btn.innerHTML = '<i class="ti ti-loader"></i>&nbsp;Downloading...';
  setProgress('dl', 70);
  showStatus('dl', 'FFmpeg is downloading the video. This may take a while depending on the file size...', 'info');

  try {
    let formData = new FormData();
    formData.append('url', url);
    formData.append('output', outName);

    let response = await fetch('/run-download', { method: 'POST', body: formData });
    let result = await response.json();

    if (result.success) {
      setProgress('dl', 100);
      showStatus('dl', '"' + outName + '" was downloaded and saved successfully.', 'success');
      document.getElementById('dl-url').value = ''; 
      checkDlReady();
    } else {
      throw new Error(result.error);
    }
  } catch(e) {
    showStatus('dl', 'Error: ' + e.message, 'error');
  }
  
  btn.disabled = false; btn.style.cursor = 'pointer';
  btn.innerHTML = '<i class="ti ti-download"></i>&nbsp;Download Video';
}

function checkLmReady() {
  var vurl = document.getElementById('lm-vurl').value.trim();
  var aurl = document.getElementById('lm-aurl').value.trim();
  var name = document.getElementById('lm-name').value.trim();
  document.getElementById('lm-btn').disabled = !(vurl && aurl && name);
}

async function doLinkMerge() {
  var vurl   = document.getElementById('lm-vurl').value.trim();
  var aurl   = document.getElementById('lm-aurl').value.trim();
  var name   = document.getElementById('lm-name').value.trim();
  var outName = name.endsWith('.mp4') ? name : name + '.mp4';
  var btn    = document.getElementById('lm-btn');

  btn.disabled = true; btn.style.cursor = 'not-allowed';
  btn.innerHTML = '<i class="ti ti-loader"></i>&nbsp;Downloading and merging...';
  setProgress('lm', 30);
  showStatus('lm', 'FFmpeg is downloading the video and audio separately, then merging them...', 'info');

  try {
    let formData = new FormData();
    formData.append('video_url', vurl);
    formData.append('audio_url', aurl);
    formData.append('output', outName);

    setProgress('lm', 60);
    let response = await fetch('/run-link-merge', { method: 'POST', body: formData });
    let result = await response.json();

    if (result.success) {
      setProgress('lm', 100);
      showStatus('lm', '"' + outName + '" was downloaded and merged successfully.', 'success');
      document.getElementById('lm-vurl').value = '';
      document.getElementById('lm-aurl').value = '';
      checkLmReady();
    } else {
      throw new Error(result.error);
    }
  } catch(e) {
    showStatus('lm', 'Error: ' + e.message, 'error');
    setProgress('lm', 0);
  }

  btn.disabled = false; btn.style.cursor = 'pointer';
  btn.innerHTML = '<i class="ti ti-arrows-join-2"></i>&nbsp;Download &amp; Merge';
}

var cvFile = null;
function cvOver(e) {
  e.preventDefault();
  var z = document.getElementById('zone-c');
  z.style.background = 'var(--bg-accent)';
  z.style.borderColor = 'var(--border-accent)';
}
function cvLeave() {
  if (!cvFile) {
    var z = document.getElementById('zone-c');
    z.style.background = '';
    z.style.borderColor = '';
  }
}
function cvDrop(e) {
  e.preventDefault();
  cvLeave();
  var f = e.dataTransfer.files[0];
  if (f) cvSet(f);
}
function cvPick(e) {
  var f = e.target.files[0];
  if (f) cvSet(f);
}

function cvSet(f) {
  cvFile = f;
  document.getElementById('zone-c').classList.add('active');
  document.getElementById('icon-c').style.color = 'var(--text-accent)';
  document.getElementById('lbl-c').style.color = 'var(--text-accent)';
  document.getElementById('sub-c').style.display = 'none';
  document.getElementById('fn-c').textContent = '✓ ' + (f.name.length > 30 ? f.name.substring(0,27)+'...' : f.name);
  document.getElementById('cv-btn').disabled = false;
}

async function doConvert() {
  var name    = document.getElementById('cv-name').value.trim();
  var quality = document.getElementById('cv-quality').value;
  var btn     = document.getElementById('cv-btn');

  if (!name && cvFile) {
    var dot = cvFile.name.lastIndexOf('.');
    name = dot > 0 ? cvFile.name.substring(0, dot) : cvFile.name;
  }
  var outName = name.endsWith('.mp4') ? name : name + '.mp4';

  btn.disabled = true; btn.style.cursor = 'not-allowed';
  btn.innerHTML = '<i class="ti ti-loader"></i>&nbsp;Converting...';
  setProgress('cv', 40);
  showStatus('cv', quality === 'copy'
    ? 'Remuxing without re-encoding. This should be faster...'
    : 'FFmpeg is re-encoding the video to H.264. Large files may take several minutes...', 'info');

  try {
    let formData = new FormData();
    formData.append('source', cvFile.name);
    formData.append('output', outName);
    formData.append('quality', quality);

    let response = await fetch('/run-convert', { method: 'POST', body: formData });
    let result = await response.json();

    if (result.success) {
      setProgress('cv', 100);
      showStatus('cv', '"' + outName + '" was saved successfully.', 'success');
    } else {
      throw new Error(result.error);
    }
  } catch(e) {
    showStatus('cv', 'Error: ' + e.message, 'error');
    setProgress('cv', 0);
  }

  btn.disabled = false; btn.style.cursor = 'pointer';
  btn.innerHTML = '<i class="ti ti-refresh"></i>&nbsp;Convert Video';
}
</script>
</body>
</html>
"""

@app.route('/')
def home():
    return HTML_PAGE

@app.route('/run-merge', methods=['POST'])
def run_merge():
    video = request.form.get('video')
    audio = request.form.get('audio')
    output = request.form.get('output')

    if not video or not audio or not output:
        return jsonify({"success": False, "error": "Video file, audio file, and output filename are required."})

    if not os.path.exists(video) or not os.path.exists(audio):
        return jsonify({"success": False, "error": "The video or audio file was not found in this folder."})

    # Normalize the extension so the output does not end in .mp4.mp4.
    output_clean = output.strip()
    if output_clean.lower().endswith('.mp4'):
        output_clean = output_clean[:-4]
    output_final = output_clean + '.mp4'

    # Pass arguments as a list so filenames containing spaces are handled correctly.
    command = ['ffmpeg', '-i', video, '-i', audio, '-c:v', 'copy', '-c:a', 'aac', '-y', output_final]
    
    try:
        subprocess.run(command, check=True)
        return jsonify({"success": True})
    except subprocess.CalledProcessError as e:
        return jsonify({"success": False, "error": f"FFmpeg Error: {str(e)}"})
    except FileNotFoundError:
        return jsonify({"success": False, "error": "FFmpeg was not found. Install it and make sure it is available on PATH (ffmpeg -version)."})

@app.route('/run-download', methods=['POST'])
def run_download():
    url = request.form.get('url')
    output = request.form.get('output')

    if not url or not output:
        return jsonify({"success": False, "error": "A URL and output filename are required."})

    # Normalize the extension so the output does not end in .mp4.mp4.
    output_clean = output.strip()
    if output_clean.lower().endswith('.mp4'):
        output_clean = output_clean[:-4]
    output_final = output_clean + '.mp4'

    # Force the output container and pass arguments as a list for filenames with spaces.
    command = ['ffmpeg', '-i', url, '-c', 'copy', '-f', 'mp4', '-y', output_final]
    
    try:
        subprocess.run(command, check=True)
        return jsonify({"success": True})
    except subprocess.CalledProcessError as e:
        return jsonify({"success": False, "error": f"FFmpeg error: {str(e)}. Check the URL and try again."})
    except FileNotFoundError:
        return jsonify({"success": False, "error": "FFmpeg was not found. Install it and make sure it is available on PATH (ffmpeg -version)."})

@app.route('/run-link-merge', methods=['POST'])
def run_link_merge():
    video_url = request.form.get('video_url')
    audio_url = request.form.get('audio_url')
    output    = request.form.get('output')

    if not video_url or not audio_url or not output:
        return jsonify({"success": False, "error": "Video URL, audio URL, and output filename are required."})

    # Normalize the extension so the output does not end in .mp4.mp4.
    output_clean = output.strip()
    if output_clean.lower().endswith('.mp4'):
        output_clean = output_clean[:-4]
    output_final = output_clean + '.mp4'

    # FFmpeg downloads both URLs directly, copies the video stream, and encodes audio as AAC.
    command = [
        'ffmpeg',
        '-i', video_url,
        '-i', audio_url,
        '-c:v', 'copy',
        '-c:a', 'aac',
        '-f', 'mp4',
        '-y', output_final
    ]

    try:
        subprocess.run(command, check=True)
        return jsonify({"success": True})
    except subprocess.CalledProcessError as e:
        return jsonify({"success": False, "error": f"FFmpeg error: {str(e)}. Check that both links are valid and have not expired."})
    except FileNotFoundError:
        return jsonify({"success": False, "error": "FFmpeg was not found. Install it and make sure it is available on PATH (ffmpeg -version)."})

@app.route('/run-convert', methods=['POST'])
def run_convert():
    source  = request.form.get('source')
    output  = request.form.get('output')
    quality = request.form.get('quality', '23')

    if not source or not output:
        return jsonify({"success": False, "error": "A source file and output filename are required."})

    if not os.path.exists(source):
        return jsonify({"success": False, "error": f'"{source}" was not found in this folder. Place the file next to app.py.'})

    # Normalize the extension so the output does not end in .mp4.mp4.
    output_clean = output.strip()
    if output_clean.lower().endswith('.mp4'):
        output_clean = output_clean[:-4]
    output_final = output_clean + '.mp4'

    # Prevent FFmpeg from overwriting the source file.
    if os.path.abspath(source) == os.path.abspath(output_final):
        return jsonify({"success": False, "error": "The output filename matches the source file. Choose a different name."})

    if quality == 'copy':
        # Remux the streams without re-encoding; some codecs are not supported by MP4.
        command = ['ffmpeg', '-i', source, '-c', 'copy', '-f', 'mp4', '-y', output_final]
    else:
        # Convert video to H.264 and audio to AAC; lower CRF means higher quality and a larger file.
        # Move MP4 metadata to the beginning so playback can start before the whole file is downloaded.
        command = [
            'ffmpeg', '-i', source,
            '-c:v', 'libx264', '-crf', quality, '-preset', 'medium',
            '-c:a', 'aac', '-b:a', '192k',
            '-movflags', '+faststart',
            '-f', 'mp4', '-y', output_final
        ]

    try:
        result = subprocess.run(command, capture_output=True, text=True, errors='replace')
        if result.returncode != 0:
            # FFmpeg can leave an empty output file when conversion fails.
            if os.path.exists(output_final) and os.path.getsize(output_final) == 0:
                try:
                    os.remove(output_final)
                except OSError:
                    pass
            tail = (result.stderr or '').strip().splitlines()[-3:]
            detail = ' | '.join(tail) if tail else 'Unknown error'
            if quality == 'copy':
                detail += ' — If remuxing fails, try one of the other quality options.'
            return jsonify({"success": False, "error": f"FFmpeg error: {detail}"})
        return jsonify({"success": True})
    except FileNotFoundError:
        return jsonify({"success": False, "error": "FFmpeg was not found. Install it and make sure it is available on PATH (ffmpeg -version)."})

if __name__ == '__main__':
    print("\nServer is running. Open http://127.0.0.1:5000 in your browser.")
    app.run(host='0.0.0.0', port=5000)
