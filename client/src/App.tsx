import React, { useState } from "react";
import "./App.css";
/*
// import L, { imageOverlay, LatLngExpression, Layer } from "leaflet";
// import { MapContainer, TileLayer, Marker, Popup } from "react-leaflet";

// const Map = () => {
//   const defaultPosition: LatLngExpression = [48.864716, 2.349]; // Paris position

//   return (
//     <div className="map__container">
//       <MapContainer id="map" center={defaultPosition} zoom={13}>
//         <TileLayer url="hesparia.jpg"></TileLayer>
//       </MapContainer>
//     </div>
//   );
// };

// function App() {
//   return (
//     <div className="App">
//       <Map></Map>
//     </div>
//   );
// }
*/

function FormBody(props: { option: string }) {
  switch (props.option) {
    case "Person":
      return PersonForm();
    case "Place":
      return PlaceForm();
    case "Thing":
      return ThingForm();
    case "Event":
      return EventForm();
    case "Link":
      return LinkForm();
    default:
      return <p>somethin broked</p>;
  }
}

function handlePersonSubmit(e: React.FormEvent<HTMLFormElement>) {
  console.log(e);
}

function PersonForm() {
  return (
    <>
      <p>Personform</p>
      <form onSubmit={(e) => handlePersonSubmit(e)}>
        <input
          name="personName"
          type="text"
          defaultValue="name"
          onFocus={(e) => {
            e.target.value = "";
          }}
        ></input>
      </form>
    </>
  );
}

function PlaceForm() {
  return <p>Placeform</p>;
}

function ThingForm() {
  return <p>Thingform</p>;
}

function EventForm() {
  return <p>eventform</p>;
}

function LinkForm() {
  return <p>LinkForm</p>;
}

function App() {
  let [dropdownItem, setDropdownItem] = useState("Person");

  let onDropChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    setDropdownItem(e.currentTarget.value);
  };
  return (
    <>
      <h1>this might be //Atlas someday!</h1>
      <p>And today might be that day!!</p>
      <select value={dropdownItem} onChange={onDropChange}>
        <option value="Person">Person</option>
        <option value="Place">Place</option>
        <option value="Thing">Thing</option>
        <option value="Event">Event</option>
        <option value="Link">Link</option>
      </select>
      <FormBody option={dropdownItem}></FormBody>
    </>
  );
}
export default App;
