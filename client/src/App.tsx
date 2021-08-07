import React from "react";
import logo from "./logo.svg";
import "./App.css";
import L, { imageOverlay, LatLngExpression, Layer } from "leaflet";
import { MapContainer, TileLayer, Marker, Popup } from "react-leaflet";
import { objects } from "./exampleObjects";

const Zoe: objects.person = {
  name: "Zoe",
  class: "Paladin",
  age: 24,
};

const Map = () => {
  const defaultPosition: LatLngExpression = [48.864716, 2.349]; // Paris position

  return (
    <div className="map__container">
      <MapContainer id="map" center={defaultPosition} zoom={13}>
        <TileLayer url="hesparia.jpg"></TileLayer>
      </MapContainer>
    </div>
  );
};

function App() {
  return (
    <div className="App">
      <Map></Map>
    </div>
  );
}

export default App;
