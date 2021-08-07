// Objects are structured with a primary type and an optional subtype

import { ObjectFlags } from "typescript";
import { Url } from "url";

//
type position = {
  value: "tbd coordinate system go brrrrrrr";
};

export namespace objects {
  export interface item {
    location: position;
    image?: Url;
  }

  export enum dndClass {
    "Wizard",
    "Sorcerer",
    "Hunter",
    "Rogue",
    "Bard",
    "Paladin",
    "Monk",
    "Cleric",
    "Druid",
    "Dragoon",
  }

  export interface person extends item {
    name: string;
    class: string;
    age: number;
  }

  export interface Galdorian extends person {}

  export interface location {
    name: string;
  }

  export interface event {}

  export interface link {}

  export interface item {}

  export interface group {}
}

/*
Categories of things:

  Characters:
    name
    hometown

    class:
      1 of:
        paladin
        bard
        the ones that don't matter
      
    level
      number
    
    description
      bunch of text

*/

// const Kalon: person = {
//   name: "Kalon",
//   age: 78,
//   nationality: "Maneirikur",
//   faction: "whisperling",
//   magic: "philosopher",
// };
