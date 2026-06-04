"""
Meridian Customer Promise Control Tower
========================================
A high-fidelity interactive prototype for PwC Advisory.

This Python file generates a complete HTML/CSS/JavaScript web application
and serves it locally. No external dependencies required.

Run: python meridian_control_tower.py
"""

import http.server
import socketserver
import webbrowser
import os
import threading

HTML_CONTENT = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Meridian Customer Promise Control Tower</title>
<style>
:root {
    --primary: #1B2A4A;
    --primary-light: #2D4A7A;
    --accent: #D4632A;
    --accent-light: #E8845A;
    --success: #2E7D4F;
    --warning: #D4892A;
    --danger: #C0392B;
    --bg: #F4F6F9;
    --card: #FFFFFF;
    --text: #1B2A4A;
    --text-light: #5A6B8A;
    --border: #E2E8F0;
    --sidebar-width: 260px;
    --header-height: 64px;
}

* { margin: 0; padding: 0; box-sizing: border-box; }

body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    background: var(--bg);
    color: var(--text);
    line-height: 1.5;
    overflow-x: hidden;
}

/* Sidebar */
.sidebar {
    position: fixed;
    left: 0;
    top: 0;
    width: var(--sidebar-width);
    height: 100vh;
    background: var(--primary);
    color: #fff;
    z-index: 1000;
    display: flex;
    flex-direction: column;
    overflow-y: auto;
}

.sidebar-brand {
    padding: 20px 20px 10px;
    border-bottom: 1px solid rgba(255,255,255,0.1);
}

.sidebar-brand h2 {
    font-size: 15px;
    font-weight: 700;
    letter-spacing: 0.5px;
    color: #fff;
}

.sidebar-brand .subtitle {
    font-size: 11px;
    color: rgba(255,255,255,0.6);
    margin-top: 4px;
}

.sidebar-brand .pwc-label {
    font-size: 10px;
    color: var(--accent-light);
    margin-top: 8px;
    text-transform: uppercase;
    letter-spacing: 1px;
}

.sidebar-nav {
    padding: 16px 0;
    flex: 1;
}

.nav-item {
    display: flex;
    align-items: center;
    padding: 12px 20px;
    color: rgba(255,255,255,0.7);
    cursor: pointer;
    transition: all 0.2s;
    font-size: 13px;
    border-left: 3px solid transparent;
}

.nav-item:hover {
    background: rgba(255,255,255,0.05);
    color: #fff;
}

.nav-item.active {
    background: rgba(255,255,255,0.1);
    color: #fff;
    border-left-color: var(--accent);
}

.nav-icon {
    width: 20px;
    height: 20px;
    margin-right: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 14px;
}

.role-switcher {
    padding: 16px 20px;
    border-top: 1px solid rgba(255,255,255,0.1);
}

.role-switcher label {
    font-size: 10px;
    text-transform: uppercase;
    letter-spacing: 1px;
    color: rgba(255,255,255,0.5);
    display: block;
    margin-bottom: 8px;
}

.role-switcher select {
    width: 100%;
    padding: 8px 12px;
    background: rgba(255,255,255,0.1);
    border: 1px solid rgba(255,255,255,0.2);
    color: #fff;
    border-radius: 6px;
    font-size: 12px;
    cursor: pointer;
}

.role-switcher select option {
    background: var(--primary);
    color: #fff;
}

/* Header */
.header {
    position: fixed;
    top: 0;
    left: var(--sidebar-width);
    right: 0;
    height: var(--header-height);
    background: #fff;
    border-bottom: 1px solid var(--border);
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 32px;
    z-index: 999;
}

.header-title {
    font-size: 18px;
    font-weight: 600;
    color: var(--text);
}

.header-meta {
    display: flex;
    align-items: center;
    gap: 20px;
}

.sprint-badge {
    background: var(--primary);
    color: #fff;
    padding: 6px 14px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 500;
}

.header-date {
    font-size: 13px;
    color: var(--text-light);
}

/* Main Content */
.main {
    margin-left: var(--sidebar-width);
    margin-top: var(--header-height);
    padding: 28px 32px;
    min-height: calc(100vh - var(--header-height));
}

/* Screen container */
.screen { display: none; }
.screen.active { display: block; }

/* Cards */
.card {
    background: var(--card);
    border-radius: 12px;
    padding: 24px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.06), 0 1px 2px rgba(0,0,0,0.04);
    border: 1px solid var(--border);
}

.card-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 16px;
}

.card-title {
    font-size: 14px;
    font-weight: 600;
    color: var(--text);
}

/* KPI Cards */
.kpi-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 16px;
    margin-bottom: 24px;
}

.kpi-card {
    background: #fff;
    border-radius: 12px;
    padding: 20px;
    border: 1px solid var(--border);
    box-shadow: 0 1px 3px rgba(0,0,0,0.04);
}

.kpi-label {
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    color: var(--text-light);
    margin-bottom: 8px;
}

.kpi-value {
    font-size: 28px;
    font-weight: 700;
    color: var(--text);
}

.kpi-change {
    font-size: 12px;
    margin-top: 6px;
    font-weight: 500;
}

.kpi-change.positive { color: var(--success); }
.kpi-change.negative { color: var(--danger); }

/* Score Circle */
.score-circle {
    width: 140px;
    height: 140px;
    border-radius: 50%;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    margin: 0 auto;
    position: relative;
}

.score-circle .score-value {
    font-size: 42px;
    font-weight: 800;
    color: var(--primary);
}

.score-circle .score-label {
    font-size: 11px;
    color: var(--text-light);
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

/* Alerts */
.alert-list { list-style: none; }

.alert-item {
    display: flex;
    align-items: flex-start;
    padding: 14px 16px;
    border-radius: 8px;
    margin-bottom: 8px;
    background: #FFF8F5;
    border-left: 4px solid var(--accent);
    cursor: pointer;
    transition: all 0.2s;
}

.alert-item:hover {
    background: #FFF0EA;
}

.alert-item.acknowledged {
    opacity: 0.5;
    background: #F8F9FA;
    border-left-color: #CCC;
}

.alert-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: var(--accent);
    margin-top: 6px;
    margin-right: 12px;
    flex-shrink: 0;
}

.alert-item.acknowledged .alert-dot { background: #CCC; }

.alert-text {
    font-size: 13px;
    color: var(--text);
    flex: 1;
}

.alert-ack-btn {
    font-size: 11px;
    color: var(--text-light);
    background: none;
    border: 1px solid var(--border);
    padding: 4px 10px;
    border-radius: 4px;
    cursor: pointer;
    margin-left: 12px;
    white-space: nowrap;
}

.alert-ack-btn:hover { background: var(--bg); }

/* Decision Panel */
.decision-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    gap: 12px;
}

.decision-card {
    background: #F8FAFC;
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 16px;
    cursor: pointer;
    transition: all 0.2s;
}

.decision-card:hover {
    border-color: var(--primary-light);
    box-shadow: 0 2px 8px rgba(0,0,0,0.08);
}

.decision-card.approved {
    background: #F0FAF4;
    border-color: var(--success);
}

.decision-card .decision-title {
    font-size: 13px;
    font-weight: 600;
    margin-bottom: 6px;
}

.decision-card .decision-status {
    font-size: 11px;
    color: var(--text-light);
}

.decision-card.approved .decision-status {
    color: var(--success);
    font-weight: 600;
}

/* Charts */
.chart-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 16px;
    margin-bottom: 24px;
}

.chart-container {
    background: #fff;
    border-radius: 12px;
    padding: 20px;
    border: 1px solid var(--border);
}

.chart-title {
    font-size: 12px;
    font-weight: 600;
    color: var(--text-light);
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-bottom: 16px;
}

canvas { width: 100% !important; height: 160px !important; }

/* Tables */
.data-table {
    width: 100%;
    border-collapse: separate;
    border-spacing: 0;
    font-size: 13px;
}

.data-table thead th {
    background: #F8FAFC;
    padding: 12px 14px;
    text-align: left;
    font-weight: 600;
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    color: var(--text-light);
    border-bottom: 1px solid var(--border);
    position: sticky;
    top: 0;
    z-index: 1;
}

.data-table tbody tr {
    cursor: pointer;
    transition: background 0.15s;
}

.data-table tbody tr:hover { background: #F8FAFC; }

.data-table tbody td {
    padding: 14px;
    border-bottom: 1px solid var(--border);
    vertical-align: middle;
}

/* Status Chips */
.chip {
    display: inline-block;
    padding: 4px 10px;
    border-radius: 12px;
    font-size: 11px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.3px;
}

.chip-critical { background: #FDE8E8; color: var(--danger); }
.chip-watch { background: #FEF3CD; color: #856404; }
.chip-healthy { background: #D4EDDA; color: var(--success); }
.chip-high { background: #FDE8E8; color: var(--danger); }
.chip-medium { background: #FEF3CD; color: #856404; }
.chip-low { background: #D4EDDA; color: var(--success); }
.chip-pending { background: #E8EDFF; color: #3B5BDB; }
.chip-inprogress { background: #FEF3CD; color: #856404; }
.chip-completed { background: #D4EDDA; color: var(--success); }
.chip-ready { background: #E8F4FD; color: #1976D2; }
.chip-notstarted { background: #F5F5F5; color: #666; }

/* Buttons */
.btn {
    padding: 10px 18px;
    border-radius: 8px;
    font-size: 13px;
    font-weight: 600;
    cursor: pointer;
    border: none;
    transition: all 0.2s;
    display: inline-flex;
    align-items: center;
    gap: 6px;
}

.btn-primary { background: var(--primary); color: #fff; }
.btn-primary:hover { background: var(--primary-light); }
.btn-accent { background: var(--accent); color: #fff; }
.btn-accent:hover { background: var(--accent-light); }
.btn-success { background: var(--success); color: #fff; }
.btn-success:hover { background: #3a9463; }
.btn-outline { background: transparent; border: 1px solid var(--border); color: var(--text); }
.btn-outline:hover { background: var(--bg); }
.btn-sm { padding: 6px 12px; font-size: 12px; }

/* Filters */
.filters-row {
    display: flex;
    gap: 12px;
    margin-bottom: 20px;
    flex-wrap: wrap;
    align-items: center;
}

.filter-input, .filter-select {
    padding: 9px 14px;
    border: 1px solid var(--border);
    border-radius: 8px;
    font-size: 13px;
    background: #fff;
    color: var(--text);
    min-width: 160px;
}

.filter-input:focus, .filter-select:focus {
    outline: none;
    border-color: var(--primary-light);
    box-shadow: 0 0 0 3px rgba(45,74,122,0.1);
}

/* Progress Bar */
.progress-bar {
    height: 8px;
    background: var(--bg);
    border-radius: 4px;
    overflow: hidden;
}

.progress-fill {
    height: 100%;
    border-radius: 4px;
    transition: width 0.5s ease;
}

.progress-fill.blue { background: var(--primary-light); }
.progress-fill.green { background: var(--success); }
.progress-fill.orange { background: var(--warning); }
.progress-fill.red { background: var(--danger); }

/* Grid layouts */
.grid-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 24px; }
.grid-3 { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 24px; }

/* Section header */
.section-header {
    font-size: 16px;
    font-weight: 700;
    color: var(--text);
    margin-bottom: 16px;
    display: flex;
    align-items: center;
    gap: 8px;
}

.section-subheader {
    font-size: 13px;
    color: var(--text-light);
    margin-bottom: 20px;
}

/* Mobile App Mock */
.mobile-frame {
    width: 380px;
    height: 720px;
    background: #fff;
    border-radius: 32px;
    border: 8px solid #222;
    margin: 0 auto;
    overflow-y: auto;
    box-shadow: 0 20px 60px rgba(0,0,0,0.2);
    position: relative;
}

.mobile-header {
    background: var(--primary);
    color: #fff;
    padding: 20px 16px 16px;
    position: sticky;
    top: 0;
    z-index: 10;
}

.mobile-header h3 {
    font-size: 16px;
    font-weight: 600;
}

.mobile-search {
    margin-top: 12px;
    padding: 10px 14px;
    background: rgba(255,255,255,0.15);
    border: none;
    border-radius: 8px;
    color: #fff;
    width: 100%;
    font-size: 13px;
}

.mobile-search::placeholder { color: rgba(255,255,255,0.6); }

.mobile-content { padding: 16px; }

.mobile-card {
    background: #F8FAFC;
    border-radius: 12px;
    padding: 16px;
    margin-bottom: 12px;
    border: 1px solid var(--border);
}

.mobile-card h4 {
    font-size: 14px;
    font-weight: 600;
    margin-bottom: 8px;
}

.mobile-card p {
    font-size: 12px;
    color: var(--text-light);
    line-height: 1.5;
}

.mobile-tag {
    display: inline-block;
    background: #E8F4FD;
    color: #1976D2;
    padding: 3px 8px;
    border-radius: 4px;
    font-size: 11px;
    margin: 2px 4px 2px 0;
}

/* Confidence Poll */
.poll-options {
    display: flex;
    gap: 8px;
    margin-top: 12px;
}

.poll-option {
    flex: 1;
    padding: 10px;
    text-align: center;
    border: 2px solid var(--border);
    border-radius: 8px;
    font-size: 11px;
    cursor: pointer;
    transition: all 0.2s;
    font-weight: 500;
}

.poll-option:hover { border-color: var(--primary-light); }
.poll-option.selected {
    border-color: var(--primary);
    background: #EEF2FF;
    color: var(--primary);
}

/* Sprint Timeline */
.timeline {
    display: flex;
    align-items: center;
    padding: 20px 0;
    position: relative;
}

.timeline-track {
    position: absolute;
    left: 0; right: 0;
    height: 4px;
    background: var(--border);
    border-radius: 2px;
}

.timeline-progress {
    position: absolute;
    left: 0;
    height: 4px;
    background: var(--primary);
    border-radius: 2px;
}

.timeline-phase {
    flex: 1;
    text-align: center;
    position: relative;
    z-index: 1;
}

.timeline-dot {
    width: 16px;
    height: 16px;
    border-radius: 50%;
    background: var(--border);
    margin: 0 auto 8px;
    border: 3px solid #fff;
    box-shadow: 0 0 0 2px var(--border);
}

.timeline-dot.completed {
    background: var(--success);
    box-shadow: 0 0 0 2px var(--success);
}

.timeline-dot.active {
    background: var(--primary);
    box-shadow: 0 0 0 2px var(--primary);
}

.timeline-label {
    font-size: 11px;
    color: var(--text-light);
    font-weight: 500;
}

/* Content comparison */
.content-compare {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 16px;
}

.content-before, .content-after {
    padding: 16px;
    border-radius: 8px;
    font-size: 13px;
    line-height: 1.6;
}

.content-before {
    background: #FFF5F5;
    border: 1px solid #FED7D7;
}

.content-after {
    background: #F0FFF4;
    border: 1px solid #C6F6D5;
}

/* Checklist */
.checklist-item {
    display: flex;
    align-items: center;
    padding: 10px 0;
    border-bottom: 1px solid var(--border);
    gap: 12px;
}

.checklist-item:last-child { border-bottom: none; }

.checklist-label {
    flex: 1;
    font-size: 13px;
}

.checklist-status {
    min-width: 100px;
}

.checklist-status select {
    padding: 4px 8px;
    border-radius: 4px;
    border: 1px solid var(--border);
    font-size: 11px;
    background: #fff;
    cursor: pointer;
}

/* Modal/Panel overlay */
.modal-overlay {
    display: none;
    position: fixed;
    top: 0; left: 0; right: 0; bottom: 0;
    background: rgba(0,0,0,0.4);
    z-index: 2000;
    align-items: center;
    justify-content: center;
}

.modal-overlay.show { display: flex; }

.modal-content {
    background: #fff;
    border-radius: 16px;
    padding: 32px;
    max-width: 500px;
    width: 90%;
    box-shadow: 0 20px 60px rgba(0,0,0,0.3);
}

.modal-content h3 {
    font-size: 18px;
    margin-bottom: 12px;
}

.modal-content p {
    font-size: 14px;
    color: var(--text-light);
    margin-bottom: 20px;
    line-height: 1.6;
}

/* Toast notification */
.toast {
    position: fixed;
    bottom: 30px;
    right: 30px;
    background: var(--primary);
    color: #fff;
    padding: 14px 24px;
    border-radius: 10px;
    font-size: 13px;
    font-weight: 500;
    z-index: 3000;
    transform: translateY(100px);
    opacity: 0;
    transition: all 0.3s;
    box-shadow: 0 8px 30px rgba(0,0,0,0.2);
}

.toast.show {
    transform: translateY(0);
    opacity: 1;
}

/* Inventory cards */
.inv-card {
    background: #fff;
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 18px;
    margin-bottom: 12px;
}

.inv-card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 10px;
}

.inv-card-title {
    font-size: 14px;
    font-weight: 600;
}

.inv-metric {
    display: flex;
    justify-content: space-between;
    padding: 6px 0;
    font-size: 12px;
    color: var(--text-light);
}

.inv-metric span:last-child { font-weight: 600; color: var(--text); }

/* Responsive */
@media (max-width: 1200px) {
    .grid-2 { grid-template-columns: 1fr; }
    .grid-3 { grid-template-columns: 1fr 1fr; }
    .kpi-grid { grid-template-columns: repeat(3, 1fr); }
}

@media (max-width: 900px) {
    .kpi-grid { grid-template-columns: repeat(2, 1fr); }
    .chart-grid { grid-template-columns: 1fr; }
}

/* Table scroll wrapper */
.table-wrapper {
    overflow-x: auto;
    border-radius: 12px;
    border: 1px solid var(--border);
}

/* Action summary bar */
.summary-bar {
    display: flex;
    gap: 24px;
    padding: 16px 20px;
    background: #F8FAFC;
    border-radius: 10px;
    margin-bottom: 20px;
}

.summary-item {
    text-align: center;
}

.summary-item .num {
    font-size: 24px;
    font-weight: 700;
    color: var(--text);
}

.summary-item .lbl {
    font-size: 11px;
    color: var(--text-light);
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

/* Board summary */
.board-summary {
    background: linear-gradient(135deg, var(--primary) 0%, var(--primary-light) 100%);
    color: #fff;
    border-radius: 12px;
    padding: 28px;
    margin-top: 24px;
}

.board-summary h3 {
    font-size: 16px;
    font-weight: 700;
    margin-bottom: 12px;
    color: #fff;
}

.board-summary p {
    font-size: 14px;
    line-height: 1.7;
    color: rgba(255,255,255,0.9);
}

/* SKU detail grid */
.sku-detail-grid {
    display: grid;
    grid-template-columns: 2fr 1fr;
    gap: 24px;
}

@media (max-width: 1100px) {
    .sku-detail-grid { grid-template-columns: 1fr; }
}

.sku-img-placeholder {
    width: 100%;
    height: 200px;
    background: linear-gradient(135deg, #E8ECF4, #D4DAE8);
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: var(--text-light);
    font-size: 13px;
}

/* Content Quality Progress */
.cq-progress {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 8px;
}

.cq-progress-label {
    font-size: 12px;
    width: 120px;
    color: var(--text-light);
}

.cq-progress-bar {
    flex: 1;
    height: 6px;
    background: #EDF2F7;
    border-radius: 3px;
}

.cq-progress-fill {
    height: 100%;
    border-radius: 3px;
    background: var(--primary-light);
}

.cq-progress-val {
    font-size: 12px;
    font-weight: 600;
    width: 40px;
    text-align: right;
}
</style>
</head>
<body>

<!-- Sidebar -->
<nav class="sidebar">
    <div class="sidebar-brand">
        <h2>MERIDIAN</h2>
        <div class="subtitle">Customer Promise Control Tower</div>
        <div class="pwc-label">PwC Advisory Prototype</div>
    </div>
    <div class="sidebar-nav">
        <div class="nav-item active" data-screen="dashboard" onclick="showScreen('dashboard')">
            <span class="nav-icon">&#9632;</span> CEO Dashboard
        </div>
        <div class="nav-item" data-screen="sku-health" onclick="showScreen('sku-health')">
            <span class="nav-icon">&#9654;</span> SKU Health Monitor
        </div>
        <div class="nav-item" data-screen="sku-detail" onclick="showScreen('sku-detail')">
            <span class="nav-icon">&#9679;</span> SKU Detail
        </div>
        <div class="nav-item" data-screen="content-hub" onclick="showScreen('content-hub')">
            <span class="nav-icon">&#9998;</span> Content Quality Hub
        </div>
        <div class="nav-item" data-screen="inventory" onclick="showScreen('inventory')">
            <span class="nav-icon">&#9733;</span> Inventory Dashboard
        </div>
        <div class="nav-item" data-screen="associate" onclick="showScreen('associate')">
            <span class="nav-icon">&#9786;</span> Associate Assist
        </div>
        <div class="nav-item" data-screen="actions" onclick="showScreen('actions')">
            <span class="nav-icon">&#10003;</span> Action Center
        </div>
        <div class="nav-item" data-screen="sprint" onclick="showScreen('sprint')">
            <span class="nav-icon">&#9201;</span> Sprint Tracker
        </div>
    </div>
    <div class="role-switcher">
        <label>Viewing as</label>
        <select id="roleSwitcher" onchange="switchRole(this.value)">
            <option value="ceo">CEO / Executive</option>
            <option value="merchant">Merchant</option>
            <option value="supply-chain">Supply Chain Lead</option>
            <option value="store-ops">Store Operations Lead</option>
            <option value="associate">Store Associate</option>
        </select>
    </div>
</nav>

<!-- Header -->
<header class="header">
    <div class="header-title" id="pageTitle">CEO Control Tower Dashboard</div>
    <div class="header-meta">
        <span class="sprint-badge">Day 48 of 90</span>
        <span class="header-date">90-Day Customer Promise Recovery Sprint</span>
    </div>
</header>

<!-- Main Content -->
<main class="main">

<!-- Screen 1: CEO Dashboard -->
<section class="screen active" id="screen-dashboard">
    <div style="display:flex;align-items:center;gap:24px;margin-bottom:24px;">
        <div class="score-circle" style="background:linear-gradient(135deg,#EEF2FF,#E8EDFF);border:3px solid var(--primary-light);">
            <span class="score-value">74</span>
            <span class="score-label">Promise Score</span>
        </div>
        <div style="flex:1;">
            <h2 style="font-size:20px;margin-bottom:6px;">Customer Promise Score: 74/100</h2>
            <p style="font-size:13px;color:var(--text-light);">Measuring availability, content quality, returns, customer sentiment, and associate readiness across priority SKUs. Up from 61 at sprint start.</p>
        </div>
    </div>

    <div class="kpi-grid">
        <div class="kpi-card">
            <div class="kpi-label">Online Conversion (Priority SKUs)</div>
            <div class="kpi-value">1.62%</div>
            <div class="kpi-change positive">&#9650; from 1.4% baseline</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-label">Return Rate Reduction</div>
            <div class="kpi-value">-7%</div>
            <div class="kpi-change positive">&#9650; improving</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-label">Stockout Incidents</div>
            <div class="kpi-value">-11%</div>
            <div class="kpi-change positive">&#9650; fewer stockouts</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-label">Content Completeness</div>
            <div class="kpi-value">81%</div>
            <div class="kpi-change positive">&#9650; from 62% baseline</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-label">Associate Confidence</div>
            <div class="kpi-value">+14%</div>
            <div class="kpi-change positive">&#9650; lift</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-label">Revenue Recovered</div>
            <div class="kpi-value">$4.2M</div>
            <div class="kpi-change positive">&#9650; estimated</div>
        </div>
    </div>

    <div class="chart-grid">
        <div class="chart-container">
            <div class="chart-title">Conversion Trend (Priority SKUs)</div>
            <canvas id="chartConversion"></canvas>
        </div>
        <div class="chart-container">
            <div class="chart-title">Return Rate Trend</div>
            <canvas id="chartReturns"></canvas>
        </div>
        <div class="chart-container">
            <div class="chart-title">Stockout Incidents (Weekly)</div>
            <canvas id="chartStockouts"></canvas>
        </div>
        <div class="chart-container">
            <div class="chart-title">Content Completeness</div>
            <canvas id="chartContent"></canvas>
        </div>
    </div>

    <div class="grid-2">
        <div class="card">
            <div class="card-header">
                <span class="card-title">Urgent Alerts</span>
                <span style="font-size:11px;color:var(--text-light);">5 active</span>
            </div>
            <ul class="alert-list" id="alertList">
                <li class="alert-item" data-alert="0">
                    <span class="alert-dot"></span>
                    <span class="alert-text"><strong>Queen Cotton Comforter Set:</strong> High stockout risk in Northeast. 2.3 days of supply remaining.</span>
                    <button class="alert-ack-btn" onclick="ackAlert(0,event)">Acknowledge</button>
                </li>
                <li class="alert-item" data-alert="1">
                    <span class="alert-dot"></span>
                    <span class="alert-text"><strong>Women's Linen Shirt:</strong> 22% return rate due to sizing confusion. Fit guidance missing.</span>
                    <button class="alert-ack-btn" onclick="ackAlert(1,event)">Acknowledge</button>
                </li>
                <li class="alert-item" data-alert="2">
                    <span class="alert-dot"></span>
                    <span class="alert-text"><strong>Modular Fabric Sofa:</strong> Product page missing dimensions. Conversion 40% below category avg.</span>
                    <button class="alert-ack-btn" onclick="ackAlert(2,event)">Acknowledge</button>
                </li>
                <li class="alert-item" data-alert="3">
                    <span class="alert-dot"></span>
                    <span class="alert-text"><strong>Men's Stretch Chino:</strong> Strong demand signal, only 3 units in top 15 stores.</span>
                    <button class="alert-ack-btn" onclick="ackAlert(3,event)">Acknowledge</button>
                </li>
                <li class="alert-item" data-alert="4">
                    <span class="alert-dot"></span>
                    <span class="alert-text"><strong>Ceramic Dinnerware Set:</strong> Overstock risk in Midwest warehouses. 94 days of supply.</span>
                    <button class="alert-ack-btn" onclick="ackAlert(4,event)">Acknowledge</button>
                </li>
            </ul>
        </div>
        <div class="card">
            <div class="card-header">
                <span class="card-title">Weekly CEO Decision Panel</span>
                <span style="font-size:11px;color:var(--text-light);">Action required</span>
            </div>
            <div class="decision-grid" id="decisionGrid">
                <div class="decision-card" onclick="approveDecision(this)">
                    <div class="decision-title">Approve Emergency Replenishment</div>
                    <div class="decision-status">Pending approval</div>
                </div>
                <div class="decision-card" onclick="approveDecision(this)">
                    <div class="decision-title">Approve Product Content Updates</div>
                    <div class="decision-status">Pending approval</div>
                </div>
                <div class="decision-card" onclick="approveDecision(this)">
                    <div class="decision-title">Escalate Warehouse Process Issue</div>
                    <div class="decision-status">Pending approval</div>
                </div>
                <div class="decision-card" onclick="approveDecision(this)">
                    <div class="decision-title">Launch Associate Microlearning</div>
                    <div class="decision-status">Pending approval</div>
                </div>
            </div>
        </div>
    </div>
</section>

<!-- Screen 2: SKU Health Monitor -->
<section class="screen" id="screen-sku-health">
    <div class="section-header">SKU Health Monitor</div>
    <div class="section-subheader">Priority SKU performance across all customer promise dimensions</div>

    <div class="filters-row">
        <input type="text" class="filter-input" placeholder="Search SKUs..." id="skuSearch" oninput="filterSKUs()">
        <select class="filter-select" id="filterCategory" onchange="filterSKUs()">
            <option value="">All Categories</option>
            <option value="Apparel">Apparel</option>
            <option value="Home">Home</option>
            <option value="Kitchen">Kitchen</option>
            <option value="Kids">Kids</option>
            <option value="Bath">Bath</option>
            <option value="Lighting">Lighting</option>
        </select>
        <select class="filter-select" id="filterRegion" onchange="filterSKUs()">
            <option value="">All Regions</option>
            <option value="Northeast">Northeast</option>
            <option value="Southeast">Southeast</option>
            <option value="Midwest">Midwest</option>
            <option value="West">West</option>
            <option value="National">National</option>
        </select>
        <select class="filter-select" id="filterStatus" onchange="filterSKUs()">
            <option value="">All Statuses</option>
            <option value="Critical">Critical</option>
            <option value="Watch">Watch</option>
            <option value="Healthy">Healthy</option>
        </select>
        <select class="filter-select" id="filterIssue" onchange="filterSKUs()">
            <option value="">All Issues</option>
            <option value="high-return">High Return Rate</option>
            <option value="high-stockout">High Stockout Risk</option>
            <option value="low-content">Low Content Score</option>
        </select>
    </div>

    <div class="table-wrapper">
        <table class="data-table" id="skuTable">
            <thead>
                <tr>
                    <th>SKU Name</th>
                    <th>Category</th>
                    <th>Region</th>
                    <th>Revenue Impact</th>
                    <th>Conv. Rate</th>
                    <th>Return Rate</th>
                    <th>Stockout Risk</th>
                    <th>Content</th>
                    <th>Sentiment</th>
                    <th>Health Score</th>
                    <th>Status</th>
                </tr>
            </thead>
            <tbody id="skuTableBody"></tbody>
        </table>
    </div>
</section>

<!-- Screen 3: SKU Detail -->
<section class="screen" id="screen-sku-detail">
    <div style="display:flex;align-items:center;gap:12px;margin-bottom:20px;">
        <button class="btn btn-outline btn-sm" onclick="showScreen('sku-health')">&larr; Back to SKU List</button>
        <span class="section-header" style="margin-bottom:0;" id="skuDetailName">Women's Linen Shirt</span>
        <span class="chip chip-critical" id="skuDetailStatus">Critical</span>
    </div>

    <div class="sku-detail-grid">
        <div>
            <div class="card" style="margin-bottom:20px;">
                <div style="display:flex;gap:20px;align-items:flex-start;">
                    <div class="sku-img-placeholder">Product Image</div>
                    <div style="flex:1;">
                        <div style="display:flex;align-items:center;gap:16px;margin-bottom:12px;">
                            <div class="score-circle" style="width:80px;height:80px;background:#FFF5F5;border:3px solid var(--danger);">
                                <span class="score-value" style="font-size:24px;" id="skuDetailScore">58</span>
                                <span class="score-label" style="font-size:9px;">Health</span>
                            </div>
                            <div>
                                <h4 style="font-size:15px;margin-bottom:4px;">Business Impact Summary</h4>
                                <ul style="font-size:12px;color:var(--text-light);list-style:none;" id="skuDetailImpact">
                                    <li>&#8226; High traffic but low conversion</li>
                                    <li>&#8226; Return rate: 22%</li>
                                    <li>&#8226; Main return reason: size mismatch</li>
                                    <li>&#8226; Reviews mention "runs large"</li>
                                    <li>&#8226; Product page missing fit guidance</li>
                                </ul>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <div class="card" style="margin-bottom:20px;">
                <div class="card-title" style="margin-bottom:14px;">Product Content Score</div>
                <div class="cq-progress"><span class="cq-progress-label">Title clarity</span><div class="cq-progress-bar"><div class="cq-progress-fill" style="width:90%;background:var(--success);"></div></div><span class="cq-progress-val">Good</span></div>
                <div class="cq-progress"><span class="cq-progress-label">Description</span><div class="cq-progress-bar"><div class="cq-progress-fill" style="width:40%;background:var(--danger);"></div></div><span class="cq-progress-val">Weak</span></div>
                <div class="cq-progress"><span class="cq-progress-label">Size/Fit info</span><div class="cq-progress-bar"><div class="cq-progress-fill" style="width:0%;"></div></div><span class="cq-progress-val" style="color:var(--danger);">Missing</span></div>
                <div class="cq-progress"><span class="cq-progress-label">Material details</span><div class="cq-progress-bar"><div class="cq-progress-fill" style="width:55%;background:var(--warning);"></div></div><span class="cq-progress-val">Partial</span></div>
                <div class="cq-progress"><span class="cq-progress-label">Images</span><div class="cq-progress-bar"><div class="cq-progress-fill" style="width:50%;background:var(--warning);"></div></div><span class="cq-progress-val">Incomplete</span></div>
                <div class="cq-progress"><span class="cq-progress-label">Reviews summary</span><div class="cq-progress-bar"><div class="cq-progress-fill" style="width:80%;background:var(--success);"></div></div><span class="cq-progress-val">Available</span></div>
            </div>

            <div class="card" style="margin-bottom:20px;">
                <div class="card-title" style="margin-bottom:14px;">Customer Feedback Summary</div>
                <div style="display:flex;flex-direction:column;gap:8px;">
                    <div style="background:#F8FAFC;padding:12px;border-radius:8px;font-size:13px;font-style:italic;border-left:3px solid var(--warning);">"Runs larger than expected"</div>
                    <div style="background:#F8FAFC;padding:12px;border-radius:8px;font-size:13px;font-style:italic;border-left:3px solid var(--warning);">"Color looks different from photos"</div>
                    <div style="background:#F8FAFC;padding:12px;border-radius:8px;font-size:13px;font-style:italic;border-left:3px solid var(--warning);">"Fabric is good but sizing is confusing"</div>
                </div>
            </div>

            <div class="card">
                <div class="card-title" style="margin-bottom:14px;">AI Recommended Actions</div>
                <ol style="font-size:13px;padding-left:20px;line-height:2;">
                    <li>Add fit note: "Relaxed fit; size down for a closer fit."</li>
                    <li>Add fabric close-up image.</li>
                    <li>Add model height and size details.</li>
                    <li>Move excess stock from West region to Northeast.</li>
                    <li>Push microlearning card to store associates.</li>
                </ol>
                <div style="margin-top:16px;display:flex;flex-wrap:wrap;gap:10px;">
                    <button class="btn btn-primary" onclick="generateContentFix()">Generate Content Fix</button>
                    <button class="btn btn-success" id="btnApproveUpdate" onclick="approvePageUpdate()">Approve Product Page Update</button>
                    <button class="btn btn-accent" onclick="createTransferTask()">Create Inventory Transfer Task</button>
                    <button class="btn btn-outline" onclick="sendLearningCard()">Send Associate Learning Card</button>
                </div>
                <div id="contentFixPanel" style="display:none;margin-top:16px;background:#F0FFF4;border:1px solid #C6F6D5;border-radius:8px;padding:16px;">
                    <div style="font-size:12px;font-weight:600;color:var(--success);margin-bottom:8px;">AI-GENERATED CONTENT FIX</div>
                    <p style="font-size:13px;line-height:1.7;">"Relaxed-fit linen shirt designed for breathable everyday wear. Runs slightly large; size down for a closer fit. Made from 100% linen with a soft washed texture. Model is 5'8'' and wearing size S. Best for warm weather, casual workwear, and weekend styling."</p>
                </div>
            </div>
        </div>

        <div>
            <div class="card" style="margin-bottom:20px;">
                <div class="card-title" style="margin-bottom:14px;">Inventory View</div>
                <div class="inv-metric"><span>Online</span><span style="color:var(--success);">Available</span></div>
                <div class="inv-metric"><span>Northeast stores</span><span style="color:var(--danger);">Low stock</span></div>
                <div class="inv-metric"><span>Southeast stores</span><span>Adequate</span></div>
                <div class="inv-metric"><span>Midwest stores</span><span>Adequate</span></div>
                <div class="inv-metric"><span>West stores</span><span style="color:var(--warning);">Overstock</span></div>
            </div>

            <div class="card">
                <div class="card-title" style="margin-bottom:14px;">Key Metrics</div>
                <div class="inv-metric"><span>Daily views</span><span>4,200</span></div>
                <div class="inv-metric"><span>Conversion</span><span>1.1%</span></div>
                <div class="inv-metric"><span>Return rate</span><span style="color:var(--danger);">22%</span></div>
                <div class="inv-metric"><span>Revenue/week</span><span>$38K</span></div>
                <div class="inv-metric"><span>Sentiment</span><span style="color:var(--warning);">Mixed</span></div>
                <div class="inv-metric"><span>Assoc. readiness</span><span style="color:var(--warning);">62%</span></div>
            </div>
        </div>
    </div>
</section>

<!-- Screen 4: Content Quality Hub -->
<section class="screen" id="screen-content-hub">
    <div class="section-header">Product Content Quality Hub</div>
    <div class="section-subheader">Fix unclear product information that causes returns and low conversion</div>

    <div class="kpi-grid" style="margin-bottom:24px;">
        <div class="kpi-card">
            <div class="kpi-label">Overall Content Completeness</div>
            <div class="kpi-value" id="contentCompleteness">81%</div>
            <div class="kpi-change positive">&#9650; from 62% baseline</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-label">SKUs with Complete Content</div>
            <div class="kpi-value">124/200</div>
            <div class="kpi-change positive">&#9650; 31 added this week</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-label">Content Issues Remaining</div>
            <div class="kpi-value">47</div>
            <div class="kpi-change positive">&#9660; down from 114</div>
        </div>
    </div>

    <div class="grid-2">
        <div class="card">
            <div class="card-title" style="margin-bottom:14px;">Before / After: Women's Linen Shirt</div>
            <div class="content-compare">
                <div class="content-before">
                    <div style="font-size:11px;font-weight:600;color:var(--danger);margin-bottom:8px;">BEFORE</div>
                    Lightweight linen shirt available in multiple colors. Comfortable and stylish.
                </div>
                <div class="content-after">
                    <div style="font-size:11px;font-weight:600;color:var(--success);margin-bottom:8px;">AFTER</div>
                    Relaxed-fit linen shirt designed for breathable everyday wear. Runs slightly large; size down for a closer fit. Made from 100% linen with a soft washed texture. Model is 5'8'' and wearing size S. Best for warm weather, casual workwear, and weekend styling.
                </div>
            </div>
        </div>

        <div class="card">
            <div class="card-title" style="margin-bottom:14px;">AI Content Assistant</div>
            <div style="background:#F8FAFC;border-radius:8px;padding:16px;margin-bottom:12px;">
                <div style="font-size:11px;color:var(--text-light);margin-bottom:8px;">SELECTED SKU</div>
                <div style="font-size:14px;font-weight:600;">Women's Linen Shirt</div>
            </div>
            <div style="font-size:12px;color:var(--text-light);margin-bottom:12px;">Content gaps detected: Fit guidance, Material close-up, Size chart</div>
            <button class="btn btn-primary btn-sm" onclick="showToast('AI content suggestions generated')">Generate Suggestions</button>
            <button class="btn btn-outline btn-sm" onclick="showToast('Content sent to review queue')">Send to Review</button>
        </div>
    </div>

    <div class="card" style="margin-top:20px;">
        <div class="card-title" style="margin-bottom:14px;">Content Checklist: Women's Linen Shirt</div>
        <div id="contentChecklist">
            <div class="checklist-item">
                <span class="checklist-label">Fit guidance</span>
                <span class="checklist-status"><select onchange="updateContentProgress()"><option>Missing</option><option>Drafted</option><option selected>Approved</option><option>Published</option></select></span>
            </div>
            <div class="checklist-item">
                <span class="checklist-label">Material details</span>
                <span class="checklist-status"><select onchange="updateContentProgress()"><option>Missing</option><option selected>Drafted</option><option>Approved</option><option>Published</option></select></span>
            </div>
            <div class="checklist-item">
                <span class="checklist-label">Care instructions</span>
                <span class="checklist-status"><select onchange="updateContentProgress()"><option>Missing</option><option selected>Drafted</option><option>Approved</option><option>Published</option></select></span>
            </div>
            <div class="checklist-item">
                <span class="checklist-label">Color accuracy</span>
                <span class="checklist-status"><select onchange="updateContentProgress()"><option>Missing</option><option>Drafted</option><option>Approved</option><option selected>Published</option></select></span>
            </div>
            <div class="checklist-item">
                <span class="checklist-label">Lifestyle image</span>
                <span class="checklist-status"><select onchange="updateContentProgress()"><option>Missing</option><option>Drafted</option><option selected>Approved</option><option>Published</option></select></span>
            </div>
            <div class="checklist-item">
                <span class="checklist-label">Close-up image</span>
                <span class="checklist-status"><select onchange="updateContentProgress()"><option selected>Missing</option><option>Drafted</option><option>Approved</option><option>Published</option></select></span>
            </div>
            <div class="checklist-item">
                <span class="checklist-label">Customer review summary</span>
                <span class="checklist-status"><select onchange="updateContentProgress()"><option>Missing</option><option>Drafted</option><option>Approved</option><option selected>Published</option></select></span>
            </div>
            <div class="checklist-item">
                <span class="checklist-label">Return policy clarity</span>
                <span class="checklist-status"><select onchange="updateContentProgress()"><option>Missing</option><option selected>Drafted</option><option>Approved</option><option>Published</option></select></span>
            </div>
        </div>
        <div style="margin-top:16px;">
            <div style="font-size:12px;color:var(--text-light);margin-bottom:6px;">Content Completeness for this SKU: <strong id="skuContentPct">63%</strong></div>
            <div class="progress-bar"><div class="progress-fill blue" id="skuContentBar" style="width:63%;"></div></div>
        </div>
    </div>
</section>

<!-- Screen 5: Inventory Dashboard -->
<section class="screen" id="screen-inventory">
    <div class="section-header">Inventory Availability Dashboard</div>
    <div class="section-subheader">Prevent stockouts of top-selling products and optimize inventory positioning</div>

    <div class="kpi-grid" style="margin-bottom:24px;">
        <div class="kpi-card">
            <div class="kpi-label">Active Stockout Risks</div>
            <div class="kpi-value" style="color:var(--danger);">6</div>
            <div class="kpi-change negative">priority SKUs at risk</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-label">Overstock Alerts</div>
            <div class="kpi-value" style="color:var(--warning);">4</div>
            <div class="kpi-change negative">excess inventory</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-label">Transfers Recommended</div>
            <div class="kpi-value">8</div>
            <div class="kpi-change positive">optimization actions</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-label">Revenue at Risk</div>
            <div class="kpi-value">$1.8M</div>
            <div class="kpi-change negative">if no action taken</div>
        </div>
    </div>

    <div class="grid-2">
        <div>
            <div class="inv-card" id="invCard1">
                <div class="inv-card-header">
                    <span class="inv-card-title">Queen Cotton Comforter Set</span>
                    <span class="chip chip-critical">Critical</span>
                </div>
                <div class="inv-metric"><span>Days of supply (NE)</span><span style="color:var(--danger);">2.3 days</span></div>
                <div class="inv-metric"><span>Demand trend</span><span>High &amp; rising</span></div>
                <div class="inv-metric"><span>Replenishment status</span><span style="color:var(--danger);">Delayed</span></div>
                <div class="inv-metric"><span>Sell-through rate</span><span>94%</span></div>
                <div style="margin-top:12px;background:#FFF8F5;border-radius:8px;padding:12px;font-size:12px;border:1px solid #FED7D7;">
                    <strong>Recommendation:</strong> Transfer 420 units from Midwest warehouse to Northeast distribution center. Estimated revenue protection: $620K.
                </div>
                <div style="margin-top:12px;display:flex;gap:8px;">
                    <button class="btn btn-success btn-sm" onclick="approveTransfer(this,'Transfer Approved')">Approve Transfer</button>
                    <button class="btn btn-outline btn-sm" onclick="approveTransfer(this,'Merchant Review Required')">Flag for Merchant Review</button>
                    <button class="btn btn-outline btn-sm" onclick="showToast('Regional stores notified')">Notify Regional Stores</button>
                </div>
            </div>

            <div class="inv-card">
                <div class="inv-card-header">
                    <span class="inv-card-title">Men's Stretch Chino</span>
                    <span class="chip chip-watch">Watch</span>
                </div>
                <div class="inv-metric"><span>Store availability</span><span style="color:var(--warning);">Low (avg 3 units/store)</span></div>
                <div class="inv-metric"><span>Online demand</span><span>High</span></div>
                <div class="inv-metric"><span>Days of supply</span><span style="color:var(--warning);">8 days</span></div>
                <div class="inv-metric"><span>Sell-through rate</span><span>78%</span></div>
                <div style="margin-top:12px;display:flex;gap:8px;">
                    <button class="btn btn-success btn-sm" onclick="showToast('Replenishment expedited')">Expedite Replenishment</button>
                    <button class="btn btn-outline btn-sm" onclick="showToast('Regional stores notified')">Notify Stores</button>
                </div>
            </div>
        </div>

        <div>
            <div class="inv-card">
                <div class="inv-card-header">
                    <span class="inv-card-title">Ceramic Dinnerware Set</span>
                    <span class="chip chip-watch">Overstock</span>
                </div>
                <div class="inv-metric"><span>Days of supply (MW)</span><span style="color:var(--warning);">94 days</span></div>
                <div class="inv-metric"><span>Demand trend</span><span>Below forecast</span></div>
                <div class="inv-metric"><span>Excess units</span><span>2,400</span></div>
                <div class="inv-metric"><span>Sell-through rate</span><span style="color:var(--warning);">31%</span></div>
                <div style="margin-top:12px;display:flex;gap:8px;">
                    <button class="btn btn-outline btn-sm" onclick="showToast('Markdown analysis initiated')">Run Markdown Analysis</button>
                    <button class="btn btn-outline btn-sm" onclick="showToast('Merchant flagged for review')">Flag for Merchant</button>
                </div>
            </div>

            <div class="inv-card">
                <div class="inv-card-header">
                    <span class="inv-card-title">Cotton Bath Towel Bundle</span>
                    <span class="chip chip-healthy">Healthy</span>
                </div>
                <div class="inv-metric"><span>Days of supply</span><span style="color:var(--success);">28 days</span></div>
                <div class="inv-metric"><span>Demand trend</span><span>Stable</span></div>
                <div class="inv-metric"><span>Replenishment</span><span style="color:var(--success);">On schedule</span></div>
                <div class="inv-metric"><span>Sell-through rate</span><span>62%</span></div>
            </div>
        </div>
    </div>
</section>

<!-- Screen 6: Associate Assist -->
<section class="screen" id="screen-associate">
    <div class="section-header">Associate Assist App</div>
    <div class="section-subheader">How store associates receive product help, inventory lookup, and customer talking points</div>

    <div style="display:flex;gap:32px;align-items:flex-start;justify-content:center;flex-wrap:wrap;">
        <div class="mobile-frame">
            <div class="mobile-header">
                <h3>Meridian Associate</h3>
                <input type="text" class="mobile-search" placeholder="Search or scan product..." value="Men's Stretch Chino">
            </div>
            <div class="mobile-content">
                <div class="mobile-card">
                    <h4>Men's Stretch Chino</h4>
                    <p>Slim fit chino with stretch fabric for comfort and mobility. Perfect for office-casual and weekend wear.</p>
                </div>

                <div class="mobile-card">
                    <h4 style="font-size:12px;color:var(--text-light);margin-bottom:8px;">KEY SELLING POINTS</h4>
                    <div class="mobile-tag">Runs true to size</div>
                    <div class="mobile-tag">Office-casual &amp; weekend</div>
                    <div class="mobile-tag">5 colors available</div>
                    <div class="mobile-tag">Easy-care stretch fabric</div>
                </div>

                <div class="mobile-card">
                    <h4 style="font-size:12px;color:var(--text-light);margin-bottom:8px;">INVENTORY</h4>
                    <div class="inv-metric"><span>This store</span><span style="font-weight:600;color:var(--warning);">3 units</span></div>
                    <div class="inv-metric"><span>Nearby store (5mi)</span><span style="font-weight:600;color:var(--success);">12 units</span></div>
                    <div class="inv-metric"><span>Online warehouse</span><span style="font-weight:600;color:var(--success);">Available</span></div>
                </div>

                <div class="mobile-card">
                    <h4 style="font-size:12px;color:var(--text-light);margin-bottom:8px;">SIZE &amp; FIT GUIDANCE</h4>
                    <p>True to size. Slim fit through the hip and thigh with a tapered leg. For a relaxed fit, size up.</p>
                </div>

                <div class="mobile-card">
                    <h4 style="font-size:12px;color:var(--text-light);margin-bottom:8px;">SUGGESTED ALTERNATIVE</h4>
                    <p style="font-weight:600;">Meridian Everyday Chino</p>
                    <p>Relaxed fit, available in 3 colors</p>
                </div>

                <div class="mobile-card">
                    <h4 style="font-size:12px;color:var(--text-light);margin-bottom:8px;">RETURN POLICY</h4>
                    <p>Eligible for standard return within 30-day policy window. No restocking fee.</p>
                </div>

                <div class="mobile-card">
                    <h4 style="font-size:12px;color:var(--text-light);margin-bottom:8px;">CONFIDENCE POLL</h4>
                    <p style="font-size:12px;margin-bottom:4px;">How confident are you helping a customer with this product?</p>
                    <div class="poll-options" id="pollOptions">
                        <div class="poll-option" onclick="selectPoll(this,0)">Not confident</div>
                        <div class="poll-option" onclick="selectPoll(this,1)">Somewhat</div>
                        <div class="poll-option" onclick="selectPoll(this,2)">Confident</div>
                    </div>
                    <div id="pollResult" style="display:none;margin-top:10px;font-size:11px;color:var(--success);font-weight:600;text-align:center;"></div>
                </div>
            </div>
        </div>

        <div style="max-width:320px;">
            <div class="card">
                <div class="card-title" style="margin-bottom:12px;">Microlearning Card</div>
                <div style="background:#F0F4FF;border-radius:8px;padding:16px;font-size:12px;line-height:1.7;">
                    <div style="font-weight:700;margin-bottom:8px;color:var(--primary);">Men's Stretch Chino - Quick Tips</div>
                    <ul style="padding-left:16px;">
                        <li>Slim fit - suggest trying their usual size</li>
                        <li>Stretch fabric = comfort without sacrificing style</li>
                        <li>Best sellers: Navy, Khaki, Charcoal</li>
                        <li>Pair with: button-down for office, tee for weekend</li>
                        <li>If customer wants relaxed: suggest Everyday Chino</li>
                    </ul>
                </div>
            </div>
            <div class="card" style="margin-top:16px;">
                <div class="card-title" style="margin-bottom:12px;">Associate Confidence Trend</div>
                <div class="inv-metric"><span>This product</span><span style="font-weight:600;">78%</span></div>
                <div class="inv-metric"><span>Category avg</span><span>71%</span></div>
                <div class="inv-metric"><span>Store avg</span><span>68%</span></div>
                <div style="margin-top:10px;">
                    <div class="progress-bar"><div class="progress-fill green" style="width:78%;"></div></div>
                </div>
            </div>
        </div>
    </div>
</section>

<!-- Screen 7: Action Center -->
<section class="screen" id="screen-actions">
    <div class="section-header">Action Center</div>
    <div class="section-subheader">Cross-functional sprint actions driving the customer promise recovery</div>

    <div class="summary-bar" id="actionSummary">
        <div class="summary-item"><div class="num" id="totalActions">8</div><div class="lbl">Total Actions</div></div>
        <div class="summary-item"><div class="num" id="completedActions">2</div><div class="lbl">Completed</div></div>
        <div class="summary-item"><div class="num" id="inProgressActions">3</div><div class="lbl">In Progress</div></div>
        <div class="summary-item"><div class="num" id="pendingActions">3</div><div class="lbl">Pending</div></div>
    </div>

    <div class="table-wrapper">
        <table class="data-table">
            <thead>
                <tr>
                    <th>Action</th>
                    <th>Owner</th>
                    <th>Function</th>
                    <th>Priority</th>
                    <th>Expected Impact</th>
                    <th>Due Date</th>
                    <th>Related SKU</th>
                    <th>Status</th>
                </tr>
            </thead>
            <tbody id="actionTableBody"></tbody>
        </table>
    </div>
</section>

<!-- Screen 8: Sprint Tracker -->
<section class="screen" id="screen-sprint">
    <div class="section-header">90-Day Sprint Impact Tracker</div>
    <div class="section-subheader">Customer Promise Recovery Sprint - Day 48 of 90</div>

    <div class="card" style="margin-bottom:24px;">
        <div class="card-title" style="margin-bottom:20px;">Sprint Timeline</div>
        <div style="position:relative;padding:30px 0;">
            <div style="display:flex;justify-content:space-between;position:relative;">
                <div style="position:absolute;top:8px;left:0;right:0;height:4px;background:var(--border);border-radius:2px;"></div>
                <div style="position:absolute;top:8px;left:0;width:53%;height:4px;background:var(--primary);border-radius:2px;"></div>
                <div style="text-align:center;position:relative;z-index:1;flex:1;">
                    <div style="width:20px;height:20px;border-radius:50%;background:var(--success);margin:0 auto 8px;border:3px solid #fff;box-shadow:0 0 0 2px var(--success);"></div>
                    <div style="font-size:11px;font-weight:600;">Diagnose &amp; Design</div>
                    <div style="font-size:10px;color:var(--text-light);">Days 0-15</div>
                    <div style="font-size:10px;color:var(--success);margin-top:4px;">Complete</div>
                </div>
                <div style="text-align:center;position:relative;z-index:1;flex:1;">
                    <div style="width:20px;height:20px;border-radius:50%;background:var(--success);margin:0 auto 8px;border:3px solid #fff;box-shadow:0 0 0 2px var(--success);"></div>
                    <div style="font-size:11px;font-weight:600;">Build MVP</div>
                    <div style="font-size:10px;color:var(--text-light);">Days 16-45</div>
                    <div style="font-size:10px;color:var(--success);margin-top:4px;">Complete</div>
                </div>
                <div style="text-align:center;position:relative;z-index:1;flex:1;">
                    <div style="width:20px;height:20px;border-radius:50%;background:var(--primary);margin:0 auto 8px;border:3px solid #fff;box-shadow:0 0 0 2px var(--primary);"></div>
                    <div style="font-size:11px;font-weight:600;">Pilot &amp; Optimize</div>
                    <div style="font-size:10px;color:var(--text-light);">Days 46-75</div>
                    <div style="font-size:10px;color:var(--primary);font-weight:600;margin-top:4px;">Active (Day 48)</div>
                </div>
                <div style="text-align:center;position:relative;z-index:1;flex:1;">
                    <div style="width:20px;height:20px;border-radius:50%;background:var(--border);margin:0 auto 8px;border:3px solid #fff;box-shadow:0 0 0 2px var(--border);"></div>
                    <div style="font-size:11px;font-weight:600;">Prove &amp; Scale</div>
                    <div style="font-size:10px;color:var(--text-light);">Days 76-90</div>
                    <div style="font-size:10px;color:var(--text-light);margin-top:4px;">Upcoming</div>
                </div>
            </div>
        </div>
    </div>

    <div class="grid-2" style="margin-bottom:24px;">
        <div class="card">
            <div class="card-title" style="margin-bottom:14px;">Completed Milestones</div>
            <ul style="list-style:none;font-size:13px;">
                <li style="padding:8px 0;border-bottom:1px solid var(--border);display:flex;align-items:center;gap:8px;"><span style="color:var(--success);">&#10003;</span> Priority SKU identification (Top 200)</li>
                <li style="padding:8px 0;border-bottom:1px solid var(--border);display:flex;align-items:center;gap:8px;"><span style="color:var(--success);">&#10003;</span> Content audit completed</li>
                <li style="padding:8px 0;border-bottom:1px solid var(--border);display:flex;align-items:center;gap:8px;"><span style="color:var(--success);">&#10003;</span> Control Tower MVP deployed</li>
                <li style="padding:8px 0;border-bottom:1px solid var(--border);display:flex;align-items:center;gap:8px;"><span style="color:var(--success);">&#10003;</span> Associate app pilot launched (50 stores)</li>
                <li style="padding:8px 0;display:flex;align-items:center;gap:8px;"><span style="color:var(--success);">&#10003;</span> First inventory transfer wave executed</li>
            </ul>
        </div>
        <div class="card">
            <div class="card-title" style="margin-bottom:14px;">Upcoming Milestones</div>
            <ul style="list-style:none;font-size:13px;">
                <li style="padding:8px 0;border-bottom:1px solid var(--border);display:flex;align-items:center;gap:8px;"><span style="color:var(--text-light);">&#9679;</span> Expand pilot to 150 stores (Day 55)</li>
                <li style="padding:8px 0;border-bottom:1px solid var(--border);display:flex;align-items:center;gap:8px;"><span style="color:var(--text-light);">&#9679;</span> Complete content fix for all Tier 1 SKUs (Day 60)</li>
                <li style="padding:8px 0;border-bottom:1px solid var(--border);display:flex;align-items:center;gap:8px;"><span style="color:var(--text-light);">&#9679;</span> Board presentation with ROI proof (Day 75)</li>
                <li style="padding:8px 0;border-bottom:1px solid var(--border);display:flex;align-items:center;gap:8px;"><span style="color:var(--text-light);">&#9679;</span> Full rollout plan approved (Day 80)</li>
                <li style="padding:8px 0;display:flex;align-items:center;gap:8px;"><span style="color:var(--text-light);">&#9679;</span> Scale decision: expand to 500+ SKUs (Day 90)</li>
            </ul>
        </div>
    </div>

    <div class="card" style="margin-bottom:24px;">
        <div class="card-title" style="margin-bottom:14px;">KPI Progress: Baseline vs Current vs Target</div>
        <div class="table-wrapper">
            <table class="data-table">
                <thead>
                    <tr>
                        <th>KPI</th>
                        <th>Baseline</th>
                        <th>Current (Day 48)</th>
                        <th>Target (Day 90)</th>
                        <th>Progress</th>
                    </tr>
                </thead>
                <tbody>
                    <tr><td>Online Conversion (Priority SKUs)</td><td>1.4%</td><td style="font-weight:600;color:var(--success);">1.62%</td><td>1.8%</td><td><div class="progress-bar" style="width:100px;"><div class="progress-fill green" style="width:55%;"></div></div></td></tr>
                    <tr><td>Return Rate Reduction</td><td>0%</td><td style="font-weight:600;color:var(--success);">7%</td><td>12%</td><td><div class="progress-bar" style="width:100px;"><div class="progress-fill green" style="width:58%;"></div></div></td></tr>
                    <tr><td>Stockout Incident Reduction</td><td>0%</td><td style="font-weight:600;color:var(--success);">11%</td><td>18%</td><td><div class="progress-bar" style="width:100px;"><div class="progress-fill green" style="width:61%;"></div></div></td></tr>
                    <tr><td>Content Completeness</td><td>62%</td><td style="font-weight:600;color:var(--success);">81%</td><td>88%</td><td><div class="progress-bar" style="width:100px;"><div class="progress-fill green" style="width:73%;"></div></div></td></tr>
                    <tr><td>Associate Confidence Lift</td><td>0%</td><td style="font-weight:600;color:var(--success);">14%</td><td>20%</td><td><div class="progress-bar" style="width:100px;"><div class="progress-fill green" style="width:70%;"></div></div></td></tr>
                    <tr><td>Revenue Recovered</td><td>$0</td><td style="font-weight:600;color:var(--success);">$4.2M</td><td>$7.5M</td><td><div class="progress-bar" style="width:100px;"><div class="progress-fill green" style="width:56%;"></div></div></td></tr>
                </tbody>
            </table>
        </div>
    </div>

    <div class="board-summary">
        <h3>Board-Ready Executive Summary</h3>
        <p>By Day 48, Meridian has improved product content completeness from 62% to 81%, reduced stockout incidents by 11%, improved conversion on priority SKUs from 1.4% to 1.62%, and recovered an estimated $4.2M in revenue. Associate confidence has lifted 14% across pilot stores. The sprint is on track to scale to additional categories after Day 90, with board presentation scheduled for Day 75.</p>
    </div>
</section>

</main>

<!-- Toast -->
<div class="toast" id="toast"></div>

<!-- Modal -->
<div class="modal-overlay" id="modal">
    <div class="modal-content">
        <h3 id="modalTitle">Confirmation</h3>
        <p id="modalText">Action completed successfully.</p>
        <button class="btn btn-primary" onclick="closeModal()">Close</button>
    </div>
</div>

<script>
// Mock Data
const skuData = [
    {name:"Women's Linen Shirt",category:"Apparel",region:"National",revenue:"$2.1M",conversion:"1.1%",returnRate:"22%",stockoutRisk:"Low",content:"54%",sentiment:"Mixed",assocReady:"62%",healthScore:58,status:"Critical"},
    {name:"Men's Stretch Chino",category:"Apparel",region:"National",revenue:"$3.4M",conversion:"2.1%",returnRate:"8%",stockoutRisk:"High",content:"78%",sentiment:"Positive",assocReady:"78%",healthScore:72,status:"Watch"},
    {name:"Queen Cotton Comforter Set",category:"Home",region:"Northeast",revenue:"$4.8M",conversion:"1.8%",returnRate:"12%",stockoutRisk:"Critical",content:"71%",sentiment:"Positive",assocReady:"55%",healthScore:52,status:"Critical"},
    {name:"Modular Fabric Sofa",category:"Home",region:"National",revenue:"$6.2M",conversion:"0.9%",returnRate:"18%",stockoutRisk:"Low",content:"42%",sentiment:"Negative",assocReady:"44%",healthScore:45,status:"Critical"},
    {name:"Ceramic Dinnerware Set",category:"Kitchen",region:"Midwest",revenue:"$1.4M",conversion:"2.4%",returnRate:"6%",stockoutRisk:"Low",content:"85%",sentiment:"Positive",assocReady:"72%",healthScore:78,status:"Watch"},
    {name:"Kids Everyday Hoodie",category:"Kids",region:"National",revenue:"$1.8M",conversion:"2.6%",returnRate:"9%",stockoutRisk:"Low",content:"88%",sentiment:"Positive",assocReady:"81%",healthScore:86,status:"Healthy"},
    {name:"Cotton Bath Towel Bundle",category:"Bath",region:"National",revenue:"$0.9M",conversion:"3.1%",returnRate:"4%",stockoutRisk:"Low",content:"92%",sentiment:"Positive",assocReady:"85%",healthScore:91,status:"Healthy"},
    {name:"Accent Floor Lamp",category:"Lighting",region:"West",revenue:"$1.1M",conversion:"1.5%",returnRate:"14%",stockoutRisk:"Medium",content:"61%",sentiment:"Mixed",assocReady:"58%",healthScore:64,status:"Watch"}
];

const actions = [
    {title:"Update fit guidance for Women's Linen Shirt",owner:"eCommerce Content Lead",func:"eCommerce",priority:"High",impact:"Reduce returns",due:"Jun 10",sku:"Women's Linen Shirt",status:"In Progress",kpi:"Return Rate"},
    {title:"Transfer Queen Comforter inventory to Northeast",owner:"Supply Chain Lead",func:"Supply Chain",priority:"Critical",impact:"Reduce stockouts",due:"Jun 7",sku:"Queen Cotton Comforter Set",status:"Pending Approval",kpi:"Stockout"},
    {title:"Publish associate learning card for Men's Stretch Chino",owner:"Store Ops Training Lead",func:"Store Operations",priority:"Medium",impact:"Improve associate confidence",due:"Jun 12",sku:"Men's Stretch Chino",status:"Ready",kpi:"Assoc. Confidence"},
    {title:"Add dimensions to Modular Fabric Sofa product page",owner:"Home Goods Merchant",func:"Merchandising",priority:"High",impact:"Improve conversion",due:"Jun 8",sku:"Modular Fabric Sofa",status:"Not Started",kpi:"Conversion"},
    {title:"Update product photos for Women's Linen Shirt",owner:"Digital Content Team",func:"eCommerce",priority:"Medium",impact:"Reduce returns",due:"Jun 15",sku:"Women's Linen Shirt",status:"In Progress",kpi:"Return Rate"},
    {title:"Resolve replenishment delay for Queen Comforter",owner:"Supply Chain Lead",func:"Supply Chain",priority:"Critical",impact:"Protect revenue",due:"Jun 6",sku:"Queen Cotton Comforter Set",status:"In Progress",kpi:"Revenue"},
    {title:"Markdown analysis for Ceramic Dinnerware overstock",owner:"Midwest Regional Merchant",func:"Merchandising",priority:"Low",impact:"Reduce overstock",due:"Jun 20",sku:"Ceramic Dinnerware Set",status:"Completed",kpi:"Inventory"},
    {title:"Deploy associate app to 50 additional stores",owner:"Store Ops Lead",func:"Store Operations",priority:"High",impact:"Scale pilot",due:"Jun 14",sku:"N/A",status:"Completed",kpi:"Assoc. Confidence"}
];

const pageTitles = {
    'dashboard': 'CEO Control Tower Dashboard',
    'sku-health': 'SKU Health Monitor',
    'sku-detail': 'SKU Detail',
    'content-hub': 'Product Content Quality Hub',
    'inventory': 'Inventory Availability Dashboard',
    'associate': 'Associate Assist App',
    'actions': 'Action Center',
    'sprint': '90-Day Sprint Impact Tracker'
};

// Navigation
function showScreen(screenId) {
    document.querySelectorAll('.screen').forEach(s => s.classList.remove('active'));
    document.getElementById('screen-' + screenId).classList.add('active');
    document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));
    document.querySelector('[data-screen="'+screenId+'"]').classList.add('active');
    document.getElementById('pageTitle').textContent = pageTitles[screenId] || '';
}

function switchRole(role) {
    if (role === 'associate') {
        showScreen('associate');
    } else if (role === 'merchant') {
        showScreen('sku-health');
    } else if (role === 'supply-chain') {
        showScreen('inventory');
    } else if (role === 'store-ops') {
        showScreen('actions');
    } else {
        showScreen('dashboard');
    }
}

// SKU Table
function renderSKUTable(data) {
    const tbody = document.getElementById('skuTableBody');
    tbody.innerHTML = '';
    data.forEach((sku, i) => {
        const statusClass = sku.status === 'Critical' ? 'chip-critical' : sku.status === 'Watch' ? 'chip-watch' : 'chip-healthy';
        const stockClass = sku.stockoutRisk === 'Critical' ? 'chip-critical' : sku.stockoutRisk === 'High' ? 'chip-high' : sku.stockoutRisk === 'Medium' ? 'chip-watch' : 'chip-healthy';
        tbody.innerHTML += '<tr onclick="openSKUDetail('+i+')"><td style="font-weight:600;">'+sku.name+'</td><td>'+sku.category+'</td><td>'+sku.region+'</td><td>'+sku.revenue+'</td><td>'+sku.conversion+'</td><td>'+sku.returnRate+'</td><td><span class="chip '+stockClass+'">'+sku.stockoutRisk+'</span></td><td>'+sku.content+'</td><td>'+sku.sentiment+'</td><td style="font-weight:700;">'+sku.healthScore+'</td><td><span class="chip '+statusClass+'">'+sku.status+'</span></td></tr>';
    });
}

function filterSKUs() {
    const search = document.getElementById('skuSearch').value.toLowerCase();
    const cat = document.getElementById('filterCategory').value;
    const region = document.getElementById('filterRegion').value;
    const status = document.getElementById('filterStatus').value;
    const issue = document.getElementById('filterIssue').value;

    let filtered = skuData.filter(sku => {
        if (search && !sku.name.toLowerCase().includes(search)) return false;
        if (cat && sku.category !== cat) return false;
        if (region && sku.region !== region) return false;
        if (status && sku.status !== status) return false;
        if (issue === 'high-return' && parseInt(sku.returnRate) < 15) return false;
        if (issue === 'high-stockout' && sku.stockoutRisk !== 'High' && sku.stockoutRisk !== 'Critical') return false;
        if (issue === 'low-content' && parseInt(sku.content) > 65) return false;
        return true;
    });
    renderSKUTable(filtered);
}

function openSKUDetail(idx) {
    const sku = skuData[idx];
    document.getElementById('skuDetailName').textContent = sku.name;
    document.getElementById('skuDetailScore').textContent = sku.healthScore;
    const statusClass = sku.status === 'Critical' ? 'chip-critical' : sku.status === 'Watch' ? 'chip-watch' : 'chip-healthy';
    document.getElementById('skuDetailStatus').className = 'chip ' + statusClass;
    document.getElementById('skuDetailStatus').textContent = sku.status;
    showScreen('sku-detail');
}

// Alerts
function ackAlert(idx, event) {
    event.stopPropagation();
    const items = document.querySelectorAll('.alert-item');
    items[idx].classList.add('acknowledged');
    items[idx].querySelector('.alert-ack-btn').textContent = 'Acknowledged';
    showToast('Alert acknowledged');
}

// Decisions
function approveDecision(el) {
    el.classList.add('approved');
    el.querySelector('.decision-status').textContent = 'Approved';
    showToast('Decision approved');
}

// SKU Detail actions
function generateContentFix() {
    document.getElementById('contentFixPanel').style.display = 'block';
    showToast('AI content fix generated');
}

function approvePageUpdate() {
    const btn = document.getElementById('btnApproveUpdate');
    btn.textContent = 'Approved';
    btn.style.background = '#aaa';
    btn.disabled = true;
    showToast('Product page update approved');
}

function createTransferTask() {
    showToast('Inventory transfer task created in Action Center');
}

function sendLearningCard() {
    showModal('Learning Card Sent', 'Microlearning card for this product has been sent to 342 store associates across affected regions. Associates will see it in their next shift briefing.');
}

// Inventory
function approveTransfer(btn, statusText) {
    const card = btn.closest('.inv-card');
    const chip = card.querySelector('.chip');
    if (statusText === 'Transfer Approved') {
        chip.className = 'chip chip-healthy';
        chip.textContent = 'Approved';
    } else {
        chip.className = 'chip chip-pending';
        chip.textContent = 'Under Review';
    }
    showToast(statusText);
}

// Associate poll
function selectPoll(el, idx) {
    document.querySelectorAll('#pollOptions .poll-option').forEach(o => o.classList.remove('selected'));
    el.classList.add('selected');
    const result = document.getElementById('pollResult');
    result.style.display = 'block';
    const msgs = ['Response recorded. Training resources will be sent.', 'Response recorded. Additional tips available.', 'Great! Your confidence helps customers.'];
    result.textContent = msgs[idx];
}

// Content Hub
function updateContentProgress() {
    const selects = document.querySelectorAll('#contentChecklist select');
    let score = 0;
    selects.forEach(sel => {
        if (sel.value === 'Published') score += 25;
        else if (sel.value === 'Approved') score += 20;
        else if (sel.value === 'Drafted') score += 10;
    });
    const pct = Math.min(100, Math.round(score / (selects.length * 25) * 100));
    document.getElementById('skuContentPct').textContent = pct + '%';
    document.getElementById('skuContentBar').style.width = pct + '%';
}

// Actions table
function renderActions() {
    const tbody = document.getElementById('actionTableBody');
    tbody.innerHTML = '';
    actions.forEach((a, i) => {
        const prClass = a.priority === 'Critical' ? 'chip-critical' : a.priority === 'High' ? 'chip-high' : a.priority === 'Medium' ? 'chip-watch' : 'chip-low';
        const stClass = a.status === 'Completed' ? 'chip-completed' : a.status === 'In Progress' ? 'chip-inprogress' : a.status === 'Pending Approval' ? 'chip-pending' : a.status === 'Ready' ? 'chip-ready' : 'chip-notstarted';
        tbody.innerHTML += '<tr><td style="font-weight:500;">'+a.title+'</td><td>'+a.owner+'</td><td>'+a.func+'</td><td><span class="chip '+prClass+'">'+a.priority+'</span></td><td>'+a.impact+'</td><td>'+a.due+'</td><td>'+a.sku+'</td><td><select class="filter-select" style="min-width:130px;font-size:11px;padding:4px 8px;" onchange="updateActionStatus('+i+',this.value)"><option '+(a.status==="Not Started"?"selected":"")+'>Not Started</option><option '+(a.status==="Ready"?"selected":"")+'>Ready</option><option '+(a.status==="In Progress"?"selected":"")+'>In Progress</option><option '+(a.status==="Pending Approval"?"selected":"")+'>Pending Approval</option><option '+(a.status==="Completed"?"selected":"")+'>Completed</option></select></td></tr>';
    });
    updateActionSummary();
}

function updateActionStatus(idx, val) {
    actions[idx].status = val;
    updateActionSummary();
    showToast('Action status updated to: ' + val);
}

function updateActionSummary() {
    document.getElementById('totalActions').textContent = actions.length;
    document.getElementById('completedActions').textContent = actions.filter(a => a.status === 'Completed').length;
    document.getElementById('inProgressActions').textContent = actions.filter(a => a.status === 'In Progress').length;
    document.getElementById('pendingActions').textContent = actions.filter(a => a.status === 'Pending Approval' || a.status === 'Ready' || a.status === 'Not Started').length;
}

// Toast
function showToast(msg) {
    const t = document.getElementById('toast');
    t.textContent = msg;
    t.classList.add('show');
    setTimeout(() => t.classList.remove('show'), 3000);
}

// Modal
function showModal(title, text) {
    document.getElementById('modalTitle').textContent = title;
    document.getElementById('modalText').textContent = text;
    document.getElementById('modal').classList.add('show');
}

function closeModal() {
    document.getElementById('modal').classList.remove('show');
}

// Charts
function drawLineChart(canvasId, data, color, label) {
    const canvas = document.getElementById(canvasId);
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    const dpr = window.devicePixelRatio || 1;
    const rect = canvas.parentElement.getBoundingClientRect();
    canvas.width = rect.width * dpr;
    canvas.height = 160 * dpr;
    canvas.style.width = rect.width + 'px';
    canvas.style.height = '160px';
    ctx.scale(dpr, dpr);

    const w = rect.width;
    const h = 160;
    const padding = {top: 20, right: 20, bottom: 30, left: 45};
    const chartW = w - padding.left - padding.right;
    const chartH = h - padding.top - padding.bottom;

    const max = Math.max(...data);
    const min = Math.min(...data);
    const range = max - min || 1;

    ctx.clearRect(0, 0, w, h);

    // Grid
    ctx.strokeStyle = '#EDF2F7';
    ctx.lineWidth = 1;
    for (let i = 0; i <= 4; i++) {
        const y = padding.top + (chartH / 4) * i;
        ctx.beginPath();
        ctx.moveTo(padding.left, y);
        ctx.lineTo(w - padding.right, y);
        ctx.stroke();
    }

    // Y-axis labels
    ctx.fillStyle = '#8896AB';
    ctx.font = '10px sans-serif';
    ctx.textAlign = 'right';
    for (let i = 0; i <= 4; i++) {
        const val = max - (range / 4) * i;
        const y = padding.top + (chartH / 4) * i;
        ctx.fillText(val.toFixed(1), padding.left - 8, y + 3);
    }

    // X-axis labels
    ctx.textAlign = 'center';
    const weeks = ['W1','W2','W3','W4','W5','W6','W7','W8'];
    data.forEach((_, i) => {
        const x = padding.left + (chartW / (data.length - 1)) * i;
        ctx.fillText(weeks[i] || 'W'+(i+1), x, h - 8);
    });

    // Area fill
    ctx.beginPath();
    data.forEach((v, i) => {
        const x = padding.left + (chartW / (data.length - 1)) * i;
        const y = padding.top + chartH - ((v - min) / range) * chartH;
        if (i === 0) ctx.moveTo(x, y);
        else ctx.lineTo(x, y);
    });
    ctx.lineTo(padding.left + chartW, padding.top + chartH);
    ctx.lineTo(padding.left, padding.top + chartH);
    ctx.closePath();
    ctx.fillStyle = color + '15';
    ctx.fill();

    // Line
    ctx.beginPath();
    data.forEach((v, i) => {
        const x = padding.left + (chartW / (data.length - 1)) * i;
        const y = padding.top + chartH - ((v - min) / range) * chartH;
        if (i === 0) ctx.moveTo(x, y);
        else ctx.lineTo(x, y);
    });
    ctx.strokeStyle = color;
    ctx.lineWidth = 2.5;
    ctx.stroke();

    // Dots
    data.forEach((v, i) => {
        const x = padding.left + (chartW / (data.length - 1)) * i;
        const y = padding.top + chartH - ((v - min) / range) * chartH;
        ctx.beginPath();
        ctx.arc(x, y, 4, 0, Math.PI * 2);
        ctx.fillStyle = color;
        ctx.fill();
        ctx.strokeStyle = '#fff';
        ctx.lineWidth = 2;
        ctx.stroke();
    });
}

function drawCharts() {
    drawLineChart('chartConversion', [1.4, 1.42, 1.45, 1.48, 1.52, 1.56, 1.59, 1.62], '#2D4A7A', 'Conversion %');
    drawLineChart('chartReturns', [18.2, 17.8, 17.1, 16.5, 16.0, 15.6, 15.2, 14.8], '#C0392B', 'Return Rate %');
    drawLineChart('chartStockouts', [42, 40, 38, 36, 34, 33, 31, 29], '#D4892A', 'Stockout Incidents');
    drawLineChart('chartContent', [62, 65, 68, 72, 74, 77, 79, 81], '#2E7D4F', 'Content %');
}

// Init
window.addEventListener('load', function() {
    renderSKUTable(skuData);
    renderActions();
    drawCharts();
    updateContentProgress();
});

window.addEventListener('resize', function() {
    drawCharts();
});
</script>
</body>
</html>'''


def main():
    # Write HTML file
    output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'meridian_control_tower.html')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(HTML_CONTENT)
    print(f"Generated: {output_path}")

    # Find available port
    port = 8080
    handler = http.server.SimpleHTTPRequestHandler

    while port < 8100:
        try:
            os.chdir(os.path.dirname(os.path.abspath(__file__)))
            server = socketserver.TCPServer(("", port), handler)
            break
        except OSError:
            port += 1
    else:
        print("Could not find an available port between 8080-8099.")
        return

    url = f"http://localhost:{port}/meridian_control_tower.html"
    print(f"\n{'='*60}")
    print(f"  Meridian Customer Promise Control Tower")
    print(f"  PwC Advisory Prototype")
    print(f"{'='*60}")
    print(f"\n  Running at: {url}")
    print(f"\n  Press Ctrl+C to stop the server.")
    print(f"{'='*60}\n")

    # Open browser
    threading.Timer(1.0, lambda: webbrowser.open(url)).start()

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
        server.shutdown()


if __name__ == '__main__':
    main()
