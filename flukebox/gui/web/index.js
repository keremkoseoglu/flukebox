/* Events */

function editClick() {
  eel.edit_config();
}

function crawlClick() {
  disableButtons();
  eel.crawl();
}

function reloadClick() {
  eel.reload();
}

function playClick() {
  var cmbPlay = document.getElementById("cmbPlaylist");
  var playlist = cmbPlay.options[cmbPlay.selectedIndex].text;
  eel.generate(playlist);
}

/* Utilities */

function disableButtons() {
  setButtonsDisabled(true);
}

eel.expose(enableButtons);
function enableButtons() {
  setButtonsDisabled(false);
}

function setButtonsDisabled(disabled) {
  var btnEdit = document.getElementById("btnEdit");
  var btnReload = document.getElementById("btnReload");
  var btnCrawl = document.getElementById("btnCrawl");
  var btnPlay = document.getElementById("btnPlay");

  btnEdit.disabled = disabled;
  btnEdit.hidden = disabled;
  btnReload.disabled = disabled;
  btnReload.hidden = disabled;
  btnCrawl.disabled = disabled;
  btnCrawl.hidden = disabled;
  btnPlay.disabled = disabled;
  btnPlay.hidden = disabled;
}

eel.expose(clearPlaylists);
function clearPlaylists() {
  var cmbPlay = document.getElementById("cmbPlaylist");
  cmbPlay.innerHTML = "";
}

eel.expose(appendPlaylist);
function appendPlaylist(name) {
  var cmbPlay = document.getElementById("cmbPlaylist");
  var opt = document.createElement("option");
  opt.value = name;
  opt.innerHTML = name;
  cmbPlay.appendChild(opt);
}

/* On load */

document.addEventListener('contextmenu', event => event.preventDefault());
eel.reload();