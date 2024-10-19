document.addEventListener('DOMContentLoaded', function () {
    const text = "Tech in Switzerland";
    const typedTextSpan = document.getElementById("typed-text");
    const cursorSpan = document.querySelector(".cursor");

    const initialDelay = 100; // Delay before typing starts (in milliseconds)
    const typingSpeed = 40; // Increased typing speed for slower effect (in milliseconds)
    let charIndex = 0;

    function typeCharacter() {
        if (charIndex < text.length) {
            typedTextSpan.textContent += text.charAt(charIndex);
            charIndex++;
            setTimeout(typeCharacter, typingSpeed);
        } else {
            // Typing complete, remove cursor after a short delay
            setTimeout(() => {
                cursorSpan.style.display = 'none';
            }, 1000); // Cursor remains visible for 1 second after typing
        }
    }

    function startTyping() {
        typedTextSpan.textContent = '';
        cursorSpan.style.display = 'inline-block';
        setTimeout(typeCharacter, initialDelay);
    }

    if (typedTextSpan && cursorSpan) {
        startTyping();
    }
});

