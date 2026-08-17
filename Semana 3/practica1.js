// GET https://mitienda.cl/api/productos
// GET, POST, PUT, DELETE
const respuestaAPI = {
	"status": 200,
	"message": "Productos recolectados",
	"data": [
		{
			"id": 1,
			"nombre": "Teclado numerico",
			"precio": 4500,
			"stock": 12,
			"categoria": "Periféricos",
			"disponible": true
		},
		{
			"id": 2,
			"nombre": "Mouse inalámbrico",
			"precio": 19900,
			"stock": 0,
			"categoria": "Periféricos",
			"disponible": false
		},
		{
			"id": 3,
			"nombre": "Monitor 24 pulgadas",
			"precio": 129900,
			"stock": 5,
			"categoria": "Monitores",
			"disponible": true
		}
	]
};

respuestaAPI.data.forEach((producto) => {
    console.log(`${producto.nombre} - $${producto.precio}`);
});

let variable = { "rut": "1-9"};  // null
console.log(typeof(variable));
let variable2 = 1/variable; // NaN
console.log(typeof(variable2)); console.log(variable2);
let variable3;
console.log(typeof(variable3)); console.log(variable3 instanceof Object);

try {
    variable2 = variable2 + y;
} catch (ex) {
    console.log(`Error: ${ex}`);
}

