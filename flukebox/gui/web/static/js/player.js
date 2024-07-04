var randomPlayList = [];
var index = -1;
var playList = [];

for (i = 0; i < playList.length; i++) {
    setArrowVisibility(i, "hidden");
}

function prev() {
    if (index == 0) { return; }
    setArrowVisibility(index, "hidden");
    index -= 1;
    refreshSongName();
}

function randomSong() {
    lazyBuildRandomPlaylist();
    randomIndex = Math.floor(Math.random() * randomPlayList.length);
    songIndex = getSongIndex(randomPlayList[randomIndex].name);
    setSong(songIndex);
}

function next() {
    if (index == playList.length - 1) { return; }
    setArrowVisibility(index, "hidden");
    index += 1;
    refreshSongName();
}

function setSong(newIndex) {
    setArrowVisibility(index, "hidden");
    index = newIndex;
    refreshSongName();
}

function setSongAndPlay(newIndex) {
    setSong(newIndex);
    refreshPlayerWindow();
}

function refreshSongName() {
    setArrowVisibility(index, "visible");
    song = playList[index];
    var show_name = song.name;
    if (show_name.length > 58) { show_name = show_name.substring(0, 58) + "..." }
    document.getElementById("currentSong").innerHTML = "<img src=" + song.icon_url + "> " + show_name + "</img>";
    removeRandomSong(song.name);
}

function refreshPlayerWindow() {
    $.ajax({
        url: "/api/play?url=" + encodeURI(song.url)
    }).then(function (data) {

    });
}

function clearPlayerWindow() {
    $.ajax({
        url: "/api/stop"
    }).then(function (data) {

    });
}

function setArrowVisibility(index, visibility) {
    var arrow = "arrow_" + index;
    var arrowObj = document.getElementById(arrow)
    if (arrowObj) { arrowObj.style.visibility = visibility; }
}

function lazyBuildRandomPlaylist() {
    if (randomPlayList.length <= 0) { randomPlayList = [...playList]; }
}

function getSongIndex(songName) {
    for (n = 0; n < playList.length; n++) {
        if (playList[n].name == songName) { return n; }
    }
    return -1;
}

function removeRandomSong(songName) {
    songIndex = -1;
    for (n = 0; n < randomPlayList.length; n++) {
        if (randomPlayList[n].name == songName) { songIndex = n; }
    }
    if (songIndex < 0) { return; }
    randomPlayList.splice(songIndex, 1)
}

function resetPlayer() {
    randomPlayList = [];
    index = -1;
}
