"""learn-pdm-lite-hgd 정답 예시 — 노이즈 vs 추세 판정과 그래프 한 장 대시보드.

실행: python build_trend.py   (작업 폴더 안에서 — data/ 아래에 Day5_설비센서_50건_가상.csv 가 있어야 한다)
출력: outputs/trend_judgement.csv, index.html, expected.json (course-forge 검증용)

원본 강의: keerhee/kma-auto-genai-3-1 · Day5_예지보전 (본 강의 ④ 분석 1, 실습과제 2)
"""
import json
from pathlib import Path

import pandas as pd

DATA = Path("data") / "Day5_설비센서_50건_가상.csv"
OUT = Path("outputs")
COLS = ["진동(mm/s)", "온도(℃)"]
BASE_N = 12   # 기준선: 처음 12점(08:00~11:40) — 정상 운전 구간
K_SIGMA = 3   # 상한: 기준선 평균 + 3σ
RUN = 3       # 3번 연속 넘으면 추세


def hhmm(t):
    return t[-5:]


# ── 노이즈 vs 추세 판정 ─────────────────────────────────────────────
def judge(df):
    rows = []
    for eq, g in df.groupby("설비", sort=False):
        g = g.reset_index(drop=True)
        for c in COLS:
            b = g.iloc[:BASE_N][c]
            ul = b.mean() + K_SIGMA * b.std()
            over = (g[c] > ul).tolist()
            start, streak = None, 0
            for i, o in enumerate(over):
                streak = streak + 1 if o else 0
                if streak == RUN and start is None:
                    start = hhmm(g.at[i - RUN + 1, "시간"])
            n_over = sum(over)
            verdict = "추세" if start else ("노이즈" if n_over else "정상")
            rows.append({"설비": eq.split("(")[0], "항목": c, "상한": round(ul, 2),
                         "상한 초과 점 수": n_over, "판정": verdict, "추세 시작": start or ""})
    return pd.DataFrame(rows)


# ── 하루 전체 평균 ± 2σ로 처음 이상 후보가 잡힌 시각 (비교용) ──────────
def first_2sigma(g):
    hits = []
    for c in COLS:
        m, s = g[c].mean(), g[c].std()
        hits += g[(g[c] > m + 2 * s) | (g[c] < m - 2 * s)]["시간"].tolist()
    return hhmm(min(hits)) if hits else None


def minutes(t):
    h, m = t.split(":")
    return int(h) * 60 + int(m)


# ── 그래프 한 장 ──────────────────────────────────────────────────
def dashboard(df, tj, earliest, first2, lead):
    a = df[df["설비"].str.startswith("설비A")]
    b = df[df["설비"].str.startswith("설비B")]
    labels = [hhmm(t) for t in a["시간"]]
    starts = tj[tj["판정"] == "추세"][["설비", "항목", "추세 시작"]].to_dict("records")
    data = {"labels": labels, "aVib": a["진동(mm/s)"].tolist(), "bVib": b["진동(mm/s)"].tolist(),
            "bTemp": b["온도(℃)"].tolist(), "marks": [{"t": s["추세 시작"], "name": f"{s['설비']} {s['항목'].split('(')[0]} 추세 시작"} for s in starts]}
    html = f"""<!doctype html>
<html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>노이즈인가 추세인가</title>
<style>
:root{{--bg:#fff;--fg:#1d1d1f;--sub:#6e6e73;--line:#e5e5ea}}
@media (prefers-color-scheme:dark){{:root{{--bg:#111;--fg:#f2f2f7;--sub:#a1a1a6;--line:#333}}}}
body{{margin:0;background:var(--bg);color:var(--fg);font-family:system-ui,-apple-system,"Segoe UI","Malgun Gothic",sans-serif}}
main{{max-width:960px;margin:0 auto;padding:20px 16px}}
.tag{{display:inline-block;font-size:12px;color:var(--sub);border:1px solid var(--line);border-radius:999px;padding:2px 10px}}
h1{{font-size:22px;margin:10px 0 6px}} p{{margin:4px 0;line-height:1.5}} .sub{{color:var(--sub);font-size:13px}}
.chart{{position:relative;height:420px;margin-top:14px}}
</style></head><body><main>
<span class="tag">실습용 가상 데이터</span>
<h1>설비B 온도는 {earliest}부터 추세 — 평균 ± 2σ({first2})보다 {lead}분 빠른 정비 신호</h1>
<p class="sub">설비A 진동 3.5 mm/s(12:40)는 한 번 튀고 돌아온 노이즈. 판정 규칙: 처음 12점 기준선 평균 + 3σ를 3번 연속 넘으면 추세.</p>
<div class="chart"><canvas id="c"></canvas></div>
<p class="sub">출처: <a href="https://github.com/keerhee/kma-auto-genai-3-1">keerhee/kma-auto-genai-3-1</a> data/Day5/Day5_설비센서_50건_가상.csv · Day5 예지보전 본 강의 ④ 분석 1</p>
</main>
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.min.js"></script>
<script>
const D = {json.dumps(data, ensure_ascii=False)};
const marks = {{id:'marks', afterDatasetsDraw(ch){{
  const x = ch.scales.x, y = ch.chartArea, g = ch.ctx;
  D.marks.forEach((m, i) => {{
    const px = x.getPixelForValue(D.labels.indexOf(m.t));
    g.save(); g.strokeStyle = '#d70015'; g.setLineDash([4, 4]);
    g.beginPath(); g.moveTo(px, y.top); g.lineTo(px, y.bottom); g.stroke();
    g.fillStyle = '#d70015'; g.font = '12px sans-serif'; g.textAlign = 'right';
    g.fillText(m.name + ' ' + m.t, px - 4, y.top + 14 + i * 16); g.restore();
  }});
}}}};
new Chart(document.getElementById('c'), {{
  type: 'line',
  data: {{labels: D.labels, datasets: [
    {{label: '설비A 진동 (mm/s)', data: D.aVib, borderColor: '#8e8e93', yAxisID: 'v', tension: .2}},
    {{label: '설비B 진동 (mm/s)', data: D.bVib, borderColor: '#0071e3', yAxisID: 'v', tension: .2}},
    {{label: '설비B 온도 (℃)', data: D.bTemp, borderColor: '#ff9500', yAxisID: 't', tension: .2}}]}},
  options: {{maintainAspectRatio: false, interaction: {{mode: 'index', intersect: false}},
    scales: {{v: {{position: 'left', title: {{display: true, text: '진동 (mm/s)'}}}},
              t: {{position: 'right', title: {{display: true, text: '온도 (℃)'}}, grid: {{drawOnChartArea: false}}}}}}}},
  plugins: [marks]
}});
</script></body></html>"""
    Path("index.html").write_text(html, encoding="utf-8")


def main():
    OUT.mkdir(exist_ok=True)
    df = pd.read_csv(DATA, encoding="utf-8-sig")
    tj = judge(df)
    tj.to_csv(OUT / "trend_judgement.csv", index=False, encoding="utf-8-sig")
    earliest = min(t for t in tj["추세 시작"] if t)
    first2 = first_2sigma(df[df["설비"].str.startswith("설비B")])
    lead = minutes(first2) - minutes(earliest)
    dashboard(df, tj, earliest, first2, lead)

    row = lambda eq, c: tj[(tj["설비"] == eq) & (tj["항목"] == c)].iloc[0]
    a_vib = df[df["설비"].str.startswith("설비A")]["진동(mm/s)"]
    values = {
        "b_temp_trend_start": {"value": row("설비B", "온도(℃)")["추세 시작"], "block": 1},
        "b_vib_trend_start": {"value": row("설비B", "진동(mm/s)")["추세 시작"], "block": 1},
        "b_temp_upper": {"value": float(row("설비B", "온도(℃)")["상한"]), "decimals": 1, "block": 1},
        "b_vib_upper": {"value": float(row("설비B", "진동(mm/s)")["상한"]), "decimals": 2, "block": 1},
        "a_vib_noise_peak": {"value": float(a_vib.max()), "decimals": 1, "block": 1},
        "a_vib_verdict": {"value": row("설비A", "진동(mm/s)")["판정"], "block": 1},
        "b_first_2sigma": {"value": first2, "block": 1},
        "lead_minutes": {"value": lead, "decimals": 0, "block": 1},
    }
    Path("expected.json").write_text(json.dumps({"values": values}, ensure_ascii=False, indent=1), encoding="utf-8")
    print(tj.to_string(index=False))
    print(f"가장 이른 추세 시작 {earliest} · 평균±2σ 첫 후보 {first2} · {lead}분 빠름")


if __name__ == "__main__":
    main()
