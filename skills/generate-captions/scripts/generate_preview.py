#!/usr/bin/env python3
"""Standalone HTML preview for caption editing.

Generates a self-contained HTML file with:
- Video playback with CSS-based caption overlay (word-by-word highlighting)
- Style controls panel (position, font size, colors, animation, etc.)
- Caption text editing panel (editable word inputs, click-to-seek timestamps)
- Export JSON and Reset buttons

The preview uses CSS custom properties for live style updates and
requestAnimationFrame for smooth caption sync during playback.
"""

import json
import os
import sys


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _escape_js_string(text):
    """Escape a string for embedding inside a JS string literal."""
    return (
        text.replace("\\", "\\\\")
        .replace("'", "\\'")
        .replace('"', '\\"')
        .replace("\n", "\\n")
        .replace("\r", "\\r")
        .replace("<", "\\x3c")
        .replace(">", "\\x3e")
    )


def _escape_html(text):
    """Escape a string for embedding in HTML attribute or content."""
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&#39;")
    )


# ---------------------------------------------------------------------------
# Main generator
# ---------------------------------------------------------------------------

def generate_preview_html(caption_data, video_relative_path):
    """Generate a CSS-based caption preview HTML string.

    Parameters
    ----------
    caption_data : dict
        The intermediate caption JSON data with keys:
        - style: {font_family, font_size, primary_color, secondary_color,
                  outline_color, outline_width, shadow_depth, background_color,
                  position, animation, words_per_line}
        - segments: [{start, end, text, words: [{text, start, end}]}]
        - resolution: {width, height}
    video_relative_path : str
        Filename (not a path traversal) of the video file, expected to be
        in the same directory as the output HTML.

    Returns
    -------
    str
        Complete HTML document as a string.
    """
    # Extract only the filename to prevent path traversal
    video_filename = os.path.basename(video_relative_path)

    style = caption_data.get("style", {})
    segments = caption_data.get("segments", [])
    resolution = caption_data.get("resolution", {"width": 1920, "height": 1080})

    font_family = style.get("font_family", "Arial Black")
    font_size = style.get("font_size", 48)
    primary_color = style.get("primary_color", "#FFFFFF")
    secondary_color = style.get("secondary_color", "#00FFB2")
    outline_color = style.get("outline_color", "#000000")
    outline_width = style.get("outline_width", 3)
    shadow_depth = style.get("shadow_depth", 0)
    background_color = style.get("background_color", None) or ""
    position = style.get("position", "center")
    animation = style.get("animation", "karaoke-sweep")
    words_per_line = style.get("words_per_line", 4)

    # Serialize data for JS embedding
    segments_json = _escape_js_string(json.dumps(segments))
    caption_data_json = _escape_js_string(json.dumps(caption_data))

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Caption Preview</title>
<style>
:root {{
    --caption-primary: {primary_color};
    --caption-secondary: {secondary_color};
    --caption-outline: {outline_color};
    --caption-outline-w: {outline_width}px;
    --caption-shadow-depth: {shadow_depth}px;
    --caption-bg: {background_color if background_color else 'transparent'};
}}

* {{ margin: 0; padding: 0; box-sizing: border-box; }}

body {{
    background: #111;
    color: #e0e0e0;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 20px;
    min-height: 100vh;
}}

h1 {{
    font-size: 1.4rem;
    margin-bottom: 16px;
    color: #ccc;
}}
h1 span {{
    font-size: 0.75rem;
    color: #666;
    font-weight: normal;
}}

/* ---- Video wrapper + caption overlay ---- */
.video-container {{
    position: relative;
    width: 100%;
    max-width: 900px;
    background: #000;
    border-radius: 8px;
    overflow: hidden;
    margin-bottom: 20px;
}}
video {{
    width: 100%;
    display: block;
}}
.caption-overlay {{
    position: absolute;
    left: 0;
    right: 0;
    display: flex;
    justify-content: center;
    pointer-events: none;
    z-index: 10;
    padding: 0 40px;
}}
.caption-overlay.pos-top {{ top: 40px; align-items: flex-start; }}
.caption-overlay.pos-center {{ top: 0; bottom: 0; align-items: center; }}
.caption-overlay.pos-bottom {{ bottom: 60px; align-items: flex-end; }}

.caption-line {{
    font-family: var(--caption-font-family, "Arial Black"), "Impact", sans-serif;
    font-size: var(--caption-font-size, {font_size}px);
    font-weight: 900;
    text-align: center;
    line-height: 1.3;
    white-space: pre-wrap;
    color: var(--caption-secondary);
    text-shadow:
        calc(var(--caption-outline-w) *  1) calc(var(--caption-outline-w) *  0) 0 var(--caption-outline),
        calc(var(--caption-outline-w) * -1) calc(var(--caption-outline-w) *  0) 0 var(--caption-outline),
        calc(var(--caption-outline-w) *  0) calc(var(--caption-outline-w) *  1) 0 var(--caption-outline),
        calc(var(--caption-outline-w) *  0) calc(var(--caption-outline-w) * -1) 0 var(--caption-outline),
        calc(var(--caption-outline-w) *  0.71) calc(var(--caption-outline-w) *  0.71) 0 var(--caption-outline),
        calc(var(--caption-outline-w) * -0.71) calc(var(--caption-outline-w) *  0.71) 0 var(--caption-outline),
        calc(var(--caption-outline-w) *  0.71) calc(var(--caption-outline-w) * -0.71) 0 var(--caption-outline),
        calc(var(--caption-outline-w) * -0.71) calc(var(--caption-outline-w) * -0.71) 0 var(--caption-outline),
        var(--caption-shadow-depth) var(--caption-shadow-depth) calc(var(--caption-shadow-depth) * 0.5) rgba(0,0,0,0.6);
    background: var(--caption-bg);
    padding: 4px 12px;
    border-radius: 4px;
}}
.caption-word {{
    display: inline;
    transition: color 0.05s ease;
}}
.caption-word.active {{
    color: var(--caption-primary);
}}

/* ---- Panels ---- */
.panels {{
    width: 100%;
    max-width: 900px;
    display: flex;
    flex-direction: column;
    gap: 16px;
}}
.panel {{
    background: #1e1e1e;
    border: 1px solid #2a2a2a;
    border-radius: 8px;
    padding: 20px;
}}
.panel h2 {{
    font-size: 1rem;
    margin-bottom: 14px;
    color: #999;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}}

/* ---- Style controls ---- */
.style-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(140px, 1fr));
    gap: 14px;
}}
.style-grid label {{
    display: flex;
    flex-direction: column;
    gap: 4px;
    font-size: 0.8rem;
    color: #888;
}}
.style-grid select,
.style-grid input[type="number"] {{
    background: #2a2a2a;
    border: 1px solid #3a3a3a;
    color: #e0e0e0;
    padding: 6px 8px;
    border-radius: 4px;
    font-size: 0.85rem;
}}
.style-grid input[type="color"] {{
    width: 100%;
    height: 30px;
    border: 1px solid #3a3a3a;
    border-radius: 4px;
    padding: 0;
    cursor: pointer;
    background: transparent;
}}
.style-grid input[type="range"] {{
    width: 100%;
    accent-color: var(--caption-primary);
}}
.range-val {{
    font-size: 0.75rem;
    color: #666;
    text-align: right;
}}

/* ---- Caption editing ---- */
.segment-list {{
    max-height: 400px;
    overflow-y: auto;
    padding-right: 4px;
}}
.segment-row {{
    display: flex;
    align-items: flex-start;
    margin-bottom: 10px;
    gap: 12px;
}}
.segment-time {{
    font-size: 0.78rem;
    font-family: "SF Mono", "Fira Code", "Consolas", monospace;
    color: #666;
    min-width: 120px;
    padding-top: 6px;
    cursor: pointer;
    white-space: nowrap;
    user-select: none;
}}
.segment-time:hover {{
    color: var(--caption-primary);
}}
.segment-words {{
    display: flex;
    flex-wrap: wrap;
    gap: 4px;
    flex: 1;
}}
.segment-words input {{
    background: #2a2a2a;
    border: 1px solid #3a3a3a;
    color: #e0e0e0;
    padding: 4px 8px;
    border-radius: 4px;
    font-size: 0.88rem;
    min-width: 50px;
}}
.segment-words input:focus {{
    outline: none;
    border-color: var(--caption-primary);
    box-shadow: 0 0 0 1px var(--caption-primary);
}}

/* ---- Action buttons ---- */
.actions {{
    display: flex;
    gap: 10px;
    margin-top: 8px;
}}
.btn {{
    border: none;
    padding: 10px 24px;
    border-radius: 6px;
    font-weight: 600;
    font-size: 0.9rem;
    cursor: pointer;
    transition: opacity 0.15s;
}}
.btn:hover {{ opacity: 0.85; }}
.btn-primary {{
    background: var(--caption-primary);
    color: #000;
}}
.btn-secondary {{
    background: #333;
    color: #e0e0e0;
}}

/* Scrollbar styling */
.segment-list::-webkit-scrollbar {{ width: 6px; }}
.segment-list::-webkit-scrollbar-track {{ background: transparent; }}
.segment-list::-webkit-scrollbar-thumb {{
    background: #444;
    border-radius: 3px;
}}
</style>
</head>
<body>

<h1>Caption Preview <span>(CSS overlay &mdash; edit &amp; export)</span></h1>

<div class="video-container">
    <video id="video" controls preload="metadata">
        <source src="{_escape_html(video_filename)}" type="video/mp4">
    </video>
    <div id="caption-overlay" class="caption-overlay pos-{_escape_html(position)}">
        <div id="caption-line" class="caption-line"></div>
    </div>
</div>

<div class="panels">
    <!-- Style Controls -->
    <div class="panel">
        <h2>Style Controls</h2>
        <div class="style-grid">
            <label>Position
                <select id="ctl-position">
                    <option value="top"{"selected" if position == "top" else ""}>Top</option>
                    <option value="center"{"selected" if position == "center" else ""}>Center</option>
                    <option value="bottom"{"selected" if position == "bottom" else ""}>Bottom</option>
                </select>
            </label>
            <label>Font Size
                <input id="ctl-fontsize" type="range" min="16" max="120" value="{font_size}">
                <span id="ctl-fontsize-val" class="range-val">{font_size}px</span>
            </label>
            <label>Highlight Color
                <input id="ctl-primary" type="color" value="{primary_color}">
            </label>
            <label>Text Color
                <input id="ctl-secondary" type="color" value="{secondary_color}">
            </label>
            <label>Outline Color
                <input id="ctl-outline" type="color" value="{outline_color}">
            </label>
            <label>Outline Width
                <input id="ctl-outline-width" type="range" min="0" max="8" value="{outline_width}">
                <span id="ctl-outline-width-val" class="range-val">{outline_width}px</span>
            </label>
            <label>Shadow Depth
                <input id="ctl-shadow" type="range" min="0" max="10" value="{shadow_depth}">
                <span id="ctl-shadow-val" class="range-val">{shadow_depth}px</span>
            </label>
            <label>Background
                <input id="ctl-bg" type="color" value="{background_color if background_color else '#000000'}">
            </label>
            <label>BG Enabled
                <select id="ctl-bg-on">
                    <option value="false"{"" if background_color else " selected"}>Off</option>
                    <option value="true"{" selected" if background_color else ""}>On</option>
                </select>
            </label>
            <label>Animation
                <select id="ctl-animation">
                    <option value="none"{"selected" if animation == "none" else ""}>None</option>
                    <option value="karaoke"{"selected" if animation == "karaoke" else ""}>Karaoke</option>
                    <option value="karaoke-sweep"{"selected" if animation == "karaoke-sweep" else ""}>Karaoke Sweep</option>
                </select>
            </label>
            <label>Words / Line
                <input id="ctl-wpl" type="number" min="1" max="20" value="{words_per_line}">
            </label>
            <label>Single Word
                <select id="ctl-single">
                    <option value="false" selected>Off</option>
                    <option value="true">On</option>
                </select>
            </label>
        </div>
    </div>

    <!-- Caption Text Editing -->
    <div class="panel">
        <h2>Caption Text</h2>
        <div id="segment-list" class="segment-list"></div>
        <div class="actions">
            <button class="btn btn-primary" id="btn-export">Export JSON</button>
            <button class="btn btn-secondary" id="btn-reset">Reset</button>
        </div>
    </div>
</div>

<script>
(function() {{
    "use strict";

    // ---- DOM refs ----
    var video = document.getElementById("video");
    var captionOverlay = document.getElementById("caption-overlay");
    var captionLine = document.getElementById("caption-line");
    var segmentList = document.getElementById("segment-list");
    var root = document.documentElement;

    // ---- Data ----
    var originalSegments = JSON.parse('{segments_json}');
    var segments = JSON.parse(JSON.stringify(originalSegments));
    var captionData = JSON.parse('{caption_data_json}');
    var resolution = captionData.resolution || {{ width: 1920, height: 1080 }};

    // ---- Style state ----
    var styleState = {{
        fontFamily: '{_escape_js_string(font_family)}',
        position: '{_escape_js_string(position)}',
        fontSize: {font_size},
        primaryColor: '{_escape_js_string(primary_color)}',
        secondaryColor: '{_escape_js_string(secondary_color)}',
        outlineColor: '{_escape_js_string(outline_color)}',
        outlineWidth: {outline_width},
        shadowDepth: {shadow_depth},
        backgroundColor: '{_escape_js_string(background_color)}',
        bgEnabled: {'true' if background_color else 'false'},
        animation: '{_escape_js_string(animation)}',
        wordsPerLine: {words_per_line},
        singleWord: false
    }};

    // ---- Smart chunking (mirrors Python logic) ----
    var SENTENCE_ENDERS = [".", "!", "?"];
    var CLAUSE_BREAKS = [",", ";", ":", "\\u2014", "\\u2013", "-"];
    var PAUSE_THRESHOLD = 0.5;

    function smartChunk(words, maxWpl) {{
        if (maxWpl <= 1) {{
            return words.map(function(w) {{ return [w]; }});
        }}
        var chunks = [];
        var cur = [];
        for (var i = 0; i < words.length; i++) {{
            cur.push(words[i]);
            var txt = (words[i].text || "").replace(/\\s+$/, "");
            var isSentEnd = SENTENCE_ENDERS.some(function(p) {{ return txt.endsWith(p); }});
            var isClause = CLAUSE_BREAKS.some(function(p) {{ return txt.endsWith(p); }});
            var hasPause = false;
            if (i < words.length - 1) {{
                hasPause = (words[i + 1].start - words[i].end) >= PAUSE_THRESHOLD;
            }}
            var atMax = cur.length >= maxWpl;
            if (isSentEnd || hasPause || atMax || (isClause && cur.length >= 2)) {{
                chunks.push(cur);
                cur = [];
            }}
        }}
        if (cur.length > 0) {{ chunks.push(cur); }}
        return chunks;
    }}

    // ---- Build all chunks from all segments ----
    var allChunks = [];

    function rebuildChunks() {{
        allChunks = [];
        var wpl = styleState.singleWord ? 1 : styleState.wordsPerLine;
        for (var si = 0; si < segments.length; si++) {{
            var seg = segments[si];
            var words = seg.words || [];
            if (words.length === 0) continue;
            var chunks = smartChunk(words, wpl);
            for (var ci = 0; ci < chunks.length; ci++) {{
                var chunk = chunks[ci];
                allChunks.push({{
                    start: chunk[0].start,
                    end: chunk[chunk.length - 1].end,
                    words: chunk
                }});
            }}
        }}
    }}

    rebuildChunks();

    // ---- CSS custom property updates ----
    function applyCSSProperties() {{
        root.style.setProperty("--caption-primary", styleState.primaryColor);
        root.style.setProperty("--caption-secondary", styleState.secondaryColor);
        root.style.setProperty("--caption-outline", styleState.outlineColor);
        root.style.setProperty("--caption-outline-w", styleState.outlineWidth + "px");
        root.style.setProperty("--caption-shadow-depth", styleState.shadowDepth + "px");
        root.style.setProperty("--caption-bg", styleState.bgEnabled ? styleState.backgroundColor : "transparent");
        root.style.setProperty("--caption-font-size", styleState.fontSize + "px");
        root.style.setProperty("--caption-font-family", '"' + styleState.fontFamily + '"');
    }}

    function applyPosition() {{
        captionOverlay.className = "caption-overlay pos-" + styleState.position;
    }}

    // ---- Caption rendering with requestAnimationFrame ----
    var lastRenderedChunkIndex = -1;
    var lastRenderedActiveWord = -1;
    var currentChunkWordSpans = [];

    function escapeHTMLText(str) {{
        var div = document.createElement("div");
        div.appendChild(document.createTextNode(str));
        return div.innerHTML;
    }}

    function renderCaption(t) {{
        // Find the active chunk
        var activeChunk = null;
        var activeIdx = -1;
        for (var i = 0; i < allChunks.length; i++) {{
            if (t >= allChunks[i].start && t < allChunks[i].end) {{
                activeChunk = allChunks[i];
                activeIdx = i;
                break;
            }}
        }}

        if (activeChunk === null) {{
            // No active chunk at this time
            if (lastRenderedChunkIndex !== -1) {{
                captionLine.innerHTML = "";
                currentChunkWordSpans = [];
                lastRenderedChunkIndex = -1;
                lastRenderedActiveWord = -1;
            }}
            return;
        }}

        // Rebuild DOM if the chunk changed
        if (activeIdx !== lastRenderedChunkIndex) {{
            captionLine.innerHTML = "";
            currentChunkWordSpans = [];
            var words = activeChunk.words;
            for (var wi = 0; wi < words.length; wi++) {{
                if (wi > 0) {{
                    var space = document.createTextNode(" ");
                    captionLine.appendChild(space);
                }}
                var span = document.createElement("span");
                span.className = "caption-word";
                span.textContent = words[wi].text;
                captionLine.appendChild(span);
                currentChunkWordSpans.push(span);
            }}
            lastRenderedChunkIndex = activeIdx;
            lastRenderedActiveWord = -1;
        }}

        // Highlight the currently spoken word based on animation mode
        if (styleState.animation === "none") {{
            // No animation: all words shown in secondary color (default), no highlight
            if (lastRenderedActiveWord !== -2) {{
                for (var j = 0; j < currentChunkWordSpans.length; j++) {{
                    currentChunkWordSpans[j].classList.remove("active");
                }}
                lastRenderedActiveWord = -2;
            }}
        }} else {{
            // Karaoke / karaoke-sweep: highlight ONLY the currently-spoken word
            var activeWordIdx = -1;
            var chunkWords = activeChunk.words;
            for (var k = 0; k < chunkWords.length; k++) {{
                if (t >= chunkWords[k].start && t < chunkWords[k].end) {{
                    activeWordIdx = k;
                    break;
                }}
            }}

            if (activeWordIdx !== lastRenderedActiveWord) {{
                for (var m = 0; m < currentChunkWordSpans.length; m++) {{
                    if (m === activeWordIdx) {{
                        currentChunkWordSpans[m].classList.add("active");
                    }} else {{
                        currentChunkWordSpans[m].classList.remove("active");
                    }}
                }}
                lastRenderedActiveWord = activeWordIdx;
            }}
        }}
    }}

    // ---- Animation loop ----
    var rafId = null;

    function tick() {{
        if (!video.paused && !video.ended) {{
            renderCaption(video.currentTime);
        }}
        rafId = requestAnimationFrame(tick);
    }}

    // Start the loop immediately; it checks paused state internally
    rafId = requestAnimationFrame(tick);

    // Also render on seek / play / pause to keep overlay in sync
    video.addEventListener("seeked", function() {{ renderCaption(video.currentTime); }});
    video.addEventListener("play", function() {{ renderCaption(video.currentTime); }});
    video.addEventListener("pause", function() {{ renderCaption(video.currentTime); }});

    // ---- Style controls wiring ----
    function onStyleChange(needsRechunk) {{
        applyCSSProperties();
        if (needsRechunk) {{
            rebuildChunks();
            // Force re-render by resetting tracking
            lastRenderedChunkIndex = -1;
            lastRenderedActiveWord = -1;
            renderCaption(video.currentTime);
        }}
    }}

    function wire(id, evt, fn) {{
        document.getElementById(id).addEventListener(evt, fn);
    }}

    wire("ctl-position", "change", function(e) {{
        styleState.position = e.target.value;
        applyPosition();
    }});

    wire("ctl-fontsize", "input", function(e) {{
        styleState.fontSize = parseInt(e.target.value, 10);
        document.getElementById("ctl-fontsize-val").textContent = e.target.value + "px";
        onStyleChange(false);
    }});

    wire("ctl-primary", "input", function(e) {{
        styleState.primaryColor = e.target.value;
        onStyleChange(false);
    }});

    wire("ctl-secondary", "input", function(e) {{
        styleState.secondaryColor = e.target.value;
        onStyleChange(false);
    }});

    wire("ctl-outline", "input", function(e) {{
        styleState.outlineColor = e.target.value;
        onStyleChange(false);
    }});

    wire("ctl-outline-width", "input", function(e) {{
        styleState.outlineWidth = parseInt(e.target.value, 10);
        document.getElementById("ctl-outline-width-val").textContent = e.target.value + "px";
        onStyleChange(false);
    }});

    wire("ctl-shadow", "input", function(e) {{
        styleState.shadowDepth = parseInt(e.target.value, 10);
        document.getElementById("ctl-shadow-val").textContent = e.target.value + "px";
        onStyleChange(false);
    }});

    wire("ctl-bg", "input", function(e) {{
        styleState.backgroundColor = e.target.value;
        onStyleChange(false);
    }});

    wire("ctl-bg-on", "change", function(e) {{
        styleState.bgEnabled = e.target.value === "true";
        onStyleChange(false);
    }});

    wire("ctl-animation", "change", function(e) {{
        styleState.animation = e.target.value;
        // Force re-render to update highlight state
        lastRenderedActiveWord = -1;
        renderCaption(video.currentTime);
    }});

    wire("ctl-wpl", "change", function(e) {{
        styleState.wordsPerLine = parseInt(e.target.value, 10);
        onStyleChange(true);
    }});

    wire("ctl-single", "change", function(e) {{
        styleState.singleWord = e.target.value === "true";
        onStyleChange(true);
    }});

    // ---- Caption text editing panel ----
    function formatTimestamp(seconds) {{
        var m = Math.floor(seconds / 60);
        var s = seconds % 60;
        var sStr = s.toFixed(2);
        if (s < 10) {{ sStr = "0" + sStr; }}
        return m + ":" + sStr;
    }}

    function buildEditPanel() {{
        segmentList.innerHTML = "";
        for (var si = 0; si < segments.length; si++) {{
            (function(segIdx) {{
                var seg = segments[segIdx];
                var row = document.createElement("div");
                row.className = "segment-row";

                // Timestamp label (click to seek)
                var timeLabel = document.createElement("div");
                timeLabel.className = "segment-time";
                timeLabel.textContent = formatTimestamp(seg.start) + " \\u2013 " + formatTimestamp(seg.end);
                timeLabel.addEventListener("click", function() {{
                    video.currentTime = seg.start;
                    video.play();
                }});
                row.appendChild(timeLabel);

                // Word input fields
                var wordsDiv = document.createElement("div");
                wordsDiv.className = "segment-words";
                var words = seg.words || [];
                for (var wi = 0; wi < words.length; wi++) {{
                    (function(wordIdx) {{
                        var w = words[wordIdx];
                        var input = document.createElement("input");
                        input.type = "text";
                        input.value = w.text;
                        input.style.width = Math.max(50, w.text.length * 10 + 20) + "px";
                        input.addEventListener("input", function(e) {{
                            segments[segIdx].words[wordIdx].text = e.target.value;
                            // Rebuild full segment text
                            segments[segIdx].text = segments[segIdx].words.map(
                                function(ww) {{ return ww.text; }}
                            ).join(" ");
                            e.target.style.width = Math.max(50, e.target.value.length * 10 + 20) + "px";
                            // Rebuild chunks and re-render
                            rebuildChunks();
                            lastRenderedChunkIndex = -1;
                            lastRenderedActiveWord = -1;
                            renderCaption(video.currentTime);
                        }});
                        wordsDiv.appendChild(input);
                    }})(wi);
                }}
                row.appendChild(wordsDiv);
                segmentList.appendChild(row);
            }})(si);
        }}
    }}

    // ---- Export JSON ----
    document.getElementById("btn-export").addEventListener("click", function() {{
        var data = JSON.parse(JSON.stringify(captionData));
        data.segments = JSON.parse(JSON.stringify(segments));
        data.style = data.style || {{}};
        data.style.font_family = styleState.fontFamily;
        data.style.font_size = styleState.fontSize;
        data.style.primary_color = styleState.primaryColor;
        data.style.secondary_color = styleState.secondaryColor;
        data.style.outline_color = styleState.outlineColor;
        data.style.outline_width = styleState.outlineWidth;
        data.style.shadow_depth = styleState.shadowDepth;
        data.style.background_color = styleState.bgEnabled ? styleState.backgroundColor : null;
        data.style.position = styleState.position;
        data.style.animation = styleState.animation;
        data.style.words_per_line = styleState.wordsPerLine;
        data.style.single_words = styleState.singleWord;

        var blob = new Blob([JSON.stringify(data, null, 2)], {{ type: "application/json" }});
        var url = URL.createObjectURL(blob);
        var a = document.createElement("a");
        a.href = url;
        a.download = "captions_edited.json";
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    }});

    // ---- Reset ----
    document.getElementById("btn-reset").addEventListener("click", function() {{
        segments = JSON.parse(JSON.stringify(originalSegments));
        rebuildChunks();
        buildEditPanel();
        lastRenderedChunkIndex = -1;
        lastRenderedActiveWord = -1;
        renderCaption(video.currentTime);
    }});

    // ---- Init ----
    applyCSSProperties();
    applyPosition();
    buildEditPanel();
    renderCaption(0);
}})();
</script>
</body>
</html>"""

    return html


# ---------------------------------------------------------------------------
# CLI entry point (standalone usage)
# ---------------------------------------------------------------------------

def main():
    """Generate an HTML preview from a caption JSON file."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Generate standalone caption preview HTML from caption JSON.",
    )
    parser.add_argument("caption_json", help="Path to caption JSON file")
    parser.add_argument(
        "--video",
        help="Path to video file (default: uses video_path from caption JSON)",
    )
    parser.add_argument(
        "-o", "--output",
        help="Output HTML file path (default: preview.html in same dir as caption JSON)",
    )
    args = parser.parse_args()

    with open(args.caption_json, "r", encoding="utf-8") as f:
        caption_data = json.load(f)

    video_path = args.video or caption_data.get("video_path", "video.mp4")

    # Compute output path
    if args.output:
        output_path = args.output
    else:
        output_dir = os.path.dirname(os.path.abspath(args.caption_json))
        output_path = os.path.join(output_dir, "preview.html")

    # Use just the filename -- the video should be in the same directory
    video_filename = os.path.basename(video_path)

    html = generate_preview_html(caption_data, video_filename)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"Preview saved to: {output_path}", file=sys.stderr)
    print(
        f"Ensure '{video_filename}' is in the same directory as '{output_path}'.",
        file=sys.stderr,
    )


if __name__ == "__main__":
    main()
