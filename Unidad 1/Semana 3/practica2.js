let texto = document.createElement("input");
texto.setAttribute("type","text");
texto.setAttribute("value", "hola");
document.body.innerHTML = "";
document.body.appendChild(texto);

const responseAPI = {
    "status": 200,
    "message": "Productos Obtenidos",
    "data": [{"id":"1","nombre":"Martillo"},{"id":"2","nombre":"Tijera"}]
};

let cmbComuna = document.createElement("select");
cmbComuna.setAttribute("name","cmbComuna");
responseAPI.data.forEach((com) => {
  let optionAux = document.createElement("option");
  optionAux.setAttribute("value", com.id);
  optionAux.innerText = com.nombre;
  cmbComuna.appendChild(optionAux);
});
document.body.appendChild(cmbComuna);




// Parte 2

const objeto = { propiedad1 : 1, propiedad2 : 2};
delete objeto.propiedad1;
console.log(objeto);
//objeto.propiedad1 = 3;
//console.log(objeto);
const ordenado = { propiedad1: 3, ...objeto};
console.log(ordenado);
// arr["propiedad1"];   NO arr[0] # Valor duro
const objeto2 = { "tipo":"IOT"};
const composicion = Object.assign({}, ordenado, objeto2); // Fusion
console.log(composicion);
const composicion2 = {ordenado, objeto2}; // Verdadera composicion
console.log(composicion2);
console.log(composicion2.objeto2);
for(let prop in composicion2){
    console.log(prop);
}
Object.entries(composicion2).forEach(([key, value]) => {
    console.log(`key: ${key}, value: ${value.propiedad1}`);
});
Object.values(composicion2).forEach(value => {
    console.log(`value: ${value}`);
});
Object.entries(composicion2).forEach(([key, value]) => {
    Object.entries(value).forEach(([key, value]) => {
        console.log(`key: ${key}, value: ${value}`);
    });
});