function toggleCollapse() {
  const element = document.getElementById("navbarNav");
  if (element.classList.contains('collapse')) {
    element.classList.remove('collapse');
  } else {
    element.classList.add('collapse');
  }
}

