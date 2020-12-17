console.log("heller")

// rainbow neon scrollbar
let progress = document.getElementById('progressBar');
console.log(progress)
let totalHeight = document.body.scrollHeight - window.innerHeight;
window.onscroll = function() {
    let progressHeight = (window.pageYOffset / totalHeight * 100);
    progress.style.height = progressHeight + '%';
}
