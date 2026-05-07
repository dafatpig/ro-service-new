#!/usr/bin/env python3
"""RO專業帶本代拉"""

from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

orders = []
ratio = {f'{i}-{i+1}E':'' for i in range(10)}
order_id = 1

PRICES = {'飛空艇英靈':500,'博物島英靈':300,'迷蹤島英靈':100,'星座塔Ⅵ':800,'混亂時空噩夢':800,'12人英靈':100,'神諭11':100}
TWD_CNY = 0.217

CLIENT_HTML = '''<!DOCTYPE html>
<html lang="zh-TW">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>RO專業帶本代拉</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@400;500;700&display=swap" rel="stylesheet">
<style>
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: 'Noto Sans TC', sans-serif; background: linear-gradient(180deg, #0f2027 0%, #203a43 50%, #2c5364 100%); color: #fff; min-height: 100vh; padding: 20px; }
.container { max-width: 520px; margin: 0 auto; }
h1 { text-align: center; font-size: 28px; font-weight: 700; background: linear-gradient(90deg, #ffd700, #ffaa00, #ffd700); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 4px; }
.subtitle { text-align: center; color: #aaa; font-size: 14px; margin-bottom: 20px; }
.tab-box { display: flex; gap: 8px; margin-bottom: 20px; }
.tab { flex: 1; padding: 14px; background: rgba(255,255,255,0.08); border: 1px solid rgba(255,255,255,0.15); color: #aaa; font-size: 16px; font-weight: 600; border-radius: 12px; text-align: center; cursor: pointer; transition: all 0.2s; }
.tab.active { background: linear-gradient(135deg, #e6b800, #ffd700); color: #1a1a2e; }
.section { display: none; }
.section.active { display: block; }
.item { display: flex; justify-content: space-between; align-items: center; padding: 14px 16px; background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.1); border-radius: 12px; margin-bottom: 10px; cursor: pointer; transition: all 0.2s; }
.item.checked { background: linear-gradient(135deg, #b8860b, #daa520); border-color: #ffd700; box-shadow: 0 4px 20px rgba(255,215,0,0.25); }
.item-left { font-size: 15px; }
.item-right { font-size: 14px; color: #ccc; }
.item.checked .item-right { color: #fff; }
.qty-box { display: none; align-items: center; gap: 6px; }
.item.checked .qty-box { display: flex; }
.qty-btn { width: 28px; height: 28px; background: rgba(255,255,255,0.25); border: none; border-radius: 6px; color: #fff; font-size: 18px; font-weight: 600; cursor: pointer; }
.qty-num { min-width: 22px; text-align: center; font-size: 15px; font-weight: 700; }
.total-box { text-align: center; font-size: 18px; font-weight: 700; margin: 16px 0; color: #ffd700; }
.input-box { margin-bottom: 12px; }
.input-box input { width: 100%; padding: 14px; background: rgba(255,255,255,0.08); border: 1px solid rgba(255,255,255,0.15); color: #fff; border-radius: 10px; font-size: 15px; }
.input-box input::placeholder { color: #777; }
.input-box textarea { width: 100%; padding: 14px; background: rgba(255,255,255,0.08); border: 1px solid rgba(255,255,255,0.15); color: #fff; border-radius: 10px; font-size: 15px; min-height: 80px; resize: none; }
.input-box textarea::placeholder { color: #777; }
.submit-btn { width: 100%; padding: 16px; background: linear-gradient(135deg, #e6b800, #ffd700); color: #1a1a2e; border: none; border-radius: 12px; font-size: 17px; font-weight: 700; cursor: pointer; }
.submit-btn:active { transform: scale(0.98); }
.ratio-list { margin-bottom: 16px; }
.ratio-row { display: flex; justify-content: space-between; padding: 10px 14px; background: rgba(255,255,255,0.05); border-radius: 8px; margin-bottom: 6px; }
.ratio-row span:first-child { color: #ccc; }
.ratio-row span:last-child { color: #4ade80; font-weight: 600; }
.upload-box { padding: 20px; background: rgba(255,255,255,0.05); border: 2px dashed rgba(255,255,255,0.2); border-radius: 12px; text-align: center; margin-bottom: 12px; }
.upload-box input { display: none; }
.upload-label { color: #aaa; font-size: 14px; cursor: pointer; }
.hint { color: #777; font-size: 13px; margin-top: 6px; }
</style>
</head>
<body>
<div class="container">
<h1>⚔️ RO專業帶本代拉</h1>
<p class="subtitle">仙境傳說RO守護永恆的愛 Classic</p>
<div class="tab-box">
<button class="tab active" data-target="dungeon" onclick="switchTab(this)">📦 躺本</button>
<button class="tab" data-target="buy" onclick="switchTab(this)">💰 代拉</button>
</div>

<div id="dungeon" class="section active">
<div class="items">
<div class="item" onclick="toggleItem(this)" data-name="飛空艇英靈"><span class="item-left">飛空艇英靈</span><span class="item-right">NT500</span><div class="qty-box"><button class="qty-btn" onclick="event.stopPropagation();changeQty(this,-1)">-</button><span class="qty-num">0</span><button class="qty-btn" onclick="event.stopPropagation();changeQty(this,1)">+</button></div></div>
<div class="item" onclick="toggleItem(this)" data-name="博物島英靈"><span class="item-left">博物島英靈</span><span class="item-right">NT300</span><div class="qty-box"><button class="qty-btn" onclick="event.stopPropagation();changeQty(this,-1)">-</button><span class="qty-num">0</span><button class="qty-btn" onclick="event.stopPropagation();changeQty(this,1)">+</button></div></div>
<div class="item" onclick="toggleItem(this)" data-name="迷蹤島英靈"><span class="item-left">迷蹤島英靈</span><span class="item-right">NT100</span><div class="qty-box"><button class="qty-btn" onclick="event.stopPropagation();changeQty(this,-1)">-</button><span class="qty-num">0</span><button class="qty-btn" onclick="event.stopPropagation();changeQty(this,1)">+</button></div></div>
<div class="item" onclick="toggleItem(this)" data-name="星座塔Ⅵ"><span class="item-left">星座塔Ⅵ</span><span class="item-right">NT800</span><div class="qty-box"><button class="qty-btn" onclick="event.stopPropagation();changeQty(this,-1)">-</button><span class="qty-num">0</span><button class="qty-btn" onclick="event.stopPropagation();changeQty(this,1)">+</button></div></div>
<div class="item" onclick="toggleItem(this)" data-name="混亂時空噩夢"><span class="item-left">混亂時空噩夢</span><span class="item-right">NT800</span><div class="qty-box"><button class="qty-btn" onclick="event.stopPropagation();changeQty(this,-1)">-</button><span class="qty-num">0</span><button class="qty-btn" onclick="event.stopPropagation();changeQty(this,1)">+</button></div></div>
<div class="item" onclick="toggleItem(this)" data-name="12人英靈"><span class="item-left">12人英靈</span><span class="item-right">NT100</span><div class="qty-box"><button class="qty-btn" onclick="event.stopPropagation();changeQty(this,-1)">-</button><span class="qty-num">0</span><button class="qty-btn" onclick="event.stopPropagation();changeQty(this,1)">+</button></div></div>
<div class="item" onclick="toggleItem(this)" data-name="神諭11"><span class="item-left">神諭11</span><span class="item-right">NT100</span><div class="qty-box"><button class="qty-btn" onclick="event.stopPropagation();changeQty(this,-1)">-</button><span class="qty-num">0</span><button class="qty-btn" onclick="event.stopPropagation();changeQty(this,1)">+</button></div></div>
</div>
<div class="total-box">總計：<span id="total">0</span> 元</div>
<div class="input-box"><textarea id="note" placeholder="選填，可以備註時間要求"></textarea></div>
<div class="input-box"><input id="lineid" type="text" placeholder="必填，提交後馬上聯繫您"></div>
<button class="submit-btn" onclick="submitDungeon()">🚀 提交訂單</button>
</div>

<div id="buy" class="section">
<div class="ratio-list" id="ratio-display"></div>
<div class="upload-box"><input type="file" id="screenshot" accept="image/*"><label class="upload-label" for="screenshot">📎 點擊上傳圖片</label></div>
<p class="hint">上傳需要代拉的物品圖片即可，馬上為您拉掉</p>
<div class="input-box"><input id="lineid2" type="text" placeholder="必填，提交後馬上聯繫您"></div>
<button class="submit-btn" onclick="submitBuy()">🚀 提交訂單</button>
</div>
</div>

<script>
const PRICES = ''' + str(PRICES) + ''';
let ratioData = {};

async function loadRatio() {
    const r = await fetch('/api/ratio');
    ratioData = await r.json();
    let html = '';
    for (let i = 0; i <= 9; i++) {
        const key = i + '-' + (i+1) + 'E';
        html += '<div class="ratio-row"><span>' + key + '</span><span>' + (ratioData[key] || '--') + '</span></div>';
    }
    document.getElementById('ratio-display').innerHTML = html;
}

function switchTab(btn) {
    document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
    document.querySelectorAll('.section').forEach(s => s.classList.remove('active'));
    btn.classList.add('active');
    document.getElementById(btn.dataset.target).classList.add('active');
    if (btn.dataset.target === 'buy') loadRatio();
}

function toggleItem(el) {
    el.classList.toggle('checked');
    const qty = el.querySelector('.qty-num');
    if (el.classList.contains('checked') && qty.textContent === '0') qty.textContent = '1';
    updateTotal();
}

function changeQty(btn, delta) {
    const el = btn.closest('.item');
    const qty = el.querySelector('.qty-num');
    let n = parseInt(qty.textContent) + delta;
    if (n < 0) n = 0;
    if (n > 10) n = 10;
    qty.textContent = n;
    if (n === 0) el.classList.remove('checked');
    updateTotal();
}

function updateTotal() {
    let t = 0;
    document.querySelectorAll('#dungeon .item.checked').forEach(el => {
        const name = el.dataset.name;
        const qty = parseInt(el.querySelector('.qty-num').textContent);
        t += (PRICES[name] || 0) * qty;
    });
    document.getElementById('total').textContent = t;
}

async function submitDungeon() {
    const items = [];
    document.querySelectorAll('#dungeon .item.checked').forEach(el => {
        const name = el.dataset.name;
        const qty = parseInt(el.querySelector('.qty-num').textContent);
        for (let i = 0; i < qty; i++) items.push(name);
    });
    const lineid = document.getElementById('lineid').value.trim();
    const note = document.getElementById('note').value.trim();
    if (!lineid) return alert('請輸入 LINE ID');
    if (items.length === 0) return alert('請選擇至少一個副本');
    await fetch('/api/order', { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({ type: '帶本', items, lineid, note }) });
    alert('✅ 提交成功！');
    document.querySelectorAll('.item').forEach(el => el.classList.remove('checked'));
    document.querySelectorAll('.qty-num').forEach(q => q.textContent = '0');
    document.getElementById('lineid').value = '';
    document.getElementById('note').value = '';
    updateTotal();
}

async function submitBuy() {
    const lineid = document.getElementById('lineid2').value.trim();
    if (!lineid) return alert('請輸入 LINE ID');
    await fetch('/api/order', { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({ type: '代拉', items: [], lineid, note: '' }) });
    alert('✅ 提交成功！');
    document.getElementById('lineid2').value = '';
}

loadRatio();
</script>
</body>
</html>'''

ADMIN_HTML = '''<!DOCTYPE html>
<html lang="zh-TW">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>RO管理後台</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@400;500;700&display=swap" rel="stylesheet">
<style>
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: 'Noto Sans TC', sans-serif; background: linear-gradient(135deg, #0f2027, #203a43, #2c5364); color: #fff; min-height: 100vh; }
.container { max-width: 680px; margin: 0 auto; padding: 24px 16px; }
h1 { text-align: center; font-size: 26px; font-weight: 700; color: #4ade80; margin-bottom: 20px; }
.tabs { display: flex; gap: 8px; margin-bottom: 20px; }
.tab { flex: 1; padding: 12px; background: rgba(255,255,255,0.08); border: 1px solid rgba(255,255,255,0.15); color: #aaa; font-size: 15px; font-weight: 600; border-radius: 10px; text-align: center; cursor: pointer; }
.tab.active { background: #e6b800; color: #1a1a2e; }
.count-box { display: flex; justify-content: space-between; align-items: center; padding: 12px 16px; background: rgba(255,255,255,0.06); border-radius: 10px; margin-bottom: 16px; }
.count-box span:first-child { color: #fbbf24; font-size: 15px; }
.count-num { font-size: 22px; font-weight: 700; color: #fbbf24; }
.panel { display: none; }
.panel.active { display: block; }
.card { background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.1); padding: 16px; border-radius: 12px; margin-bottom: 12px; }
.card-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; }
.card-type { font-size: 16px; font-weight: 700; padding: 4px 10px; border-radius: 6px; }
.card-type.dungeon { background: rgba(139,92,246,0.2); color: #a78bfa; }
.card-type.buy { background: rgba(34,197,94,0.2); color: #4ade80; }
.card-time { color: #888; font-size: 13px; }
.card-items { margin: 10px 0; }
.item-tag { display: inline-block; background: rgba(230,184,0,0.15); color: #ffd700; padding: 4px 10px; border-radius: 6px; margin: 0 6px 6px 0; font-size: 14px; }
.card-price { margin: 10px 0; color: #fbbf24; font-weight: 600; }
.card-line { color: #4ade80; font-size: 14px; margin: 8px 0; }
.card-note { color: #aaa; font-size: 13px; font-style: italic; }
.card-btns { display: flex; gap: 8px; margin-top: 12px; }
.btn { padding: 10px 16px; border: none; border-radius: 8px; font-size: 14px; font-weight: 600; cursor: pointer; }
.btn-complete { background: #22c55e; color: white; }
.btn-paid { background: #fbbf24; color: #1a1a2e; }
.btn-paid-done { background: #555; color: #999; cursor: default; }
.btn-delete { background: rgba(239,68,68,0.2); color: #fca5a5; }
.ratio-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 10px; }
.ratio-item { display: flex; justify-content: space-between; align-items: center; padding: 10px 12px; background: rgba(255,255,255,0.05); border-radius: 8px; }
.ratio-item label { color: #aaa; font-size: 14px; }
.ratio-item input { width: 70px; padding: 6px; background: rgba(255,255,255,0.1); border: 1px solid rgba(255,255,255,0.2); color: #fff; border-radius: 6px; text-align: center; }
.btn-save { width: 100%; padding: 14px; background: #e6b800; color: #1a1a2e; border: none; border-radius: 10px; font-size: 16px; font-weight: 700; cursor: pointer; margin-top: 16px; }
.empty { text-align: center; color: #666; padding: 30px; }
</style>
</head>
<body>
<div class="container">
<h1>⚙️ RO管理後台</h1>
<div class="tabs">
<button class="tab active" data-target="pending" onclick="switchTab(this)">⏳ 待辦</button>
<button class="tab" data-target="history" onclick="switchTab(this)">📋 記錄</button>
<button class="tab" data-target="ratio" onclick="switchTab(this)">💰 代拉比例</button>
</div>

<div id="pending" class="panel active">
<div class="count-box"><span>待辦事項</span><span class="count-num" id="pending-count">0</span></div>
<div id="pending-list"></div>
</div>

<div id="history" class="panel">
<div id="history-list"></div>
</div>

<div id="ratio" class="panel">
<div class="ratio-grid">
<div class="ratio-item"><label>0-1E：</label><input id="ratio-0-1"></div>
<div class="ratio-item"><label>1-2E：</label><input id="ratio-1-2"></div>
<div class="ratio-item"><label>2-3E：</label><input id="ratio-2-3"></div>
<div class="ratio-item"><label>3-4E：</label><input id="ratio-3-4"></div>
<div class="ratio-item"><label>4-5E：</label><input id="ratio-4-5"></div>
<div class="ratio-item"><label>5-6E：</label><input id="ratio-5-6"></div>
<div class="ratio-item"><label>6-7E：</label><input id="ratio-6-7"></div>
<div class="ratio-item"><label>7-8E：</label><input id="ratio-7-8"></div>
<div class="ratio-item"><label>8-9E：</label><input id="ratio-8-9"></div>
<div class="ratio-item"><label>9-10E：</label><input id="ratio-9-10"></div>
</div>
<button class="btn-save" onclick="saveRatio()">💾 儲存代拉比例</button>
</div>
</div>

<script>
const TWD_CNY = 0.217;
const PRICES = ''' + str(PRICES) + ''';

async function loadOrders() {
    const res = await fetch('/api/orders');
    const data = await res.json();
    const all = data.orders || [];
    
    let pending = all.filter(o => !o.done);
    let history = all.filter(o => o.done);
    
    pending.sort((a,b) => b.id - a.id);
    let unpaid = history.filter(o => !o.paid).sort((a,b) => b.id - a.id);
    let paid = history.filter(o => o.paid).sort((a,b) => b.id - a.id);
    history = [...unpaid, ...paid];
    
    document.getElementById('pending-count').textContent = pending.length;
    document.getElementById('pending-list').innerHTML = pending.length ? pending.map(o => renderCard(o, true)).join('') : '<div class="empty">暫無待辦事項</div>';
    document.getElementById('history-list').innerHTML = history.length ? history.map(o => renderCard(o, false)).join('') : '<div class="empty">暫無記錄</div>';
}

function renderCard(o, showBtns) {
    const typeClass = o.type === '帶本' ? 'dungeon' : 'buy';
    let itemsHtml = '';
    if (o.items && o.items.length) {
        const counts = {};
        o.items.forEach(i => counts[i] = (counts[i] || 0) + 1);
        itemsHtml = '<div class="card-items">' + Object.entries(counts).map(([name, qty]) => '<span class="item-tag">' + name + 'x' + qty + '</span>').join('') + '</div>';
    }
    let priceHtml = '';
    if (o.type === '帶本' && o.items && o.items.length) {
        let twd = 0;
        o.items.forEach(i => twd += PRICES[i] || 0);
        const cny = Math.floor(twd * TWD_CNY);
        priceHtml = '<div class="card-price">' + twd + ' 元 ≈ ' + cny + ' 人民币</div>';
    }
    let noteHtml = o.note ? '<div class="card-note">備註：' + o.note + '</div>' : '';
    let btnsHtml = '';
    if (showBtns) {
        btnsHtml = '<div class="card-btns"><button class="btn btn-complete" onclick="completeOrder(' + o.id + ')">✅ 完成</button><button class="btn btn-paid" onclick="paidOrder(' + o.id + ')">❌ 未收款</button><button class="btn btn-delete" onclick="deleteOrder(' + o.id + ')">🗑️</button></div>';
    } else {
        const paidBtn = o.paid ? '<span style="color:#666;font-size:13px;margin-right:8px;">已收款</span>' : '<button class="btn btn-paid" onclick="paidOrder(' + o.id + ')">❌ 未收款</button>';
        btnsHtml = '<div class="card-btns">' + paidBtn + '<button class="btn btn-delete" onclick="deleteOrder(' + o.id + ')">🗑️</button></div>';
    }
    
    return '<div class="card"><div class="card-header"><span class="card-type ' + typeClass + '">' + o.type + '</span><span class="card-time">' + o.time + '</span></div>' + itemsHtml + priceHtml + '<div class="card-line">LINE: ' + (o.lineid || '--') + '</div>' + noteHtml + btnsHtml + '</div>';
}

async function completeOrder(id) {
    await fetch('/api/action', { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({id, action: 'complete'}) });
    loadOrders();
}

async function paidOrder(id) {
    await fetch('/api/action', { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({id, action: 'paid'}) });
    loadOrders();
}

async function deleteOrder(id) {
    if (!confirm('確定刪除？')) return;
    await fetch('/api/action', { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({id, action: 'delete'}) });
    loadOrders();
}

function switchTab(btn) {
    document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
    document.querySelectorAll('.panel').forEach(p => p.classList.remove('active'));
    btn.classList.add('active');
    document.getElementById(btn.dataset.target).classList.add('active');
    if (btn.dataset.target === 'ratio') loadRatio();
    if (btn.dataset.target === 'pending' || btn.dataset.target === 'history') loadOrders();
}

async function loadRatio() {
    const r = await fetch('/api/ratio');
    const data = await r.json();
    for (let i = 0; i <= 9; i++) {
        const key = i + '-' + (i+1) + 'E';
        document.getElementById('ratio-' + key).value = data[key] || '';
    }
}

async function saveRatio() {
    const r = {};
    for (let i = 0; i <= 9; i++) {
        const key = i + '-' + (i+1) + 'E';
        r[key] = document.getElementById('ratio-' + key).value;
    }
    await fetch('/api/ratio', { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify(r) });
    alert('✅ 已儲存！');
}

loadOrders();
setInterval(loadOrders, 15000);
</script>
</body>
</html>'''

@app.route('/')
@app.route('/client')
def client():
    return CLIENT_HTML

@app.route('/admin')
def admin():
    return ADMIN_HTML

@app.route('/api/orders')
def api_orders():
    return jsonify({'orders': orders})

@app.route('/api/ratio', methods=['GET'])
def api_ratio():
    return jsonify(ratio)

@app.route('/api/ratio', methods=['POST'])
def api_save_ratio():
    global ratio
    ratio.update(request.json)
    return jsonify({'ok': True})

@app.route('/api/order', methods=['POST'])
def api_order():
    global order_id
    data = request.json
    order = {
        'id': order_id,
        'type': data.get('type', '帶本'),
        'items': data.get('items', []),
        'lineid': data.get('lineid', ''),
        'note': data.get('note', ''),
        'done': False,
        'paid': False,
        'time': datetime.now().strftime('%Y-%m-%d %H:%M')
    }
    orders.append(order)
    order_id += 1
    return jsonify({'ok': True})

@app.route('/api/action', methods=['POST'])
def api_action():
    data = request.json
    oid = data.get('id')
    action = data.get('action')
    for o in orders:
        if o['id'] == oid:
            if action == 'complete':
                o['done'] = True
            elif action == 'paid':
                o['paid'] = True
            elif action == 'delete':
                orders.remove(o)
            break
    return jsonify({'ok': True})