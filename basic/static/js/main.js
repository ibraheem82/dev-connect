
// -> GET SEARCH FORM AND PAGE LINKS
let searchForm = document.getElementById('searchForm')
//  Grabing all the pagination button and getting them by thier className.
// It will return a queryset of items
let pageLinks  = document.getElementsByClassName('page-link')
// Check if searchForm exist
// --> ENSURE SEARCH FORM EXIST
if (searchForm) {
    // Looping through every single items and add an event handler, so all the page links will have an event handler it will allows  to do something when that page item is clicked on or when the page button is clicked on.
    for(let i = 0; pageLinks.length > i; i++) {
      // Get page link.
      // Indexing it by the value.
      // get each page link on each iteration.
      // grab each elements and add eventlisteners.
        pageLinks[i].addEventListener('click', function(e) {
          e.preventDefault()
          

          // GETTING THE DATA Attributes
          // * the dataset -> [page] which is data[-page]
          let page = this.dataset.page
          console.log('PAGE', page);

          // Adding hidden search input
          // we are passing it the current page value
          searchForm.innerHTML += `<input value=${page} name="page" hidden />`
            


          // Submitting the form
          searchForm.submit()
          
        })
    }
}