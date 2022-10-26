document.addEventListener('DOMContentLoaded', () => {
  let options = {
    callback: (isTruncated) => {},
  };
  for (let selector of ['.card-title']) {
    document.querySelectorAll(selector).forEach((el) => {
      new Dotdotdot(el, options);
    });
  }

  const reader_img = document.getElementById('page');
  const preload = document.getElementById('preload');
  if (reader_img && preload) {
    reader_img.onload = () => {
      preload.src = preload.dataset.src;
    };

    if (reader_img.complete) {
      // image is already loaded
      reader_img.onload();
    }
  }
});
