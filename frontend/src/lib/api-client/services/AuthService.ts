/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { ForgotPasswordRequest } from "../models/ForgotPasswordRequest";
import type { LoginRequest } from "../models/LoginRequest";
import type { LoginResponse } from "../models/LoginResponse";
import type { MessageResponse } from "../models/MessageResponse";
import type { RegisterRequest } from "../models/RegisterRequest";
import type { ResetPasswordRequest } from "../models/ResetPasswordRequest";
import type { CancelablePromise } from "../core/CancelablePromise";
import { OpenAPI } from "../core/OpenAPI";
import { request as __request } from "../core/request";
export class AuthService {
  /**
   * Login
   * @param requestBody
   * @returns LoginResponse Successful Response
   * @throws ApiError
   */
  public static loginApiAuthLoginPost(requestBody: LoginRequest): CancelablePromise<LoginResponse> {
    return __request(OpenAPI, {
      method: "POST",
      url: "/api/auth/login",
      body: requestBody,
      mediaType: "application/json",
      errors: {
        422: `Validation Error`,
      },
    });
  }
  /**
   * Read Users Me
   * @returns LoginResponse Successful Response
   * @throws ApiError
   */
  public static readUsersMeApiAuthMeGet(): CancelablePromise<LoginResponse> {
    return __request(OpenAPI, {
      method: "GET",
      url: "/api/auth/me",
    });
  }
  /**
   * Register
   * @param requestBody
   * @returns LoginResponse Successful Response
   * @throws ApiError
   */
  public static registerApiAuthRegisterPost(
    requestBody: RegisterRequest,
  ): CancelablePromise<LoginResponse> {
    return __request(OpenAPI, {
      method: "POST",
      url: "/api/auth/register",
      body: requestBody,
      mediaType: "application/json",
      errors: {
        422: `Validation Error`,
      },
    });
  }
  /**
   * Forgot Password
   * @param requestBody
   * @returns MessageResponse Successful Response
   * @throws ApiError
   */
  public static forgotPasswordApiAuthForgotPasswordPost(
    requestBody: ForgotPasswordRequest,
  ): CancelablePromise<MessageResponse> {
    return __request(OpenAPI, {
      method: "POST",
      url: "/api/auth/forgot-password",
      body: requestBody,
      mediaType: "application/json",
      errors: {
        422: `Validation Error`,
      },
    });
  }
  /**
   * Reset Password
   * @param requestBody
   * @returns MessageResponse Successful Response
   * @throws ApiError
   */
  public static resetPasswordApiAuthResetPasswordPost(
    requestBody: ResetPasswordRequest,
  ): CancelablePromise<MessageResponse> {
    return __request(OpenAPI, {
      method: "POST",
      url: "/api/auth/reset-password",
      body: requestBody,
      mediaType: "application/json",
      errors: {
        422: `Validation Error`,
      },
    });
  }
}
