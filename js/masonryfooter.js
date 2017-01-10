var elem = document.querySelector('.news-feed');
var msnry = new Masonry( elem, {
  // options
  itemSelector: 'figure',
  columnWidth: 200
});

// element argument can be a selector string
//   for an individual element
var msnry = new Masonry( '.news-feed', {
  // options
});
