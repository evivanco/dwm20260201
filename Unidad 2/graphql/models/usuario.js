const mongoose = require('mongoose');
const usuarioSchema = mongoose.Schema({
    nombre: String,
    pass: String
});

module.exports = mongoose.model('Usuario', usuarioSchema);