//This function will create a new post
function newPost() {
  fetch('/new_post', {
      method: 'POST',
      body: JSON.stringify({
        content: document.querySelector('#post-content').value
      })
    })
    .then(response => response.json())
    .then(result => {
      // Display success alert
      document.querySelector("#post-added-alert").innerHTML = `<div class="alert alert-success" role="alert">${result.message}</div>`
      //remove alert after 1 sec
      setTimeout(() => {
        document.querySelector("#post-added-alert").remove()
      }, 1000);

      //close modal
      document.querySelector("#close").click()
      //clear input field
      document.querySelector('#post-content').value = '';
    });
}

function editing_post(post_id) {

  fetch('/editing_post', {
      method: 'POST',
      body: JSON.stringify({
        id: post_id
      })
    })
    .then(response => response.json())
    .then(result => {

      // pull the model
      model = document.querySelector("#edit_post")
      //get the input field and fill it with the content of the post
      model.querySelector("input").value = result.content
      //set name so i can get the post id when user submits
      model.querySelector("input").setAttribute("name", post_id)
    });
}

function edit_post() {
  // pull the model
  model = document.querySelector("#edit_post")
  fetch('/edit_post', {
      method: 'POST',
      body: JSON.stringify({
        id: model.querySelector('input').getAttribute("name"),
        content: model.querySelector('input').value
      })
    })
    .then(response => response.json())
    .then(result => {
      //close modal
      model.querySelector("#close_edit_post").click()

      // Display success alert
      document.querySelector("#post-edited-alert").innerHTML = `<div class="alert alert-success" role="alert">${result.message}</div>`

      //remove alert after 1 sec
      setTimeout(() => {
        document.querySelector("#post-edited-alert").remove()
      }, 1000);


    });
}

//display on users profile page
function follow() {
  //get me the value which is the id of the users page were on
  id = document.querySelector("#follow_button").value;
  //get request
  fetch(`/follow/${id}`)
    .then(response => response.json())
    .then(follow => {
      // baised on response you display button
      button = document.querySelector("#follow_button");
      if (follow.message === "remove button") {
        button.style.display = "none";
      } else if (follow.message === "Unfollow") {
        button.innerHTML = "Unfollow";
      } else {
        button.innerHTML = "Follow";
      }
    });
}

function follow_button() {
  fetch('/follow', {
      method: 'POST',
      body: JSON.stringify({
        button: document.querySelector("#follow_button").innerHTML,
        user_id: document.querySelector("#follow_button").value
      })
    })
    .then(response => response.json())
    .then(result => {
      follow();
    });
}


function like(user_id, post_id) {
  fetch('/like', {
      method: 'POST',
      body: JSON.stringify({
        user_id: user_id,
        post_id: post_id
      })
    })
    .then(response => response.json())
    .then(result => {
      window.location.reload()
    });
}
