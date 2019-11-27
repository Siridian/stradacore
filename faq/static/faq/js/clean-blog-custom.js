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