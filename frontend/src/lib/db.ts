
import app from "./app";
import { collection, doc, getDoc, getDocs, initializeFirestore, query, QueryFieldFilterConstraint, setDoc, updateDoc } from "firebase/firestore";
import type { DocumentData } from "firebase/firestore";

const dbSettings = { experimentalForceLongPolling: true };
const db = initializeFirestore(app, dbSettings);

/**
 * Get document data from the database
 * @param collectionName name of the collection to get the document from
 * @param id id of the document to get
 * @returns document data
 */
export async function getDocumentData<T = any>(collectionName: string, id: string) {
    const docRef = doc(db, collectionName, id);
    const docSnap = await getDoc(docRef);

    if (!docSnap.exists())
        throw new Error("No such document!");

    return docSnap.data() as T;
}

/**
 * Get all document data from a collection with constraints
 * @param T type of the document data
 * @param collectionName name of the collection to get the documents from
 * @param constraints constraints to apply to the query. Example: where("name", "==", "Bob")
 * @returns 
 */
export async function getDocumentDatas<T = any>(collectionName: string, ...constraints: QueryFieldFilterConstraint[]) {
    const q = query(collection(db, collectionName), ...constraints);
    const querySnapshot = await getDocs(q);
    const docDatas = querySnapshot.docs.map(doc => {
        const id = doc.id;
        return { id, ...doc.data() } as T;
    });
    return docDatas;
}

/**
 * Add a document to a collection
 * @param collectionName name of the collection to add the document to
 * @param data data to add to the document
 * @param id id of the document to add
 */
export async function addDocument<T = any>(collectionName: string, data: T, id?: string | undefined) {
    if (!data) throw new Error("No data provided to add the document!");

    const docRef = doc(collection(db, collectionName), id);
    await setDoc(docRef, data);
}

/**
 * Update a document in a collection
 * @param collectionName name of the collection to update the document in
 * @param id id of the document to update
 * @param data data to update the document with
 */
export async function updateDocument<T = any>(collectionName: string, id: string, data: Partial<T>) {
    if (!data) throw new Error("No data provided to update the document!");

    const docRef = doc(db, collectionName, id);
    await updateDoc<DocumentData, DocumentData>(docRef, data);
}

export default db;