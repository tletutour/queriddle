const sqlite3 = require('sqlite3').verbose();
//var path = document.location.pathname;
let db = new sqlite3.Database('base.db', (err) => {
    if (err) {
        console.error(err.message);
    }
})
console.log('Connected to the database.');

db.serialize(() => {
  db.each(`SELECT annee FROM matieres GROUP BY annee `, (err, row) => {
    if (err) {
      console.error(err.message);
    }
    console.log(row);

  });
});

db.close((err) => {
  if (err) {
    console.error(err.message);
  }
  console.log('Close the database connection.');
});