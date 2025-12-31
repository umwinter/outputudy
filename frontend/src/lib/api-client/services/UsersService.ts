/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { User } from "../models/User";
import type { CancelablePromise } from "../core/CancelablePromise";
import { OpenAPI } from "../core/OpenAPI";
import { request as __request } from "../core/request";
export class UsersService {
  /**
   * List Users
   * @returns User Successful Response
   * @throws ApiError
   */
  public static listUsersApiUsersGet(): CancelablePromise<Array<User>> {
    return __request(OpenAPI, {
      method: "GET",
      url: "/api/users",
    });
  }
  /**
   * Get User
   * @param userId
   * @returns any Successful Response
   * @throws ApiError
   */
  public static getUserApiUsersUserIdGet(userId: number): CancelablePromise<User | null> {
    return __request(OpenAPI, {
      method: "GET",
      url: "/api/users/{user_id}",
      path: {
        user_id: userId,
      },
      errors: {
        422: `Validation Error`,
      },
    });
  }
}
