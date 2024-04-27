import { dummyInstance } from "@/api/axios";

export const getData = (url: string): Promise<any> => {
    return dummyInstance.get(url);
}