# SPDX-FileCopyrightText: Copyright (c) 2026 The Newton Developers
# SPDX-License-Identifier: Apache-2.0

"""Serve a local, single-chart viewer for Newton's published ASV data."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import threading
import urllib.error
import urllib.parse
import urllib.request
import webbrowser
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any

DEFAULT_SOURCE_URL = "https://newton-physics.github.io/newton-asv/"
DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 8765

HTML = r"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Newton ASV Viewer</title>
  <script src="https://cdn.plot.ly/plotly-2.35.2.min.js"></script>
  <style>
    :root {
      color-scheme: light;
      --bg: #f7f8fa;
      --panel: #ffffff;
      --ink: #20242a;
      --muted: #626b76;
      --line: #d9dee6;
      --accent: #007c89;
      --accent-2: #b4495d;
      --soft: #eef4f5;
    }
    * { box-sizing: border-box; }
    body {
      margin: 0;
      min-height: 100vh;
      background: var(--bg);
      color: var(--ink);
      font: 14px/1.45 system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    }
    main {
      display: grid;
      grid-template-columns: minmax(300px, 360px) minmax(0, 1fr);
      min-height: 100vh;
    }
    aside {
      border-right: 1px solid var(--line);
      background: var(--panel);
      padding: 18px;
      display: flex;
      flex-direction: column;
      gap: 14px;
      min-height: 100vh;
    }
    section {
      padding: 18px 22px 14px;
      display: flex;
      min-width: 0;
      flex-direction: column;
      gap: 14px;
    }
    h1 {
      margin: 0;
      font-size: 20px;
      font-weight: 700;
      letter-spacing: 0;
    }
    label {
      display: block;
      margin-bottom: 6px;
      color: var(--muted);
      font-size: 12px;
      font-weight: 650;
      text-transform: uppercase;
    }
    input,
    select,
    button {
      width: 100%;
      border: 1px solid var(--line);
      border-radius: 6px;
      background: #fff;
      color: var(--ink);
      font: inherit;
    }
    input,
    select {
      min-height: 36px;
      padding: 7px 9px;
    }
    select[size] {
      min-height: 240px;
      padding: 4px;
    }
    option {
      padding: 5px 7px;
    }
    button {
      min-height: 36px;
      padding: 7px 10px;
      cursor: pointer;
      background: var(--accent);
      border-color: var(--accent);
      color: #fff;
      font-weight: 650;
    }
    button.secondary {
      background: #fff;
      color: var(--ink);
      border-color: var(--line);
    }
    .row {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 10px;
    }
    .action-row {
      grid-template-columns: repeat(3, minmax(0, 1fr));
    }
    .checks {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 8px 10px;
    }
    .check {
      display: flex;
      align-items: center;
      gap: 8px;
      min-width: 0;
      color: var(--ink);
      font-weight: 500;
      text-transform: none;
    }
    .check input {
      width: 16px;
      min-height: 16px;
      padding: 0;
      flex: 0 0 auto;
    }
    .series-toggles {
      display: flex;
      gap: 12px;
      margin-top: 8px;
      flex-wrap: wrap;
    }
    .source,
    .status {
      color: var(--muted);
      font-size: 12px;
      overflow-wrap: anywhere;
    }
    .source a {
      color: var(--accent);
      text-decoration: none;
    }
    .toolbar {
      display: grid;
      grid-template-columns: minmax(120px, 1fr) minmax(135px, 1fr) 135px 135px 115px 130px;
      gap: 12px;
      align-items: end;
    }
    .plot-shell {
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: 8px;
      min-height: 640px;
      height: calc(100vh - 130px);
      padding: 10px;
      min-width: 0;
    }
    .plot-shell.matrix {
      height: auto;
      min-height: 0;
      padding: 0;
      background: transparent;
      border: 0;
    }
    #plot {
      width: 100%;
      height: 100%;
    }
    .matrix-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(360px, 1fr));
      gap: 14px;
      align-items: start;
    }
    .matrix-card {
      min-width: 0;
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 8px;
    }
    .matrix-title {
      min-height: 36px;
      margin: 0 2px 6px;
      color: var(--ink);
      font-size: 12px;
      font-weight: 650;
      line-height: 1.25;
      overflow-wrap: anywhere;
    }
    .matrix-meta {
      color: var(--muted);
      font-weight: 500;
    }
    .matrix-plot {
      width: 100%;
      height: 260px;
    }
    .empty {
      display: grid;
      place-items: center;
      height: 100%;
      color: var(--muted);
      font-size: 15px;
      text-align: center;
      padding: 30px;
    }
    @media (max-width: 900px) {
      main {
        grid-template-columns: 1fr;
      }
      aside {
        min-height: auto;
        border-right: 0;
        border-bottom: 1px solid var(--line);
      }
      .toolbar {
        grid-template-columns: 1fr;
      }
      .plot-shell {
        height: 70vh;
      }
      .plot-shell.matrix {
        height: auto;
      }
      .matrix-grid {
        grid-template-columns: 1fr;
      }
    }
  </style>
</head>
<body>
<main>
  <aside>
    <div>
      <h1>Newton ASV Viewer</h1>
      <div class="source">Source: <a id="source-link" target="_blank" rel="noreferrer"></a></div>
    </div>

    <div>
      <label for="benchmark-filter">Benchmark filter</label>
      <input id="benchmark-filter" type="search" placeholder="Filter benchmarks">
    </div>

    <div>
      <label for="benchmark-list">Benchmarks <span id="benchmark-count"></span></label>
      <select id="benchmark-list" size="14"></select>
    </div>

    <div>
      <label for="config-list">Machine / environment</label>
      <select id="config-list"></select>
    </div>

    <div>
      <label for="series-list">Series</label>
      <select id="series-list" size="5" multiple></select>
      <div class="series-toggles">
        <label class="check"><input id="all-series" type="checkbox">All series</label>
        <label class="check"><input id="separate-y-axes" type="checkbox" checked>Separate axes</label>
      </div>
    </div>

    <div class="row action-row">
      <button id="refresh" type="button">Refresh</button>
      <button id="view-toggle" type="button" class="secondary">Matrix view</button>
      <button id="copy-url" type="button" class="secondary">Copy URL</button>
    </div>

    <div class="status" id="status">Loading index...</div>
  </aside>

  <section>
    <div class="toolbar">
      <div>
        <label for="x-axis">X axis</label>
        <select id="x-axis">
          <option value="date" selected>Commit date</option>
          <option value="revision">ASV revision</option>
        </select>
      </div>
      <div>
        <label for="date-range">Date range</label>
        <select id="date-range">
          <option value="all" selected>All history</option>
          <option value="30d">Last 30 days</option>
          <option value="90d">Last 90 days</option>
          <option value="6m">Last 6 months</option>
          <option value="1y">Last year</option>
          <option value="custom">Custom</option>
        </select>
      </div>
      <div>
        <label for="date-start">From</label>
        <input id="date-start" type="date">
      </div>
      <div>
        <label for="date-end">To</label>
        <input id="date-end" type="date">
      </div>
      <div>
        <label for="last-points">Last points</label>
        <input id="last-points" type="number" min="0" step="1" value="0">
      </div>
      <div class="checks">
        <label class="check"><input id="log-y" type="checkbox">Log Y</label>
        <label class="check"><input id="zero-y" type="checkbox" checked>Zero Y</label>
        <label class="check"><input id="show-tags" type="checkbox" checked>Tags</label>
        <label class="check"><input id="lines" type="checkbox" checked>Lines</label>
      </div>
    </div>

    <div class="plot-shell">
      <div id="plot"><div class="empty">Select a benchmark.</div></div>
    </div>
  </section>
</main>

<script>
'use strict';

const CHART_COLORS = ['#007c89', '#b4495d', '#5f6caf', '#c97818', '#228b55', '#7b4ea3', '#455a64', '#d1495b'];
const MAX_SEPARATE_Y_AXES = 8;

const state = {
  index: null,
  benchmarks: [],
  filteredBenchmarks: [],
  currentBenchmark: null,
  currentConfigIndex: 0,
  currentRaw: null,
  currentGraphBenchmark: null,
  currentGraphConfigIndex: null,
  currentGraphState: null,
  currentSeriesCount: 0,
  viewMode: 'single',
  graphCache: {},
  commitCache: {},
  commitRangeCache: {},
  graphLoadToken: 0,
  drawToken: 0,
};

const els = {
  sourceLink: document.getElementById('source-link'),
  filter: document.getElementById('benchmark-filter'),
  benchmarkList: document.getElementById('benchmark-list'),
  benchmarkCount: document.getElementById('benchmark-count'),
  configList: document.getElementById('config-list'),
  seriesList: document.getElementById('series-list'),
  allSeries: document.getElementById('all-series'),
  separateYAxes: document.getElementById('separate-y-axes'),
  status: document.getElementById('status'),
  plot: document.getElementById('plot'),
  plotShell: document.querySelector('.plot-shell'),
  refresh: document.getElementById('refresh'),
  viewToggle: document.getElementById('view-toggle'),
  copyUrl: document.getElementById('copy-url'),
  xAxis: document.getElementById('x-axis'),
  dateRange: document.getElementById('date-range'),
  dateStart: document.getElementById('date-start'),
  dateEnd: document.getElementById('date-end'),
  lastPoints: document.getElementById('last-points'),
  logY: document.getElementById('log-y'),
  zeroY: document.getElementById('zero-y'),
  showTags: document.getElementById('show-tags'),
  lines: document.getElementById('lines'),
};

function setStatus(text) {
  els.status.textContent = text;
}

function friendlyBenchmarkName(name) {
  const benchmark = state.index.benchmarks[name];
  return benchmark.pretty_name || name;
}

function compactBenchmarkLabel(name) {
  const pretty = friendlyBenchmarkName(name);
  if (pretty !== name) {
    return pretty + '  -  ' + name;
  }
  return name;
}

function configLabel(config) {
  const gpu = config.gpu || 'CPU / unknown GPU';
  const os = (config.os || '').replace(/ version .*/, '');
  return `${config.machine} | ${gpu} | Python ${config.python} | ${os}`;
}

function convertBenchmarkParamValue(value) {
  const numeric = Number(value);
  if (!Number.isNaN(numeric) && value !== '') {
    return numeric;
  }
  const stringMatch = String(value).match(/^u?'(.+)'$/);
  if (stringMatch) {
    return stringMatch[1];
  }
  const classMatch = String(value).match(/^<class '(.+)'>$/);
  if (classMatch) {
    return classMatch[1];
  }
  return value;
}

function comboFromFlatIndex(params, flatIndex) {
  let idx = flatIndex;
  const selected = new Array(params.length);
  for (let k = params.length - 1; k >= 0; --k) {
    const j = idx % params[k].length;
    selected[k] = j;
    idx = (idx - j) / params[k].length;
  }
  return selected;
}

function comboCount(params) {
  return params.reduce((count, values) => count * values.length, 1);
}

function comboLabel(benchmark, flatIndex) {
  if (!benchmark.params.length) {
    return friendlyBenchmarkName(benchmark.name);
  }
  const selection = comboFromFlatIndex(benchmark.params, flatIndex);
  return selection.map((paramIndex, i) => {
    const value = convertBenchmarkParamValue(benchmark.params[i][paramIndex]);
    return `${benchmark.param_names[i]}=${value}`;
  }).join(', ');
}

function allValues(raw, benchmark) {
  const values = [];
  for (const point of raw) {
    const y = point[1];
    if (Array.isArray(y)) {
      for (const v of y) {
        if (v !== null && Number.isFinite(v)) {
          values.push(v);
        }
      }
    } else if (y !== null && Number.isFinite(y)) {
      values.push(y);
    }
  }
  return values;
}

function unitScale(benchmark, rawValues) {
  const maxAbs = Math.max(...rawValues.map((v) => Math.abs(v)), 0);
  if (benchmark.unit === 'seconds') {
    if (maxAbs < 1e-6) return {multiplier: 1e9, unit: 'ns', title: 'Runtime'};
    if (maxAbs < 1e-3) return {multiplier: 1e6, unit: 'us', title: 'Runtime'};
    if (maxAbs < 1) return {multiplier: 1e3, unit: 'ms', title: 'Runtime'};
    if (maxAbs < 120) return {multiplier: 1, unit: 's', title: 'Runtime'};
    return {multiplier: 1 / 60, unit: 'min', title: 'Runtime'};
  }
  if (benchmark.unit === 'bytes') {
    if (maxAbs < 1e6) return {multiplier: 1e-3, unit: 'KB', title: 'Memory'};
    if (maxAbs < 1e9) return {multiplier: 1e-6, unit: 'MB', title: 'Memory'};
    return {multiplier: 1e-9, unit: 'GB', title: 'Memory'};
  }
  return {multiplier: 1, unit: benchmark.unit || 'value', title: 'Value'};
}

function chartColor(index) {
  return CHART_COLORS[index % CHART_COLORS.length];
}

function selectedSeriesIndices() {
  if (els.allSeries.checked) {
    return Array.from({length: state.currentSeriesCount}, (_, i) => i);
  }
  return Array.from(els.seriesList.selectedOptions).map((option) => Number(option.value));
}

function updateSeriesControlState() {
  const isMatrix = state.viewMode === 'matrix';
  const hasMultipleSeries = state.currentSeriesCount > 1;
  els.allSeries.disabled = isMatrix || !hasMultipleSeries;
  els.separateYAxes.disabled = isMatrix || !hasMultipleSeries;
  els.seriesList.disabled = isMatrix || els.allSeries.checked || !hasMultipleSeries;
}

function updateSeriesList(benchmark) {
  const previous = new Set(selectedSeriesIndices());
  els.seriesList.textContent = '';
  const count = comboCount(benchmark.params);
  state.currentSeriesCount = count;

  if (count === 1) {
    els.allSeries.checked = false;
    const option = new Option('Single series', 0, true, true);
    els.seriesList.add(option);
    updateSeriesControlState();
    return;
  }

  const defaultLimit = Math.min(count, 8);
  for (let i = 0; i < count; ++i) {
    const selected = els.allSeries.checked || (previous.size ? previous.has(i) : i < defaultLimit);
    const option = new Option(comboLabel(benchmark, i), i, selected, selected);
    els.seriesList.add(option);
  }
  updateSeriesControlState();
}

function xValue(revision) {
  if (els.xAxis.value === 'date') {
    const timestamp = state.index.revision_to_date[String(revision)];
    return timestamp ? new Date(timestamp) : revision;
  }
  return revision;
}

function dateInputValue(timestamp) {
  if (!timestamp) {
    return '';
  }
  return new Date(timestamp).toISOString().slice(0, 10);
}

function dateInputTimestamp(value, endOfDay) {
  if (!value) {
    return null;
  }
  return Date.parse(value + (endOfDay ? 'T23:59:59.999Z' : 'T00:00:00.000Z'));
}

function shiftedTimestamp(timestamp, {days = 0, months = 0, years = 0}) {
  const date = new Date(timestamp);
  date.setUTCFullYear(date.getUTCFullYear() + years);
  date.setUTCMonth(date.getUTCMonth() + months);
  date.setUTCDate(date.getUTCDate() + days);
  return date.getTime();
}

function rawDateExtent(raw) {
  const timestamps = raw
    .map((point) => state.index.revision_to_date[String(point[0])])
    .filter((timestamp) => Number.isFinite(timestamp));
  if (!timestamps.length) {
    return null;
  }
  return {
    min: Math.min(...timestamps),
    max: Math.max(...timestamps),
  };
}

function dateRangeForRaw(raw) {
  if (els.xAxis.value !== 'date') {
    return null;
  }

  const extent = rawDateExtent(raw);
  if (!extent) {
    return null;
  }

  const preset = els.dateRange.value;
  if (preset === 'custom') {
    return {
      start: dateInputTimestamp(els.dateStart.value, false) ?? extent.min,
      end: dateInputTimestamp(els.dateEnd.value, true) ?? extent.max,
    };
  }

  const end = extent.max;
  if (preset === '30d') {
    return {start: shiftedTimestamp(end, {days: -30}), end};
  }
  if (preset === '90d') {
    return {start: shiftedTimestamp(end, {days: -90}), end};
  }
  if (preset === '6m') {
    return {start: shiftedTimestamp(end, {months: -6}), end};
  }
  if (preset === '1y') {
    return {start: shiftedTimestamp(end, {years: -1}), end};
  }
  return {start: extent.min, end: extent.max};
}

function syncDateInputs(raw) {
  const extent = rawDateExtent(raw);
  const isCustom = els.dateRange.value === 'custom';
  els.dateStart.disabled = els.xAxis.value !== 'date' || !isCustom;
  els.dateEnd.disabled = els.xAxis.value !== 'date' || !isCustom;

  if (!extent || isCustom) {
    return;
  }

  const range = dateRangeForRaw(raw);
  els.dateStart.value = dateInputValue(range ? range.start : extent.min);
  els.dateEnd.value = dateInputValue(range ? range.end : extent.max);
}

function visibleRawPoints(raw) {
  let points = raw;
  const range = dateRangeForRaw(raw);
  if (range) {
    points = points.filter((point) => {
      const timestamp = state.index.revision_to_date[String(point[0])];
      return timestamp >= range.start && timestamp <= range.end;
    });
  }
  return maybeLimitPoints(points);
}

function maybeLimitPoints(points) {
  const count = Number(els.lastPoints.value || 0);
  if (!count || points.length <= count) {
    return points;
  }
  return points.slice(points.length - count);
}

function allRevisionRaw() {
  return Object.keys(state.index.revision_to_date).map((revision) => [Number(revision), null]);
}

function fullCommitHash(revision) {
  return state.index.revision_to_hash[String(revision)] || '';
}

function escapeHtml(value) {
  return String(value || '').replace(/[&<>"']/g, (char) => ({
    '&': '&amp;',
    '<': '&lt;',
    '>': '&gt;',
    '"': '&quot;',
    "'": '&#39;',
  }[char]));
}

function fallbackCommitInfo(revision) {
  const hash = fullCommitHash(revision);
  return {
    short_hash: hash.slice(0, state.index.hash_length),
    full_hash: hash,
    author: '',
    date: '',
    subject: '',
    body: '',
    url: hash ? state.index.show_commit_url + hash : '',
  };
}

function commitRangeKey(baseHash, headHash) {
  return `${baseHash}..${headHash}`;
}

function pointSortKey(point) {
  const timestamp = state.index.revision_to_date[String(point[0])];
  return Number.isFinite(timestamp) ? timestamp : point[0];
}

async function loadCommitMetadata(raw) {
  const hashes = Array.from(new Set(raw.map((point) => fullCommitHash(point[0])).filter(Boolean)));
  const missing = hashes.filter((hash) => !state.commitCache[hash]);

  if (missing.length) {
    setStatus(`Loading commit details for ${missing.length} commits...`);
    try {
      const query = new URLSearchParams({hashes: missing.join(',')});
      const details = await fetchJson('/api/commits?' + query.toString());
      for (const [hash, detail] of Object.entries(details)) {
        state.commitCache[hash] = detail;
      }
    } catch (err) {
      for (const hash of missing) {
        state.commitCache[hash] = {
          short_hash: hash.slice(0, state.index.hash_length),
          full_hash: hash,
          author: '',
          date: '',
          subject: 'Commit metadata unavailable',
          body: err.message,
          url: state.index.show_commit_url + hash,
        };
      }
    }
  }

  const commitInfo = {};
  for (const point of raw) {
    const revision = point[0];
    const hash = fullCommitHash(revision);
    commitInfo[revision] = state.commitCache[hash] || fallbackCommitInfo(revision);
  }
  return commitInfo;
}

async function loadCommitRanges(allRaw, visibleRaw, commitInfo) {
  const visibleRevisions = new Set(visibleRaw.map((point) => point[0]));
  const sortedRaw = allRaw.slice().sort((a, b) => pointSortKey(a) - pointSortKey(b));
  const missingPairs = [];

  for (let i = 0; i < sortedRaw.length; ++i) {
    const revision = sortedRaw[i][0];
    if (!visibleRevisions.has(revision) || i === 0) {
      continue;
    }
    const baseHash = fullCommitHash(sortedRaw[i - 1][0]);
    const headHash = fullCommitHash(revision);
    const key = commitRangeKey(baseHash, headHash);
    if (baseHash && headHash && !state.commitRangeCache[key]) {
      missingPairs.push(key);
    }
  }

  if (missingPairs.length) {
    setStatus(`Loading commit ranges for ${missingPairs.length} benchmark intervals...`);
    try {
      const query = new URLSearchParams({pairs: Array.from(new Set(missingPairs)).join(',')});
      const ranges = await fetchJson('/api/commit-ranges?' + query.toString());
      for (const [key, detail] of Object.entries(ranges)) {
        state.commitRangeCache[key] = detail;
        for (const commit of detail.commits || []) {
          if (commit.full_hash) {
            state.commitCache[commit.full_hash] = commit;
          }
        }
      }
    } catch (err) {
      for (const key of missingPairs) {
        const headHash = key.split('..')[1];
        state.commitRangeCache[key] = {
          count: 1,
          commits: [state.commitCache[headHash] || {subject: err.message, short_hash: headHash.slice(0, 8)}],
        };
      }
    }
  }

  const rangesByRevision = {};
  for (let i = 0; i < sortedRaw.length; ++i) {
    const point = sortedRaw[i];
    const revision = point[0];
    if (!visibleRevisions.has(revision)) {
      continue;
    }
    const headHash = fullCommitHash(revision);
    if (i === 0) {
      rangesByRevision[revision] = {
        count: 1,
        first: true,
        commits: [commitInfo[revision] || fallbackCommitInfo(revision)],
      };
      continue;
    }
    const baseHash = fullCommitHash(sortedRaw[i - 1][0]);
    rangesByRevision[revision] = state.commitRangeCache[commitRangeKey(baseHash, headHash)] || {
      count: 1,
      commits: [commitInfo[revision] || fallbackCommitInfo(revision)],
    };
  }
  return rangesByRevision;
}

function rangeSummary(range) {
  if (!range) {
    return '';
  }
  if (range.first) {
    return 'First measured point';
  }
  const count = range.count || (range.commits || []).length;
  return count === 1 ? '1 commit since previous measured point' : `${count} commits since previous measured point`;
}

function rangeDetails(range) {
  if (!range || !range.commits || !range.commits.length) {
    return '';
  }
  return range.commits.map((commit) => {
    const hash = escapeHtml(commit.short_hash || (commit.full_hash || '').slice(0, 8));
    const subject = escapeHtml(commit.subject || '');
    const author = escapeHtml(commit.author || '');
    return `${hash} ${subject}${author ? ' - ' + author : ''}`;
  }).join('<br>');
}

function commitCustomData(point, commitInfo, rangeInfo) {
  const revision = point[0];
  const info = commitInfo[revision] || fallbackCommitInfo(revision);
  const range = rangeInfo[revision];
  const shortHash = info.short_hash || (info.full_hash || '').slice(0, state.index.hash_length);
  const date = info.date ? info.date.replace('T', ' ').replace('Z', ' UTC') : '';
  return [
    revision,
    escapeHtml(shortHash),
    escapeHtml(info.author),
    escapeHtml(date),
    escapeHtml(info.subject),
    escapeHtml(info.body),
    escapeHtml(info.full_hash),
    escapeHtml(rangeSummary(range)),
    rangeDetails(range),
  ];
}

function pointHoverTemplate(includeCommitDetails) {
  const lines = [
    '<b>%{y:.5g}</b>',
  ];
  if (!includeCommitDetails) {
    lines.push('<extra>%{fullData.name}</extra>');
    return lines.join('<br>');
  }

  lines.push(
    '<b>Measured commit</b>',
    '%{customdata[1]} %{customdata[4]}',
    'Hash: %{customdata[6]}',
    '%{customdata[5]}',
    'Author: %{customdata[2]}',
    'Date: %{customdata[3]}',
    'Revision: %{customdata[0]}',
    '<br><b>%{customdata[7]}</b>',
    '%{customdata[8]}',
    '<extra></extra>',
  );
  return lines.join('<br>');
}

function buildTraces(raw, benchmark, commitInfo, rangeInfo) {
  const selected = selectedSeriesIndices();
  const scale = unitScale(benchmark, allValues(raw, benchmark));
  const traces = [];

  if (!benchmark.params.length) {
    const points = maybeLimitPoints(raw);
    const color = chartColor(0);
    traces.push({
      x: points.map((point) => xValue(point[0])),
      y: points.map((point) => point[1] === null ? null : point[1] * scale.multiplier),
      customdata: points.map((point) => commitCustomData(point, commitInfo, rangeInfo)),
      mode: els.lines.checked ? 'lines+markers' : 'markers',
      name: friendlyBenchmarkName(benchmark.name),
      hovertemplate: pointHoverTemplate(true),
      line: {width: 2.5, color},
      marker: {size: 6, color},
    });
    return {traces, scale};
  }

  for (const [traceIndex, idx] of selected.entries()) {
    const points = maybeLimitPoints(raw);
    const color = chartColor(traceIndex);
    traces.push({
      x: points.map((point) => xValue(point[0])),
      y: points.map((point) => {
        if (!Array.isArray(point[1]) || point[1][idx] === null) {
          return null;
        }
        return point[1][idx] * scale.multiplier;
      }),
      customdata: points.map((point) => commitCustomData(point, commitInfo, rangeInfo)),
      mode: els.lines.checked ? 'lines+markers' : 'markers',
      name: comboLabel(benchmark, idx),
      hovertemplate: pointHoverTemplate(traceIndex === 0),
      line: {width: 2.25, color},
      marker: {size: 6, color},
    });
  }
  return {traces, scale};
}

function applySeparateYAxes(layout, traces, scale) {
  if (traces.length <= 1 || traces.length > MAX_SEPARATE_Y_AXES) {
    return false;
  }

  const rightAxisCount = traces.length - 1;
  const axisBand = Math.min(0.14, rightAxisCount * 0.035);
  const domainEnd = 1 - axisBand;
  const rightStep = rightAxisCount > 1 ? axisBand / (rightAxisCount - 1) : 0;
  layout.margin.r = Math.max(layout.margin.r, 66 + rightAxisCount * 18);
  layout.margin.l = Math.max(layout.margin.l, 82);
  layout.xaxis.domain = [0, domainEnd];

  traces.forEach((trace, index) => {
    const color = trace.line.color || chartColor(index);
    const axisName = index === 0 ? 'yaxis' : `yaxis${index + 1}`;
    const axisRef = index === 0 ? 'y' : `y${index + 1}`;
    trace.yaxis = axisRef;

    const axis = {
      title: {
        text: index === 0 ? `${scale.title} (${scale.unit})` : '',
        font: {color},
      },
      type: els.logY.checked ? 'log' : 'linear',
      rangemode: els.zeroY.checked && !els.logY.checked ? 'tozero' : 'normal',
      tickformat: ',.4~g',
      showgrid: index === 0,
      gridcolor: '#edf0f4',
      zeroline: false,
      showline: true,
      linecolor: color,
      tickcolor: color,
      tickfont: {color, size: 11},
    };

    if (index > 0) {
      axis.overlaying = 'y';
      axis.side = 'right';
      axis.anchor = 'free';
      axis.position = rightAxisCount === 1 ? 1 : domainEnd + rightStep * (index - 1);
      axis.showgrid = false;
    }

    layout[axisName] = axis;
  });
  return true;
}

function tagShapesAndAnnotations(raw) {
  if (!els.showTags.checked || els.xAxis.value !== 'date') {
    return {shapes: [], annotations: []};
  }

  const revisions = raw.map((point) => point[0]);
  const minRev = Math.min(...revisions);
  const maxRev = Math.max(...revisions);
  const shapes = [];
  const annotations = [];

  for (const [tag, revision] of Object.entries(state.index.tags || {})) {
    if (revision < minRev || revision > maxRev) {
      continue;
    }
    const timestamp = state.index.revision_to_date[String(revision)];
    if (!timestamp) {
      continue;
    }
    const x = new Date(timestamp);
    shapes.push({
      type: 'line',
      xref: 'x',
      yref: 'paper',
      x0: x,
      x1: x,
      y0: 0,
      y1: 1,
      line: {color: 'rgba(120, 120, 120, 0.35)', width: 1, dash: 'dot'},
    });
    annotations.push({
      x,
      y: 1.01,
      xref: 'x',
      yref: 'paper',
      text: tag,
      showarrow: false,
      textangle: -45,
      font: {size: 10, color: '#626b76'},
    });
  }
  return {shapes, annotations};
}

function clearPlotContainer() {
  for (const node of els.plot.querySelectorAll('.js-plotly-plot')) {
    Plotly.purge(node);
  }
  els.plot.innerHTML = '';
}

function matrixSeriesIndices(benchmark) {
  const count = comboCount(benchmark.params);
  const limit = Math.min(count, 6);
  return Array.from({length: limit}, (_, i) => i);
}

function matrixHoverTemplate(unit) {
  const xLine = els.xAxis.value === 'date' ? '%{x|%Y-%m-%d %H:%M}' : 'Revision axis: %{x}';
  return [
    `<b>%{y:.5g} ${unit}</b>`,
    xLine,
    'Revision: %{customdata[0]}',
    'Commit: %{customdata[1]}',
    '<extra>%{fullData.name}</extra>',
  ].join('<br>');
}

function buildMatrixTraces(raw, benchmark) {
  const visibleRaw = visibleRawPoints(raw);
  const scale = unitScale(benchmark, allValues(visibleRaw, benchmark));
  const traces = [];
  const hovertemplate = matrixHoverTemplate(scale.unit);

  if (!benchmark.params.length) {
    traces.push({
      x: visibleRaw.map((point) => xValue(point[0])),
      y: visibleRaw.map((point) => point[1] === null ? null : point[1] * scale.multiplier),
      customdata: visibleRaw.map((point) => [
        point[0],
        fullCommitHash(point[0]).slice(0, state.index.hash_length),
      ]),
      mode: els.lines.checked ? 'lines+markers' : 'markers',
      name: 'value',
      hovertemplate,
      line: {width: 1.8},
      marker: {size: 4},
    });
    return {visibleRaw, traces, scale, seriesTotal: 1, seriesShown: 1};
  }

  const seriesTotal = comboCount(benchmark.params);
  const indices = matrixSeriesIndices(benchmark);
  for (const idx of indices) {
    traces.push({
      x: visibleRaw.map((point) => xValue(point[0])),
      y: visibleRaw.map((point) => {
        if (!Array.isArray(point[1]) || point[1][idx] === null) {
          return null;
        }
        return point[1][idx] * scale.multiplier;
      }),
      customdata: visibleRaw.map((point) => [
        point[0],
        fullCommitHash(point[0]).slice(0, state.index.hash_length),
      ]),
      mode: els.lines.checked ? 'lines+markers' : 'markers',
      name: comboLabel(benchmark, idx),
      hovertemplate,
      line: {width: 1.5},
      marker: {size: 3.5},
    });
  }
  return {visibleRaw, traces, scale, seriesTotal, seriesShown: indices.length};
}

function matrixTagShapes(raw) {
  if (!els.showTags.checked || els.xAxis.value !== 'date') {
    return [];
  }

  const revisions = raw.map((point) => point[0]);
  const minRev = Math.min(...revisions);
  const maxRev = Math.max(...revisions);
  const shapes = [];
  for (const [tag, revision] of Object.entries(state.index.tags || {})) {
    if (revision < minRev || revision > maxRev) {
      continue;
    }
    const timestamp = state.index.revision_to_date[String(revision)];
    if (!timestamp) {
      continue;
    }
    const x = new Date(timestamp);
    shapes.push({
      type: 'line',
      xref: 'x',
      yref: 'paper',
      x0: x,
      x1: x,
      y0: 0,
      y1: 1,
      line: {color: 'rgba(120, 120, 120, 0.25)', width: 1, dash: 'dot'},
    });
  }
  return shapes;
}

function matrixLayout(raw, scale, traces) {
  const dateAxis = els.xAxis.value === 'date';
  const range = dateAxis ? dateRangeForRaw(raw) : null;
  return {
    paper_bgcolor: '#ffffff',
    plot_bgcolor: '#ffffff',
    margin: {l: 54, r: 12, t: 8, b: 42},
    hovermode: 'closest',
    showlegend: traces.length > 1,
    legend: {
      orientation: 'h',
      y: -0.28,
      x: 0,
      font: {size: 9},
      itemwidth: 30,
    },
    xaxis: {
      title: dateAxis ? 'Date' : 'ASV revision',
      type: dateAxis ? 'date' : 'linear',
      showgrid: true,
      gridcolor: '#edf0f4',
      zeroline: false,
      tickfont: {size: 10},
      titlefont: {size: 10},
      nticks: 5,
      range: range ? [new Date(range.start), new Date(range.end)] : undefined,
    },
    yaxis: {
      title: scale.unit,
      type: els.logY.checked ? 'log' : 'linear',
      rangemode: els.zeroY.checked && !els.logY.checked ? 'tozero' : 'normal',
      tickformat: ',.3~g',
      showgrid: true,
      gridcolor: '#edf0f4',
      zeroline: false,
      tickfont: {size: 10},
      titlefont: {size: 10},
    },
    colorway: CHART_COLORS,
    shapes: matrixTagShapes(raw),
  };
}

function graphCacheKey(benchmarkName, configIndex) {
  return `${configIndex}\n${benchmarkName}`;
}

async function fetchGraphForConfig(benchmarkName, configIndex) {
  const key = graphCacheKey(benchmarkName, configIndex);
  if (state.graphCache[key]) {
    return state.graphCache[key];
  }

  const raw = await fetchJson(graphUrl(benchmarkName, state.index.graph_param_list[configIndex]));
  state.graphCache[key] = raw;
  return raw;
}

async function forEachWithConcurrency(items, limit, worker) {
  let next = 0;
  const workers = Array.from({length: Math.min(limit, items.length)}, async () => {
    while (next < items.length) {
      const index = next;
      next += 1;
      await worker(items[index], index);
    }
  });
  await Promise.all(workers);
}

function createMatrixCard(benchmarkName) {
  const card = document.createElement('div');
  card.className = 'matrix-card';
  card.title = benchmarkName;

  const title = document.createElement('div');
  title.className = 'matrix-title';
  title.textContent = friendlyBenchmarkName(benchmarkName);

  const plot = document.createElement('div');
  plot.className = 'matrix-plot';

  card.append(title, plot);
  card.addEventListener('dblclick', async () => {
    state.currentBenchmark = benchmarkName;
    els.benchmarkList.value = benchmarkName;
    await switchViewMode('single');
  });
  return {card, title, plot};
}

async function drawMatrix() {
  const drawToken = ++state.drawToken;
  state.graphLoadToken += 1;
  const configIndex = Number(els.configList.value || state.currentConfigIndex || 0);
  state.currentConfigIndex = configIndex;
  syncDateInputs(state.currentRaw || allRevisionRaw());
  els.plotShell.classList.add('matrix');
  clearPlotContainer();

  const names = state.filteredBenchmarks.length ? state.filteredBenchmarks : state.benchmarks;
  if (!names.length) {
    els.plot.innerHTML = '<div class="empty">No benchmarks match the filter.</div>';
    setStatus('No benchmarks match the filter.');
    updateLocationHash();
    return;
  }

  const grid = document.createElement('div');
  grid.className = 'matrix-grid';
  els.plot.append(grid);

  const cards = new Map();
  for (const name of names) {
    const card = createMatrixCard(name);
    cards.set(name, card);
    grid.append(card.card);
  }

  let plotted = 0;
  let empty = 0;
  let failed = 0;
  setStatus(`Loading ${names.length} benchmark charts...`);

  await forEachWithConcurrency(names, 6, async (name) => {
    const {title, plot} = cards.get(name);
    try {
      const benchmark = state.index.benchmarks[name];
      const raw = await fetchGraphForConfig(name, configIndex);
      if (drawToken !== state.drawToken) {
        return;
      }

      const {visibleRaw, traces, scale, seriesTotal, seriesShown} = buildMatrixTraces(raw, benchmark);
      const values = traces.flatMap((trace) => trace.y.filter((v) => v !== null && Number.isFinite(v)));
      if (!visibleRaw.length || !values.length) {
        empty += 1;
        plot.innerHTML = '<div class="empty">No points in range.</div>';
        title.innerHTML = `${escapeHtml(friendlyBenchmarkName(name))}<br><span class="matrix-meta">No points</span>`;
        return;
      }

      const seriesNote = seriesTotal > seriesShown ? ` | ${seriesShown}/${seriesTotal} series` : '';
      title.innerHTML = [
        escapeHtml(friendlyBenchmarkName(name)),
        `<br><span class="matrix-meta">${visibleRaw.length} pts | ${scale.unit}${seriesNote}</span>`,
      ].join('');
      await Plotly.newPlot(plot, traces, matrixLayout(raw, scale, traces), {
        responsive: true,
        displaylogo: false,
        modeBarButtonsToRemove: ['lasso2d', 'select2d'],
      });
      plotted += 1;
    } catch (err) {
      if (drawToken !== state.drawToken) {
        return;
      }
      failed += 1;
      plot.innerHTML = '<div class="empty">No data for this environment.</div>';
      title.innerHTML = `${escapeHtml(friendlyBenchmarkName(name))}<br><span class="matrix-meta">No data</span>`;
    } finally {
      if (drawToken === state.drawToken) {
        const done = plotted + empty + failed;
        setStatus(`Matrix view: ${done}/${names.length} processed; ${plotted} charts shown.`);
      }
    }
  });

  if (drawToken !== state.drawToken) {
    return;
  }
  setStatus(`Matrix view: ${plotted} charts shown, ${empty} empty, ${failed} unavailable.`);
  updateLocationHash();
}

function setViewMode(mode) {
  state.viewMode = mode;
  els.viewToggle.textContent = mode === 'matrix' ? 'Single chart' : 'Matrix view';
  els.plotShell.classList.toggle('matrix', mode === 'matrix');
  updateSeriesControlState();
}

async function switchViewMode(mode) {
  setViewMode(mode);
  updateLocationHash();
  if (mode === 'matrix') {
    await drawMatrix();
  } else {
    if (!state.currentBenchmark && els.benchmarkList.value) {
      state.currentBenchmark = els.benchmarkList.value;
    }
    if (state.currentBenchmark) {
      await loadGraph(true);
    } else {
      clearPlotContainer();
      els.plot.innerHTML = '<div class="empty">Select a benchmark.</div>';
      setStatus('Select a benchmark.');
    }
  }
}

async function renderCurrentView() {
  if (state.viewMode === 'matrix') {
    await drawMatrix();
  } else {
    await drawCurrentGraph();
  }
}

async function drawCurrentGraph() {
  if (state.viewMode !== 'single') {
    return;
  }
  if (!state.currentRaw || !state.currentBenchmark) {
    return;
  }

  const drawToken = ++state.drawToken;
  els.plotShell.classList.remove('matrix');
  const benchmark = state.index.benchmarks[state.currentBenchmark];
  syncDateInputs(state.currentRaw);
  const visibleRaw = visibleRawPoints(state.currentRaw);
  if (!visibleRaw.length) {
    clearPlotContainer();
    els.plot.innerHTML = '<div class="empty">No benchmark points in the selected date range.</div>';
    setStatus('No benchmark points in the selected date range.');
    updateLocationHash();
    return;
  }

  const commitInfo = await loadCommitMetadata(visibleRaw);
  const rangeInfo = await loadCommitRanges(state.currentRaw, visibleRaw, commitInfo);
  if (drawToken !== state.drawToken) {
    return;
  }

  const {traces, scale} = buildTraces(visibleRaw, benchmark, commitInfo, rangeInfo);
  const {shapes, annotations} = tagShapesAndAnnotations(visibleRaw);
  const config = state.currentGraphState;
  const dateAxis = els.xAxis.value === 'date';
  const subtitle = `${config.machine} | ${config.gpu || 'CPU / unknown GPU'} | Python ${config.python}`;
  const range = dateAxis ? dateRangeForRaw(state.currentRaw) : null;

  const layout = {
    title: {
      text: `${friendlyBenchmarkName(state.currentBenchmark)}<br><sup>${subtitle}</sup>`,
      x: 0.02,
      xanchor: 'left',
      font: {size: 20},
    },
    paper_bgcolor: '#ffffff',
    plot_bgcolor: '#ffffff',
    margin: {l: 78, r: 26, t: 82, b: 70},
    hovermode: 'x unified',
    legend: {
      orientation: 'h',
      y: -0.22,
      x: 0,
      font: {size: 11},
    },
    xaxis: {
      title: dateAxis ? 'Commit date' : 'ASV revision',
      type: dateAxis ? 'date' : 'linear',
      showgrid: true,
      gridcolor: '#edf0f4',
      zeroline: false,
      range: range ? [new Date(range.start), new Date(range.end)] : undefined,
      rangeslider: dateAxis ? {visible: true, thickness: 0.08} : undefined,
    },
    yaxis: {
      title: `${scale.title} (${scale.unit})`,
      type: els.logY.checked ? 'log' : 'linear',
      rangemode: els.zeroY.checked && !els.logY.checked ? 'tozero' : 'normal',
      tickformat: ',.4~g',
      showgrid: true,
      gridcolor: '#edf0f4',
      zeroline: false,
    },
    colorway: CHART_COLORS,
    shapes,
    annotations,
  };

  const separateAxes = els.separateYAxes.checked && applySeparateYAxes(layout, traces, scale);
  clearPlotContainer();
  Plotly.newPlot(els.plot, traces, layout, {
    responsive: true,
    displaylogo: false,
    modeBarButtonsToRemove: ['lasso2d', 'select2d'],
    toImageButtonOptions: {
      format: 'png',
      filename: 'newton-asv-' + state.currentBenchmark.replace(/[^a-zA-Z0-9_.-]/g, '_'),
      scale: 2,
    },
  });

  const values = traces.flatMap((trace) => trace.y.filter((v) => v !== null && Number.isFinite(v)));
  const lastValue = values.length ? values[values.length - 1] : null;
  const valueText = lastValue === null ? 'no values' : `${lastValue.toPrecision(5)} ${scale.unit}`;
  const axisText = separateAxes ? '; separate y-axes enabled' : '';
  setStatus(
    `${visibleRaw.length} visible of ${state.currentRaw.length} revisions; ` +
    `latest visible value ${valueText}${axisText}.`
  );
}

async function fetchJson(url) {
  const response = await fetch(url);
  if (!response.ok) {
    const message = await response.text();
    throw new Error(message || `${response.status} ${response.statusText}`);
  }
  return response.json();
}

function graphUrl(benchmarkName, config) {
  const query = new URLSearchParams({
    benchmark: benchmarkName,
    state: JSON.stringify(config),
  });
  return '/api/graph?' + query.toString();
}

async function loadGraph(allowFallback) {
  const benchmarkName = state.currentBenchmark;
  if (!benchmarkName) {
    return;
  }
  const loadToken = ++state.graphLoadToken;
  const configs = state.index.graph_param_list;
  let start = Number(els.configList.value || 0);
  const attempts = allowFallback ? configs.length : 1;
  let lastError = null;

  setStatus('Loading graph data...');

  for (let offset = 0; offset < attempts; ++offset) {
    const configIndex = (start + offset) % configs.length;
    const config = configs[configIndex];
    try {
      const raw = await fetchJson(graphUrl(benchmarkName, config));
      if (loadToken !== state.graphLoadToken || state.viewMode !== 'single') {
        return;
      }
      state.currentConfigIndex = configIndex;
      state.currentRaw = raw;
      state.currentGraphBenchmark = benchmarkName;
      state.currentGraphConfigIndex = configIndex;
      state.currentGraphState = config;
      els.configList.value = String(configIndex);
      updateSeriesList(state.index.benchmarks[benchmarkName]);
      updateLocationHash();
      await drawCurrentGraph();
      return;
    } catch (err) {
      lastError = err;
    }
  }

  if (loadToken !== state.graphLoadToken || state.viewMode !== 'single') {
    return;
  }
  state.currentRaw = null;
  state.currentGraphBenchmark = null;
  state.currentGraphConfigIndex = null;
  state.currentGraphState = null;
  clearPlotContainer();
  els.plot.innerHTML = '<div class="empty">No graph data for the selected benchmark and environment.</div>';
  setStatus('No graph data found. ' + (lastError ? lastError.message : ''));
}

function applyBenchmarkFilter() {
  const q = els.filter.value.trim().toLowerCase();
  state.filteredBenchmarks = state.benchmarks.filter((name) => compactBenchmarkLabel(name).toLowerCase().includes(q));
  els.benchmarkList.textContent = '';
  for (const name of state.filteredBenchmarks) {
    const option = new Option(compactBenchmarkLabel(name), name);
    option.title = name;
    els.benchmarkList.add(option);
  }
  els.benchmarkCount.textContent = `(${state.filteredBenchmarks.length})`;

  if (state.currentBenchmark && state.filteredBenchmarks.includes(state.currentBenchmark)) {
    els.benchmarkList.value = state.currentBenchmark;
  } else if (state.filteredBenchmarks.length) {
    els.benchmarkList.value = state.filteredBenchmarks[0];
  }
}

function loadFromLocationHash() {
  const params = new URLSearchParams(location.hash.replace(/^#/, ''));
  const benchmark = params.get('benchmark');
  const config = params.get('config');
  const series = params.get('series');
  const xAxis = params.get('x');
  const range = params.get('range');
  const from = params.get('from');
  const to = params.get('to');
  const last = params.get('last');
  const view = params.get('view');
  const axes = params.get('axes');
  if (benchmark && state.index.benchmarks[benchmark]) {
    state.currentBenchmark = benchmark;
  }
  if (config !== null) {
    const index = Number(config);
    if (Number.isInteger(index) && index >= 0 && index < state.index.graph_param_list.length) {
      state.currentConfigIndex = index;
      els.configList.value = String(index);
    }
  }
  if (series) {
    els.seriesList.dataset.pendingSelection = series;
  }
  if (xAxis === 'date' || xAxis === 'revision') {
    els.xAxis.value = xAxis;
  }
  if (['all', '30d', '90d', '6m', '1y', 'custom'].includes(range)) {
    els.dateRange.value = range;
  }
  if (from) {
    els.dateStart.value = from;
  }
  if (to) {
    els.dateEnd.value = to;
  }
  if (last !== null && Number.isFinite(Number(last))) {
    els.lastPoints.value = last;
  }
  if (axes === 'shared') {
    els.separateYAxes.checked = false;
  } else if (axes === 'separate') {
    els.separateYAxes.checked = true;
  }
  if (view === 'matrix') {
    state.viewMode = 'matrix';
  }
}

function updateLocationHash() {
  const params = new URLSearchParams();
  if (state.viewMode === 'matrix') {
    params.set('view', 'matrix');
  }
  if (state.currentBenchmark) {
    params.set('benchmark', state.currentBenchmark);
  }
  params.set('config', String(state.currentConfigIndex));
  if (els.xAxis.value !== 'date') {
    params.set('x', els.xAxis.value);
  }
  if (els.dateRange.value !== 'all') {
    params.set('range', els.dateRange.value);
  }
  if (els.dateRange.value === 'custom') {
    if (els.dateStart.value) {
      params.set('from', els.dateStart.value);
    }
    if (els.dateEnd.value) {
      params.set('to', els.dateEnd.value);
    }
  }
  if (Number(els.lastPoints.value || 0) > 0) {
    params.set('last', els.lastPoints.value);
  }
  if (state.viewMode === 'single' && !els.separateYAxes.checked) {
    params.set('axes', 'shared');
  }
  const selected = selectedSeriesIndices();
  if (state.viewMode === 'single' && els.allSeries.checked) {
    params.set('series', 'all');
  } else if (state.viewMode === 'single' && selected.length) {
    params.set('series', selected.join(','));
  }
  history.replaceState(null, '', '#' + params.toString());
}

function applyPendingSeriesSelection() {
  const pending = els.seriesList.dataset.pendingSelection;
  if (!pending) {
    return;
  }
  if (pending === 'all') {
    els.allSeries.checked = true;
    for (const option of els.seriesList.options) {
      option.selected = true;
    }
    delete els.seriesList.dataset.pendingSelection;
    updateSeriesControlState();
    return;
  }
  els.allSeries.checked = false;
  const wanted = new Set(pending.split(',').map((v) => Number(v)));
  for (const option of els.seriesList.options) {
    option.selected = wanted.has(Number(option.value));
  }
  delete els.seriesList.dataset.pendingSelection;
  updateSeriesControlState();
}

async function init() {
  const meta = await fetchJson('/api/meta');
  els.sourceLink.href = meta.source_url;
  els.sourceLink.textContent = meta.source_url;

  state.index = await fetchJson('/api/index');
  state.benchmarks = Object.keys(state.index.benchmarks).sort();

  for (const [i, config] of state.index.graph_param_list.entries()) {
    els.configList.add(new Option(configLabel(config), String(i)));
  }

  loadFromLocationHash();
  applyBenchmarkFilter();
  if (state.currentBenchmark) {
    els.benchmarkList.value = state.currentBenchmark;
  }
  els.configList.value = String(state.currentConfigIndex);
  setViewMode(state.viewMode);
  if (state.viewMode === 'matrix') {
    await drawMatrix();
  } else {
    await loadGraph(true);
    applyPendingSeriesSelection();
    await drawCurrentGraph();
  }
}

async function selectBenchmarkFromList(force) {
  const benchmark = els.benchmarkList.value;
  if (!benchmark) {
    return;
  }
  const selectedConfigIndex = Number(els.configList.value || 0);
  const graphAlreadyCurrent =
    benchmark === state.currentGraphBenchmark &&
    selectedConfigIndex === state.currentGraphConfigIndex &&
    state.currentRaw;
  if (!force && graphAlreadyCurrent) {
    return;
  }
  state.currentBenchmark = benchmark;
  updateLocationHash();
  if (state.viewMode === 'matrix') {
    if (force) {
      await switchViewMode('single');
    }
    return;
  }
  await loadGraph(true);
}

els.filter.addEventListener('input', () => {
  applyBenchmarkFilter();
  if (state.viewMode === 'matrix') {
    drawMatrix();
  }
});
els.benchmarkList.addEventListener('input', () => {
  selectBenchmarkFromList(false);
});
els.benchmarkList.addEventListener('change', () => {
  selectBenchmarkFromList(false);
});
els.benchmarkList.addEventListener('click', () => {
  selectBenchmarkFromList(false);
});
els.benchmarkList.addEventListener('dblclick', () => {
  selectBenchmarkFromList(true);
});
els.benchmarkList.addEventListener('keydown', (event) => {
  if (event.key === 'Enter') {
    selectBenchmarkFromList(true);
  }
});
els.configList.addEventListener('change', async () => {
  state.currentConfigIndex = Number(els.configList.value);
  updateLocationHash();
  if (state.viewMode === 'matrix') {
    await drawMatrix();
  } else {
    await loadGraph(false);
  }
});
els.seriesList.addEventListener('change', () => {
  updateLocationHash();
  renderCurrentView();
});
els.allSeries.addEventListener('change', () => {
  if (els.allSeries.checked) {
    for (const option of els.seriesList.options) {
      option.selected = true;
    }
  }
  updateSeriesControlState();
  updateLocationHash();
  renderCurrentView();
});
els.separateYAxes.addEventListener('change', () => {
  updateLocationHash();
  renderCurrentView();
});
for (const el of [els.xAxis, els.dateRange, els.lastPoints, els.logY, els.zeroY, els.showTags, els.lines]) {
  el.addEventListener('change', () => {
    updateLocationHash();
    renderCurrentView();
  });
}
for (const el of [els.dateStart, els.dateEnd]) {
  el.addEventListener('change', () => {
    els.dateRange.value = 'custom';
    updateLocationHash();
    renderCurrentView();
  });
}
els.refresh.addEventListener('click', async () => {
  if (state.viewMode === 'matrix') {
    state.graphCache = {};
    await drawMatrix();
  } else {
    await loadGraph(false);
  }
});
els.viewToggle.addEventListener('click', async () => {
  await switchViewMode(state.viewMode === 'matrix' ? 'single' : 'matrix');
});
els.copyUrl.addEventListener('click', async () => {
  updateLocationHash();
  await navigator.clipboard.writeText(location.href);
  setStatus('Copied current view URL.');
});

init().catch((err) => {
  els.plot.innerHTML = '<div class="empty">Failed to load ASV data.</div>';
  setStatus(err.message);
  console.error(err);
});
</script>
</body>
</html>
"""


def sanitize_filename(name: str) -> str:
    """Match ``asv.util.sanitize_filename`` for graph JSON paths."""
    bad_names = {
        "CON",
        "PRN",
        "AUX",
        "NUL",
        "COM1",
        "COM2",
        "COM3",
        "COM4",
        "COM5",
        "COM6",
        "COM7",
        "COM8",
        "COM9",
        "LPT1",
        "LPT2",
        "LPT3",
        "LPT4",
        "LPT5",
        "LPT6",
        "LPT7",
        "LPT8",
        "LPT9",
    }
    bad_chars = '<>:"/\\^|?*'
    cleaned = "".join("_" if c in bad_chars or ord(c) < 32 else c for c in name)
    if cleaned.upper() in bad_names:
        cleaned += "_"
    return cleaned


def graph_path(benchmark_name: str, state: dict[str, Any]) -> str:
    """Build the ASV graph JSON path for a benchmark and machine state."""
    parts: list[str] = []
    for key, value in state.items():
        if value is None:
            part = f"{key}-null"
        elif value:
            part = f"{key}-{value}"
        else:
            part = key
        parts.append(sanitize_filename(str(part)))
    parts.sort()
    parts.insert(0, "graphs")
    parts.append(sanitize_filename(benchmark_name))
    quoted = [urllib.parse.quote(part, safe="") for part in parts]
    return "/".join(quoted) + ".json"


class AsvDataProxy:
    """Small read-through cache for the published ASV static files."""

    def __init__(self, source_url: str, timeout: float, git_repo: str) -> None:
        self.source_url = source_url.rstrip("/") + "/"
        self.timeout = timeout
        self.git_repo = git_repo
        self._cache: dict[str, bytes] = {}
        self._commit_cache: dict[str, dict[str, str]] = {}
        self._commit_range_cache: dict[str, dict[str, Any]] = {}
        self._lock = threading.Lock()

    def fetch(self, path: str) -> bytes:
        with self._lock:
            cached = self._cache.get(path)
        if cached is not None:
            return cached

        url = urllib.parse.urljoin(self.source_url, path)
        request = urllib.request.Request(url, headers={"User-Agent": "newton-asv-viewer/1.0"})
        with urllib.request.urlopen(request, timeout=self.timeout) as response:
            data = response.read()

        with self._lock:
            self._cache[path] = data
        return data

    def fetch_commit(self, commit_hash: str) -> dict[str, str]:
        """Fetch and cache GitHub commit metadata for tooltip enrichment."""
        normalized_hash = commit_hash.strip()
        self.validate_commit_hash(normalized_hash, "commit hash")

        with self._lock:
            cached = self._commit_cache.get(normalized_hash)
        if cached is not None:
            return cached

        result = self.fetch_local_commit(normalized_hash)
        if result is None:
            result = self.fetch_github_commit(normalized_hash)

        with self._lock:
            self._commit_cache[normalized_hash] = result
        return result

    def fetch_github_commit(self, commit_hash: str) -> dict[str, str]:
        url = f"https://api.github.com/repos/newton-physics/newton/commits/{commit_hash}"
        request = urllib.request.Request(
            url,
            headers={
                "Accept": "application/vnd.github+json",
                "User-Agent": "newton-asv-viewer/1.0",
            },
        )
        try:
            with urllib.request.urlopen(request, timeout=self.timeout) as response:
                raw_data = response.read()
            data = json.loads(raw_data)
            return self.parse_github_commit_metadata(commit_hash, data)
        except urllib.error.HTTPError as exc:
            return self.commit_error_metadata(commit_hash, f"GitHub returned HTTP {exc.code}")
        except urllib.error.URLError as exc:
            return self.commit_error_metadata(commit_hash, f"Could not reach GitHub: {exc.reason}")

    def fetch_local_commit(self, commit_hash: str) -> dict[str, str] | None:
        output = self.run_git(
            [
                "log",
                "-1",
                "--format=format:%H%x1f%an%x1f%aI%x1f%s%x1f%b%x1e",
                commit_hash,
            ]
        )
        commits = self.parse_git_commit_records(output)
        return commits[0] if commits else None

    def fetch_commit_range(self, pair: str) -> dict[str, Any]:
        """Fetch commits after the previous measured hash through the measured hash."""
        try:
            base_hash, head_hash = [part.strip() for part in pair.split("..", 1)]
        except ValueError as exc:
            raise ValueError(f"Invalid commit range: {pair!r}") from exc

        self.validate_commit_hash(base_hash, "base commit hash")
        self.validate_commit_hash(head_hash, "head commit hash")

        cache_key = f"{base_hash}..{head_hash}"
        with self._lock:
            cached = self._commit_range_cache.get(cache_key)
        if cached is not None:
            return cached

        compare_url = f"https://github.com/newton-physics/newton/compare/{base_hash}...{head_hash}"
        local_result = self.fetch_local_commit_range(base_hash, head_hash, compare_url)
        if local_result is not None:
            result = local_result
        elif base_hash == head_hash:
            result: dict[str, Any] = {"count": 0, "commits": [], "url": compare_url}
        else:
            api_url = f"https://api.github.com/repos/newton-physics/newton/compare/{base_hash}...{head_hash}"
            request = urllib.request.Request(
                api_url,
                headers={
                    "Accept": "application/vnd.github+json",
                    "User-Agent": "newton-asv-viewer/1.0",
                },
            )
            try:
                with urllib.request.urlopen(request, timeout=self.timeout) as response:
                    raw_data = response.read()
                data = json.loads(raw_data)
                commits = [
                    self.parse_github_commit_metadata(str(commit.get("sha") or ""), commit)
                    for commit in data.get("commits", [])
                    if isinstance(commit, dict)
                ]
                result = {
                    "count": len(commits),
                    "commits": commits,
                    "url": str(data.get("html_url") or compare_url),
                }
            except urllib.error.HTTPError as exc:
                result = self.commit_range_error_metadata(
                    head_hash,
                    compare_url,
                    f"GitHub returned HTTP {exc.code}",
                )
            except urllib.error.URLError as exc:
                result = self.commit_range_error_metadata(
                    head_hash,
                    compare_url,
                    f"Could not reach GitHub: {exc.reason}",
                )

        with self._lock:
            self._commit_range_cache[cache_key] = result
        return result

    def fetch_local_commit_range(self, base_hash: str, head_hash: str, compare_url: str) -> dict[str, Any] | None:
        if base_hash == head_hash:
            return {"count": 0, "commits": [], "url": compare_url, "source": "local git"}

        output = self.run_git(
            [
                "log",
                "--reverse",
                "--format=format:%H%x1f%an%x1f%aI%x1f%s%x1f%b%x1e",
                f"{base_hash}..{head_hash}",
            ]
        )
        if output is None:
            return None

        commits = self.parse_git_commit_records(output)
        return {
            "count": len(commits),
            "commits": commits,
            "url": compare_url,
            "source": "local git",
        }

    def run_git(self, args: list[str]) -> str | None:
        try:
            completed = subprocess.run(
                ["git", "-C", self.git_repo, *args],
                capture_output=True,
                check=False,
                encoding="utf-8",
                errors="replace",
                timeout=self.timeout,
            )
        except (FileNotFoundError, subprocess.SubprocessError, TimeoutError):
            return None
        if completed.returncode != 0:
            return None
        return completed.stdout

    @staticmethod
    def validate_commit_hash(commit_hash: str, label: str) -> None:
        if not commit_hash or any(c not in "0123456789abcdefABCDEF" for c in commit_hash):
            raise ValueError(f"Invalid {label}: {commit_hash!r}")

    @staticmethod
    def parse_git_commit_records(output: str | None) -> list[dict[str, str]]:
        if not output:
            return []

        commits = []
        for record in output.strip("\x1e\n").split("\x1e"):
            record = record.strip("\n")
            if not record:
                continue
            parts = record.split("\x1f", 4)
            if len(parts) < 5:
                continue
            full_hash, author, date, subject, body = parts
            body_line = next((line.strip() for line in body.splitlines() if line.strip()), "")
            commits.append(
                {
                    "short_hash": full_hash[:8],
                    "full_hash": full_hash,
                    "author": author,
                    "date": date,
                    "subject": subject.strip(),
                    "body": body_line,
                    "url": f"https://github.com/newton-physics/newton/commit/{full_hash}",
                }
            )
        return commits

    @staticmethod
    def parse_github_commit_metadata(commit_hash: str, data: dict[str, Any]) -> dict[str, str]:
        commit = data.get("commit") or {}
        author = commit.get("author") or {}
        github_author = data.get("author") or {}
        message = str(commit.get("message") or "")
        lines = message.splitlines()
        subject = lines[0].strip() if lines else ""
        body = next((line.strip() for line in lines[1:] if line.strip()), "")
        author_name = str(author.get("name") or "")
        author_login = str(github_author.get("login") or "")
        if author_login and author_login != author_name:
            author_name = f"{author_name} ({author_login})" if author_name else author_login

        full_hash = str(data.get("sha") or commit_hash)
        return {
            "short_hash": full_hash[:8],
            "full_hash": full_hash,
            "author": author_name,
            "date": str(author.get("date") or ""),
            "subject": subject,
            "body": body,
            "url": str(data.get("html_url") or f"https://github.com/newton-physics/newton/commit/{full_hash}"),
        }

    @staticmethod
    def commit_error_metadata(commit_hash: str, message: str) -> dict[str, str]:
        return {
            "short_hash": commit_hash[:8],
            "full_hash": commit_hash,
            "author": "",
            "date": "",
            "subject": "Commit metadata unavailable",
            "body": message,
            "url": f"https://github.com/newton-physics/newton/commit/{commit_hash}",
        }

    def commit_range_error_metadata(self, head_hash: str, compare_url: str, message: str) -> dict[str, Any]:
        return {
            "count": 1,
            "commits": [self.commit_error_metadata(head_hash, message)],
            "url": compare_url,
        }


class AsvViewerHandler(BaseHTTPRequestHandler):
    """HTTP handler for the local ASV viewer."""

    proxy: AsvDataProxy

    def log_message(self, format: str, *args: Any) -> None:
        sys.stderr.write(f"{self.address_string()} - {format % args}\n")

    def send_bytes(self, data: bytes, content_type: str, status: HTTPStatus = HTTPStatus.OK) -> None:
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(data)

    def send_json(self, payload: Any, status: HTTPStatus = HTTPStatus.OK) -> None:
        data = json.dumps(payload).encode("utf-8")
        self.send_bytes(data, "application/json; charset=utf-8", status)

    def send_error_json(self, status: HTTPStatus, message: str) -> None:
        self.send_json({"error": message}, status)

    def do_GET(self) -> None:
        parsed = urllib.parse.urlparse(self.path)
        try:
            if parsed.path == "/":
                self.send_bytes(HTML.encode("utf-8"), "text/html; charset=utf-8")
            elif parsed.path == "/api/meta":
                self.send_json({"source_url": self.proxy.source_url})
            elif parsed.path == "/api/index":
                self.send_bytes(self.proxy.fetch("index.json"), "application/json; charset=utf-8")
            elif parsed.path == "/api/info":
                self.send_bytes(self.proxy.fetch("info.json"), "application/json; charset=utf-8")
            elif parsed.path == "/api/graph":
                self.handle_graph(parsed.query)
            elif parsed.path == "/api/commits":
                self.handle_commits(parsed.query)
            elif parsed.path == "/api/commit-ranges":
                self.handle_commit_ranges(parsed.query)
            else:
                self.send_error_json(HTTPStatus.NOT_FOUND, "Not found")
        except urllib.error.HTTPError as exc:
            self.send_error_json(HTTPStatus(exc.code), f"Upstream returned HTTP {exc.code}")
        except urllib.error.URLError as exc:
            self.send_error_json(HTTPStatus.BAD_GATEWAY, f"Could not reach ASV source: {exc.reason}")
        except TimeoutError:
            self.send_error_json(HTTPStatus.GATEWAY_TIMEOUT, "Timed out reaching ASV source")
        except ValueError as exc:
            self.send_error_json(HTTPStatus.BAD_REQUEST, str(exc))

    def handle_graph(self, query: str) -> None:
        params = urllib.parse.parse_qs(query)
        benchmark_values = params.get("benchmark")
        state_values = params.get("state")
        if not benchmark_values or not state_values:
            raise ValueError("Missing benchmark or state query parameter")

        benchmark_name = benchmark_values[0]
        state = json.loads(state_values[0])
        if not isinstance(state, dict):
            raise ValueError("Graph state must be a JSON object")

        path = graph_path(benchmark_name, state)
        self.send_bytes(self.proxy.fetch(path), "application/json; charset=utf-8")

    def handle_commits(self, query: str) -> None:
        params = urllib.parse.parse_qs(query)
        hashes_value = params.get("hashes", [""])[0]
        hashes = [commit_hash.strip() for commit_hash in hashes_value.split(",") if commit_hash.strip()]
        if len(hashes) > 100:
            raise ValueError("At most 100 commit hashes can be requested at once")

        result = {commit_hash: self.proxy.fetch_commit(commit_hash) for commit_hash in hashes}
        self.send_json(result)

    def handle_commit_ranges(self, query: str) -> None:
        params = urllib.parse.parse_qs(query)
        pairs_value = params.get("pairs", [""])[0]
        pairs = [pair.strip() for pair in pairs_value.split(",") if pair.strip()]
        if len(pairs) > 100:
            raise ValueError("At most 100 commit ranges can be requested at once")

        result = {pair: self.proxy.fetch_commit_range(pair) for pair in pairs}
        self.send_json(result)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-url", default=DEFAULT_SOURCE_URL, help="Published ASV site URL.")
    parser.add_argument("--git-repo", default=".", help="Local Newton git repository used for commit metadata.")
    parser.add_argument("--host", default=DEFAULT_HOST, help="Host interface for the local server.")
    parser.add_argument("--port", type=int, default=DEFAULT_PORT, help="Port for the local server.")
    parser.add_argument("--timeout", type=float, default=30.0, help="Timeout for upstream ASV requests.")
    parser.add_argument("--no-browser", action="store_true", help="Do not open the viewer in a browser.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    AsvViewerHandler.proxy = AsvDataProxy(args.source_url, args.timeout, args.git_repo)
    server = ThreadingHTTPServer((args.host, args.port), AsvViewerHandler)
    url = f"http://{args.host}:{args.port}/"
    print(f"Serving Newton ASV viewer at {url}")
    print(f"Using ASV data source {AsvViewerHandler.proxy.source_url}")

    if not args.no_browser:
        webbrowser.open(url)

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping ASV viewer.")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
