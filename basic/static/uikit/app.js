// Invoke Functions Call on Document Loaded
// document.addEventListener('DOMContentLoaded', function () {
//   hljs.highlightAll();
// });




// let alertWrapper = document.querySelector('.alert');
// let alertClose = document.querySelector('.alert__close');

// alertClose.addEventListener('click', () => {
//   if (alertWrapper) {
//   console.log('Alert Wrapper clicked');
//     alertWrapper.remove();

//   }
// });


let alertWrapper = document.querySelector('.alert')
let alertClose = document.querySelector('.alert__close')


if (alertWrapper) {
  console.log('Alert Wrapper clicked');
  alertClose.addEventListener('click', () =>
    alertWrapper.style.display = 'none'
  )
}




// if(alertWrapper) {
//   alertClose.addEventListener('click', () => 
//     alertWrapper.style.display  = 'none';
    // alertWrapper.remove();
//   console.log('Alert Wrapper clicked');

//   )
// }



