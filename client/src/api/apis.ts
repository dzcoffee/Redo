import { baseInstance } from "@/api/axios";

export const getData = (url: string): Promise<any> => {
    return baseInstance.get(url);
}

export const getDataById = (url:string, id: string): Promise<any> => {
    return baseInstance.get(`${url}/${id}`);
}

export const postData = (url: string, data: unknown): Promise<any> => {
    return baseInstance.post(`${url}`, data);
}

export const signIn = (auth: {'id': string, 'password': string}): Promise<any> => {
    return baseInstance.post('/login', auth);
}