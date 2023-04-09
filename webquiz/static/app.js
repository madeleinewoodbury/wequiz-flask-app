function removeFlash() {
  const flashMessage = document.getElementById('flash-message');
  flashMessage.remove();
}

setTimeout(() => {
  const alerts = document.getElementById('alert-container');
  alerts.remove();
}, '5000');

let isMultipleChoice = document.getElementById('is_multiple_choice');
let choices = document.getElementById('choices');
isMultipleChoice.onchange = function () {
  choices.classList.contains('hidden')
    ? choices.classList.remove('hidden')
    : choices.classList.add('hidden');
};
