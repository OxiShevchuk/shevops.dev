document.addEventListener('DOMContentLoaded', () => {
    const counterSection = document.getElementById('counterSection');
    const counterValues = document.querySelectorAll('.counter-value');
    let countersStarted = false; // Flag to ensure counters only start once

    // Easing function: Ease-Out Quad (starts fast, decelerates)
    const easeOutQuad = (t) => t * (2 - t); 
    // Another popular ease-out option: easeOutCubic = (t) => (--t) * t * t + 1;

    const startCounter = (entry) => {
        if (entry.isIntersecting && !countersStarted) {
            countersStarted = true; // Set flag to true to prevent re-triggering

            counterValues.forEach(counter => {
                const target = +counter.dataset.target; // Get target from data-target attribute, convert to number
                const duration = 2000; // Animation duration in milliseconds (e.g., 2 seconds)
                let start = 0;
                let startTime = null;

                const animate = (currentTime) => {
                    if (!startTime) startTime = currentTime;
                    const linearProgress = (currentTime - startTime) / duration;
                    const easedProgress = easeOutQuad(Math.min(linearProgress, 1)); // Apply easeOutQuad here

                    const value = Math.floor(easedProgress * target); // Use easedProgress
                    counter.textContent = value;

                    if (linearProgress < 1) { // Continue until linearProgress reaches 1
                        requestAnimationFrame(animate);
                    }
                };

                requestAnimationFrame(animate);
            });

            // Optional: Disconnect observer after counters have started if you only want it to run once
            observer.disconnect(); 
        }
    };

    // Create an Intersection Observer
    const observer = new IntersectionObserver(entries => {
        entries.forEach(startCounter);
    }, {
        threshold: 0.5 // Trigger when 50% of the section is visible
    });

    // Observe the counter section
    if (counterSection) {
        observer.observe(counterSection);
    }
});



const track = document.getElementById('carouselItems');// The container holding all carousel items

let items = document.querySelectorAll('#carouselItems .item');// Select all original carousel items

let currentIndex = 0; // Tracks current position in the carousel
let itemsPerSlide = window.innerWidth >= 768 ? 2 : 1; // Number of items shown per view (2 on desktop, 1 on mobile)
let autoplayInterval = null; // Stores the interval timer for autoplay

// Clone first and last items for seamless infinite scrolling
function cloneSlides() {
  const clonesBefore = [];
  const clonesAfter = [];

  // Clone the last N items and place before (for backward looping)
  for (let i = 0; i < itemsPerSlide; i++) {
    const firstClone = items[i].cloneNode(true); // Clone from start
    const lastClone = items[items.length - 1 - i].cloneNode(true); // Clone from end
    clonesAfter.push(firstClone);
    clonesBefore.unshift(lastClone);
  }

  // Add clones to beginning and end of the track
  clonesBefore.forEach(clone => track.insertBefore(clone, track.firstChild));
  clonesAfter.forEach(clone => track.appendChild(clone));

  // Re-select all items after clones are added
  items = document.querySelectorAll('#carouselItems .item');
}

// Get the width of a single carousel item
function getItemWidth() {
  return items[0].offsetWidth;
}

// Apply translateX to move the carousel to the current position
function updateTrack(animate = true) {
  const offset = getItemWidth() * (currentIndex + itemsPerSlide); // Include clone offset
  track.style.transition = animate ? 'transform 0.5s ease-in-out' : 'none'; // Smooth or instant jump
  track.style.transform = `translateX(-${offset}px)`; // Move track left
}

// Move to next slide
function nextSlide() {
  currentIndex++;
  updateTrack();

  // If at the end of real items, reset to beginning (after transition)
  if (currentIndex >= items.length - itemsPerSlide * 2) {
    setTimeout(() => {
      currentIndex = 0;
      updateTrack(false); // Jump instantly (no animation)
    }, 510); // Slight delay to let animation finish
  }
}

// Move to previous slide
function prevSlide() {
  currentIndex--;
  updateTrack();

  // If before start, jump to the last real slide
  if (currentIndex < 0) {
    setTimeout(() => {
      currentIndex = items.length - itemsPerSlide * 2 - 1;
      updateTrack(false);
    }, 510);
  }
}

// Start the autoplay timer
function startAutoplay() {
  autoplayInterval = setInterval(() => {
    nextSlide();
  }, 7000); // Slide every 4 seconds
}

// Stop the autoplay timer
function stopAutoplay() {
  clearInterval(autoplayInterval);
}

// Navigation button events
document.getElementById('nextBtn').addEventListener('click', () => {
  stopAutoplay();
  nextSlide();
  startAutoplay();
});

document.getElementById('prevBtn').addEventListener('click', () => {
  stopAutoplay();
  prevSlide();
  startAutoplay();
});

// Update number of visible items when window is resized
window.addEventListener('resize', () => {
  itemsPerSlide = window.innerWidth >= 768 ? 2 : 1;
  updateTrack(false); // Recalculate position instantly
});

// Initial setup
cloneSlides(); // Add clones for infinite scroll
updateTrack(false); // Jump to correct position


// === Visibility-controlled autoplay ===

const carouselWrapper = document.querySelector('.carousel-wrapper'); // The element to observe

// Create an intersection observer
const carouselObserver = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      startAutoplay();  // Start when carousel enters view
    } else {
      stopAutoplay();   // Stop when carousel leaves view
    }
  });
}, {
  threshold: 0.5  // Adjust as needed (0.5 = 50% visible)
});

// Start observing carousel wrapper
carouselObserver.observe(carouselWrapper);

//Back to Top Button
//Get the button
let mybutton = document.getElementById("btn-back-to-top");

// When the user scrolls down 20px from the top of the document, show the button
window.onscroll = function () {
  scrollFunction();
};

function scrollFunction() {
  if (
    document.body.scrollTop > 20 ||
    document.documentElement.scrollTop > 20
  ) {
    mybutton.style.display = "block";
  } else {
    mybutton.style.display = "none";
  }
}
// When the user clicks on the button, scroll to the top of the document
mybutton.addEventListener("click", backToTop);

function backToTop() {
  document.body.scrollTop = 0;
  document.documentElement.scrollTop = 0;
}