import datetime

# 1. Read Astronomy JS
with open('astronomy.min.js', 'r') as f:
    astronomy_js = f.read()

# 2. CSS Content
css_content = r"""
:root {
    --primary: #005dac;
    --on-primary: #ffffff;
    --hover: #00539a;
    --background: #f9f9ff;
    --surface: #ffffff;
    --text: #181c21;
    --border: #c1c6d4;
    --muted: #f2f3fc;
    --success: #0b6b1d;
    --on-success: #ffffff;
    --danger: #ba1a1a;
    --on-danger: #ffffff;
    --highlight-bg: #d4e3ff;
}
@media (prefers-color-scheme: dark) {
    :root:not(.light) {
        --primary: #a5c8ff;
        --on-primary: #00315f;
        --hover: #72adff;
        --background: #101319;
        --surface: #0b0e14;
        --text: #e0e2ea;
        --border: #414752;
        --muted: #181c21;
        --success: #82db7e;
        --on-success: #00390a;
        --danger: #ffb4ab;
        --on-danger: #93000a;
        --highlight-bg: #001c3a;
    }
}
:root.dark {
    --primary: #a5c8ff;
    --on-primary: #00315f;
    --hover: #72adff;
    --background: #101319;
    --surface: #0b0e14;
    --text: #e0e2ea;
    --border: #414752;
    --muted: #181c21;
    --success: #82db7e;
    --on-success: #00390a;
    --danger: #ffb4ab;
    --on-danger: #93000a;
    --highlight-bg: #001c3a;
}
* {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
    outline-offset: 2px;
}
*:focus-visible {
    outline: 2px solid var(--primary);
}
body {
    background: var(--background);
    color: var(--text);
    font-family: sans-serif;
    display: flex;
    justify-content: center;
    min-height: 100vh;
    padding: 1rem;
}
.container {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 8px;
    max-width: 960px;
    padding: 2rem;
    width: 100%;
    position: relative;
    margin: 2rem 0;
}
.hidden {
    display: none !important;
}
h1, h2, h3, label {
    margin: .5rem 0;
}
label {
    display: block;
    font-weight: 700;
}
input, select, button {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 4px;
    color: var(--text);
    font-size: 1rem;
    padding: .5rem;
    width: 100%;
}
button {
    cursor: pointer;
}
button:disabled {
    opacity: .6;
    cursor: not-allowed;
}
.primary {
    background: var(--primary);
    color: var(--on-primary);
    border: 0;
}
.primary:hover:not(:disabled) {
    background: var(--hover);
}
.secondary:hover:not(:disabled) {
    background: var(--muted);
}
.danger, .success {
    color: var(--on-danger);
    border: 0;
    background: var(--danger);
}
.success {
    background: var(--success);
    color: var(--on-success);
}
.danger:hover, .success:hover {
    filter: brightness(.9);
}
.selectors {
    position: absolute;
    right: 2rem;
    top: 1rem;
    display: flex;
    gap: 8px;
}
.selectors select {
    width: auto;
    font-size: .9rem;
}
.row {
    display: flex;
    gap: 1rem;
    margin-bottom: 1rem;
}
.group {
    flex: 1;
}
.party-row {
    display: flex;
    gap: .5rem;
    align-items: center;
    margin-bottom: .5rem;
}
.party-row input[type=text] {
    flex: 2;
}
.party-row input[type=number] {
    flex: 1;
}
.party-row button {
    width: auto;
    padding: .5rem 1rem;
}
.results-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1rem;
    margin-top: 1rem;
}
table {
    border-collapse: collapse;
    margin-top: 1rem;
    width: 100%;
    font-size: .9rem;
}
th, td {
    border: 1px solid var(--border);
    padding: .5rem;
    text-align: left;
}
th {
    background: var(--primary);
    color: var(--on-primary);
}
.comparison {
    margin-top: 2rem;
    padding-top: 1rem;
    border-top: 1px solid var(--border);
}
.positive {
    color: var(--success);
    font-weight: 700;
}
.negative {
    color: var(--danger);
    font-weight: 700;
}
.step {
    border: 1px solid var(--border);
    margin-bottom: 1rem;
    padding: 1rem;
    border-radius: 4px;
}
.highlight {
    background: var(--highlight-bg);
    font-weight: 700;
}
.error {
    color: var(--danger);
    font-size: .9rem;
    margin: 1rem 0;
    display: block;
    font-weight: 500;
}
dialog {
    background: var(--surface);
    color: var(--text);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 1.5rem;
    max-width: 800px;
    max-height: 90%;
    width: 100%;
    margin: auto;
    position: fixed;
    overflow-y: auto;
}
dialog::backdrop {
    background: rgba(0, 0, 0, 0.5);
}
.dialog-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1.5rem;
}
.dialog-header h2 {
    margin: 0;
    font-size: 1.5rem;
}
.close-button {
    background: transparent;
    color: var(--text);
    padding: .25rem;
    font-size: 1.5rem;
    line-height: 1;
    border: 0;
    width: auto;
    cursor: pointer;
}
.close-button:hover {
    background: var(--muted);
    color: var(--text);
}
.actions {
    display: flex;
    gap: 1rem;
    margin-top: 1rem;
}
.info {
    font-size: .9rem;
    opacity: .8;
    line-height: 1.6;
}
.stats {
    margin-top: 1rem;
    padding: 1rem;
    border: 1px solid var(--border);
    border-radius: 4px;
}
@media(max-width: 768px) {
    .results-grid {
        grid-template-columns: 1fr;
    }
    .selectors {
        position: static;
        justify-content: end;
        margin-bottom: .5rem;
    }
    .row {
        flex-direction: column;
    }
}

/* Tab Styles */
.tabs {
    display: flex;
    gap: 0;
    margin-bottom: 2rem;
    border-bottom: 1px solid var(--border);
}
.tab-btn {
    background: var(--surface);
    border: 1px solid var(--border);
    border-bottom: none;
    padding: 0.75rem 1.5rem;
    cursor: pointer;
    font-weight: 600;
    color: var(--text);
    opacity: 0.7;
    border-radius: 8px 8px 0 0;
    margin-right: 0.25rem;
}
.tab-btn:hover {
    background: var(--muted);
    opacity: 1;
}
.tab-btn.active {
    background: var(--primary);
    color: var(--on-primary);
    opacity: 1;
    border-color: var(--primary);
}
.tab-pane {
    display: none;
}
.tab-pane.active {
    display: block;
}

/* Map specific */
#mapCanvas {
    width: 100%;
    height: auto;
    border: 1px solid var(--border);
    background-color: #87CEEB;
    border-radius: 4px;
    margin-top: 1rem;
    image-rendering: pixelated;
}
.map-controls {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 1rem;
    margin-bottom: 1rem;
}
"""

# 3. HTML Structure
html_start = r"""<!DOCTYPE html>
<html lang="en">
	<head>
		<meta charset="UTF-8">
		<meta name="viewport" content="width=device-width,initial-scale=1">
		<title>Indonesia Election & Visibility Tools</title>
		<style>
""" + css_content + r"""
		</style>
	</head>
	<body>
		<div class="container">
            <div class="selectors">
				<select id="language">
					<option value="en">English</option>
					<option value="id">Bahasa Indonesia</option>
				</select>
				<select id="theme">
					<option value="auto">Auto</option>
					<option value="light">Light</option>
					<option value="dark">Dark</option>
				</select>
			</div>

            <div class="tabs">
                <button class="tab-btn active" onclick="switchTab('apportionment')">Apportionment</button>
                <button class="tab-btn" onclick="switchTab('visibility')">Visibility Map</button>
            </div>

            <!-- APPORTIONMENT SECTION -->
            <div id="apportionment" class="tab-pane active">
			    <h1 id="title"></h1>
			    <p id="subtitle" class="info"></p>
			    <div id="input">
				    <div class="row">
					    <div class="group">
						    <label id="seatsLabel" for="seats"></label>
						    <input type="number" id="seats" min="1" value="10">
					    </div>
					    <div class="group">
						    <label id="thresholdLabel" for="threshold"></label>
						    <input type="text" id="threshold" value="4">
					    </div>
				    </div>
				    <div id="list" style="margin-bottom:1rem"></div>
				    <div class="row" style="gap:.5rem">
					    <button id="add" class="secondary" style="flex:1"></button>
					    <button id="clear" class="secondary" style="flex:1"></button>
					    <button id="import" class="secondary" style="flex:1"></button>
				    </div>
				    <input type="file" id="file" accept=".csv,.tsv,.txt" class="hidden">
				    <span id="error" class="error hidden" aria-live="polite"></span>
				    <button id="calculate" class="primary"></button>
			    </div>
			    <div id="results" class="hidden">
				    <div class="actions">
					    <button id="edit" class="secondary" style="flex:1"></button>
					    <button id="steps" class="secondary" style="flex:1"></button>
					    <button id="export" class="success" style="flex:1"></button>
				    </div>
				    <div id="stats" class="stats"></div>
				    <div class="results-grid">
					    <div>
						    <h2 id="hareTitle"></h2>
						    <div id="hare"></div>
					    </div>
					    <div>
						    <h2 id="sainteLagueTitle"></h2>
						    <div id="sainteLague"></div>
					    </div>
				    </div>
				    <div class="comparison">
					    <h2 id="compareTitle"></h2>
					    <div id="compare"></div>
				    </div>
			    </div>
            </div>

            <!-- VISIBILITY MAP SECTION -->
            <div id="visibility" class="tab-pane">
                <h1 id="mapTitle">Hilal Visibility Map</h1>
                <p class="info" id="mapSubtitle">Indonesia Region</p>

                <div class="map-controls">
                    <div class="group">
                        <label id="dateLabel" for="mapDate">Date</label>
                        <input type="date" id="mapDate">
                    </div>
                    <div class="group">
                        <label id="criteriaLabel" for="mapCriteria">Criteria</label>
                        <select id="mapCriteria">
                            <option value="mabbims">MABBIMS (Alt≥3°, Elong≥6.4°)</option>
                            <option value="alt0">Altitude > 0°</option>
                        </select>
                    </div>
                    <div class="group">
                         <label>&nbsp;</label>
                         <button id="renderMap" class="primary">Render Map</button>
                    </div>
                </div>
                <div id="mapStatus" class="info" style="font-style:italic; min-height: 1.2em;"></div>
                <canvas id="mapCanvas"></canvas>
                <div id="mapLegend" class="info" style="margin-top:0.5rem">
                    <span style="display:inline-block;width:12px;height:12px;background:#0b6b1d;margin-right:4px;"></span><span id="legendVisible">Visible</span>
                    <span style="display:inline-block;width:12px;height:12px;background:#87CEEB;border:1px solid #ccc;margin-left:8px;margin-right:4px;"></span><span id="legendNotVisible">Not Visible</span>
                </div>
            </div>

		</div>
		<dialog id="modal">
			<div class="dialog-header">
				<h2 id="modalTitle"></h2>
				<button id="close" class="close-button">×</button>
			</div>
			<div id="modalSteps"></div>
		</dialog>

        <script>
""" + astronomy_js + r"""
        </script>

		<script>
            // ----- TABS -----
            function switchTab(tabId) {
                document.querySelectorAll('.tab-content, .tab-pane').forEach(el => el.classList.remove('active'));
                document.querySelectorAll('.tab-btn').forEach(el => el.classList.remove('active'));

                document.getElementById(tabId).classList.add('active');
                // Find button (simple match)
                const btns = document.querySelectorAll('.tab-btn');
                if (tabId === 'apportionment') btns[0].classList.add('active');
                if (tabId === 'visibility') btns[1].classList.add('active');
            }

            // ----- APPORTIONMENT LOGIC -----
			const text = {
				en: {
                    // Apportionment Strings
					title: 'ApportionmentCalc',
					subtitle: 'Electoral seat allocation calculator: Sainte-Laguë vs Hare Quota',
					autoTheme: 'Auto Theme',
					lightTheme: 'Light',
					darkTheme: 'Dark',
					seatsLabel: 'Total Seats',
					thresholdLabel: 'Electoral Threshold (%)',
					add: '+ Add Party',
					calculate: 'Calculate Allocation',
					edit: 'Edit Inputs',
					steps: 'Show Sainte-Laguë Steps',
					export: 'Export to CSV',
					hareTitle: 'Hare Quota Method',
					sainteLagueTitle: 'Sainte-Laguë Method',
					compareTitle: 'Results Comparison',
					modalTitle: 'Sainte-Laguë Step-by-Step',
					party: 'Party',
					votes: 'Votes',
					seatsColumn: 'Seats',
					remainder: 'Remainder',
					diff: 'Diff',
					quota: 'Quota',
					totalVotes: 'Total Valid Votes',
					thresholdVotes: 'Threshold Votes',
					belowThreshold: 'Parties below threshold',
					partyPlaceholder: 'Party Name',
					votesPlaceholder: 'Votes',
					alertSeats: 'Total seats must be at least 1.',
					alertParties: 'Please add at least one party with votes.',
					round: 'Round',
					winner: 'Winner',
					quotient: 'Quotient',
					divisor: 'Divisor',
					seatAllocated: 'Seat #{n}',
					divisorsText: 'Divisors: 1, 3, 5, 7...',
					quotientDetail: 'Quotient Detail',
					detailsLimited: 'Showing details for the first {n} rounds only.',
					summaryLimited: 'Showing first {n} rounds only.',
					winnerPrefix: 'Winner: ',
					share: '%',
					passedHeader: 'Passed Threshold?',
					hareSeatsHeader: 'Hare Seats',
					sainteLagueSeatsHeader: 'Kursi Sainte-Laguë',
					differenceHeader: 'Difference',
					yes: 'Yes',
					no: 'No',
					import: 'Import CSV/TSV',
					alertImport: 'Error importing file. Please ensure it is a valid CSV/TSV with "Party" and "Votes" columns.',
					clear: 'Clear All',
					clearConfirm: 'Are you sure you want to clear all parties?',
					removeParty: 'Remove Party',
					closeModal: 'Close Modal',
					languageLabel: 'Language',
					themeLabel: 'Theme',
                    // Map Strings
                    mapTitle: 'Hilal Visibility Map',
                    mapSubtitle: 'Indonesia Region',
                    renderMap: 'Render Map',
                    dateLabel: 'Date',
                    criteriaLabel: 'Criteria',
                    legendVisible: 'Visible',
                    legendNotVisible: 'Not Visible'
				},
				id: {
					title: 'ApportionmentCalc',
					subtitle: 'Kalkulator alokasi kursi pemilu: Sainte-Laguë vs Kuota Hare',
					autoTheme: 'Tema Otomatis',
					lightTheme: 'Terang',
					darkTheme: 'Gelap',
					seatsLabel: 'Jumlah Kursi',
					thresholdLabel: 'Ambang Batas Parlemen (%)',
					add: '+ Tambah Partai',
					calculate: 'Hitung Alokasi',
					edit: 'Ubah Input',
					steps: 'Tampilkan Langkah Sainte-Laguë',
					export: 'Ekspor ke CSV',
					hareTitle: 'Metode Kuota Hare',
					sainteLagueTitle: 'Metode Sainte-Laguë',
					compareTitle: 'Perbandingan Hasil',
					modalTitle: 'Langkah-langkah Sainte-Laguë',
					party: 'Partai',
					votes: 'Suara',
					seatsColumn: 'Kursi',
					remainder: 'Sisa',
					diff: 'Selisih',
					quota: 'BPP (Bilangan Pembagi Pemilih)',
					totalVotes: 'Total Suara Sah',
					thresholdVotes: 'Suara Ambang Batas',
					belowThreshold: 'Partai di bawah ambang batas',
					partyPlaceholder: 'Nama Partai',
					votesPlaceholder: 'Jumlah Suara',
					alertSeats: 'Jumlah kursi harus minimal 1.',
					alertParties: 'Harap tambahkan setidaknya satu partai dengan suara.',
					round: 'Putaran',
					winner: 'Pemenang',
					quotient: 'Bilangan',
					divisor: 'Pembagi',
					seatAllocated: 'Kursi ke-{n}',
					divisorsText: 'Pembagi: 1, 3, 5, 7...',
					quotientDetail: 'Rincian Bilangan',
					detailsLimited: 'Menampilkan rincian untuk {n} putaran pertama saja.',
					summaryLimited: 'Menampilkan {n} putaran pertama saja.',
					winnerPrefix: 'Pemenang: ',
					share: '%',
					passedHeader: 'Lolos Ambang Batas?',
					hareSeatsHeader: 'Kursi Hare',
					sainteLagueSeatsHeader: 'Kursi Sainte-Laguë',
					differenceHeader: 'Selisih',
					yes: 'Ya',
					no: 'Tidak',
					import: 'Impor CSV/TSV',
					alertImport: 'Gagal mengimpor file. Pastikan format CSV/TSV valid dengan kolom "Partai" dan "Suara".',
					clear: 'Hapus Semua',
					clearConfirm: 'Apakah Anda yakin ingin menghapus semua partai?',
					removeParty: 'Hapus Partai',
					closeModal: 'Tutup Modal',
					languageLabel: 'Bahasa',
					themeLabel: 'Tema',
                    mapTitle: 'Peta Visibilitas Hilal',
                    mapSubtitle: 'Wilayah Indonesia',
                    renderMap: 'Render Peta',
                    dateLabel: 'Tanggal',
                    criteriaLabel: 'Kriteria',
                    legendVisible: 'Terlihat',
                    legendNotVisible: 'Tidak Terlihat'
				}
			};
			const elements = new Proxy({}, { get: (_, id) => document.getElementById(id) });
			const escape = string => string.replace(/[&<>"']/g, char => '&#' + char.charCodeAt(0) + ';');
			const STEPS_LIMIT = 50;
			const SUMMARY_LIMIT = 1000;

			class ApportionmentCalc {
				constructor() {
					this.parties = Object.entries({
						Apple: 25000,
						Blueberry: 15000,
						Cherry: 9000,
						Date: 5000,
						Elderberry: 1500
					}).map(([name, votes], i) => ({
						id: i + 1,
						name: name + ' Party',
						votes
					}));
					this.nextIndex = 6;
					this.data = null;
					this.setup();
					this.theme('auto');
					this.lang(navigator.language?.startsWith('id') ? 'id' : 'en');
				}
				setup() {
					const handlers = {
						add: () => this.add(),
						clear: () => this.clear(),
						calculate: () => this.calculate(),
						edit: () => this.display('input'),
						steps: () => this.modal(true),
						close: () => this.modal(false),
						export: () => this.export(),
						import: () => elements.file.click()
					};
					Object.entries(handlers).forEach(([id, handler]) => { if(elements[id]) elements[id].onclick = handler });
					elements.file.onchange = event => this.load(event.target.files[0]);
					elements.modal.onclick = event => {
						const rect = elements.modal.getBoundingClientRect();
						const inDialog = rect.top <= event.clientY && event.clientY <= rect.top + rect.height && rect.left <= event.clientX && event.clientX <= rect.left + rect.width;
						!inDialog && this.modal(false);
					};
					elements.modal.addEventListener('close', () => this.lastFocus?.focus());
					elements.language.onchange = event => this.lang(event.target.value);
					elements.theme.onchange = event => this.theme(event.target.value);
					elements.input.oninput = () => this.error();
					document.onkeydown = event => this.key(event);
					elements.list.onclick = event => {
						const row = event.target.closest('.party-row');
						event.target.matches('.danger') && row && this.remove(+row.dataset.id);
					};
					elements.list.onchange = event => {
						const row = event.target.closest('.party-row');
						const party = row && this.parties.find(p => p.id === +row.dataset.id);
						party && (event.target.type === 'text' ? party.name = event.target.value : event.target.value = party.votes = Math.max(0, Math.round(+event.target.value) || 0));
					};
				}
				key(event) {
					((event.ctrlKey || event.metaKey) && event.key === 'Enter') && this.calculate();
					const row = event.target.closest('.party-row');
					!event.ctrlKey && !event.metaKey && event.key === 'Enter' && row && event.target.matches('input') && (
						event.preventDefault(),
						(() => {
							const party = this.parties.find(p => p.id === +row.dataset.id);
							party && (event.target.type === 'text' ? party.name = event.target.value : party.votes = Math.max(0, Math.round(+event.target.value) || 0));
						})(),
						event.target.type === 'text' ? event.target.nextElementSibling?.focus() : row.nextElementSibling ? row.nextElementSibling.querySelector('input')?.focus() : this.add()
					);
				}
				string(key) {
					return text[this.language]?.[key] ?? key;
				}
				format(value, options = {}) {
					return value.toLocaleString(this.language === 'id' ? 'id-ID' : 'en-US', options);
				}
				table(headers, body) {
					return `<table><thead><tr>${headers.map(header => `<th>${header}</th>`).join('')}</tr></thead><tbody>${body}</tbody></table>`;
				}
				theme(themeName) {
					document.documentElement.className = themeName === 'auto' ? '' : themeName;
					elements.theme.value = themeName;
				}
				lang(language) {
					this.language = elements.language.value = document.documentElement.lang = language;
					Object.keys(text.en).forEach(key => elements[key] && (elements[key].textContent = this.string(key)));
					[...elements.theme.options].forEach(option => option.textContent = this.string(option.value + 'Theme'));
					[['close', 'closeModal'], ['language', 'languageLabel'], ['theme', 'themeLabel']].forEach(([id, key]) => elements[id].setAttribute('aria-label', this.string(key)));
					this.renderParties();
					!elements.results.classList.contains('hidden') && this.data && this.renderResults();
				}
				display(section) {
					['input', 'results'].forEach(id => elements[id].classList.toggle('hidden', id !== section));
					section === 'results' ? (elements.results.setAttribute('tabindex', '-1'), elements.results.focus()) : elements.seats.focus();
				}
				modal(visible) {
					visible ? (this.lastFocus = document.activeElement, this.renderSteps(), elements.modal.showModal()) : elements.modal.close();
				}
				error(message) {
					elements.error.textContent = message || '';
					elements.error.classList.toggle('hidden', !message);
				}
				add() {
					this.error();
					this.parties.push({ id: this.nextIndex++, name: '', votes: 0 });
					this.renderParties();
					elements.list.lastElementChild?.querySelector('input')?.focus();
				}
				clear() {
					confirm(this.string('clearConfirm')) && (this.parties = [], this.renderParties(), this.add(), this.error());
				}
				remove(id) {
					this.error();
					const index = this.parties.findIndex(party => party.id === id);
					this.parties = this.parties.filter(party => party.id !== id);
					this.renderParties();
					const target = Math.min(index, this.parties.length - 1);
					target >= 0 ? elements.list.children[target]?.querySelector('.danger')?.focus() : elements.add.focus();
				}
				renderParties() {
					elements.list.innerHTML = this.parties.map((party, i) => `<div class="party-row" data-id="${party.id}"><input type="text" value="${escape(party.name)}" placeholder="${this.string('partyPlaceholder')}" aria-label="${this.string('partyPlaceholder')} ${i + 1}"><input type="number" value="${party.votes || ''}" placeholder="${this.string('votesPlaceholder')}" min="0" aria-label="${this.string('votesPlaceholder')} ${i + 1}"><button class="danger" aria-label="${this.string('removeParty')} ${i + 1}">×</button></div>`).join('');
				}
				load(file) {
					const reader = new FileReader();
					reader.onload = event => {
						try {
							const lines = event.target.result.split(/\\r?\\n/).filter(line => line.trim());
							!lines.length && (() => { throw 0; })();
							const separator = lines[0].split('\\t').length > lines[0].split(',').length ? '\\t' : ',';
							const parse = line => line.split(new RegExp(`\\\\${separator}(?=(?:(?:[^"]*"){2})*[^"]*$)`)).map(cell => cell.trim().replace(/^"|"$/g, '').replace(/""/g, '"'));
							const header = parse(lines[0]);
							const find = regex => header.findIndex(cell => regex.test(cell));
							let nameIndex = find(/party|partai|name|nama/i), voteIndex = find(/vote|suara/i), start = 1;
							(nameIndex < 0 || voteIndex < 0) && (
								start = 0,
								(() => {
									const isNumber = cell => /^\d+$/.test(cell.replace(/[.,]/g, '').trim());
									voteIndex = header.findIndex(isNumber);
									nameIndex = voteIndex >= 0 && header.length === 2 ? 1 - voteIndex : header.findIndex(cell => !isNumber(cell));
								})()
							);
							(nameIndex < 0 || voteIndex < 0) && (() => { throw 0; })();
							const parties = lines.slice(start).map(line => {
								const cells = parse(line);
								return cells[nameIndex] ? { id: this.nextIndex++, name: cells[nameIndex], votes: +((cells[voteIndex] || '').replace(/[^\d.]/g, '')) || 0 } : null;
							}).filter(Boolean);
							!parties.length && (() => { throw 0; })();
							this.parties = parties;
							this.error();
							this.renderParties();
							elements.file.value = '';
						} catch {
							this.error(this.string('alertImport'));
						}
					};
					file && reader.readAsText(file);
				}
				calculate() {
					this.error();
					const seats = parseInt(elements.seats.value), threshold = parseFloat(elements.threshold.value.replace(',', '.')) || 0;
					this.parties = this.parties.filter(p => p.name.trim() || p.votes > 0);
					this.renderParties();
					(isNaN(seats) || seats < 1) ? this.error(this.string('alertSeats')) : (() => {
						const valid = this.parties.filter(party => party.votes >= 0 && (party.name || party.votes > 0)).map(party => ({ ...party, name: party.name || `${this.string('party')} ${party.id}`, hare: 0, sainteLague: 0, remainder: 0 }));
						const total = valid.reduce((sum, party) => sum + party.votes, 0);
						total === 0 ? this.error(this.string('alertParties')) : (() => {
							const minimumVotes = total * threshold / 100, passed = valid.filter(party => party.votes >= minimumVotes - 1e-7);
							!passed.length ? this.error(this.string('belowThreshold')) : (() => {
								const quota = total / seats;
								passed.forEach(party => {
									party.hare = Math.floor(party.votes * seats / total);
									party.remainder = (party.votes * seats % total) / seats;
									party.divisor = 1;
									party.quotient = party.votes;
								});
								let allocated = passed.reduce((sum, party) => sum + party.hare, 0);
								[...passed].sort((a, b) => b.remainder - a.remainder || b.votes - a.votes).slice(0, seats - allocated).forEach(party => party.hare++);
								const steps = Array.from({ length: seats }, (_, i) => {
									const winner = passed.reduce((best, party) => party.quotient > best.quotient || (party.quotient === best.quotient && party.votes > best.votes) ? party : best);
									const step = { round: i + 1, winner: winner.name, winnerId: winner.id, value: winner.quotient, divisor: winner.divisor, all: i < STEPS_LIMIT ? passed.map(({ id, name, quotient, divisor }) => ({ id, name, quotient, divisor })) : null };
									winner.sainteLague++;
									winner.divisor += 2;
									winner.quotient = winner.votes / winner.divisor;
									return step;
								});
								this.data = { total, minimumVotes, threshold, seats, quota, steps, results: valid.map(party => ({ ...party, passed: party.votes >= minimumVotes - 1e-7 })) };
								this.renderResults();
								this.display('results');
							})();
						})();
					})();
				}
				renderResults() {
					this.data && (() => {
						const { results, total, minimumVotes, threshold, quota } = this.data, passed = results.filter(result => result.passed), failed = results.filter(result => !result.passed);
						const row = (result, seats, extra = '') => `<tr><td>${escape(result.name)}</td><td>${this.format(result.votes)}</td><td>${this.format(result.votes / total * 100, { maximumFractionDigits: 2 })}%</td><td><strong>${seats}</strong></td>${extra}</tr>`;
						elements.stats.innerHTML = `<div class="info">${this.string('totalVotes')}: ${this.format(total)}<br>${this.string('thresholdVotes')} (${this.format(threshold)}%): ${this.format(minimumVotes, { maximumFractionDigits: 0 })}` + (failed.length ? `<br><span style="font-style:italic">${this.string('belowThreshold')}: ${failed.map(result => `${escape(result.name)} (${this.format(result.votes)}, ${this.format(result.votes / total * 100, { maximumFractionDigits: 2 })}%)`).join(', ')}</span>` : '') + '</div>';
						const headers = ['party', 'votes', 'share', 'seatsColumn'].map(key => this.string(key));
						elements.hare.innerHTML = `<p class="info">${this.string('quota')}: ${this.format(quota)}</p>` + this.table([...headers, this.string('remainder')], [...passed].sort((a, b) => b.hare - a.hare).map(result => row(result, result.hare, `<td>${this.format(result.remainder, { maximumFractionDigits: 6 })}</td>`)).join(''));
						elements.sainteLague.innerHTML = `<p class="info">${this.string('divisorsText')}</p>` + this.table(headers, [...passed].sort((a, b) => b.sainteLague - a.sainteLague).map(result => row(result, result.sainteLague)).join(''));
						elements.compare.innerHTML = this.table([this.string('party'), 'Hare', 'Sainte-Laguë', this.string('diff')], [...passed].sort((a, b) => b.votes - a.votes).map(result => {
							const difference = result.sainteLague - result.hare;
							return `<tr><td>${escape(result.name)}</td><td>${result.hare}</td><td>${result.sainteLague}</td><td class="${difference > 0 ? 'positive' : difference < 0 ? 'negative' : 'neutral'}">${difference > 0 ? '+' : ''}${difference}</td></tr>`;
						}).join(''));
					})();
				}
				renderSteps() {
					const { steps } = this.data || {};
					steps?.length && (() => {
						const summary = steps.slice(0, SUMMARY_LIMIT), summaryWarning = steps.length > SUMMARY_LIMIT ? `<p class="info" style="margin-top:1rem;font-style:italic">${this.string('summaryLimited').replace('{n}', SUMMARY_LIMIT)}</p>` : '';
						const details = steps.slice(0, STEPS_LIMIT), detailsWarning = steps.length > STEPS_LIMIT ? `<p class="info" style="margin-top:1rem;font-style:italic">${this.string('detailsLimited').replace('{n}', STEPS_LIMIT)}</p>` : '';
						const template = this.string('seatAllocated'), prefix = this.string('winnerPrefix'), options = { maximumFractionDigits: 2 };
						elements.modalSteps.innerHTML = this.table(['round', 'winner', 'quotient', 'divisor'].map(key => this.string(key)), summary.map(step => `<tr><td>${template.replace('{n}', step.round)}</td><td><strong>${escape(step.winner)}</strong></td><td>${this.format(step.value, options)}</td><td>${step.divisor}</td></tr>`).join('')) + summaryWarning + `<h3 style="margin-top:2rem">${this.string('quotientDetail')}</h3>${detailsWarning}` + details.map(step => step.all ? `<div class="step"><h4>${template.replace('{n}', step.round)} - ${prefix}${escape(step.winner)}</h4>` + this.table(step.all.map(quotient => `${escape(quotient.name)} (/${quotient.divisor})`), `<tr>${step.all.map(quotient => `<td class="${quotient.id === step.winnerId ? 'highlight' : ''}">${this.format(quotient.quotient, options)}</td>`).join('')}</tr>`) + '</div>' : '').join('') + detailsWarning;
					})();
				}
				export() {
					this.data && (() => {
						const { results } = this.data, total = results.reduce((sum, party) => sum + party.votes, 0);
						const headers = [this.string('party'), this.string('votes'), this.string('share'), this.string('passedHeader'), this.string('hareSeatsHeader'), this.string('sainteLagueSeatsHeader'), this.string('differenceHeader')].join(',');
						const csv = headers + '\\n' + results.map(result => `"${result.name.replace(/"/g, '""')}",${result.votes},"${this.format(result.votes / total * 100, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}",${result.passed ? this.string('yes') : this.string('no')},${result.hare},${result.sainteLague},${result.sainteLague - result.hare}`).join('\\n');
						Object.assign(document.createElement('a'), { href: URL.createObjectURL(new Blob([csv], { type: 'text/csv' })), download: `apportionment_${new Date().toISOString().slice(0, 19).replace(/[T:]/g, '-')}.csv` }).click();
					})();
				}
			}
			new ApportionmentCalc();


            // ----- VISIBILITY MAP LOGIC -----
            const mapCanvas = document.getElementById('mapCanvas');
            const mapCtx = mapCanvas.getContext('2d');
            const mapStatus = document.getElementById('mapStatus');
            const dateInput = document.getElementById('mapDate');
            const criteriaSelect = document.getElementById('mapCriteria');
            const renderBtn = document.getElementById('renderMap');

            // Default date
            dateInput.valueAsDate = new Date();

            const INDONESIA_BOUNDS = { minLat: -11, maxLat: 6, minLon: 95, maxLon: 141 };
            const PPD = 15; // Pixels per degree. 46 deg width * 15 = 690px. Fits well.

            let isRendering = false;
            let cancelRender = false;

            renderBtn.onclick = () => {
                if (isRendering) {
                    cancelRender = true;
                    // wait for loop to stop then restart
                    setTimeout(startRender, 100);
                } else {
                    startRender();
                }
            };

            function startRender() {
                cancelRender = false;
                isRendering = true;
                renderBtn.disabled = true;
                mapStatus.textContent = 'Calculating...';

                const bounds = INDONESIA_BOUNDS;
                const criteria = criteriaSelect.value;
                const dateStr = dateInput.value;
                // Use 12:00 UTC to avoid timezone edge cases for "that day"
                const date = new Date(dateStr + 'T12:00:00Z');

                const widthDeg = bounds.maxLon - bounds.minLon;
                const heightDeg = bounds.maxLat - bounds.minLat;

                mapCanvas.width = Math.ceil(widthDeg * PPD);
                mapCanvas.height = Math.ceil(heightDeg * PPD);

                // Default background (ocean)
                mapCtx.fillStyle = '#87CEEB';
                mapCtx.fillRect(0, 0, mapCanvas.width, mapCanvas.height);

                const imageData = mapCtx.getImageData(0, 0, mapCanvas.width, mapCanvas.height);
                const data = imageData.data;
                const totalPixels = mapCanvas.width * mapCanvas.height;
                let pixelIndex = 0;
                const chunkSize = 5000;

                function processChunk() {
                    if (cancelRender) {
                        isRendering = false;
                        renderBtn.disabled = false;
                        mapStatus.textContent = 'Cancelled.';
                        return;
                    }

                    const end = Math.min(pixelIndex + chunkSize, totalPixels);

                    for (; pixelIndex < end; pixelIndex++) {
                        const x = pixelIndex % mapCanvas.width;
                        const y = Math.floor(pixelIndex / mapCanvas.width);

                        // Lat from Top (maxLat) down
                        const lat = bounds.maxLat - (y / PPD);
                        const lon = bounds.minLon + (x / PPD);

                        const visible = checkVisibility(lat, lon, date, criteria);

                        if (visible) {
                            const idx = pixelIndex * 4;
                            // #0b6b1d (Green Success Color) -> R:11, G:107, B:29
                            data[idx] = 11;
                            data[idx+1] = 107;
                            data[idx+2] = 29;
                            data[idx+3] = 255;
                        }
                    }
                    mapCtx.putImageData(imageData, 0, 0);

                    if (pixelIndex < totalPixels) {
                        mapStatus.textContent = `Rendering... ${Math.round(pixelIndex/totalPixels*100)}%`;
                        requestAnimationFrame(processChunk);
                    } else {
                        isRendering = false;
                        renderBtn.disabled = false;
                        mapStatus.textContent = 'Done.';
                    }
                }
                requestAnimationFrame(processChunk);
            }

            function checkVisibility(lat, lon, date, criteria) {
                const observer = new Astronomy.Observer(lat, lon, 0);

                // Estimate Sunset Time for this location on this day
                // Local Noon approx:
                const noonOffsetDays = -lon / 360.0;
                const searchTime = date.AddDays(noonOffsetDays);

                // Search for sunset (+1 means upper limb touches horizon? No, +1 is direction rise->set?
                // Astronomy.SearchRiseSet(body, observer, direction, startTime, limitDays)
                // Direction: +1 = set, -1 = rise. Wait, usually rise is +1?
                // Docs: "direction=+1 for setting, -1 for rising"

                const sunset = Astronomy.SearchRiseSet(Astronomy.Body.Sun, observer, 1, searchTime, 1);
                if (!sunset) return false;

                const time = sunset.time;

                // Moon Params
                // Topocentric Altitude
                const moonEq = Astronomy.Equator(Astronomy.Body.Moon, time, observer, true, true);
                const moonHor = Astronomy.Horizon(time, observer, moonEq.ra, moonEq.dec, 'normal');
                const alt = moonHor.altitude;

                // Geocentric Elongation
                const elong = Astronomy.AngleFromSun(Astronomy.Body.Moon, time);

                if (criteria === 'mabbims') {
                    // Alt >= 3 deg, Elong >= 6.4 deg
                    return (alt >= 3 && elong >= 6.4);
                } else if (criteria === 'alt0') {
                    return (alt > 0);
                }
                return false;
            }

		</script>
	</body>
</html>
"""

with open('index.html', 'w') as f:
    f.write(html_start)
