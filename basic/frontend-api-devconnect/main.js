let loginBtn = document.getElementById('login-btn');
let logoutBtn = document.getElementById('logout-btn');

let token = localStorage.getItem('$(api-token)$');
// * if token login btn should be removed else logout btn should be removed.
// ! Logic
token ? loginBtn.remove() : logoutBtn.remove();


logoutBtn.addEventListener('click', (e) => {
  e.preventDefault()
  localStorage.removeItem('$(api-token)$')
  window.location = 'file:///C:/xampp/htdocs/frontend-api-devconnect/auth.html'
})


let projectsUrl = "http://127.0.0.1:8000/api/projects/";
// will get projects
let getProjects = () => {
  fetch(projectsUrl)
    .then((response) => response.json())
    .then((data) => {
      console.log(data);
      // passed here.
      buildProjects(data);
    });
};

let buildProjects = (projects) => {
  let projectsWrapper = document.getElementById("projects--wrapper");
  projectsWrapper.innerHTML = '';
  // console.log(`Project wrapper ${projectsWrapper}`);
  // console.log(projectsWrapper);

  for (let i = 0; projects.length > i; i++) {
    let project = projects[i];
    // console.log(project);

    // * Displaying api in frontend.
    let projectCard = `
            <div class="project--card">
                <img src="http://127.0.0.1:8000${project.featured_image}">


                <div>

                         <div class="card--header">
                                
                <h3>${project.title}</h3>
                <strong class="vote--option" data-vote="up" data-project="${
                  project.id
                }">&#43;</strong>
                <strong class="vote--option" data-vote="down" data-project="${
                  project.id
                }">&#8722;</strong>
                                
                                
                </div>
                <i>${project.vote_ratio}% Positive feedback</i>
                <p>${project.description.substring(0, 100)}</p>
        </div>
            </div>
        `;
    projectsWrapper.innerHTML += projectCard;
  }

  addVoteEvents();
};

let addVoteEvents = () => {
  let voteBtns = document.getElementsByClassName("vote--option");

  for (let i = 0; voteBtns.length > i; i++) {
    voteBtns[i].addEventListener("click", (e) => {
      // console.log('Vote was clicked: ', i);

    //   * Added to localStorage.
    // * Getting the localStorage on each request.
      let token = localStorage.getItem('$(api-token)$')
      console.log(token);
      let vote = e.target.dataset.vote;
      let project = e.target.dataset.project;
    //   console.log("PROJECT:", project, "VOTE:", vote);
    fetch(`http://127.0.0.1:8000/api/projects/${project}/vote/`,  {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${token}`
        },
        body:JSON.stringify({'value': vote})
    })
    .then(response=>response.json())
    .then(data=>{
        console.log('Done:', data);
        // * Anytime the vote is complete, load in more projects
getProjects();

    })
    });
  }
};
// {{URL}}/api/projects/32a5038f-7e6e-42f3-a336-c0fd4d47a03f/vote/
getProjects();
