import json

with open("final_trains.json", "r", encoding="utf-8") as f:
    trains = json.load(f)

for t in trains:
    h = int(t["hakata_dep"].split(":")[0])
    if 5 <= h < 10:
        t["time_band"] = "morning"
    elif 10 <= h < 16:
        t["time_band"] = "day"
    elif 16 <= h < 20:
        t["time_band"] = "evening"
    else:
        t["time_band"] = "night"

trains_json_str = json.dumps(trains, ensure_ascii=False)

html_template = """<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
  <title>JR博多駅→JR久留米駅 時刻表</title>
  <script src="https://www.gstatic.com/antigravity/web/dev/tailwindcss.min.js"></script>
  <style>
    /* Compact scrollbar */
    ::-webkit-scrollbar {
      width: 4px;
      height: 4px;
    }
    ::-webkit-scrollbar-thumb {
      background: rgba(150, 150, 150, 0.3);
      border-radius: 4px;
    }
    .no-scrollbar::-webkit-scrollbar {
      display: none;
    }
    .no-scrollbar {
      -ms-overflow-style: none;
      scrollbar-width: none;
    }
  </style>
</head>
<body class="bg-transparent text-[var(--foreground)] antialiased p-1 select-none font-sans">
  <div class="bg-[var(--card)] text-[var(--foreground)] border border-[var(--border)] rounded-2xl shadow-md overflow-hidden max-w-xl mx-auto flex flex-col h-[480px]">
    
    <!-- Top Bar -->
    <div class="px-3 py-2 border-b border-[var(--border)] bg-[var(--card)]/95 backdrop-blur flex items-center justify-between shrink-0">
      <div>
        <div class="flex items-center gap-1.5">
          <span class="inline-block w-2.5 h-2.5 rounded-full bg-emerald-500 animate-pulse"></span>
          <h1 class="font-bold text-sm tracking-tight">JR 博多 → 久留米</h1>
          <span class="text-[10px] px-1.5 py-0.5 rounded bg-emerald-100 text-emerald-800 dark:bg-emerald-950 dark:text-emerald-300 font-medium border border-emerald-300 dark:border-emerald-800">普通乗車券のみ</span>
        </div>
        <p class="text-[10.5px] text-[var(--muted-foreground)] mt-0.5">特急・新幹線除外 / 全便毎日運転（土休日も同一ダイヤ）</p>
      </div>

      <!-- Rapid Filter Toggle -->
      <button id="toggleRapidBtn" onclick="toggleRapidFilter()" class="text-xs px-2.5 py-1 rounded-lg border border-[var(--border)] bg-[var(--background)] hover:bg-[var(--accent)] text-[var(--foreground)] transition flex items-center gap-1 shrink-0 font-medium shadow-sm">
        <span id="rapidIcon">⚡</span>
        <span id="rapidLabel">快速のみ</span>
      </button>
    </div>

    <!-- Time Band Tabs (Fits completely on mobile screen) -->
    <div class="px-2 py-1 bg-[var(--background)]/70 border-b border-[var(--border)] flex items-center gap-1 text-xs shrink-0 overflow-x-auto no-scrollbar">
      <button class="band-btn flex-1 min-w-[56px] py-1 px-1 rounded-md text-center font-medium transition text-[11px]" data-band="now" onclick="selectBand('now')">
        ⏱️ 次の便
      </button>
      <button class="band-btn flex-1 min-w-[56px] py-1 px-1 rounded-md text-center font-medium transition text-[11px]" data-band="morning" onclick="selectBand('morning')">
        🌅 朝 <span class="opacity-70 text-[9px]">5-9</span>
      </button>
      <button class="band-btn flex-1 min-w-[56px] py-1 px-1 rounded-md text-center font-medium transition text-[11px]" data-band="day" onclick="selectBand('day')">
        ☀️ 昼 <span class="opacity-70 text-[9px]">10-15</span>
      </button>
      <button class="band-btn flex-1 min-w-[56px] py-1 px-1 rounded-md text-center font-medium transition text-[11px]" data-band="evening" onclick="selectBand('evening')">
        🌇 夕 <span class="opacity-70 text-[9px]">16-19</span>
      </button>
      <button class="band-btn flex-1 min-w-[56px] py-1 px-1 rounded-md text-center font-medium transition text-[11px]" data-band="night" onclick="selectBand('night')">
        🌙 夜 <span class="opacity-70 text-[9px]">20-23</span>
      </button>
      <button class="band-btn py-1 px-2 rounded-md text-center font-medium transition text-[11px]" data-band="all" onclick="selectBand('all')">
        全便
      </button>
    </div>

    <!-- Column Headers -->
    <div class="grid grid-cols-12 px-3 py-1 text-[11px] font-semibold text-[var(--muted-foreground)] bg-[var(--background)]/40 border-b border-[var(--border)] shrink-0 items-center">
      <div class="col-span-2">始発駅</div>
      <div class="col-span-2 text-center text-blue-600 dark:text-blue-400 font-bold">博多発</div>
      <div class="col-span-3 text-center">鳥栖(着/発)</div>
      <div class="col-span-2 text-center text-emerald-600 dark:text-emerald-400 font-bold">久留米着</div>
      <div class="col-span-3 text-right">種別 / 所要</div>
    </div>

    <!-- Trains List -->
    <div id="trainList" class="flex-1 overflow-y-auto divide-y divide-[var(--border)] text-xs">
      <!-- Injected by JavaScript -->
    </div>

    <!-- Bottom Status Bar -->
    <div class="px-3 py-1.5 bg-[var(--background)]/90 border-t border-[var(--border)] text-[10.5px] text-[var(--muted-foreground)] flex items-center justify-between shrink-0">
      <span class="flex items-center gap-1.5 truncate">
        <span class="inline-block w-1.5 h-1.5 rounded-full bg-blue-500"></span>
        <span class="truncate">行をタップで詳細・接続先を表示</span>
      </span>
      <span class="font-mono text-[10px] shrink-0 font-semibold text-[var(--foreground)]" id="countBadge">47便</span>
    </div>

  </div>

  <script>
    const TRAINS = __TRAINS_PLACEHOLDER__;

    let currentBand = 'day';
    let rapidOnly = false;
    let expandedRowId = null;

    function getAutoBand() {
      const h = new Date().getHours();
      if (h >= 5 && h < 10) return 'morning';
      if (h >= 10 && h < 16) return 'day';
      if (h >= 16 && h < 20) return 'evening';
      return 'night';
    }

    function selectBand(band) {
      currentBand = band;
      expandedRowId = null;
      render();
    }

    function toggleRapidFilter() {
      rapidOnly = !rapidOnly;
      expandedRowId = null;
      const btn = document.getElementById('toggleRapidBtn');
      const label = document.getElementById('rapidLabel');
      if (rapidOnly) {
        btn.classList.add('bg-blue-600', 'text-white', 'border-blue-600');
        btn.classList.remove('bg-[var(--background)]', 'text-[var(--foreground)]');
        label.innerText = '快速中';
      } else {
        btn.classList.remove('bg-blue-600', 'text-white', 'border-blue-600');
        btn.classList.add('bg-[var(--background)]', 'text-[var(--foreground)]');
        label.innerText = '快速のみ';
      }
      render();
    }

    function toggleDetail(no) {
      expandedRowId = (expandedRowId === no) ? null : no;
      render();
    }

    function getCurrentTimeMinutes() {
      const d = new Date();
      return d.getHours() * 60 + d.getMinutes();
    }

    function timeToMinutes(tStr) {
      const [h, m] = tStr.split(':').map(Number);
      return (h < 4 ? h + 24 : h) * 60 + m;
    }

    function render() {
      // Update tab styles
      document.querySelectorAll('.band-btn').forEach(btn => {
        if (btn.dataset.band === currentBand) {
          btn.className = 'band-btn flex-1 min-w-[56px] py-1 px-1 rounded-md text-center font-bold text-[11px] bg-[var(--foreground)] text-[var(--background)] shadow-sm transition';
        } else {
          btn.className = 'band-btn flex-1 min-w-[56px] py-1 px-1 rounded-md text-center font-medium text-[11px] text-[var(--muted-foreground)] hover:bg-[var(--accent)] hover:text-[var(--foreground)] transition';
        }
      });

      const nowMin = getCurrentTimeMinutes();

      // Filter trains
      let list = TRAINS;

      if (rapidOnly) {
        list = list.filter(t => t.type_badge === '快速' || t.type_badge === '区間快速');
      }

      if (currentBand === 'now') {
        const upcoming = list.filter(t => timeToMinutes(t.hakata_dep) >= nowMin);
        list = upcoming.length >= 6 ? upcoming.slice(0, 8) : list.slice(0, 8);
      } else if (currentBand !== 'all') {
        list = list.filter(t => t.time_band === currentBand);
      }

      document.getElementById('countBadge').innerText = `${list.length}便 表示中`;

      const container = document.getElementById('trainList');
      if (list.length === 0) {
        container.innerHTML = `
          <div class="py-12 text-center text-[var(--muted-foreground)]">
            <p class="text-sm font-semibold">該当する列車がありません</p>
            <p class="text-xs mt-1">「快速のみ」を解除するか、別の時間帯をお選びください</p>
          </div>
        `;
        return;
      }

      container.innerHTML = list.map(t => {
        const isRapid = t.type_badge === '快速';
        const isSectRapid = t.type_badge === '区間快速';
        const isExpanded = expandedRowId === t.no;
        
        let badgeHtml = '';
        if (isRapid) {
          badgeHtml = '<span class="inline-block px-1.5 py-0.2 rounded font-bold bg-blue-600 text-white text-[10px]">快速</span>';
        } else if (isSectRapid) {
          badgeHtml = '<span class="inline-block px-1.5 py-0.2 rounded font-bold bg-amber-500 text-white text-[10px]">区快</span>';
        } else {
          badgeHtml = '<span class="inline-block px-1.5 py-0.2 rounded font-medium bg-slate-200 text-slate-800 dark:bg-slate-700 dark:text-slate-300 text-[10px]">普通</span>';
        }

        const tosuDisplay = t.is_transfer 
          ? `<div class="flex items-center justify-center gap-0.5 text-[10px] text-amber-600 dark:text-amber-400 font-semibold font-mono">
               <span>${t.tosu_arr}</span>
               <span class="text-[8.5px] px-0.5 rounded bg-amber-100 dark:bg-amber-950 text-amber-800 dark:text-amber-300 border border-amber-300 dark:border-amber-800 font-sans">乗換</span>
               <span>${t.tosu_dep}</span>
             </div>`
          : `<div class="flex items-center justify-center gap-1 text-[11px] text-[var(--muted-foreground)] font-mono">
               <span>${t.tosu_arr}</span>
               <span class="text-[9px] opacity-40">/</span>
               <span>${t.tosu_dep}</span>
             </div>`;

        const transferHint = t.is_transfer 
          ? `<div class="text-[9.5px] text-amber-600 dark:text-amber-400 font-medium truncate text-right">鳥栖乗換</div>`
          : `<div class="text-[9.5px] text-[var(--muted-foreground)] truncate text-right">${t.dest}行</div>`;

        // Detailed view when expanded
        const detailHtml = isExpanded ? `
          <div class="col-span-12 px-2.5 py-2 mt-1 rounded-lg bg-[var(--background)] border border-[var(--border)] text-[11px] space-y-1">
            <div class="flex items-center justify-between font-medium">
              <span class="text-[var(--muted-foreground)]">運行状況:</span>
              <span class="text-emerald-600 dark:text-emerald-400 font-semibold">毎日運転（平日・土休日共通）</span>
            </div>
            <div class="flex items-center justify-between">
              <span class="text-[var(--muted-foreground)]">種別・行先:</span>
              <span class="font-medium text-[var(--foreground)]">${t.type_badge} (${t.note || t.dest + '行'})</span>
            </div>
            ${t.is_transfer ? `
            <div class="p-1.5 rounded bg-amber-50 dark:bg-amber-950/40 border border-amber-200 dark:border-amber-900 text-[10.5px] text-amber-900 dark:text-amber-200">
              ⚡ <strong>鳥栖乗換:</strong> 博多発便は鳥栖止まり。鳥栖駅(${t.tosu_arr}着)にて向かいホーム等の<strong>${t.tosu_dep}発 ${t.transfer_info.replace('鳥栖乗換 ', '')}</strong>に乗り継ぎ久留米(${t.kurume_arr}着)へ先着します。
            </div>` : `
            <div class="p-1.5 rounded bg-blue-50 dark:bg-blue-950/40 border border-blue-200 dark:border-blue-900 text-[10.5px] text-blue-900 dark:text-blue-200">
              🚆 <strong>直通運転:</strong> 乗り換えなしで久留米駅まで直通します。
            </div>`}
          </div>
        ` : '';

        return `
          <div class="px-3 py-1.5 hover:bg-[var(--accent)]/40 transition cursor-pointer select-none" onclick="toggleDetail(${t.no})">
            <div class="grid grid-cols-12 items-center">
              <!-- 始発駅 -->
              <div class="col-span-2">
                <span class="font-medium text-[11px] text-[var(--foreground)] truncate block">${t.origin}</span>
              </div>

              <!-- 博多発 -->
              <div class="col-span-2 text-center">
                <span class="font-bold text-[13px] font-mono text-blue-600 dark:text-blue-400 tracking-tight">${t.hakata_dep}</span>
              </div>

              <!-- 鳥栖 着/発 -->
              <div class="col-span-3 text-center">
                ${tosuDisplay}
              </div>

              <!-- 久留米着 -->
              <div class="col-span-2 text-center">
                <span class="font-bold text-[13px] font-mono text-emerald-600 dark:text-emerald-400 tracking-tight">${t.kurume_arr}</span>
              </div>

              <!-- 種別・所要時間 -->
              <div class="col-span-3 flex flex-col items-end">
                <div class="flex items-center gap-1">
                  ${badgeHtml}
                  <span class="text-[10.5px] font-bold text-[var(--foreground)] font-mono">${t.travel_time}分</span>
                </div>
                ${transferHint}
              </div>
            </div>
            ${detailHtml}
          </div>
        `;
      }).join('');
    }

    // Auto initialize to current time band
    currentBand = getAutoBand();
    render();
  </script>
</body>
</html>
"""

html_final = html_template.replace("__TRAINS_PLACEHOLDER__", trains_json_str)

target_path = r"C:\Users\admin\.gemini\antigravity\brain\d6ba54ff-a05e-4941-8ae5-4c70319c95f3\hakata_kurume_timetable.html"
with open(target_path, "w", encoding="utf-8") as f:
    f.write(html_final)

print("Successfully written HTML artifact:", target_path)
