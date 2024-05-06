import { baseInstance } from "@/api/axios";
import type { User } from "@/domain/type";

export const getData = (url: string): Promise<any> => {
    return baseInstance.get(url);
}

export const getDataById = (url:string, id: string): Promise<any> => {
    return baseInstance.get(`${url}/${id}`);
}

export const postData = (url: string, data?: unknown): Promise<any> => {
    return baseInstance.post(`${url}`, data);
}

export const signIn = (auth: {'username': string, 'password': string}): Promise<any> => {
    return baseInstance.post('/user/login', auth);
}

export const signUp = (auth: User): Promise<any> => {
    return baseInstance.post('/user/create', auth);
}