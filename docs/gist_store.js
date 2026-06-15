// gist_store.js — shared cloud storage via GitHub Gist
// All progress/scores stored in student's personal Gist file

function getSession() {
  return JSON.parse(sessionStorage.getItem('ptc_session') || 'null');
}

async function gistLoad() {
  var sess = getSession();
  if (!sess || !sess.gist_id) return {};
  try {
    var res = await fetch('https://api.github.com/gists/' + sess.gist_id, {
      headers: { 'Authorization': 'token ' + sess.token, 'Accept': 'application/vnd.github.v3+json' }
    });
    if (!res.ok) return {};
    var data = await res.json();
    var file = data.files[sess.gist_file];
    if (!file || !file.content) return {};
    return JSON.parse(file.content || '{}');
  } catch(e) { console.error('gistLoad error', e); return {}; }
}

async function gistSave(obj) {
  var sess = getSession();
  if (!sess || !sess.gist_id) { console.error('No session or gist_id'); return false; }
  if (!sess.token || sess.token === '' || sess.token === 'REPLACED') {
    console.error('Invalid token');
    alert('Setup error: Gist token is missing. Please ask your tutor to regenerate the app.');
    return false;
  }
  var files = {};
  files[sess.gist_file] = { content: JSON.stringify(obj, null, 2) };
  try {
    var res = await fetch('https://api.github.com/gists/' + sess.gist_id, {
      method: 'PATCH',
      headers: {
        'Authorization': 'token ' + sess.token,
        'Accept': 'application/vnd.github.v3+json',
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ files: files })
    });
    if (res.status === 401) {
      alert('⚠️ Your session token has expired or been revoked. Please ask your tutor to update the app with a new token.');
      return false;
    }
    if (!res.ok) {
      console.error('gistSave HTTP error', res.status);
      return false;
    }
    return true;
  } catch(e) { console.error('gistSave error', e); return false; }
}

// Load data for a specific student (used by parent dashboard)
async function gistLoadForStudent(gist_id, gist_file, token) {
  try {
    var res = await fetch('https://api.github.com/gists/' + gist_id, {
      headers: { 'Authorization': 'token ' + token, 'Accept': 'application/vnd.github.v3+json' }
    });
    if (!res.ok) return {};
    var data = await res.json();
    var file = data.files[gist_file];
    if (!file || !file.content) return {};
    return JSON.parse(file.content || '{}');
  } catch(e) { return {}; }
}

// High-level helpers
async function markDayComplete(day) {
  var data = await gistLoad();
  if (!data.completed) data.completed = {};
  data.completed[day] = { ts: Date.now() };
  return gistSave(data);
}

async function isDayComplete(day) {
  var data = await gistLoad();
  return !!(data.completed && data.completed[day]);
}

async function saveScore(day, earned, total) {
  var data = await gistLoad();
  if (!data.scores) data.scores = {};
  data.scores[day] = { earned: earned, total: total, pct: Math.round(earned/total*100), ts: Date.now() };
  return gistSave(data);
}

async function saveAnswers(day, answers) {
  var data = await gistLoad();
  if (!data.answers) data.answers = {};
  // Only save first attempt — don't overwrite if already saved
  if (!data.answers[day]) {
    data.answers[day] = { ts: Date.now(), answers: answers };
    return gistSave(data);
  }
  return true;
}

async function getAnswers(day) {
  var data = await gistLoad();
  return (data.answers && data.answers[day]) ? data.answers[day].answers : null;
}
