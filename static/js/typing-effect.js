document.addEventListener('DOMContentLoaded', function () {
    const phrases = [
        "Tech from Switzerland",
        "Startups from Switzerland",
        "Innovation from Switzerland"
    ];
    const typedTextSpan = document.getElementById("typed-text");
    const cursorSpan = document.querySelector(".cursor");

    const initialDelay = 100; // Delay before typing starts (in milliseconds)
    const typingSpeed = 40; // Typing speed (in milliseconds)
    const pauseDuration = 2000; // 2-second pause between phrases
    let phraseIndex = 0;
    let charIndex = 0;

    function typePhrase() {
        if (charIndex < phrases[phraseIndex].length) {
            typedTextSpan.textContent = phrases[phraseIndex].substring(0, charIndex + 1);
            charIndex++;
            setTimeout(typePhrase, typingSpeed);
        } else {
            if (phraseIndex < phrases.length - 1) {
                setTimeout(startNextPhrase, pauseDuration);
            } else {
                // Remove the cursor after the last phrase is typed
                setTimeout(() => {
                    cursorSpan.style.display = 'none';
                }, 1000);
            }
        }
    }

    function startNextPhrase() {
        phraseIndex++;
        charIndex = 0;
        typePhrase();
    }

    function startTyping() {
        typedTextSpan.textContent = '';
        cursorSpan.style.display = 'inline-block';
        setTimeout(typePhrase, initialDelay);
    }

    if (typedTextSpan && cursorSpan) {
        startTyping();
    }
});
