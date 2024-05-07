import axios, { type AxiosInstance } from 'axios';

const DUMMY_URL = 'http://localhost:3000';
const SERVER_URL = 'https://port-0-redoback-1ru12mlvuze1ma.sel5.cloudtype.app';

let postPending = false;

/**
 * @description
 * axios 인스턴스 요청 인터셉터
 * 요청 사전 작업을 수행 (apis.ts 참조)
 * @param instance 인터셉터를 적용할 axios 인스턴스
 */
const baseRequestInterceptor = (instance: AxiosInstance): void => {
    instance.interceptors.request.use(
      (config) => {
        // POST 요청 중복 방지
        if (config.method === 'post') {
          if (postPending)
            return Promise.reject(new Error('이미 요청이 진행중입니다.'));
          postPending = true;
        }
        return config;
      },
      (err) => {
        console.log(err.toJSON());
        return Promise.reject(err);
      }
    );
};
  
/**
 * @description
 * 인스턴스 응답 인터셉터
 * 응답 후 then으로 넘어가기 전에 작업 수행
 * @param instance
 */
const baseResponseInterceptor = (instance: AxiosInstance): void => {
  instance.interceptors.response.use(
    (res) => {
      if (res.config.method === 'post') {
        postPending = false;
      }
      // console.log(res.data);
      return res.data;
    },
    async (err: any) => {
      if (err.config.method === 'post') {
        postPending = false;
      }
      console.log(err);
      return Promise.reject(err);
    }
  );
};
  
/**
 * @description
 * axios 인스턴스 생성
 * @param url
 * @param options
 * @returns
 */
export const baseApi = (url: string, options?: object): AxiosInstance => {
  const instance = axios.create({
    baseURL: url,
    headers: {
      'Content-Type': 'application/json',
    },
    ...options,
  });
  baseRequestInterceptor(instance);
  baseResponseInterceptor(instance);
  return instance;
};
  
// export const baseInstance = baseApi(BASE_URL);
export const dummyInstance = baseApi(DUMMY_URL);
export const baseInstance = baseApi(SERVER_URL);