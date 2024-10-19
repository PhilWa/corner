document.addEventListener('DOMContentLoaded', function () {
    const initialText = "Tech from Switzerland";
    const newText = "Innovation from Switzerland";
    const typedTextSpan = document.getElementById("typed-text");
    const cursorSpan = document.querySelector(".cursor");

    const initialDelay = 100; // Delay before typing starts (in milliseconds)
    const typingSpeed = 40; // Typing speed (in milliseconds)
    const pauseDuration = 4000; // 4-second pause
    let charIndex = 0;

    function typeInitialText() {
        if (charIndex < initialText.length) {
            typedTextSpan.textContent += initialText.charAt(charIndex);
            charIndex++;
            setTimeout(typeInitialText, typingSpeed);
        } else {
            setTimeout(startOverwriting, pauseDuration);
        }
    }

    function startOverwriting() {
        charIndex = 0;
        overwriteText();
    }

    function overwriteText() {
        if (charIndex < newText.length) {
            typedTextSpan.textContent = newText.slice(0, charIndex + 1) + initialText.slice(charIndex + 1);
            charIndex++;
            setTimeout(overwriteText, typingSpeed);
        } else {
            // Typing complete, remove cursor after a short delay
            setTimeout(() => {
                cursorSpan.style.display = 'none';
            }, 1000);
        }
    }

    function startTyping() {
        typedTextSpan.textContent = '';
        cursorSpan.style.display = 'inline-block';
        setTimeout(typeInitialText, initialDelay);
    }

    if (typedTextSpan && cursorSpan) {
        startTyping();
    }
});