// ---------------------------------------------------------
// Static mock data — swap this file for a fetch() to your
// FastAPI endpoints once the backend is ready. Shape stays
// the same: AUTHORS[], BOOKS[] (with nested reviews[]).
// ---------------------------------------------------------

const AUTHORS = [
  {
    id: 1,
    name: "Naomi Alderisi",
    bio: "Writes quiet, character-driven fiction about people rebuilding their lives in small towns.",
    initials: "NA",
  },
  {
    id: 2,
    name: "Femi Okonkwo-Blythe",
    bio: "Historian turned novelist, known for meticulously researched historical fiction.",
    initials: "FB",
  },
  {
    id: 3,
    name: "Yuki Tanaka Marsh",
    bio: "Poet and essayist exploring memory, migration, and the domestic everyday.",
    initials: "YT",
  },
  {
    id: 4,
    name: "Callum Reyes",
    bio: "Science journalist writing narrative nonfiction on climate and the ocean.",
    initials: "CR",
  },
  {
    id: 5,
    name: "Priya Vantham",
    bio: "Fantasy author building slow-burn, folklore-rooted worlds.",
    initials: "PV",
  },
];

const BOOKS = [
  {
    id: 1,
    title: "The Quiet Ledger",
    authorId: 1,
    genre: "Fiction",
    pages: 312,
    year: 2019,
    description:
      "A bookkeeper in a dying mill town discovers a decade of falsified accounts left by her late father, and has to decide who the truth is actually for.",
    reviews: [
      { reviewer: "M. Ostrander", rating: 5, comment: "Restrained and devastating. Not a wasted sentence." },
      { reviewer: "j.reads", rating: 4, comment: "Slow start, but it earns the ending." },
      { reviewer: "Terri K.", rating: 4, comment: "Quietly one of the best things I read this year." },
    ],
  },
  {
    id: 2,
    title: "Harbor Light, 1911",
    authorId: 2,
    genre: "Historical Fiction",
    pages: 428,
    year: 2021,
    description:
      "Three lighthouse keepers' families navigate a shipping strike on a fictional New England coast, based on real labor archives.",
    reviews: [
      { reviewer: "Dockside Reader", rating: 5, comment: "The research shows without ever showing off." },
      { reviewer: "Priya S.", rating: 5, comment: "Immersive and humane. I felt the cold." },
    ],
  },
  {
    id: 3,
    title: "Salt and Second Names",
    authorId: 2,
    genre: "Historical Fiction",
    pages: 356,
    year: 2023,
    description:
      "A sequel of sorts to Harbor Light — following a granddaughter tracing her family's name changes through three generations of migration.",
    reviews: [
      { reviewer: "wrenlibrary", rating: 4, comment: "Didn't need to have read the first book, but it helps." },
      { reviewer: "Aaron D.", rating: 3, comment: "Good, though the middle section drags a little." },
    ],
  },
  {
    id: 4,
    title: "Small Weather",
    authorId: 3,
    genre: "Poetry",
    pages: 96,
    year: 2020,
    description:
      "A collection tracing one household across four seasons — grief, cooking, language lost and relearned.",
    reviews: [
      { reviewer: "L. Fenwick", rating: 5, comment: "I read it in one sitting on the train and missed my stop." },
      { reviewer: "poetry_pete", rating: 5, comment: "The kitchen poems in particular are extraordinary." },
      { reviewer: "Nour A.", rating: 4, comment: "Spare, precise, a little devastating." },
    ],
  },
  {
    id: 5,
    title: "What the Table Remembers",
    authorId: 3,
    genre: "Essays",
    pages: 208,
    year: 2022,
    description:
      "Essays on inherited recipes and the versions of ourselves we set aside to belong somewhere new.",
    reviews: [
      { reviewer: "homecook88", rating: 4, comment: "Made me call my grandmother, which is the highest compliment I can give a book." },
    ],
  },
  {
    id: 6,
    title: "The Warming Line",
    authorId: 4,
    genre: "Nonfiction",
    pages: 288,
    year: 2022,
    description:
      "A narrative account following three research vessels tracking a shifting current, and the fishing towns watching it move.",
    reviews: [
      { reviewer: "ClimateReads", rating: 5, comment: "Clear-eyed reporting without losing the human stakes." },
      { reviewer: "B. Holt", rating: 4, comment: "Dense in places but consistently gripping." },
    ],
  },
  {
    id: 7,
    title: "Deep Field",
    authorId: 4,
    genre: "Nonfiction",
    pages: 244,
    year: 2024,
    description:
      "On the last unmapped trenches of the Pacific, and the small submersible teams racing to document them before deep-sea mining begins.",
    reviews: [
      { reviewer: "oceanic_j", rating: 5, comment: "Read like a thriller. Could not put it down." },
    ],
  },
  {
    id: 8,
    title: "The Ninth Orchard",
    authorId: 5,
    genre: "Fantasy",
    pages: 512,
    year: 2018,
    description:
      "A grafter tends an orchard that grows one true memory per tree — and one season, the trees start disagreeing with each other.",
    reviews: [
      { reviewer: "Fable & Co", rating: 5, comment: "Folklore-rooted worldbuilding at its best." },
      { reviewer: "R. Voss", rating: 4, comment: "Slow-burn in the best way. Stick with the first hundred pages." },
      { reviewer: "moth_reads", rating: 5, comment: "Reread it the week I finished it." },
    ],
  },
  {
    id: 9,
    title: "A Debt of Crows",
    authorId: 5,
    genre: "Fantasy",
    pages: 468,
    year: 2021,
    description:
      "Companion novel set in the same world, following the orchard's estranged rival family and the debts owed between them.",
    reviews: [
      { reviewer: "Fable & Co", rating: 4, comment: "Not quite as tight as the first, still excellent." },
      { reviewer: "K. Emberly", rating: 5, comment: "The best kind of companion novel — stands entirely on its own." },
    ],
  },
  {
    id: 10,
    title: "Return Address",
    authorId: 1,
    genre: "Fiction",
    pages: 274,
    year: 2023,
    description:
      "A postal worker in a coastal town spends a year trying to deliver a single undeliverable letter to its rightful owner.",
    reviews: [
      { reviewer: "j.reads", rating: 4, comment: "Gentle, funny, a little sad. Very her." },
      { reviewer: "Sam O.", rating: 3, comment: "Sweet but slight compared to The Quiet Ledger." },
    ],
  },
];

// small color set keyed by genre — used for the spine / accent bars
const GENRE_COLOR = {
  "Fiction": "sage",
  "Historical Fiction": "ochre",
  "Poetry": "rose",
  "Essays": "rose",
  "Nonfiction": "slate",
  "Fantasy": "plum",
};
