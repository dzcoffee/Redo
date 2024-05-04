import { dummyInstance } from "@/api/axios";

export const getData = (url: string): Promise<any> => {
    return dummyInstance.get(url);
}

export const getDataById = (url:string, id: string): Promise<any> => {
    return dummyInstance.get(`${url}/${id}`);
}

export const postData = (url: string, data: unknown): Promise<any> => {
    return dummyInstance.post(`${url}`, data);
}