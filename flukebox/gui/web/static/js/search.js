const searchBox = document.getElementById('searchBox');
let originalMap = new Map();

// Show search box on Cmd+F
document.addEventListener('keydown', function (e) {
    const isMac = navigator.platform.toUpperCase().includes('MAC');
    if (isMac && e.metaKey && e.key === 'f') {
        e.preventDefault();
        searchBox.style.display = 'block';
        searchBox.focus();

        // Save original text contents once
        if (originalMap.size === 0) {
            document.querySelectorAll('.songName').forEach(el => {
                originalMap.set(el, el.textContent);
            });
        }
    }
});

// Handle Enter and Escape in search box
searchBox.addEventListener('keydown', function (e) {
    if (e.key === 'Enter') {
        const keyword = searchBox.value.trim();
        const regex = new RegExp(`(${keyword})`, 'gi');

        document.querySelectorAll('.songName').forEach(el => {
            const original = originalMap.get(el) || el.textContent;

            if (!keyword) {
                el.innerHTML = original;
            } else {
                el.innerHTML = original.replace(regex, '<mark>$1</mark>');
            }
        });
    }

    if (e.key === 'Escape') {
        searchBox.value = '';
        searchBox.style.display = 'none';

        // Reset all songName elements
        document.querySelectorAll('.songName').forEach(el => {
            const original = originalMap.get(el);
            if (original) el.innerHTML = original;
        });
    }
});