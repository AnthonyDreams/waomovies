function validarFormulario(){
 
  var nombre= document.getElementById('nombre').value;
  var correo = document.getElementById('correo').value;
  var clave = document.getElementById('clave').value;
  var clave2 = document.getElementById('clave2').value;
  
  //Test campo obligatorio
    if(nombre == null || nombre.length == 0 || /^\s+$/.test(nombre)){
    alert('ERROR: El campo nombre no debe ir vacío o lleno de solamente espacios en blanco');
    return false;
    }
  
  
    //Test correo
    if(!(/\S+@\S+\.\S+/.test(correo))){
    alert('ERROR: Debe escribir un correo válido');
    return false;
    }

    //Test fecha
    if(!isNaN(clave)){
    alert('ERROR: Debe elegir una fecha');
    return false;
    }

    if(!isNaN(clave2)){
    alert('ERROR: Debe elegir una fecha');
    return false;
    }

    //Test comboBox
    if(clave != clave2){
    alert('ERROR: Las contraseñas no coinciden');
    return false;
    }


}