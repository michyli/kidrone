const dropdownBtns = document.querySelectorAll('.projectDropdown');

dropdownBtns.forEach((btn) => {
  btn.querySelector('.dropdownBtn').addEventListener('click', function() {
    if (btn.classList.contains('show')) {
      btn.classList.remove('show');
    } else {
    dropdownBtns.forEach((el) => el.classList.remove('show'));
    btn.classList.add('show');
    }
  })
})