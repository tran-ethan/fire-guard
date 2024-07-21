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

export async function getWildFire(id: string) {
    return await getDocumentData<WildFire>("wildfires", id);
}

export async function getWildFires(...constraints: QueryFieldFilterConstraint[]) {
    return await getDocumentDatas<WildFire>("wildfires", ...constraints);
}
