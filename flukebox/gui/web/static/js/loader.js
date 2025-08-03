/* Events */

function editClick() {
  $.ajax({
    url: "/api/edit_config"
  }).then(function (data) { });
}

function crawlClick() {
  disableButtons();
  $.ajax({
    url: "/api/crawl"
  }).then(function (data) {
    enableButtons();
  });
}

function reloadClick() {
  clearPlaylists();

  $.ajax({
    url: "/api/playlists"
  }).then(function (data) {
    for (var i = 0; i < data.length; i++) { appendPlaylist(data[i]["name"]); }
    loadStartPlaylist();
  });
}

function loadStartPlaylist() {
  $.ajax({
    url: "/api/start_playlist"
  }).then(function (data) {
    if (data["start_playlist"] != "") {
      loadPlaylist(data["start_playlist"], data["no_local"]);
      $("#cmbPlaylist").val(data["start_playlist"]);
    }
  });
}

function loadClick() {
  var cmbPlay = document.getElementById("cmbPlaylist");
  var playlist = cmbPlay.options[cmbPlay.selectedIndex].text;
  loadPlaylist(playlist, false);
}

/* Utilities */

function loadPlaylist(playlist, no_local) {
  var api_url = "api/generate?playlist=" + playlist + "&no_local=" + no_local
  var that = this;

  $.ajax({
    url: api_url
  }).then(function (data) {
    that.playList = data;
    var songHtml = "";

    for (var i = 0; i < that.playList.length; i++) {
      song = that.playList[i]
      songHtml += "<nobr><img src='" + song.icon_url + "'> ";
      songHtml += "<a href='#' onClick='setSongAndPlay(" + i + ")'>";
      songHtml += "<span class='songName'>" + song.name + "</span>";
      songHtml += "</a> ";
      songHtml += "<span id='arrow_" + i + "'><big> ⭐️</big></span></nobr> &nbsp;&nbsp;";
    }

    $("#songList").html(songHtml);

    for (var i = 0; i < that.playList.length; i++) {
      that.setArrowVisibility(i, "hidden");
    }

    that.resetPlayer();
  });
}

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
  btnQuit.disabled = disabled;
  btnQuit.hidden = disabled;
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

function quit() {
  $.ajax({
    url: "/api/quit"
  }).then(function (data) {
    return;
  });
}

/* On load */

$(document).ready(function () {
  reloadClick();
});