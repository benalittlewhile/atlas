export interface Pin {
  UID: number; // = db index or whatever
  name: string;
  latlangcoord: any; //TODO: fix this, needs to use the actual type
  category: string;
  timeStart: number;
  timeEnd: number;
  visible: boolean;
  relatedPeople: Person[];
  relatedThings: Thing[];
  relatedEvents: Event[];
  relatedPlaces: Place[];
  description: string;
  misc: string;
}

export interface Person extends Pin {
  age: number;
  height: number;
  nationality: string; //this will likely be an enum
  faction: string; //also likely enum
  orgPosition: string;
  job: string;
}

export interface Event extends Pin {
  date: Date;
  time: string; // TODO fix this
  preEvents: Event[];
  postEvents: Event[];
}

export interface Thing extends Pin {
  origin: string;
  properties: string;
}

export interface Place extends Pin {
  nationality: string; // maybe enum?
}
