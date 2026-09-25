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

html_code = """<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">
  <title>JR博多駅→JR久留米駅 時刻表</title>
  <script src="https://www.gstatic.com/antigravity/web/dev/tailwindcss.min.js"></script>
  <style>
    /* CSS Variables & Theme Fallbacks */
    :root {
      --bg-page: #f8fafc;
      --bg-card: #ffffff;
      --border-color: #e2e8f0;
      --text-main: #0f172a;
      --text-muted: #64748b;
      --primary-color: #2563eb;
      --accent-color: #f1f5f9;
    }
    @media (prefers-color-scheme: dark) {
      :root {
        --bg-page: #0b0f17;
        --bg-card: #151d2c;
        --border-color: #26334d;
        --text-main: #f1f5f9;
        --text-muted: #94a3b8;
        --primary-color: #3b82f6;
        --accent-color: #1e293b;
      }
    }

    body {
      background-color: var(--background, var(--bg-page));
      color: var(--foreground, var(--text-main));
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, "Hiragino Kaku Gothic ProN", "Meiryo", sans-serif;
      margin: 0;
      padding: 0;
      -webkit-tap-highlight-color: transparent;
      user-select: none;
    }

    /* Scrollbar */
    ::-webkit-scrollbar {
      width: 4px;
      height: 4px;
    }
    ::-webkit-scrollbar-thumb {
      background: rgba(140, 160, 190, 0.3);
      border-radius: 4px;
    }
    .no-scrollbar::-webkit-scrollbar {
      display: none;
    }
    .no-scrollbar {
      -ms-overflow-style: none;
      scrollbar-width: none;
    }

    /* Active Tab */
    .tab-active {
      background-color: var(--foreground, #0f172a) !important;
      color: var(--background, #ffffff) !important;
      font-weight: 700;
      box-shadow: 0 1px 3px rgba(0,0,0,0.12);
    }
  </style>
</head>
<body class="antialiased p-1.5 sm:p-4 min-h-screen flex flex-col justify-start">
  
  <div class="w-full max-w-lg mx-auto bg-[var(--card,var(--bg-card))] border border-[var(--border,var(--border-color))] rounded-2xl shadow-lg overflow-hidden flex flex-col">

    <!-- Header Section -->
    <header class="px-3.5 py-3 border-b border-[var(--border,var(--border-color))] bg-[var(--card,var(--bg-card))]">
      <div class="flex items-center justify-between">
        <div>
          <div class="flex items-center gap-1.5">
            <span class="inline-block w-2.5 h-2.5 rounded-full bg-emerald-500 animate-pulse"></span>
            <h1 class="text-base font-extrabold tracking-tight">JR 博多 ➔ 久留米</h1>
            <span class="text-[10px] px-1.5 py-0.5 rounded font-bold bg-blue-100 text-blue-800 dark:bg-blue-950 dark:text-blue-300 border border-blue-200 dark:border-blue-800">普通乗車券のみ</span>
          </div>
          <p class="text-[11px] text-[var(--muted-foreground,var(--text-muted))] mt-0.5">
            鹿児島本線下り <span class="font-medium text-emerald-600 dark:text-emerald-400">全47便 毎日運転（土休日も同一）</span>
          </p>
        </div>

        <!-- Rapid Toggle Button -->
        <button id="rapidToggle" onclick="toggleRapidFilter()" class="flex items-center gap-1 px-2.5 py-1.5 rounded-xl border border-[var(--border,var(--border-color))] bg-[var(--accent,var(--accent-color))] hover:opacity-80 transition text-xs font-semibold shadow-sm">
          <span>⚡</span>
          <span id="rapidToggleLabel">快速のみ</span>
        </button>
      </div>

      <!-- Quick Criteria Note -->
      <div class="mt-2 pt-2 border-t border-[var(--border,var(--border-color))]/50 flex flex-wrap gap-x-3 gap-y-1 text-[10px] text-[var(--muted-foreground,var(--text-muted))]">
        <span>❌ 特急・新幹線除外</span>
        <span>❌ 二日市止・後続追いつかれ便除外</span>
        <span>✅ 鳥栖始発接続便 掲載</span>
      </div>
    </header>

    <!-- Time Band Tabs (Mobile Optimized) -->
    <nav class="p-1.5 bg-[var(--accent,var(--accent-color))]/50 border-b border-[var(--border,var(--border-color))] flex items-center gap-1 overflow-x-auto no-scrollbar text-xs">
      <button class="tab-btn flex-1 min-w-[54px] py-1.5 px-1 rounded-lg text-center transition font-medium text-[11px] text-[var(--muted-foreground,var(--text-muted))]" data-band="now" onclick="changeBand('now')">
        ⏱️ 次の便
      </button>
      <button class="tab-btn flex-1 min-w-[54px] py-1.5 px-1 rounded-lg text-center transition font-medium text-[11px] text-[var(--muted-foreground,var(--text-muted))]" data-band="morning" onclick="changeBand('morning')">
        🌅 朝 <span class="opacity-70 text-[9px] block sm:inline">5-9時</span>
      </button>
      <button class="tab-btn flex-1 min-w-[54px] py-1.5 px-1 rounded-lg text-center transition font-medium text-[11px] text-[var(--muted-foreground,var(--text-muted))]" data-band="day" onclick="changeBand('day')">
        ☀️ 昼 <span class="opacity-70 text-[9px] block sm:inline">10-15時</span>
      </button>
      <button class="tab-btn flex-1 min-w-[54px] py-1.5 px-1 rounded-lg text-center transition font-medium text-[11px] text-[var(--muted-foreground,var(--text-muted))]" data-band="evening" onclick="changeBand('evening')">
        🌇 夕 <span class="opacity-70 text-[9px] block sm:inline">16-19時</span>
      </button>
      <button class="tab-btn flex-1 min-w-[54px] py-1.5 px-1 rounded-lg text-center transition font-medium text-[11px] text-[var(--muted-foreground,var(--text-muted))]" data-band="night" onclick="changeBand('night')">
        🌙 夜 <span class="opacity-70 text-[9px] block sm:inline">20-23時</span>
      </button>
      <button class="tab-btn py-1.5 px-2 rounded-lg text-center transition font-medium text-[11px] text-[var(--muted-foreground,var(--text-muted))]" data-band="all" onclick="changeBand('all')">
        全便
      </button>
    </nav>

    <!-- Table Sticky Column Headers -->
    <div class="grid grid-cols-12 px-3 py-1.5 text-[11px] font-bold text-[var(--muted-foreground,var(--text-muted))] bg-[var(--card,var(--bg-card))] border-b border-[var(--border,var(--border-color))] items-center shadow-sm">
      <div class="col-span-2">始発</div>
      <div class="col-span-2 text-center text-blue-600 dark:text-blue-400">博多発</div>
      <div class="col-span-3 text-center">鳥栖 (着/発)</div>
      <div class="col-span-2 text-center text-emerald-600 dark:text-emerald-400">久留米着</div>
      <div class="col-span-3 text-right">種別 / 所要</div>
    </div>

    <!-- Main List Container (Fits on 1 mobile screen without overflow in tab view) -->
    <main id="timetableContainer" class="divide-y divide-[var(--border,var(--border-color))] overflow-y-auto max-h-[58vh] sm:max-h-[600px] text-xs">
      <!-- Injected by JavaScript -->
    </main>

    <!-- Footer Notice -->
    <footer class="px-3.5 py-2 bg-[var(--accent,var(--accent-color))]/70 border-t border-[var(--border,var(--border-color))] flex items-center justify-between text-[11px] text-[var(--muted-foreground,var(--text-muted))]">
      <div class="flex items-center gap-1.5">
        <span class="inline-block w-2 h-2 rounded-full bg-blue-500"></span>
        <span>行をタップで乗り継ぎ・運行詳細</span>
      </div>
      <span id="listCountLabel" class="font-mono font-semibold text-[var(--foreground,var(--text-main))]">--便</span>
    </footer>

  </div>

  <script>
    const TRAINS = __TRAINS_PLACEHOLDER__;

    let activeBand = 'day';
    let isRapidFilter = false;
    let selectedTrainNo = null;

    function detectBand() {
      const h = new Date().getHours();
      if (h >= 5 && h < 10) return 'morning';
      if (h >= 10 && h < 16) return 'day';
      if (h >= 16 && h < 20) return 'evening';
      return 'night';
    }

    function changeBand(band) {
      activeBand = band;
      selectedTrainNo = null;
      render();
    }

    function toggleRapidFilter() {
      isRapidFilter = !isRapidFilter;
      selectedTrainNo = null;
      const btn = document.getElementById('rapidToggle');
      const label = document.getElementById('rapidToggleLabel');
      if (isRapidFilter) {
        btn.classList.add('bg-blue-600', 'text-white', 'border-blue-600');
        btn.classList.remove('bg-[var(--accent,var(--accent-color))]', 'text-[var(--foreground,var(--text-main))]');
        label.innerText = '快速中';
      } else {
        btn.classList.remove('bg-blue-600', 'text-white', 'border-blue-600');
        btn.classList.add('bg-[var(--accent,var(--accent-color))]', 'text-[var(--foreground,var(--text-main))]');
        label.innerText = '快速のみ';
      }
      render();
    }

    function toggleRow(no) {
      selectedTrainNo = (selectedTrainNo === no) ? null : no;
      render();
    }

    function getNowMinutes() {
      const now = new Date();
      return now.getHours() * 60 + now.getMinutes();
    }

    function parseMin(timeStr) {
      const [h, m] = timeStr.split(':').map(Number);
      return (h < 4 ? h + 24 : h) * 60 + m;
    }

    function render() {
      // Update Tab Styles
      document.querySelectorAll('.tab-btn').forEach(btn => {
        if (btn.dataset.band === activeBand) {
          btn.className = 'tab-btn tab-active flex-1 min-w-[54px] py-1.5 px-1 rounded-lg text-center transition font-bold text-[11px]';
        } else {
          btn.className = 'tab-btn flex-1 min-w-[54px] py-1.5 px-1 rounded-lg text-center transition font-medium text-[11px] text-[var(--muted-foreground,var(--text-muted))] hover:bg-[var(--accent,var(--accent-color))]';
        }
      });

      let items = TRAINS;

      // Filter by Rapid
      if (isRapidFilter) {
        items = items.filter(t => t.type_badge === '快速' || t.type_badge === '区間快速');
      }

      // Filter by Band
      const nowMin = getNowMinutes();
      if (activeBand === 'now') {
        const afterNow = items.filter(t => parseMin(t.hakata_dep) >= nowMin);
        items = afterNow.length >= 6 ? afterNow.slice(0, 8) : items.slice(0, 8);
      } else if (activeBand !== 'all') {
        items = items.filter(t => t.time_band === activeBand);
      }

      document.getElementById('listCountLabel').innerText = `${items.length}便 表示中`;

      const container = document.getElementById('timetableContainer');
      if (items.length === 0) {
        container.innerHTML = `
          <div class="py-12 px-4 text-center text-[var(--muted-foreground,var(--text-muted))]">
            <p class="text-sm font-bold">条件に合う列車がありません</p>
            <p class="text-xs mt-1">「快速のみ」をオフにするか、別の時間帯を選択してください。</p>
          </div>
        `;
        return;
      }

      container.innerHTML = items.map(t => {
        const isRapid = t.type_badge === '快速';
        const isSect = t.type_badge === '区間快速';
        const isSelected = selectedTrainNo === t.no;

        let badge = '';
        if (isRapid) {
          badge = '<span class="px-1.5 py-0.5 rounded font-black bg-blue-600 text-white text-[10px] tracking-tight">快速</span>';
        } else if (isSect) {
          badge = '<span class="px-1.5 py-0.5 rounded font-bold bg-amber-500 text-white text-[10px] tracking-tight">区快</span>';
        } else {
          badge = '<span class="px-1.5 py-0.5 rounded font-medium bg-slate-200 text-slate-800 dark:bg-slate-700 dark:text-slate-200 text-[10px]">普通</span>';
        }

        // Tosu display
        const tosuHtml = t.is_transfer
          ? `<div class="flex items-center justify-center gap-0.5 font-mono text-[10.5px] text-amber-600 dark:text-amber-400 font-bold">
               <span>${t.tosu_arr}</span>
               <span class="text-[8px] px-0.5 rounded bg-amber-100 dark:bg-amber-950 text-amber-800 dark:text-amber-300 font-sans border border-amber-300 dark:border-amber-800">換</span>
               <span>${t.tosu_dep}</span>
             </div>`
          : `<div class="flex items-center justify-center gap-1 font-mono text-[11px] text-[var(--muted-foreground,var(--text-muted))]">
               <span>${t.tosu_arr}</span>
               <span class="opacity-40 text-[9px]">/</span>
               <span>${t.tosu_dep}</span>
             </div>`;

        // Right side info
        const rightSub = t.is_transfer
          ? `<div class="text-[9.5px] text-amber-600 dark:text-amber-400 font-bold truncate">鳥栖で乗換</div>`
          : `<div class="text-[9.5px] text-[var(--muted-foreground,var(--text-muted))] truncate">${t.dest}行</div>`;

        // Expand detail card
        const detailCard = isSelected ? `
          <div class="mt-2 p-2.5 rounded-xl bg-[var(--accent,var(--accent-color))]/70 border border-[var(--border,var(--border-color))] space-y-1.5 text-[11px]">
            <div class="flex items-center justify-between border-b border-[var(--border,var(--border-color))]/60 pb-1">
              <span class="text-[var(--muted-foreground,var(--text-muted))]">運行日:</span>
              <span class="font-bold text-emerald-600 dark:text-emerald-400">毎日運転（土休日も平日と同一時刻）</span>
            </div>
            <div class="flex items-center justify-between border-b border-[var(--border,var(--border-color))]/60 pb-1">
              <span class="text-[var(--muted-foreground,var(--text-muted))]">始発駅・終点:</span>
              <span class="font-semibold">${t.origin}駅 始発 ➔ ${t.dest}行</span>
            </div>
            <div class="flex items-center justify-between border-b border-[var(--border,var(--border-color))]/60 pb-1">
              <span class="text-[var(--muted-foreground,var(--text-muted))]">種別詳細:</span>
              <span class="font-semibold text-blue-600 dark:text-blue-400">${t.type_badge}（${t.note || t.dest + '行'}）</span>
            </div>
            ${t.is_transfer ? `
            <div class="p-2 rounded-lg bg-amber-50 dark:bg-amber-950/60 border border-amber-200 dark:border-amber-800 text-[11px] text-amber-900 dark:text-amber-200">
              ⚡ <strong>鳥栖駅乗り継ぎ:</strong> 博多発便は鳥栖止まりです。鳥栖駅<strong>${t.tosu_arr}着</strong>後、向かいホーム等の<strong>${t.tosu_dep}発 ${t.transfer_info.replace('鳥栖乗換 ', '')}</strong>へスムーズに乗り継ぎ、久留米駅<strong>${t.kurume_arr}着</strong>となります。
            </div>` : `
            <div class="p-2 rounded-lg bg-blue-50 dark:bg-blue-950/60 border border-blue-200 dark:border-blue-800 text-[11px] text-blue-900 dark:text-blue-200">
              🚆 <strong>久留米まで直通:</strong> 鳥栖駅での乗り換えなしで、久留米駅まで直通運行します。
            </div>`}
          </div>
        ` : '';

        return `
          <div class="px-3 py-2 hover:bg-[var(--accent,var(--accent-color))]/40 transition cursor-pointer select-none" onclick="toggleRow(${t.no})">
            <div class="grid grid-cols-12 items-center">
              <!-- 始発駅 -->
              <div class="col-span-2">
                <span class="font-semibold text-[11px] truncate block">${t.origin}</span>
              </div>

              <!-- 博多発 -->
              <div class="col-span-2 text-center">
                <span class="text-[14px] font-black font-mono text-blue-600 dark:text-blue-400 tracking-tight">${t.hakata_dep}</span>
              </div>

              <!-- 鳥栖 (着/発) -->
              <div class="col-span-3 text-center">
                ${tosuHtml}
              </div>

              <!-- 久留米着 -->
              <div class="col-span-2 text-center">
                <span class="text-[14px] font-black font-mono text-emerald-600 dark:text-emerald-400 tracking-tight">${t.kurume_arr}</span>
              </div>

              <!-- 種別・所要時間 -->
              <div class="col-span-3 flex flex-col items-end">
                <div class="flex items-center gap-1">
                  ${badge}
                  <span class="text-[11px] font-black font-mono">${t.travel_time}分</span>
                </div>
                ${rightSub}
              </div>
            </div>
            ${detailCard}
          </div>
        `;
      }).join('');
    }

    // Initialize to current time band
    activeBand = detectBand();
    render();
  </script>
</body>
</html>
"""

html_final = html_code.replace("__TRAINS_PLACEHOLDER__", trains_json_str)

target_path = r"C:\Users\admin\.gemini\antigravity\brain\d6ba54ff-a05e-4941-8ae5-4c70319c95f3\hakata_kurume_timetable.html"
with open(target_path, "w", encoding="utf-8") as f:
    f.write(html_final)

print("Saved standalone HTML to:", target_path)
