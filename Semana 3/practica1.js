// respuestaAPI = apicall(); // GET https://algo.cl/api/productos

const respuestaAPI = {
    "status": 200,
    "message" : "Productos obtenidos correctamente",
    "data": [
        {
            "id": 1,
            "nombre": "Teclado",
            "precio": 4590
        },
        {
            "id": 2,
            "nombre": "Mouse",
            "precio": 6000
        }
    ]
};

respuestaAPI.data.forEach((producto) => {
    console.log(`${producto.nombre} - $${producto.precio}`);
})

let variable1 = null;
console.log(typeof(variable1));
variable1 = { "rut": "1-9"};
console.log(typeof(variable1.rut));
let variable2 = NaN;
console.log(typeof(variable2));
variable2 = 1/0;
console.log(typeof(variable2)); console.log(variable2);
variable2 = 1/variable1;
console.log(typeof(variable2)); console.log(variable2);
let variable3;
console.log(typeof(variable3));
console.log(variable3 instanceof Object)
console.log(null instanceof Object);
try { // Controlados Accepted, Reject, Except
    variable2 = variable2 + y;
} catch (err) {
    console.log(`Error ${err}`);
}