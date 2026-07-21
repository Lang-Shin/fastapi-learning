// ---------------------------------------------------------
// Shared helpers for pages still running on static data.js:
// book.html, author.html, authors.html.
//
// index.html no longer uses this file — it's rendered
// server-side by Jinja2 now (see templates/index.html).
// ---------------------------------------------------------

function getAuthor(id) {
  return AUTHORS.find(a => a.id === Number(id));
}

function getBook(id) {
  return BOOKS.find(b => b.id === Number(id));
}

function booksByAuthor(authorId) {
  return BOOKS.filter(b => b.authorId === Number(authorId));
}

function toneClass(genre) {
  return "tone-" + (GENRE_COLOR[genre] || "sage");
}

function avgRating(book) {
  if (!book.reviews || book.reviews.length === 0) return null;
  const sum = book.reviews.reduce((acc, r) => acc + r.rating, 0);
  return sum / book.reviews.length;
}

function dotsHtml(rating) {
  const rounded = Math.round(rating || 0);
  let out = '<span class="dots" aria-label="' + (rating ? rating.toFixed(1) : "No ratings") + ' out of 5">';
  for (let i = 1; i <= 5; i++) {
    out += `<span class="dot ${i <= rounded ? "filled" : ""}"></span>`;
  }
  out += "</span>";
  return out;
}

function ratingLineHtml(book) {
  const avg = avgRating(book);
  const count = book.reviews ? book.reviews.length : 0;
  if (!avg) {
    return `<span class="rating-line">${dotsHtml(0)} <span>No reviews yet</span></span>`;
  }
  return `<span class="rating-line">${dotsHtml(avg)} <span class="num">${avg.toFixed(1)}</span><span>(${count})</span></span>`;
}

function bookCardHtml(book) {
  const author = getAuthor(book.authorId);
  return `
    <a class="card ${toneClass(book.genre)}" href="book.html?id=${book.id}">
      <span class="tag-genre">${book.genre}</span>
      <h3>${book.title}</h3>
      <span class="by">by ${author ? author.name : "Unknown"}</span>
      <div class="meta">
        ${ratingLineHtml(book)}
        <span>${book.pages}p · ${book.year}</span>
      </div>
    </a>`;
}

function authorCardHtml(author) {
  const count = booksByAuthor(author.id).length;
  return `
    <a class="author-card" href="author.html?id=${author.id}">
      <span class="avatar">${author.initials}</span>
      <div>
        <h3>${author.name}</h3>
        <p>${author.bio}</p>
        <span class="book-count">${count} book${count === 1 ? "" : "s"} tracked</span>
      </div>
    </a>`;
}

function spineHtml(book) {
  return `
    <a class="spine ${toneClass(book.genre)}" href="book.html?id=${book.id}" title="${book.title}">
      <span class="spine-label">${book.title}</span>
    </a>`;
}

function coverBlockHtml(book) {
  return `
    <div class="cover-block ${toneClass(book.genre)}">
      <span class="cover-title">${book.title}</span>
    </div>`;
}

// ---- page: authors.html ----
function renderAuthors() {
  document.getElementById("author-grid").innerHTML = AUTHORS.map(authorCardHtml).join("");
  document.getElementById("author-count").textContent = AUTHORS.length;
}

// ---- page: book.html?id= ----
function renderBookDetail() {
  const params = new URLSearchParams(window.location.search);
  const book = getBook(params.get("id"));
  const root = document.getElementById("book-root");

  if (!book) {
    root.innerHTML = `<p class="empty-state">This book isn't on the shelf. It may have been misfiled — <a href="index.html">back to all books</a>.</p>`;
    return;
  }

  const author = getAuthor(book.authorId);
  document.title = book.title + " · Bookmark";

  root.innerHTML = `
    <div class="breadcrumb"><a href="index.html">Books</a> / ${book.title}</div>
    <div class="detail-head">
      ${coverBlockHtml(book)}
      <div>
        <h1>${book.title}</h1>
        <div class="by-line">by <a href="author.html?id=${author.id}">${author.name}</a> · ${book.year}</div>
        <div class="tags-row">
          <span class="pill">${book.genre}</span>
          <span class="pill">${book.pages} pages</span>
        </div>
        <p class="desc">${book.description}</p>
        <div class="rating-summary">
          ${dotsHtml(avgRating(book) || 0)}
          <span class="big-num">${avgRating(book) ? avgRating(book).toFixed(1) : "—"}</span>
          <span style="color:var(--taupe); font-size:13px;">${book.reviews.length} review${book.reviews.length === 1 ? "" : "s"}</span>
        </div>
      </div>
    </div>
    <div class="reviews">
      <h2>Reviews</h2>
      ${book.reviews.length ? book.reviews.map(r => `
        <div class="review">
          <div class="review-top">
            <span class="reviewer">${r.reviewer}</span>
            ${dotsHtml(r.rating)}
          </div>
          <p class="comment">${r.comment}</p>
        </div>`).join("") : `<p class="empty-state">No reviews yet.</p>`}
    </div>`;
}

// ---- page: author.html?id= ----
function renderAuthorDetail() {
  const params = new URLSearchParams(window.location.search);
  const author = getAuthor(params.get("id"));
  const root = document.getElementById("author-root");

  if (!author) {
    root.innerHTML = `<p class="empty-state">No author on file with that id — <a href="authors.html">back to all authors</a>.</p>`;
    return;
  }

  document.title = author.name + " · Bookmark";
  const books = booksByAuthor(author.id);

  root.innerHTML = `
    <div class="breadcrumb"><a href="authors.html">Authors</a> / ${author.name}</div>
    <div class="detail-head" style="grid-template-columns: 90px 1fr;">
      <span class="avatar" style="width:90px; height:90px; font-size:26px;">${author.initials}</span>
      <div>
        <h1>${author.name}</h1>
        <p class="desc" style="margin-top:10px;">${author.bio}</p>
      </div>
    </div>
    <div class="section-head" style="margin-top:40px;">
      <h2>Books on shelf</h2>
      <span class="count-tag">${books.length} title${books.length === 1 ? "" : "s"}</span>
    </div>
    <div class="grid">${books.map(bookCardHtml).join("")}</div>`;
}