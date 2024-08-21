import {
    QueryFieldFilterConstraint,
    Timestamp,
} from "firebase/firestore";
import {
    getDocumentData,
    getDocumentDatas,
} from "./db";

export type WildFire = {
    lat: number;
    lon: number;
    agency: string;
    cause: string;
    date: Timestamp;
    responseType: string;
    hectares: number;
}

const collectionName = "livedata";

export async function getWildFire(id: string) {
    return await getDocumentData<WildFire>(collectionName, id);
}

export async function getWildFires(...constraints: QueryFieldFilterConstraint[]) {
    return await getDocumentDatas<WildFire>(collectionName, ...constraints);
}

export async function getWildfirePrediction(lat: number, lon: number) {
    //send a post request to a api endpoint to get the prediction
}
