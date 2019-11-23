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