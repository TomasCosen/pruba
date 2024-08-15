// app.js
const path = require("path");
const express = require("express");
const { engine } = require("express-handlebars");
const { Server } = require("socket.io");

const PORT = 3000;

const app = express();
console.log(__dirname);
app.engine("handlebars", engine());
app.set("view engine", "handlebars");
app.set("views", path.join(__dirname, "/views"));

app.use(express.json());
app.use(express.urlencoded({ extended: true }));

app.use(express.static(path.join(__dirname, "/public")));

app.get("/", (req, res) => {
  res.setHeader("Content-Type", "text/html");
  res.status(200).render("home");
});

const usuarios = [];
const mensajes = [];

const server = app.listen(PORT, () => {
  console.log(`Server escuchando en puerto ${PORT}`);
});

const io = new Server(server);

io.on("connection", (socket) => {
  console.log(`Se ha conectado un cliente con id ${socket.id}`);
  socket.emit("mensajesPrevios", mensajes);

  socket.on("id", (nombre) => {
    usuarios.push({ id: socket.id, nombre });
    socket.broadcast.emit("nuevoUsuario", nombre);
  });

  socket.on("mensaje", (nombre, mensaje) => {
    mensajes.push({ nombre, mensaje });
    io.emit("nuevoMensaje", nombre, mensaje);
  });

  socket.on("disconnect", () => {
    const usuario = usuarios.find((u) => u.id === socket.id);
    if (usuario) {
      io.emit("saleUsuario", usuario.nombre);
    }
  });
});
