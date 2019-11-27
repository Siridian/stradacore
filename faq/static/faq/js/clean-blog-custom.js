var csrftoken = Cookies.get('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

$("#satisfy").on('click', function(){
    $("#satisfied").css({display: "inline"});
    $("#satisfy").css({display: "none"});
    $("#unsatisfy").css({display: "none"});
    $.post(
        "/faq/answer_validate/",
        {
            "user_question": last_query,
            "answer_id": answer_id
        },
        function(){
            alert("Votre avis a été enregistré !")
        }
     )
})

$("#unsatisfy").on('click', function(){
    $("#unsatisfied").css({display: "inline"});
    $("#satisfy").css({display: "none"});
    $("#unsatisfy").css({display: "none"});
})

$(".fa-download").on('click', function(event){
    console.log(event.target)
    let recipe_id = $(event.target).find("input")[0].value;
    let recipe_file_name = event.target.id.split("/")[1]
    fetch('/recipes/recipe_download/' + recipe_id)
      .then(resp => resp.blob())
      .then(blob => {
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.style.display = 'none';
        a.href = url;
        a.download = recipe_file_name;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
      })
      .catch(() => alert('oh no!'));
})

$(".fa-repeat").on('click', function(event){
    let recipe_container = $(event.target).parent()[0];
    $.post(
        "/recipes/recipe_refresh/",
        {
            "recipe_type": recipe_container.id[0],
            "recipe_ids": recipe_ids
        },
        function(response){
            if(response['status'] == 'out'){
                $(recipe_container).html("<h3>Aucune autre recette n'est disponible !</h3>")
            }
            else{
                recipe_ids += response['id'] + " "
                console.log(recipe_ids)
                $($(recipe_container).children("h3")[0]).text(response['name']);
                $($(recipe_container).children("div")[1]).html(response['directions']);
                $($(recipe_container).children("div")[0]).children().remove();
                response["ingredients"].forEach(element => $($(recipe_container).children("div")[0]).append("<p>" + element + "</p>"));
            }
        }
     )
})