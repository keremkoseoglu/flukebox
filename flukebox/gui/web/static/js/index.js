/* Events */

function editClick() {
  $.ajax({
    url: "/api/edit_config"
  }).then(function(data) {});
}

function crawlClick() {
  disableButtons();
  $.ajax({
    url: "/api/crawl"
  }).then(function(data) {
    enableButtons();
  });
}

function reloadClick() {
  clearPlaylists();

  $.ajax({
    url: "/api/playlists"
  }).then(function(data) {
    for (var i = 0; i < data.length; i++) {
        appendPlaylist(data[i]["name"]);
    }
  });
}

function playClick() {
  var cmbPlay = document.getElementById("cmbPlaylist");
  var playlist = cmbPlay.options[cmbPlay.selectedIndex].text;
  var api_url = "api/generate?playlist=" + playlist
  $.ajax({
    url: api_url
  }).then(function(data) {});
}

/* Utilities */

function disableButtons() {
  setButtonsDisabled(true);
}

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

function clearPlaylists() {
  var cmbPlay = document.getElementById("cmbPlaylist");
  cmbPlay.innerHTML = "";
}

function appendPlaylist(name) {
  var cmbPlay = document.getElementById("cmbPlaylist");
  var opt = document.createElement("option");
  opt.value = name;
  opt.innerHTML = name;
  cmbPlay.appendChild(opt);
}

/* On load */

$(document).ready(function() { 
  reloadClick();
});