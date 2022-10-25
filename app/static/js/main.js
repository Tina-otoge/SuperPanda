document.addEventListener('DOMContentLoaded', () => {
  let options = {
    callback: (isTruncated) => {},
  };
  for (let selector of ['.card-title']) {
    document.querySelectorAll(selector).forEach((el) => {
      new Dotdotdot(el, options);
    });
  }
});
