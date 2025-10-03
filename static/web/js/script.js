$(document).ready(function(){

// 000000000000000000000000000000000000000000000000000000000000000000000000000000000
// 000000000000000000000000000000000000000000000000000000000000000000000000000000000
// 000000000000000000000000000000000000000000000000000000000000000000000000000000000
    function getCSRFToken() {
        const cookies = document.cookie.split(';');
        for (let cookie of cookies) {
            const [name, value] = cookie.trim().split('=');
            if (name === 'csrftoken') {
                return value;
            }
        }
        return null;
    }

// 000000000000000000000000000000000000000000000000000000000000000000000000000000000
// 000000000000000000000000000000000000000000000000000000000000000000000000000000000
// 000000000000000000000000000000000000000000000000000000000000000000000000000000000

    $(document).on('scroll', function() {
        var scrollDistance = $(this).scrollTop();
        if (scrollDistance > 100) {
          $('.scroll-to-top').fadeIn();
        } else {
          $('.scroll-to-top').fadeOut();
        }
      });
    
// 000000000000000000000000000000000000000000000000000000000000000000000000000000000
// 000000000000000000000000000000000000000000000000000000000000000000000000000000000
// 000000000000000000000000000000000000000000000000000000000000000000000000000000000
    
    control_scroll=(elemnto)=>{
        window.scrollTo({
            top: elemnto,
            behavior: 'smooth'
        });
    }

// 000000000000000000000000000000000000000000000000000000000000000000000000000000000
// 000000000000000000000000000000000000000000000000000000000000000000000000000000000
// 000000000000000000000000000000000000000000000000000000000000000000000000000000000
    
    document.querySelectorAll('.scroll-link').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href').substring(1);
            // const targetElement = $(targetId);
            // console.log(targetElement.offset().top)
            
            // const targetElement = $(targetId).offset().top;
            // console.log(targetElement.offsetTop);
            
            // Desplazamiento suave
            control_scroll($(targetId).offset().top);
            
        });
    });

// 000000000000000000000000000000000000000000000000000000000000000000000000000000000
// 000000000000000000000000000000000000000000000000000000000000000000000000000000000
// 000000000000000000000000000000000000000000000000000000000000000000000000000000000
// 000000000000000000000000000000000000000000000000000000000000000000000000000000000
// 000000000000000000000000000000000000000000000000000000000000000000000000000000000

        var pathname =location.pathname.replace(/\/$/, "");
        try {
            document.querySelector(`a.nav-link[href='${pathname}']`).parentElement.classList.add("active");
        } catch (error) {
            console.log("***ERROR 1");
            console.log(error);
            try {
                // activa el menu del utlimo nivel 
                document.querySelector(`a.dropdown-item[href='${decodeURIComponent(location.pathname)}']`).classList.add("active");
                document.querySelector(`a.dropdown-item[href='${decodeURIComponent(location.pathname)}']`).parentNode.parentNode.parentNode.parentElement.classList.add("active");
                document.querySelector(`a.dropdown-item[href='${decodeURIComponent(location.pathname)}']`).parentNode.parentNode.firstElementChild.classList.add("active"); 
                document.querySelector(`a.dropdown-item[href='${decodeURIComponent(location.pathname)}']`).parentNode.parentNode.classList.add("active"); 
                document.querySelector(`a.dropdown-item[href='${decodeURIComponent(location.pathname)}']`).parentNode.parentNode.parentNode.classList.add('active'); 

            } catch (error) {
                console.log("***ERROR 2");
                console.log(error);
            }
            
        }

// 000000000000000000000000000000000000000000000000000000000000000000000000000000000
// 000000000000000000000000000000000000000000000000000000000000000000000000000000000
// 000000000000000000000000000000000000000000000000000000000000000000000000000000000
// 000000000000000000000000000000000000000000000000000000000000000000000000000000000

    try {
        if(location.pathname!='/'){
            control_scroll($('#contenido').offset().top); 
        }
    } catch (error) {
        //
    }


// 000000000000000000000000000000000000000000000000000000000000000000000000000000000
// 000000000000000000000000000000000000000000000000000000000000000000000000000000000
// 000000000000000000000000000000000000000000000000000000000000000000000000000000000
    $('#btn_form_sugerencia').on('click', async function(event){
        //   event.preventDefault(); // Previene el envío estándar del formulario

        fetch('sugerencia', {
            method: 'POST',
            body: JSON.stringify({ 
                csrfmiddlewaretoken: $("input[name='csrfmiddlewaretoken']").val(),
                'apellido_nombre' : $("#id_apellido_nombre").val(),
                'telefono' : $("#id_telefono").val(),
                'email' : $("#id_email").val(),
                'tipo_usuario' : $("#id_tipo_usuario").val(),
                'tipo_sugerencia' : $("#id_tipo_sugerencia").val(),
                'mensaje' : $("#id_mensaje").val(),
            }),
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCSRFToken()
            }
        })
        .then(async function (resultado){
            data=await resultado.json();
            if(data.error){
                $('#div_mensaje_sugerencia').addClass("alert alert-danger");
                $('#div_mensaje_sugerencia').html(data.error);
            }else{
                $('#mail_suscribir').val("");
                $('#div_mensaje_sugerencia').removeClass("alert alert-danger");
                $('#div_mensaje_sugerencia').addClass("alert alert-success");
                $('#div_mensaje_sugerencia').html(data.mensaje);
                $("#form_sugerencia").trigger("reset");
                $(this).attr("disabled");

            }

        })
        .catch((e)=>{
            $('#div_mensaje_sugerencia').addClass("alert alert-danger");
            $('#div_mensaje_sugerencia').html("error al enviar el formulario, verifique su conexion");
        });
    });



// 000000000000000000000000000000000000000000000000000000000000000000000000000000000
// 000000000000000000000000000000000000000000000000000000000000000000000000000000000
// 000000000000000000000000000000000000000000000000000000000000000000000000000000000

    $('#btn_enviar_contacto').on('click', async function(event){
        //   event.preventDefault(); // Previene el envío estándar del formulario
        resultado =await $.post("contacto", {
			csrfmiddlewaretoken: $("input[name='csrfmiddlewaretoken']").val(),
            'name': $('#id_nombre').val(),
            'email': $('#id_email').val(),
            'mensaje': $('#id_mensaje').val(),
		})
        .then(function (resultado){
            console.log(resultado);
        })
        .catch((e)=>{
            console.table(e);
            // console.table(e.responseText);
            // console.table(e.status);
            // console.table(e.statusText);
        });
    });

// 000000000000000000000000000000000000000000000000000000000000000000000000000000000
// 000000000000000000000000000000000000000000000000000000000000000000000000000000000
// 000000000000000000000000000000000000000000000000000000000000000000000000000000000
// susucribirse
$('#btn_suscribir').on('click', async function(event){
    if($('#mail_suscribir').val().length > 5){
        fetch('/suscribir', {
            method: 'POST',
            body: JSON.stringify({ email: $('#mail_suscribir').val(), token: getCSRFToken() }),
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCSRFToken()
            }
        })
        .then(async function (resultado){
            data=await resultado.json();
            if(data.error){
                $('#div_mensaje').addClass("alert alert-danger");
                $('#div_mensaje').html(data.error);
            }else{
                $('#mail_suscribir').val("");
                $('#div_mensaje').removeClass("alert alert-danger");
                $('#div_mensaje').addClass("alert alert-success");
                $('#div_mensaje').html(data.mensaje);
            }

        })
        .catch((e)=>{
            $('#div_mensaje').addClass("alert alert-danger");
            $('#div_mensaje').html("error al enviar el formulario, verifique su conexion");
        });
    }
    else{
        $('#div_mensaje').addClass("alert alert-danger");
        $('#div_mensaje').html("debe ingresar un email valido");
    }

    });

// 000000000000000000000000000000000000000000000000000000000000000000000000000000000
// 000000000000000000000000000000000000000000000000000000000000000000000000000000000
// 000000000000000000000000000000000000000000000000000000000000000000000000000000000
// 000000000000000000000000000000000000000000000000000000000000000000000000000000000
// 000000000000000000000000000000000000000000000000000000000000000000000000000000000
// 000000000000000000000000000000000000000000000000000000000000000000000000000000000
// REGSITRARSE
$('#btn_registrarse').on('click', async function(event){
    if($('#email').val().length > 5 && $('#numero_agente_cuil').val().length > 4){
        $(this).attr("value", "Enviando Formulario...");
        fetch('/registrar_usuario_institucional', {
            method: 'POST',
            body: JSON.stringify({ 
                numero_agente_cuil: $('#numero_agente_cuil').val(), 
                email: $('#email').val(), 
                token: getCSRFToken() }),
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCSRFToken()
            }
        })
        .then(async function (resultado){
            data=await resultado.json();
            if(data.error){
                $('#div_mensaje').addClass("alert alert-danger");
                $('#div_mensaje').html(data.error);
            }else{
                $('#email').val("");
                $('#numero_agente_cuil').val("");
                $('#div_mensaje').removeClass("alert alert-danger");
                $('#div_mensaje').addClass("alert alert-success");
                $('#div_mensaje').html(data.mensaje);
            }
            $("#email").attr("value", "Enviar");
        })
        .catch((e)=>{
            $("#email").attr("value", "Enviar");
            $('#div_mensaje').addClass("alert alert-danger");
            $('#div_mensaje').html("error al enviar el formulario, verifique su conexion");
        });
    }
    else{
        $('#div_mensaje').addClass("alert alert-danger");
        $('#div_mensaje').html("debe ingresar un email valido");
    }

 
    });


// 000000000000000000000000000000000000000000000000000000000000000000000000000000000
$("#ico_sugerencia").on('click', function(e){
    $("#btn_sugerencia").attr("aria-expanded", "true");
    $("#btn_sugerencia").removeClass("collapsed");
    $("#div_sugerencia").addClass("show");
});



// 000000000000000000000000000000000000000000000000000000000000000000000000000000000
// 000000000000000000000000000000000000000000000000000000000000000000000000000000000
// 000000000000000000000000000000000000000000000000000000000000000000000000000000000

    

});