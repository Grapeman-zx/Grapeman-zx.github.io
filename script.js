const likeButtons = [
  {
    button: document.querySelector("#like-button"),
    count: document.querySelector("#like-count"),
    countKey: "grapeman_video_like_count",
    likedKey: "grapeman_video_has_liked",
  },
  {
    button: document.querySelector("#support-like-button"),
    count: document.querySelector("#support-like-count"),
    countKey: "grapeman_support_like_count",
    likedKey: "grapeman_support_has_liked",
  },
];

function readCount(key) {
  return Number.parseInt(localStorage.getItem(key) || "0", 10);
}

function renderLike(item) {
  if (!item.button || !item.count) {
    return;
  }

  const count = readCount(item.countKey);
  const liked = localStorage.getItem(item.likedKey) === "true";
  item.count.textContent = String(count);
  item.button.classList.toggle("is-liked", liked);
  item.button.setAttribute("aria-pressed", String(liked));
}

function toggleLike(item) {
  const count = readCount(item.countKey);
  const liked = localStorage.getItem(item.likedKey) === "true";
  const nextLiked = !liked;
  const nextCount = Math.max(0, count + (nextLiked ? 1 : -1));

  localStorage.setItem(item.countKey, String(nextCount));
  localStorage.setItem(item.likedKey, String(nextLiked));
  renderLike(item);
}

likeButtons.forEach((item) => {
  renderLike(item);
  item.button?.addEventListener("click", () => toggleLike(item));
});
